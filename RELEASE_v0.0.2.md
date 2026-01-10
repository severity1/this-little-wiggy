# 🎉 this-little-wiggy v0.0.2 Release

## What's New

We're excited to announce v0.0.2 of this-little-wiggy! This release focuses on making the plugin smarter and cleaner with intelligent task evaluation and significant code cleanup.

### ✨ Intelligent Task Evaluation

**Previously:** The hook wrapped every prompt and forced execution with ralph-loop

**Now:** The hook sends a MANDATORY DIRECTIVE that tells Claude to EVALUATE the task first

The directive provides clear decision criteria:

**PROCEED IMMEDIATELY (without ralph-loop):**
- Simple questions, lookups, or explanations
- Single-line fixes or minor typo corrections
- Reading/exploring code without making changes
- User explicitly says "don't loop" or "just do it once"

**INVOKE RALPH-LOOP for:**
- Multi-file code changes or refactoring
- Slash commands that write code (e.g., /tdd, /commit)
- Feature implementation requiring build/test/lint cycles
- Any work where quality gates apply

When ralph-loop IS invoked, Claude provides feedback: *"Invoking ralph-loop (reason)"*

**Example:**
```bash
# Simple task - executes directly
claude "fix this typo"

# Complex task - wrapped with ralph-loop + feedback
claude "build a REST API for todos"
> Invoking ralph-loop (multi-file implementation requiring quality gates)
```

**Technical change:** Updated `scripts/prompt-evaluator.py` directive from "EXECUTE THIS PROMPT" to "EVALUATE: Does this request require autonomous execution with quality gates?"

### 🧹 Codebase Cleanup

Removed **247+ lines** of dead code to improve maintainability:

- **Deleted `agents/task-evaluator.md` (50 lines)**: Was supposed to classify tasks, but the hook directive handles this more efficiently
- **Deleted `skills/task-analyzer/SKILL.md` (72 lines)**: Bypassed by direct hook implementation
- **Deleted `skills/task-analyzer/references/ralph-template.md` (53 lines)**: No longer needed
- **Removed test classes (90 lines)**: Corresponding tests for deleted agent/skill
- **Fixed ruff linting**: Import sorting and formatting issues

The architecture is now simpler: User prompt → Hook evaluates → Claude decides → Execute (with or without ralph-loop)

### 📚 Documentation Improvements

**Slash Command Usage Pattern:**

The README now explains why you need a prefix for slash commands:

```bash
# ❌ This expands the slash command BEFORE the hook sees it
claude "/tdd phase1"

# ✅ Prefix lets the hook wrap it first
claude "Execute /tdd phase1"
claude "Implement /tdd GH issue 32"
```

Without a prefix word, slash commands expand immediately in Claude Code, before the hook can evaluate them for ralph-loop wrapping.

**Changes:**
- Updated Quick Example to show prefix pattern
- Added dedicated "Slash commands" usage section
- Included explanation of why prefixes are necessary
- Changed init command directive from "IMPORTANT" to "MANDATORY"

## 🔧 Technical Details

**Commits:**
- `a407d65` - feat: add intelligent task evaluation and user feedback
- `d5bc5a0` - chore: remove unused agent/skill and fix ruff linting issues

**Stats:**
- 8 files changed
- 32 insertions(+)
- 279 deletions(-)

## 📦 Installation

Install or upgrade via the marketplace:

```bash
claude plugin marketplace add severity1/severity1-marketplace
claude plugin install this-little-wiggy@severity1-marketplace
```

Or from source:

```bash
git clone https://github.com/severity1/this-little-wiggy.git
cd this-little-wiggy
claude plugin marketplace add /absolute/path/to/this-little-wiggy/.dev-marketplace/.claude-plugin/marketplace.json
claude plugin install this-little-wiggy@local-dev
```

## 🚀 Getting Started

```bash
/this-little-wiggy:init
```

The setup wizard will discover your project's completion criteria and configure the plugin automatically.

## 📋 Requirements

- Claude Code 2.0.22+
- [ralph-loop](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-loop) plugin

## 🙏 Thank You

Thanks to everyone testing and providing feedback! This release makes this-little-wiggy smarter and more maintainable.

---

**Full Changelog**: https://github.com/severity1/this-little-wiggy/compare/v0.0.1...v0.0.2
