# 🎉 this-little-wiggy v0.0.2 Release

## What's New

We're excited to announce v0.0.2 of this-little-wiggy! This release focuses on making the plugin smarter and cleaner with intelligent task evaluation and significant code cleanup.

### ✨ Intelligent Task Evaluation

The hook now automatically evaluates task complexity before invoking ralph-loop:

- **Smart Detection**: Simple tasks execute normally without ralph-loop overhead
- **Clear Feedback**: When ralph-loop is invoked, you'll see a clear announcement with rationale
- **Better UX**: No more wrapping every task - only complex implementations get the autonomous treatment

**Example:**
```bash
# Simple task - executes directly
claude "fix this typo"

# Complex task - automatically wrapped with ralph-loop
claude "build a REST API for todos"
> 🔄 Invoking ralph-loop for complex implementation task...
```

### 🧹 Codebase Cleanup

Removed **247 lines** of dead code to improve maintainability:

- Deleted unused `task-evaluator` agent (never invoked in current architecture)
- Removed bypassed `task-analyzer` skill
- Cleaned up corresponding test classes
- Fixed all ruff linting issues (import sorting, line length)

### 📚 Documentation Improvements

- Enhanced README with clearer slash command usage patterns
- Added prefix pattern examples: `"Execute /tdd phase1"`
- Explained why prefixes prevent premature slash command expansion

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
