# PR Template

Use this template when creating pull requests:

```bash
gh pr create --title "type: description" --body "$(cat <<'EOF'
## Summary
[Brief description of what this PR does]

## Changes
- [List key changes]
- [Be specific]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-reviewed
- [ ] Updated documentation
- [ ] No console.logs or debug code

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Additional Context
[Any extra information reviewers should know]
EOF
)"
```

## Usage Notes

- **Title**: Follows conventional commits format (`feat:`, `fix:`, etc.)
- **Sections**: Fill in relevant sections, remove inapplicable ones
- **Checkboxes**: Check applicable items before submitting
- **Screenshots**: Include for any UI/visual changes
