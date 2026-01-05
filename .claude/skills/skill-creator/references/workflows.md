# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Cookbook Pattern (Routing Workflows)

For skills that route user requests to different sub-workflows based on intent, use the structured Cookbook pattern. This pattern provides explicit decision logic through IF/THEN/EXAMPLES syntax.

**When to use:**
- Skill supports 3+ distinct operation modes
- User intent needs to be matched to the appropriate mode
- Each mode has its own detailed workflow in a reference file

**Structure overview:**
```markdown
## Cookbook

### Operation Name

- IF: [condition that triggers this operation]
- THEN: Read and execute: `references/operation-workflow.md`
- EXAMPLES:
  - "Example user request that would trigger this"
  - "Another example request"
```

**Production example:** See `docs-framework/SKILL.md` for Navigate/Produce/Maintain routing.

**Full documentation:** See [cookbook-pattern.md](cookbook-pattern.md) for complete template and guidelines.