# Context Report Template

<purpose>
For questions like: "What do I need to know before implementing X?" / "What would be affected if I change Y?"
Focus: Provide the knowledge foundation needed for planning or decision-making.
</purpose>

<template>
# Context: {Topic/Change Description}

**Session**: {session_id}
**Generated**: {timestamp}

---

## Summary

{2-3 paragraphs summarizing:
- The relevant systems/components involved
- Key constraints and considerations
- What someone needs to understand before proceeding}

---

## Affected Areas

### Primary Impact

| File/Component | Role | Why It's Affected |
|----------------|------|-------------------|
| `{path}` | {what it does} | {how it would be impacted} |

### Secondary Impact

| File/Component | Role | Potential Effect |
|----------------|------|------------------|
| `{path}` | {what it does} | {indirect effects} |

---

## Key Systems Involved

### {System 1}

**Location**: `{path}`

**Relevance**: {Why this matters for the task at hand}

**Key Points**:
- {Important fact 1}
- {Important fact 2}

**File**: `{path}:{lines}`
```{language}
{Relevant code snippet}
```

### {System 2}

{Continue with other relevant systems...}

---

## Constraints & Invariants

### {Constraint Category}

| Constraint | Source | Implication |
|------------|--------|-------------|
| {rule/limitation} | `{file}:{line}` | {what this means for changes} |

### Existing Patterns

{Patterns that should be maintained or considered}

**Pattern**: `{name}`
**Used in**: `{files}`
**Expectation**: {What new code should follow}

---

## Dependencies to Consider

### Upstream (Things This Depends On)

| Dependency | Location | Notes |
|------------|----------|-------|
| `{component}` | `{path}` | {relevant details} |

### Downstream (Things That Depend On This)

| Dependent | Location | Impact of Changes |
|-----------|----------|-------------------|
| `{component}` | `{path}` | {what would break/need updating} |

---

## Existing Tests

| Test File | Coverage | Relevance |
|-----------|----------|-----------|
| `{path}` | {what it tests} | {why it matters} |

**Testing Considerations**:
- {What tests might need updating}
- {What new tests might be needed}

---

## Configuration & Environment

| Config | Location | Purpose |
|--------|----------|---------|
| `{setting}` | `{file}` | {what it controls} |

---

## Prior Art

### Similar Implementations

{Examples of similar patterns already in the codebase}

**File**: `{path}:{lines}`
```{language}
{Example code}
```

**Lesson**: {What can be learned from this existing implementation}

---

## Open Questions

{Questions that emerged during research that might need clarification}

- {Question 1}
- {Question 2}

---

## Recommended Next Steps

1. {First thing to investigate or decide}
2. {Second consideration}
3. {Third step}

---

## File Reference

| File | Relevance | Key Content |
|------|-----------|-------------|
| `{path}` | Critical | {description} |
| `{path}` | High | {description} |
| `{path}` | Medium | {description} |

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
- Focus on what someone NEEDS TO KNOW before acting
- Identify dependencies and ripple effects
- Surface constraints that might not be obvious
- Don't suggest solutions - provide the foundation for planning
- Flag risks and considerations
- Point to prior art and existing patterns
</writing_principles>
