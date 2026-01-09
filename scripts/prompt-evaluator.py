#!/usr/bin/env python3
"""
this-little-wiggy Prompt Evaluator Hook

Intercepts user prompts and wraps complex tasks with ralph-loop
using completion criteria from project config.
"""

import json
import os
import sys
from pathlib import Path

import yaml


def output_json(additional_context: str) -> None:
    """Output in UserPromptSubmit hook format."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(output))


def pass_through(prompt: str) -> None:
    """Pass prompt through unchanged."""
    output_json(prompt)
    sys.exit(0)


def get_project_dir() -> Path | None:
    """Get project directory from environment or cwd."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        return Path(project_dir)
    # Fallback to cwd for testing
    return Path.cwd()


def load_config() -> dict | None:
    """Load and parse config.yml, return None if not found or invalid."""
    project_dir = get_project_dir()
    if not project_dir:
        return None

    config_path = project_dir / ".claude" / "this-little-wiggy" / "config.yml"
    if not config_path.exists():
        return None
    try:
        return yaml.safe_load(config_path.read_text())
    except Exception:
        return None


def main() -> None:
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = input_data.get("prompt", "")

    # Bypass conditions
    if prompt.startswith("*"):
        pass_through(prompt[1:].strip())

    if prompt.startswith("/this-little-wiggy:"):
        pass_through(prompt)

    if prompt.startswith("/ralph-loop:ralph-loop"):
        pass_through(prompt)

    # Load config - pass through if not found
    config = load_config()
    if not config:
        pass_through(prompt)

    ralph_wrapper = config.get("ralphWrapper", "")
    if not ralph_wrapper:
        pass_through(prompt)

    # Build wrapped prompt and escape shell-sensitive characters
    wrapped_prompt = ralph_wrapper.replace("{task}", prompt)
    # Escape backticks to prevent shell command substitution
    wrapped_prompt = wrapped_prompt.replace("`", "\\`")
    escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')

    evaluation_context = f"""TASK EVALUATION

Original user request: "{escaped_prompt}"

EVALUATE: Is this a complex task that benefits from autonomous execution with self-correction?

PROCEED DIRECTLY if:
- Simple questions, lookups, or explanations
- Single-line fixes or typos
- Reading/exploring code without making changes

EXECUTE THIS WRAPPED PROMPT if complex (multi-step implementation, refactoring, multi-file changes):

{wrapped_prompt}

If simple, proceed with the original request. If complex, execute the wrapped prompt above exactly as shown."""

    output_json(evaluation_context)
    sys.exit(0)


if __name__ == "__main__":
    main()
