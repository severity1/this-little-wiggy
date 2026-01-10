#!/usr/bin/env python3
"""
Tests for skill structure and content validation.
"""

from pathlib import Path

import pytest
import yaml

PLUGIN_ROOT = Path(__file__).parent.parent


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
