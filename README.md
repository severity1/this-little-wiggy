# this-little-wiggy

> "Mayor Quimby gives Ralph the instructions. Ralph executes them."

A Claude Code plugin that prepares prompts for the [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) loop plugin. Named after The Simpsons episode where Mayor Quimby desperately gives Ralph instructions at the electric chair controls.

## What It Does

Intercepts complex multi-step tasks and automatically:
1. Detects if a task would benefit from autonomous iteration
2. Wraps it in the proper Ralph Wiggum format with success criteria
3. Hands off to `/ralph-loop` for autonomous execution

**Before**: You manually structure prompts with phases and completion markers

**After**: Just type your task naturally - this-little-wiggy formats it for Ralph

## Quick Example

```bash
# You type:
claude "build a REST API for todos"

# this-little-wiggy detects complex task, generates:
/ralph-loop "Build a REST API for todos.

Phases:
Phase 1: Setup project structure
Phase 2: Implement CRUD endpoints
Phase 3: Add validation
Phase 4: Write tests

Verification: uv run pytest

<promise>COMPLETE</promise>
" --max-iterations 30 --completion-promise "COMPLETE"
```

## Installation

```bash
# Add marketplace (coming soon)
claude plugin marketplace add severity1/claude-code-marketplace

# Install
claude plugin install this-little-wiggy@claude-code-marketplace
```

**Requires**: [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) plugin

## Setup

Run the init wizard to configure your project:

```bash
/this-little-wiggy:init
```

The wizard asks:
- Project type (API, CLI, library, etc.)
- Test command (pytest, npm test, etc.)
- Default iteration limit
- Phase style (multi-phase, TDD, single)

Saves to `.claude/this-little-wiggy/config.json`

## Usage

**Normal use** - complex tasks auto-detected and formatted:
```bash
claude "implement user authentication with JWT"
claude "refactor the payment module"
claude "add comprehensive test coverage"
```

**Bypass** - skip formatting:
```bash
claude "* just fix this one line"  # * prefix bypasses
claude "/help"                      # slash commands bypass
```

## How It Works

```
User prompt
    │
    v
┌─────────────────────────┐
│ UserPromptSubmit Hook   │
│ - Detect complex task   │
│ - Load config.json      │
│ - Generate Ralph format │
└─────────────────────────┘
    │
    v
/ralph-loop (autonomous execution)
```

## Status

**Work in Progress** - See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for details.

## The Simpsons Reference

Named after "This Little Wiggy" (S9E18) where Mayor Quimby ends up at Ralph's mercy at the electric chair controls. Quimby desperately gives Ralph clear instructions - and the tension of whether Ralph will execute them correctly mirrors the autonomous loop: you give it a well-structured plan and hope it completes successfully.

## License

MIT
