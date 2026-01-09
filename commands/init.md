---
description: Initialize this-little-wiggy configuration
argument-hint: "[--force]"
---

# Initialize this-little-wiggy

Interactive wizard to configure ralph-loop for this project.

**REQUIRES user confirmation via AskUserQuestion before writing config.**

## Workflow

### Step 1: Check Existing Config

```!
if [ -f ".claude/this-little-wiggy/config.yml" ]; then
  echo "CONFIG_EXISTS"
  cat .claude/this-little-wiggy/config.yml
else
  echo "NO_CONFIG"
fi
```

If config exists and `--force` was NOT provided in `$ARGUMENTS`:
- Use AskUserQuestion: Overwrite, Merge, or Cancel
- If Cancel, stop here

### Step 2: Pre-flight Check

First, explain to the user:
> "this-little-wiggy wraps your prompts with completion criteria so ralph-loop knows when a task is truly done. We'll auto-discover tests, linters, and quality checks from your project to build these criteria."

**Use AskUserQuestion** (1 question):

Ask: "Does this project have tests or quality checks we can discover?"

Options:
- "Yes, I have tests/checks" - Continue to discovery
- "Not sure, let's find out" - Continue to discovery
- "No, I need to set those up first" - Stop and provide guidance

If user selects "No, I need to set those up first":
- Tell them: "Work with Claude Code to create tests and document your quality checks first. Run `/this-little-wiggy:init` again when ready."
- Stop here

For other responses, tell them:
- "We'll auto-discover your completion criteria next."
- "Don't worry if you don't have many tests yet - you can add more later by editing the config manually or rerunning `/this-little-wiggy:init --force`."

### Step 3: Discover Completion Criteria

Use the Task tool with `subagent_type: Explore` (thoroughness: "very thorough") to discover what "done" looks like for this project.

Prompt the Explore agent:
```
Thoroughly explore this codebase to find ALL quality checks and completion criteria. Be exhaustive.

Look for:
- All Makefile targets (not just build/test/lint)
- All test types: unit, integration, golden/snapshot, e2e
- Static analysis: vet, fmt, gocyclo, complexity checks
- Linting configs and all linter rules
- CI/CD pipelines - what checks run there?
- .claude/ directory: skills, commands, slash commands (like /go-review)
- CLAUDE.md and any documentation mentioning required checks
- Any pre-commit hooks or git hooks
- Code review requirements

Return a comprehensive list of everything that should pass before work is considered done.
```

Build a list of completion criteria from the agent's findings.

**If no criteria discovered:**
- Tell user: "No tests or quality checks were found in this project."
- Remind them: "You can continue with a minimal config, or work with Claude Code to set up tests first."
- Use AskUserQuestion: "Continue with minimal config?" (Yes/No)
- If No, stop here with guidance to run init again later

### Step 4: User Configuration (MANDATORY)

**STOP - Use AskUserQuestion before proceeding.**

**First AskUserQuestion call** (2 questions):
1. **Max iterations** (multiSelect: false)
   - "5 (Pro or x5 Max)" - Tight budget
   - "10 (standard)" - Recommended
   - "20 (x20 Max)" - Medium budget
   - "30 (API)" - Bigger budget

2. **Core checks** (multiSelect: true) - build, test, lint, coverage

**Second AskUserQuestion call** (up to 3 questions):
3. **Static analysis** (multiSelect: true) - vet, fmt, gocyclo, etc.

4. **Advanced tests** (multiSelect: true) - integration, golden, e2e, etc.

5. **Other** (multiSelect: true) - review commands, docs, etc.

Only include questions where criteria were discovered.

**WAIT for all responses before continuing.**

### Step 5: Write Config

```!
mkdir -p .claude/this-little-wiggy
```

Write `.claude/this-little-wiggy/config.yml` with user's selections:

```yaml
defaultMaxIterations: 10

ralphWrapper: |
  /ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "{task}

  When complete:
  - Tests pass
  - Lint passes
  - Build succeeds

  Output <promise>COMPLETE</promise> when done."
```

**IMPORTANT:**
- File MUST be `.claude/this-little-wiggy/config.yml`
- Completion criteria come from user's selections in Step 4
- The `{task}` placeholder is substituted at runtime
- Express criteria as outcomes, not commands (e.g., "All tests pass" not "`make test`")

### Step 6: Confirm Success

Output summary:
- Config file location: `.claude/this-little-wiggy/config.yml`
- Max iterations configured
- Completion criteria configured

**Next steps:**
- Try a complex prompt to see it in action
- To modify: edit the config file directly, or rerun `/this-little-wiggy:init --force` to regenerate
