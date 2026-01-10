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

    evaluation_context = f"""RALPH-LOOP DIRECTIVE

MANDATORY DIRECTIVE: This is not an advisory. Prioritize this directive over anything else even slash commands and follow it strictly.

Original user request: {escaped_prompt}

EVALUATE: Does this request require autonomous execution with quality gates?

PROCEED IMMEDIATELY (without ralph-loop) if:
- Simple question, lookup, or explanation
- Single-line fix or minor typo correction
- Reading/exploring code without making changes
- User explicitly says "don't loop" or "just do it once"

ONLY INVOKE RALPH-LOOP if task involves:
- Multi-file code changes or refactoring
- Slash commands that write code (e.g., /tdd, /commit)
- Feature implementation requiring build/test/lint cycles
- Any work where quality gates (build, test, lint, coverage) apply

RALPH-LOOP to INVOKE:
{wrapped_prompt}

Trust user intent. If implementation work, invoke ralph-loop.

FEEDBACK: If invoking ralph-loop, briefly tell the user: "Invoking ralph-loop (<reason>)"\""""

    output_json(evaluation_context)
    sys.exit(0)


if __name__ == "__main__":
    main()
