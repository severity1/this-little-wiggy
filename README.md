# this-little-wiggy

> "Mayor Quimby gives Ralph the instructions. Ralph executes them."

Type vibes, ship autonomy. Detects complex implementation tasks and wraps them in [ralph-loop](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-loop) format with project-specific completion criteria.

## Why?

You've already curated your workflows - slash commands, TDD prompts, issue references. Why write more prompts just to make them ralph-loop compatible?

this-little-wiggy lets you keep using your established workflows. Your existing prompts automatically get wrapped in ralph-loop format when they're complex enough to benefit from autonomous execution.

## What It Does

Intercepts complex implementation tasks and wraps them with project-specific completion criteria for autonomous execution.

**Before**: Manually structure every prompt with ralph-loop syntax and completion markers

**After**: Use your existing slash commands and prompts - this-little-wiggy handles the wrapping

## Quick Example

```bash
# You type your natural prompt:
claude "build a REST API for todos"

# Or use slash commands with a prefix:
claude "Execute /tdd phase1"

# this-little-wiggy wraps it for ralph-loop:
/ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "build a REST API for todos

When complete:
- Tests pass
- Lint passes
- Build succeeds

Output <promise>COMPLETE</promise> when done."
```

## Installation

**Requirements:**
- Claude Code 2.0.22+
- [ralph-loop](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-loop) plugin
- Python 3.10+ with `pyyaml` installed (`pip install pyyaml`)

> **Windows users:** Ensure Python is in your PATH and `pyyaml` is installed in the Python environment that Claude Code uses.

### Option 1: Via Marketplace (Recommended)

**1. Add the marketplace:**
```bash
claude plugin marketplace add severity1/severity1-marketplace
```

**2. Install the plugin:**
```bash
claude plugin install this-little-wiggy@severity1-marketplace
```

**3. Restart Claude Code**

Verify installation with `/plugin` command. You should see the this-little-wiggy plugin listed.

### Option 2: Local Plugin Installation (for Development)

**1. Clone the repository:**
```bash
git clone https://github.com/severity1/this-little-wiggy.git
cd this-little-wiggy
```

**2. Add the local marketplace:**
```bash
claude plugin marketplace add /absolute/path/to/this-little-wiggy/.dev-marketplace/.claude-plugin/marketplace.json
```

Replace `/absolute/path/to/` with the actual path where you cloned the repository.

**3. Install the plugin:**
```bash
claude plugin install this-little-wiggy@local-dev
```

**4. Restart Claude Code**

Verify installation with `/plugin` command. You should see "1 plugin available, 1 already installed".

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

**Normal prompts** - complex tasks auto-detected:
```bash
claude "implement user authentication"
claude "build a REST API for todos"
```

**Slash commands** - prefix with a word to prevent premature expansion:
```bash
claude "Execute /tdd phase1"
claude "Implement /tdd GH issue 32"
```

> **Why the prefix?** Without it, slash commands expand immediately before the hook can evaluate them. Adding "Execute", "Implement", or any word first lets the hook wrap the command with ralph-loop.

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
User prompt → Hook (prompt-evaluator.py) → RALPH-LOOP DIRECTIVE → Claude executes /ralph-loop:ralph-loop
```

The hook reads your project config and wraps prompts with completion criteria. Claude then evaluates whether to execute the wrapped prompt based on task complexity.

## Testing

```bash
uv run pytest tests/ -v
```

## License

MIT
