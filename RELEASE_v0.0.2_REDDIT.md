# this-little-wiggy v0.0.2 - Now with Smart Task Detection

Hey folks! Just shipped v0.0.2 of this-little-wiggy (Claude Code plugin that auto-wraps complex tasks for autonomous execution with ralph-loop).

## What Changed

### 🧠 Smart Task Evaluation

The hook now evaluates whether your task actually needs ralph-loop before wrapping it. No more overhead for simple stuff.

**Previously:** Every prompt got wrapped → ralph-loop decided what to do

**Now:** Hook evaluates first → only complex tasks get wrapped

**Example:**
```bash
# Simple fix - executes immediately
claude "fix typo on line 42"

# Complex implementation - gets wrapped with ralph-loop
claude "build a REST API with auth"
> Invoking ralph-loop (multi-file implementation with quality gates)
```

The directive now tells Claude to EVALUATE the task:
- Simple questions/fixes? → Proceed without ralph-loop
- Multi-file changes, slash commands that write code, features needing build/test/lint? → Invoke ralph-loop

When ralph-loop IS invoked, you get clear feedback about why.

### 🧹 Removed 247 Lines of Dead Code

Turns out we had an unused agent and skill that never got called in the actual execution flow. Deleted:
- `task-evaluator` agent (was supposed to classify tasks, but hook does this now)
- `task-analyzer` skill (was bypassed by direct hook implementation)
- Corresponding test classes
- Fixed all ruff linting issues

Simpler is better.

### 📚 Better Docs

Updated README to explain the slash command prefix pattern:

```bash
# This expands the slash command BEFORE the hook sees it (bad)
claude "/tdd phase1"

# This lets the hook wrap it first (good)
claude "Execute /tdd phase1"
```

Without a prefix, slash commands expand immediately and the hook can't evaluate them.

## Install/Update

**Via marketplace:**
```bash
claude plugin marketplace add severity1/severity1-marketplace
claude plugin install this-little-wiggy@severity1-marketplace
```

**From source:**
```bash
git clone https://github.com/severity1/this-little-wiggy.git
cd this-little-wiggy
claude plugin marketplace add /path/to/this-little-wiggy/.dev-marketplace/.claude-plugin/marketplace.json
claude plugin install this-little-wiggy@local-dev
```

## Requirements

- Claude Code 2.0.22+
- [ralph-loop](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-loop) plugin

## What is this-little-wiggy?

For those new here: this-little-wiggy auto-detects complex implementation tasks and wraps them with project-specific completion criteria for autonomous execution. Keep using your existing prompts and slash commands - the plugin handles the wrapping.

Basically: Type vibes, ship autonomy. Let Claude iterate until your build/test/lint passes.

**Full changelog:** https://github.com/severity1/this-little-wiggy/compare/v0.0.1...v0.0.2

Feedback welcome! This is still early days.
