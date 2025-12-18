# Cookbook Report Template

<purpose>
For questions like: "How do I do X?" / "How would I implement Y?"
Focus: Step-by-step guidance using patterns from THIS codebase.
</purpose>

<template>
# How to: {Task Description}

**Session**: {session_id}
**Generated**: {timestamp}

---

## Quick Start

{2-3 sentences: The fastest path to accomplish the task, referencing existing patterns.}

---

## Step-by-Step Guide

### Step 1: {Action}

**What to do**: {Clear instruction}

**Follow this pattern from the codebase**:

**File**: `{path}:{lines}`
```{language}
{Real code snippet showing the pattern to follow}
```

**Adapt it by**: {How to modify for their use case}

### Step 2: {Action}

{Continue with next step...}

---

## Key Files to Modify

| File | Purpose | What to Add/Change |
|------|---------|-------------------|
| `{path}` | {role in the system} | {specific changes needed} |

---

## Patterns to Follow

### {Pattern Name}

This codebase uses {pattern description}. Here's an example:

**File**: `{path}:{lines}`
```{language}
{Example showing the pattern}
```

**Why this pattern**: {Brief explanation of the approach}

### {Pattern Name 2}

{Continue with additional patterns...}

---

## Common Pitfalls

- **{Pitfall 1}**: {What to avoid and why}
- **{Pitfall 2}**: {What to avoid and why}

---

## Testing Your Implementation

{How to verify the implementation works, based on existing test patterns}

```bash
{Commands to run tests}
```

---

## Related Files

| File | Relevance |
|------|-----------|
| `{path}` | {why it's relevant} |

---

## Research Methodology

### Queries Investigated

| ID | Title | Objective |
|----|-------|-----------|
| 001 | {title} | {objective} |

### Files Examined

{count} files examined across {count} subagents.
</template>

<writing_principles>
- Focus on ACTIONABLE guidance
- Show patterns TO FOLLOW, not just describe them
- Include real code the user can adapt
- Make it a recipe they can execute
- Anticipate common mistakes
</writing_principles>
