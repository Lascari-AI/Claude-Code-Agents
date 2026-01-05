---
name: git
description: Git workflow conventions and guardrails for this project. Use when performing any git operations, writing commits, understanding commit message conventions, or when agents need to follow project git standards without invoking explicit commands.
---

# Git Conventions

## Commit Types

Use conventional commits format with these types:

| Type | Use When |
|------|----------|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Restructuring without behavior change |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance, dependencies, config |

## Commit Message Format

```
type: concise description in imperative mood

Optional body explaining WHY, not just WHAT.
Reference issues when applicable.
```

Examples:
- `feat: add user authentication flow`
- `fix: prevent null pointer in checkout`
- `refactor: extract validation logic to separate module`

## Guardrails

These apply to ALL git operations:

- **Never force push** - Destructive to shared history
- **Never hard reset** - Use soft reset or revert instead
- **Never skip pre-commit hooks** - If they fail, fix the issue
- **Warn on main/master** - Confirm before commits or pushes to protected branches

## Attribution Rule

Never include AI attribution in commits:
- No "Generated with Claude Code"
- No "Co-Authored-By: Claude"

## References

- **[PR Template](references/pr-template.md)** - Standard pull request structure and format

## Commands

For interactive workflows, use the dedicated commands:

- `/git:commit` - Full interactive commit workflow with options
- `/git:sync-main` - Sync local main with remote
