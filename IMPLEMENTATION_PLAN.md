# this-little-wiggy Implementation Plan

> "Mayor Quimby gives Ralph the instructions. Ralph executes them." - This plugin prepares prompts for the ralph-wiggum loop plugin.

A Claude Code plugin that intercepts complex tasks, wraps them in the proper Ralph Wiggum format with success criteria, and hands off to `/ralph-loop` for autonomous execution.

## Overview

**Problem**: The ralph-wiggum plugin requires prompts to be properly formatted with:
- Clear completion criteria
- Phased execution plan
- `<promise>COMPLETE</promise>` markers
- Test/verification commands

**Solution**: this-little-wiggy intercepts user prompts, detects complex multi-step tasks, and automatically wraps them in Ralph-ready format before handing off to `/ralph-loop`.

## Architecture

```
this-little-wiggy/
├── .claude-plugin/
│   └── plugin.json               # Plugin metadata
├── hooks/
│   └── hooks.json                # UserPromptSubmit hook registration
├── scripts/
│   └── prompt-wrapper.py         # Detect & wrap complex tasks
├── commands/
│   └── init.md                   # /this-little-wiggy:init wizard
├── skills/
│   └── task-analyzer/
│       ├── SKILL.md              # Analyze task, generate Ralph format
│       └── references/
│           ├── prompt-templates.md    # Ralph format templates
│           └── phase-patterns.md      # Task decomposition patterns
└── tests/
    ├── test_hook.py
    ├── test_skill.py
    └── test_integration.py
```

## Flow Diagram

```
User: "build a REST API for todos"
        │
        v
┌─────────────────────────────────────────────┐
│ UserPromptSubmit Hook                        │
│ scripts/prompt-wrapper.py                    │
├─────────────────────────────────────────────┤
│ 1. Check bypass prefixes (*, /)              │
│ 2. Wrap with evaluation prompt               │
│ 3. Claude evaluates: complex multi-step?     │
│    - If simple: pass through unchanged       │
│    - If complex: invoke task-analyzer skill  │
│ 4. Skill loads config.json settings          │
│ 5. Skill generates Ralph-format prompt       │
│ 6. Output: /ralph-loop invocation            │
└─────────────────────────────────────────────┘
        │
        v
/ralph-loop "Build a REST API for todos.

Requirements:
- CRUD operations
- Input validation
- Tests passing

Phases:
Phase 1: Setup project structure and dependencies
Phase 2: Implement CRUD endpoints
Phase 3: Add input validation
Phase 4: Write and run tests

Verification: uv run pytest

When all phases complete and tests pass:
<promise>COMPLETE</promise>
" --max-iterations 30 --completion-promise "COMPLETE"
```

## Components

### 1. Hook: prompt-wrapper.py

**Purpose**: Intercept prompts and route to evaluation

**Logic**:
```python
# Bypass conditions
if prompt.startswith("*"):   # Explicit bypass
if prompt.startswith("/"):   # Slash commands

# Wrap with evaluation prompt
wrapped = f"""
TASK EVALUATION

Original request: "{prompt}"

EVALUATE: Is this a complex multi-step task that would benefit from
autonomous iteration with ralph-wiggum?

COMPLEX TASK indicators:
- Multiple distinct phases (build, test, deploy)
- Requires iterative implementation
- Has measurable completion criteria
- Would take multiple conversation turns manually

If COMPLEX: Invoke the task-analyzer skill to generate a Ralph-ready prompt
If SIMPLE: Proceed with original request unchanged
"""
```

**Token overhead**: ~150 tokens per prompt

### 2. Command: /this-little-wiggy:init

**Purpose**: Interactive wizard to configure project defaults

**Questions (via AskUserQuestion)**:

1. **Project Type**
   - API / CLI / Library / Frontend / Full-stack / Other
   - Affects: Phase templates, verification commands

2. **Test Command**
   - pytest / npm test / go test / make test / custom
   - Affects: Verification step in Ralph prompt

3. **Build Command** (optional)
   - npm run build / go build / make / custom / none
   - Affects: Build verification step

4. **Default Max Iterations**
   - 20 / 30 / 50 / custom
   - Affects: --max-iterations flag

5. **Phase Style**
   - single-phase: One monolithic task
   - multi-phase: 2-4 distinct phases
   - tdd-loop: Write tests -> Implement -> Verify -> Refactor

**Output**: `.claude/this-little-wiggy/config.json`

```json
{
  "projectType": "api",
  "testCommand": "uv run pytest",
  "buildCommand": null,
  "defaultMaxIterations": 30,
  "phaseStyle": "multi-phase"
}
```

### 3. Skill: task-analyzer

**Purpose**: Analyze task and generate Ralph-format prompt

**SKILL.md Workflow**:

```markdown
# Task Analyzer Skill

Generates Ralph Wiggum-ready prompts from user tasks.

## Input
- Original user task
- Project config from .claude/this-little-wiggy/config.json

## Process

1. **Analyze Task Scope**
   - Identify discrete deliverables
   - Estimate complexity
   - Determine verification methods

2. **Generate Phases** (based on phaseStyle)
   - single-phase: One comprehensive phase
   - multi-phase: Break into 2-4 logical phases
   - tdd-loop: Test -> Implement -> Verify -> Refactor cycle

3. **Build Ralph Prompt**
   - Clear task description
   - Numbered phases with acceptance criteria
   - Verification command from config
   - Completion promise marker

4. **Output**
   - Complete /ralph-loop command ready to execute
```

**Reference Files**:

- `prompt-templates.md`: Templates for different project types
- `phase-patterns.md`: Common phase decomposition patterns

### 4. Config Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "projectType": {
      "type": "string",
      "enum": ["api", "cli", "library", "frontend", "fullstack", "other"]
    },
    "testCommand": {
      "type": "string",
      "description": "Command to run tests"
    },
    "buildCommand": {
      "type": ["string", "null"],
      "description": "Command to build project (optional)"
    },
    "defaultMaxIterations": {
      "type": "integer",
      "minimum": 5,
      "maximum": 100,
      "default": 30
    },
    "phaseStyle": {
      "type": "string",
      "enum": ["single-phase", "multi-phase", "tdd-loop"],
      "default": "multi-phase"
    }
  },
  "required": ["projectType", "testCommand", "defaultMaxIterations", "phaseStyle"]
}
```

## Ralph Prompt Templates

### Multi-Phase Template (Default)

```
{task_description}

Requirements:
{requirements_list}

Phases:
Phase 1: {phase_1_description}
  - {acceptance_criteria_1}
Phase 2: {phase_2_description}
  - {acceptance_criteria_2}
Phase 3: {phase_3_description}
  - {acceptance_criteria_3}

Verification: {test_command}

When all phases complete and verification passes:
<promise>COMPLETE</promise>
```

### TDD Loop Template

```
{task_description}

Follow TDD approach:
1. Write failing tests for the feature
2. Implement minimum code to pass tests
3. Run tests: {test_command}
4. If tests fail: debug and fix
5. Refactor if needed
6. Repeat until all tests pass

When all tests pass:
<promise>COMPLETE</promise>
```

### Single Phase Template

```
{task_description}

Requirements:
{requirements_list}

Implementation:
- Complete all requirements
- Ensure tests pass
- Verify: {test_command}

When complete:
<promise>COMPLETE</promise>
```

## Implementation Steps

### Phase 1: Core Infrastructure

1. Create plugin manifest (`.claude-plugin/plugin.json`)
2. Create hook registration (`hooks/hooks.json`)
3. Implement basic prompt-wrapper.py with bypass logic
4. Add evaluation prompt wrapper

### Phase 2: Init Command

1. Create `commands/init.md` with AskUserQuestion workflow
2. Define config.json schema
3. Implement config file creation
4. Add .gitignore entry for config

### Phase 3: Task Analyzer Skill

1. Create `skills/task-analyzer/SKILL.md`
2. Create `references/prompt-templates.md`
3. Create `references/phase-patterns.md`
4. Implement phase generation logic

### Phase 4: Integration

1. Wire hook -> skill -> ralph-loop handoff
2. Handle edge cases (no config, ralph-wiggum not installed)
3. Add error handling and user feedback

### Phase 5: Testing & Documentation

1. Write unit tests for hook
2. Write integration tests
3. Create README.md with usage examples
4. Create demo GIF

## Dependencies

- **Required**: ralph-wiggum plugin (for /ralph-loop command)
- **Python**: 3.10+ (standard library only)
- **Claude Code**: 2.0.22+ (for AskUserQuestion tool)

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No config.json | Prompt user to run `/this-little-wiggy:init` first |
| ralph-wiggum not installed | Warn user, output formatted prompt for manual use |
| Empty/trivial prompt | Pass through unchanged |
| Already Ralph-formatted | Detect and pass through |
| Bypass prefix | Skip all processing |

## Token Overhead

| Component | Tokens | When |
|-----------|--------|------|
| Evaluation prompt | ~150 | Every prompt |
| Skill load (complex) | ~300 | Only complex tasks |
| Reference files | ~200 | Only when generating |
| **Total (simple)** | **~150** | Simple tasks |
| **Total (complex)** | **~650** | Complex tasks |

## Success Criteria

- [ ] `/this-little-wiggy:init` creates valid config.json via AskUserQuestion
- [ ] Hook correctly detects complex vs simple tasks
- [ ] Generated prompts work with `/ralph-loop` command
- [ ] Bypass prefixes work (*, /)
- [ ] Tests pass with >80% coverage
- [ ] Documentation complete with examples

## Future Enhancements

- Per-task question overrides (disabled for v1)
- Custom phase templates per project type
- Integration with prompt-improver for vague task clarification
- Metrics tracking for iteration success rates
