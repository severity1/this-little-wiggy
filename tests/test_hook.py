#!/usr/bin/env python3
"""
Tests for the prompt-evaluator hook script.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "prompt-evaluator.py"

TEST_CONFIG = """defaultMaxIterations: 10

ralphWrapper: |
  /ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "{task}

  When complete:
  - Tests pass
  - Build succeeds

  Output <promise>COMPLETE</promise> when done."
"""


def run_hook(prompt: str, config_exists: bool = False) -> dict:
    """Run the hook script with given prompt and return parsed output."""
    input_data = json.dumps({"prompt": prompt})

    with tempfile.TemporaryDirectory() as tmpdir:
        if config_exists:
            config_dir = Path(tmpdir) / ".claude" / "this-little-wiggy"
            config_dir.mkdir(parents=True)
            (config_dir / "config.yml").write_text(TEST_CONFIG)

        env = {**os.environ, "CLAUDE_PROJECT_DIR": tmpdir}
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            env=env,
            input=input_data,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            pytest.fail(f"Hook failed: {result.stderr}")

        return json.loads(result.stdout)


class TestBypassConditions:
    """Test bypass conditions that skip evaluation."""

    def test_bypass_asterisk_prefix(self):
        """Asterisk prefix should strip and pass through."""
        output = run_hook("*build a todo api")
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == "build a todo api"

    def test_bypass_asterisk_with_spaces(self):
        """Asterisk with leading spaces in content should be preserved."""
        output = run_hook("*  spaced content")
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == "spaced content"

    def test_bypass_own_commands(self):
        """Our own commands should pass through."""
        output = run_hook("/this-little-wiggy:init")
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == "/this-little-wiggy:init"

    def test_bypass_own_commands_with_args(self):
        """Our commands with arguments should pass through."""
        output = run_hook("/this-little-wiggy:init --force")
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == "/this-little-wiggy:init --force"

    def test_bypass_ralph_loop(self):
        """ralph-loop command should pass through to avoid double-wrapping."""
        output = run_hook('/ralph-loop:ralph-loop "Build API" --max-iterations 20')
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == '/ralph-loop:ralph-loop "Build API" --max-iterations 20'


class TestNoConfigBehavior:
    """Test behavior when config doesn't exist."""

    def test_no_config_passes_through(self):
        """Without config, prompts should pass through unchanged."""
        output = run_hook("build a REST API", config_exists=False)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == "build a REST API"

    def test_no_config_other_slash_commands(self):
        """Other slash commands pass through without config."""
        output = run_hook("/build-feature foo", config_exists=False)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == "/build-feature foo"


class TestEvaluationRequest:
    """Test that normal prompts trigger evaluation with wrapped prompt."""

    def test_normal_prompt_requests_evaluation(self):
        """Normal prompts with config should show directive and wrapped prompt."""
        output = run_hook("build a REST API for todos", config_exists=True)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "RALPH-LOOP DIRECTIVE" in context
        assert "build a REST API for todos" in context
        assert "/ralph-loop:ralph-loop" in context

    def test_slash_command_requests_evaluation(self):
        """Other slash commands with config should get directive."""
        output = run_hook("/build-feature authentication", config_exists=True)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "RALPH-LOOP DIRECTIVE" in context
        assert "/build-feature authentication" in context

    def test_special_characters_escaped(self):
        """Special characters in prompt should be properly escaped."""
        output = run_hook('Test with "quotes" and \\backslash', config_exists=True)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "RALPH-LOOP DIRECTIVE" in context

    def test_wrapped_prompt_includes_task(self):
        """Wrapped prompt should include the original task."""
        output = run_hook("implement user auth", config_exists=True)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "implement user auth" in context
        assert "When complete:" in context


class TestOutputFormat:
    """Test output JSON format."""

    def test_output_has_correct_structure(self):
        """Output should have hookSpecificOutput with additionalContext."""
        output = run_hook("test prompt", config_exists=True)
        assert "hookSpecificOutput" in output
        assert "hookEventName" in output["hookSpecificOutput"]
        assert "additionalContext" in output["hookSpecificOutput"]
        assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"

    def test_empty_prompt_handled(self):
        """Empty prompt should be handled gracefully."""
        output = run_hook("", config_exists=False)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert context == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
