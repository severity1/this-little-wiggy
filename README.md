# this-little-wiggy

> "Mayor Quimby gives Ralph the instructions. Ralph executes them."

A Claude Code plugin that prepares prompts for the [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) loop plugin.

## What It Does

Intercepts complex tasks and wraps them with project-specific completion criteria for autonomous execution.

**Before**: You manually structure prompts with completion markers

**After**: Just type naturally - this-little-wiggy formats it for Ralph

## Quick Example

```bash
# You type:
claude "build a REST API for todos"

# this-little-wiggy generates:
/ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "build a REST API for todos

When complete:
- Tests pass
- Lint passes
- Build succeeds

Output <promise>COMPLETE</promise> when done."
```

## Installation

```bash
# From the this-little-wiggy directory
claude plugin marketplace add "$(pwd)/.dev-marketplace/.claude-plugin/marketplace.json"
claude plugin install this-little-wiggy@local-dev
```

**Requires**: [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) plugin

## Setup

```bash
/this-little-wiggy:init
```

The wizard:
1. Explores your codebase to discover completion criteria
2. Asks for max iterations (budget-based: 5/10/20/30)
3. Lets you validate the discovered criteria
4. Saves config to `.claude/this-little-wiggy/config.yml`

## Usage

**Normal** - complex tasks auto-detected:
```bash
claude "implement user authentication"
claude "refactor the payment module"
```

**Bypass**:
```bash
claude "* just fix this one line"    # * prefix bypasses
claude "/ralph-loop:ralph-loop ..."             # already wrapped
```

## Config

```yaml
# .claude/this-little-wiggy/config.yml
defaultMaxIterations: 10

ralphWrapper: |
  /ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "{task}

  When complete:
  - Tests pass
  - Lint passes
  - Build succeeds

  Output <promise>COMPLETE</promise> when done."
```

## Architecture

```
User prompt → Hook → Task Evaluator (haiku) → Task Analyzer → /ralph-loop:ralph-loop
```

## Testing

```bash
uv run pytest tests/ -v
```

## License

MIT
