---
name: task-analyzer
description: Executes pre-configured Ralph loop command with user's task. Invoked by task-evaluator agent for complex tasks.
---

# Task Analyzer Skill

This skill takes a user's task and executes the pre-configured ralph-loop command from the project's config.

## Prerequisites

This skill requires:
1. Project config at `.claude/this-little-wiggy/config.yml` (run `/this-little-wiggy:init` first)
2. The `ralph-wiggum` plugin installed (provides `/ralph-loop` command)

## Workflow

### Step 1: Load Config

Read the project configuration:

```!
cat .claude/this-little-wiggy/config.yml
```

If config doesn't exist, stop and tell the user:
"Config not found. Please run `/this-little-wiggy:init` first to set up quality gates."

### Step 2: Check ralph-wiggum Plugin

Verify the ralph-loop command is available. If the ralph-wiggum plugin is not installed:
- Warn the user: "ralph-wiggum plugin not detected. Installing would enable autonomous loop execution."
- Proceed with the task normally (without loop)

### Step 3: Execute Ralph Command

Extract `ralphWrapper` from the config. It contains the full `/ralph-loop` command with a `{task}` placeholder.

Substitute `{task}` with the original user request that was passed to this skill.

Execute the resulting command. For example, if the user's task was "Build a REST API for todos" and the config contains:

```
/ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "{task}

When complete:
- Build succeeds
- Lint passes
- All tests pass

Output <promise>COMPLETE</promise> when done."
```

The executed command becomes:

```
/ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "Build a REST API for todos

When complete:
- Build succeeds
- Lint passes
- All tests pass

Output <promise>COMPLETE</promise> when done."
```

## Important Notes

- The `ralphWrapper` is pre-generated during `/this-little-wiggy:init`
- This skill does minimal work - just substitution and execution
- The user can modify `config.yml` directly to customize the wrapper
- If gates need to change, re-run `/this-little-wiggy:init --force`
