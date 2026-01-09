# Ralph Wrapper Template

Generic self-correction template for ralph-loop.

## Template

```
/ralph-loop:ralph-loop --max-iterations {{defaultMaxIterations}} --completion-promise "COMPLETE" "{task}

When complete:
{{#each criteria}}
- {{this}}
{{/each}}

Output <promise>COMPLETE</promise> when done."
```

## Example

```
/ralph-loop:ralph-loop --max-iterations 10 --completion-promise "COMPLETE" "{task}

When complete:
- Tests pass
- Lint passes
- Build succeeds

Output <promise>COMPLETE</promise> when done."
```

## Why This Format?

- Flags before task for clarity
- Completion criteria discovered from project
- User validates what "done" means
- Works for any methodology (TDD, BDD, etc.)

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
