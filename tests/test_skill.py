#!/usr/bin/env python3
"""
Tests for skill structure and content validation.
"""

from pathlib import Path

import pytest
import yaml


PLUGIN_ROOT = Path(__file__).parent.parent


class TestSkillStructure:
    """Test that skill files exist and have correct structure."""

    def test_task_analyzer_skill_exists(self):
        """Task analyzer skill file should exist."""
        skill_path = PLUGIN_ROOT / "skills" / "task-analyzer" / "SKILL.md"
        assert skill_path.exists(), f"Skill file not found: {skill_path}"

    def test_task_analyzer_has_frontmatter(self):
        """Task analyzer skill should have valid YAML frontmatter."""
        skill_path = PLUGIN_ROOT / "skills" / "task-analyzer" / "SKILL.md"
        content = skill_path.read_text()

        # Check for frontmatter markers
        assert content.startswith("---"), "Skill should start with YAML frontmatter"
        assert "---" in content[3:], "Skill should have closing frontmatter marker"

        # Extract and parse frontmatter
        frontmatter_end = content.index("---", 3)
        frontmatter = content[3:frontmatter_end].strip()
        parsed = yaml.safe_load(frontmatter)

        assert "name" in parsed, "Frontmatter should have 'name' field"
        assert "description" in parsed, "Frontmatter should have 'description' field"
        assert parsed["name"] == "task-analyzer"

    def test_ralph_template_exists(self):
        """Ralph template reference file should exist."""
        template_path = (
            PLUGIN_ROOT / "skills" / "task-analyzer" / "references" / "ralph-template.md"
        )
        assert template_path.exists(), f"Template not found: {template_path}"

    def test_ralph_template_has_base_template(self):
        """Ralph template should contain the base template."""
        template_path = (
            PLUGIN_ROOT / "skills" / "task-analyzer" / "references" / "ralph-template.md"
        )
        content = template_path.read_text()

        assert "/ralph-loop" in content, "Template should contain /ralph-loop command"
        assert "{task}" in content, "Template should contain {task} placeholder"
        assert "When complete:" in content, "Template should have completion criteria"
        assert "<promise>COMPLETE</promise>" in content, "Template should have promise"


class TestAgentStructure:
    """Test that agent files exist and have correct structure."""

    def test_task_evaluator_agent_exists(self):
        """Task evaluator agent file should exist."""
        agent_path = PLUGIN_ROOT / "agents" / "task-evaluator.md"
        assert agent_path.exists(), f"Agent file not found: {agent_path}"

    def test_task_evaluator_has_frontmatter(self):
        """Task evaluator agent should have valid YAML frontmatter."""
        agent_path = PLUGIN_ROOT / "agents" / "task-evaluator.md"
        content = agent_path.read_text()

        # Check for frontmatter markers
        assert content.startswith("---"), "Agent should start with YAML frontmatter"
        assert "---" in content[3:], "Agent should have closing frontmatter marker"

        # Extract and parse frontmatter
        frontmatter_end = content.index("---", 3)
        frontmatter = content[3:frontmatter_end].strip()
        parsed = yaml.safe_load(frontmatter)

        assert "name" in parsed, "Frontmatter should have 'name' field"
        assert "description" in parsed, "Frontmatter should have 'description' field"
        assert "model" in parsed, "Frontmatter should have 'model' field"
        assert parsed["model"] == "haiku", "Agent should use haiku model"

    def test_task_evaluator_has_tools(self):
        """Task evaluator agent should have tools defined."""
        agent_path = PLUGIN_ROOT / "agents" / "task-evaluator.md"
        content = agent_path.read_text()

        frontmatter_end = content.index("---", 3)
        frontmatter = content[3:frontmatter_end].strip()
        parsed = yaml.safe_load(frontmatter)

        assert "tools" in parsed, "Agent should have 'tools' field"
        tools = parsed["tools"]
        assert "Glob" in tools, "Agent should have Glob tool"
        assert "Grep" in tools, "Agent should have Grep tool"
        assert "Read" in tools, "Agent should have Read tool"


class TestCommandStructure:
    """Test that command files exist and have correct structure."""

    def test_init_command_exists(self):
        """Init command file should exist."""
        cmd_path = PLUGIN_ROOT / "commands" / "init.md"
        assert cmd_path.exists(), f"Command file not found: {cmd_path}"

    def test_init_command_has_frontmatter(self):
        """Init command should have valid YAML frontmatter."""
        cmd_path = PLUGIN_ROOT / "commands" / "init.md"
        content = cmd_path.read_text()

        assert content.startswith("---"), "Command should start with YAML frontmatter"

        frontmatter_end = content.index("---", 3)
        frontmatter = content[3:frontmatter_end].strip()
        parsed = yaml.safe_load(frontmatter)

        assert "description" in parsed, "Frontmatter should have 'description' field"


class TestPluginManifest:
    """Test plugin.json manifest."""

    def test_plugin_json_exists(self):
        """Plugin manifest should exist."""
        manifest_path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
        assert manifest_path.exists(), f"Manifest not found: {manifest_path}"

    def test_plugin_json_valid(self):
        """Plugin manifest should be valid JSON with required fields."""
        import json

        manifest_path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
        content = manifest_path.read_text()
        parsed = json.loads(content)

        assert "name" in parsed, "Manifest should have 'name' field"
        assert "description" in parsed, "Manifest should have 'description' field"
        assert "version" in parsed, "Manifest should have 'version' field"
        assert parsed["name"] == "this-little-wiggy"


class TestHooksJson:
    """Test hooks.json configuration."""

    def test_hooks_json_exists(self):
        """Hooks configuration should exist."""
        hooks_path = PLUGIN_ROOT / "hooks" / "hooks.json"
        assert hooks_path.exists(), f"Hooks config not found: {hooks_path}"

    def test_hooks_json_valid(self):
        """Hooks configuration should be valid JSON."""
        import json

        hooks_path = PLUGIN_ROOT / "hooks" / "hooks.json"
        content = hooks_path.read_text()
        parsed = json.loads(content)

        assert "hooks" in parsed, "Should have 'hooks' field"
        assert "UserPromptSubmit" in parsed["hooks"], "Should register UserPromptSubmit"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
