---
allowed-tools: Read, Bash(git:*), Bash(gh:*)
description: Analyze changes and create smart git commit(s)
arguments: "Additional instructions for the commit"
model: "sonnet"
---

additional instructions = $ARGUMENTS

> Conventions and guardrails are defined in the git skill (.claude/skills/git/SKILL.md)

# Smart Git Commit

## Workflow

### 1. Context Gathering

Before analyzing changes, gather repository context:

```bash
git rev-parse --show-toplevel  # Confirm we're in a git repo
git branch --show-current      # Current branch name
git rev-parse --abbrev-ref @{upstream} 2>/dev/null  # Upstream tracking
git status -sb                 # Ahead/behind status
```

### 2. Analyze Changes

Check current git status and analyze what changed:

```bash
git status
git diff --staged
git diff
```

### 3. Present Options

Based on the changes, present options in this exact format:

```
## Summary

- [Change category 1]
  - [Specific change]
  - [Specific change]
- [Change category 2]
  - [Specific change]
  - [Specific change]

## Options

1. Quick commit - Stage all and commit with a single message
2. Atomic commits - Split into [N] focused commits by logical grouping
3. Manual staging - Let me choose what to stage

## Recommendation

- Option [N]
  - [Brief reason 1]
  - [Brief reason 2]
```

Recommendation logic:
- If the changes are simple and cohesive, recommend option 1
- If the changes touch multiple unrelated areas, recommend option 2

### 4. Generate Message(s)

For each commit, follow the conventions from the git skill:
- Use appropriate commit type (feat/fix/docs/style/refactor/perf/test/chore)
- Follow conventional commits format: `type: description`
- For complex changes, include a body explaining WHY

### 5. Execute

Show the suggested message and ask for approval using a numbered list:

```
## Commit Message

`type: description`

## Approve?

1. Use as-is
2. Modify message
3. Add body details
4. Stage different files
```

Once approved, create the commit.

**Pre-commit hooks:**
- If pre-commit hooks fail, STOP and report the error
- Do NOT offer to skip hooks with `-n` or `--no-verify`
- The user must fix the issues before committing

### 6. Post-commit

After successful commit(s), run:

```bash
git log -1 --oneline   # Show the commit
git status             # Confirm working tree state
```

Then present next steps as a numbered list:

```
## Next Steps

1. Push to remote
2. Create a PR (using `gh pr create`)
3. Do nothing
```

If on `main`/`master` branch, warn before pushing and confirm.

## Formatting Rules

- Always present options to the user as a numbered list (1, 2, 3, 4)
  - Enables quick selection via hotkeys
  - No typing required from user
- Use bullets with subbullets for informational content
  - Summaries, explanations, status updates

## Success Criteria

- Commit(s) created with conventional format
- All pre-commit hooks passed
- Working tree in expected state
  - Clean, or only intentionally unstaged files remain
- Push completed if requested
