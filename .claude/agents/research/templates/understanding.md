# Understanding Report Template

<purpose>
For questions like: "How does X work?" / "What is the architecture of Y?"
Focus: Explain the system, its components, and how they interact.
</purpose>

<template>
# Understanding: {System/Component Name}

**Session**: {session_id}
**Generated**: {timestamp}

---

## Executive Summary

{3-5 paragraphs providing a complete conceptual understanding.
Someone reading only this section should grasp:
- What the system/component does
- How it fits into the larger architecture
- Key design decisions and their rationale
- How the pieces work together}

---

## Architecture Overview

{High-level description of the system structure}

```
{ASCII diagram showing component relationships}

Example:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │────▶│  Database   │
│   Request   │     │   Handler   │     │   Layer     │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │   Service   │
                    │   Layer     │
                    └─────────────┘
```

---

## Core Components

### {Component 1}

**Purpose**: {What this component does}

**Location**: `{path}`

**Key Responsibilities**:
- {Responsibility 1}
- {Responsibility 2}

**How it works**:

{Detailed explanation of the component's internal logic}

**File**: `{path}:{lines}`
```{language}
{Code showing the key logic}
```

**Explanation**: {Why this code works this way}

### {Component 2}

{Continue with other components...}

---

## Data Flow

{Describe how data moves through the system}

### {Flow 1}: {Description}

1. **{Step 1}**: {What happens} (`{file}:{line}`)
2. **{Step 2}**: {What happens} (`{file}:{line}`)
3. **{Step 3}**: {What happens} (`{file}:{line}`)

```{language}
{Code showing the flow}
```

---

## Key Interfaces

### {Interface/Contract Name}

**Defined in**: `{path}:{lines}`

```{language}
{Interface/type definition}
```

**Used by**: {Components that implement or consume this}

---

## Design Decisions

### Why {Decision}?

{Explanation of the architectural choice and its trade-offs}

**Evidence**: `{path}:{lines}`

---

## Dependencies

### Internal Dependencies

| Component | Depends On | Relationship |
|-----------|------------|--------------|
| `{component}` | `{dependency}` | {how they interact} |

### External Dependencies

| Package | Purpose | Used In |
|---------|---------|---------|
| `{package}` | {what it provides} | `{files}` |

---

## File Map

| File | Role | Key Content |
|------|------|-------------|
| `{path}` | {role} | {what it contains} |

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
- Explain the WHY, not just the WHAT
- Use diagrams to show relationships
- Trace data/control flow through the system
- Connect components to show how they work together
- Help the reader build a mental model
</writing_principles>
