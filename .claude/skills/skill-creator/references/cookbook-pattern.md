# Cookbook Pattern

The Cookbook pattern is a structured template for skills that route user requests to different sub-workflows based on intent. It provides clear decision logic through IF/THEN/EXAMPLES syntax.

## When to Use

Use the Cookbook pattern when:
- Skill has 3+ distinct operation modes
- User intent drives which workflow executes
- Each mode has its own detailed workflow in a reference file
- Clear routing logic is needed between operations

Do NOT use when:
- Skill has a single linear workflow
- All operations are closely related
- Simple single-purpose skills

## Production Example

See `docs-framework/SKILL.md` for a battle-tested implementation with Navigate/Produce/Maintain operations.

---

## Full Template

```markdown
---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}}
---

# Purpose

{{PURPOSE_STATEMENT}}
Follow the `Instructions`, execute the `Workflow`, based on the `Cookbook`.

## Variables

{{VARIABLE_NAME_1}}: {{VARIABLE_VALUE_1}}
{{VARIABLE_NAME_2}}: {{VARIABLE_VALUE_2}}

## Instructions

- Based on the user's request, follow the `Cookbook` to determine which tool to use.

### {{SPECIAL_INSTRUCTION_SECTION_NAME}}

- IF: {{CONDITION_DESCRIPTION}}
- THEN:
  - {{ACTION_STEP_1}}
  - {{ACTION_STEP_2}}
  - {{ACTION_STEP_3}}
- EXAMPLES:
  - "{{EXAMPLE_TRIGGER_1}}"
  - "{{EXAMPLE_TRIGGER_2}}"
  - "{{EXAMPLE_TRIGGER_3}}"

## Workflow

1. Understand the user's request.
2. READ: `{{SKILL_TOOLING_PATH}}` to understand our tooling.
3. Follow the `Cookbook` to determine which tool to use.
4. Execute the `{{TOOL_EXECUTION_PATH}}: {{FUNCTION_SIGNATURE}}` tool.

## Cookbook

### {{COOKBOOK_ENTRY_1_NAME}}

- IF: {{COOKBOOK_ENTRY_1_CONDITION}}
- THEN: Read and execute: `{{COOKBOOK_ENTRY_1_PATH}}`
- EXAMPLES:
  - "{{COOKBOOK_ENTRY_1_EXAMPLE_1}}"
  - "{{COOKBOOK_ENTRY_1_EXAMPLE_2}}"
  - "{{COOKBOOK_ENTRY_1_EXAMPLE_3}}"

### {{COOKBOOK_ENTRY_2_NAME}}

- IF: {{COOKBOOK_ENTRY_2_CONDITION}}
- THEN: Read and execute: `{{COOKBOOK_ENTRY_2_PATH}}`
- EXAMPLES:
  - "{{COOKBOOK_ENTRY_2_EXAMPLE_1}}"
  - "{{COOKBOOK_ENTRY_2_EXAMPLE_2}}"
  - "{{COOKBOOK_ENTRY_2_EXAMPLE_3}}"
```

---

## Template Variables Reference

| Variable | Description |
|----------|-------------|
| `{{SKILL_NAME}}` | Hyphen-case skill identifier (e.g., `docs-framework`) |
| `{{SKILL_DESCRIPTION}}` | Trigger phrases and when to use (for frontmatter) |
| `{{PURPOSE_STATEMENT}}` | One-sentence description of what this skill does |
| `{{VARIABLE_NAME_N}}` | Configuration flag or path name (e.g., `DOCS_ROOT`) |
| `{{VARIABLE_VALUE_N}}` | Default value for the variable (e.g., `docs/`) |
| `{{SPECIAL_INSTRUCTION_SECTION_NAME}}` | Name for special handling logic section |
| `{{CONDITION_DESCRIPTION}}` | When to apply special instructions |
| `{{ACTION_STEP_N}}` | Steps to execute for special instructions |
| `{{EXAMPLE_TRIGGER_N}}` | Example user phrases that trigger special handling |
| `{{SKILL_TOOLING_PATH}}` | Path to skill's main tooling/reference file |
| `{{TOOL_EXECUTION_PATH}}` | Path to executable tool |
| `{{FUNCTION_SIGNATURE}}` | Function name and parameters |
| `{{COOKBOOK_ENTRY_N_NAME}}` | Name of the cookbook option (e.g., `Navigate`) |
| `{{COOKBOOK_ENTRY_N_CONDITION}}` | When to use this cookbook entry |
| `{{COOKBOOK_ENTRY_N_PATH}}` | Path to the cookbook's workflow file |
| `{{COOKBOOK_ENTRY_N_EXAMPLE_N}}` | Example user phrases for this entry |

---

## Section-by-Section Guide

### Purpose Section

Establishes the skill's function and references the execution model.

**Required elements:**
- Brief purpose statement
- Standard phrase: `Follow the 'Instructions', execute the 'Workflow', based on the 'Cookbook'.`

### Variables Section

Define reusable paths and configuration values at the top for easy modification.

**Common variables:**
- `SKILL_ROOT`: Path to skill directory (e.g., `.claude/skills/my-skill/`)
- `DOCS_ROOT`: Output directory for documentation skills
- Custom flags for behavior modification

### Instructions Section

General guidance that applies across all cookbook entries.

**Optional special instructions:**
- Use IF/THEN format for conditional handling
- Include EXAMPLES to clarify triggering conditions
- Keep focused on cross-cutting concerns

### Workflow Section

High-level numbered steps (usually 3-4) that define execution flow.

**Standard pattern:**
1. Understand request/intent
2. Match to Cookbook entry
3. Read and execute referenced workflow

### Cookbook Section

Multiple entries using IF/THEN/EXAMPLES format. Each entry routes to a sub-workflow.

**Entry structure:**
- **IF**: Condition/intent description
- **THEN**: Action (typically read and execute a reference file)
- **EXAMPLES**: 3+ example user requests

---

## Best Practices

1. **Keep SKILL.md lean**: Detailed workflows belong in referenced files
2. **3+ examples per entry**: Clarifies intent matching
3. **One reference file per cookbook entry**: Maintains separation of concerns
4. **Variables at top**: Easy to modify paths and configuration
5. **Consistent IF/THEN/EXAMPLES format**: Enables pattern matching

## Anti-Patterns

- Embedding full workflow logic in SKILL.md instead of references
- Fewer than 2 examples per cookbook entry
- Deeply nested references (keep one level deep)
- Mixing cookbook routing with inline instructions
- Omitting the standard Purpose phrase

---

## Initialization

Generate a Cookbook-pattern skill with:

```bash
scripts/init_skill.py <skill-name> --path <output-directory> --template cookbook
```
