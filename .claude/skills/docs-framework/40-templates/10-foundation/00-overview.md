---
covers: Templates for the Foundation zone — overview, purpose, principles, and boundaries.
type: overview
concepts: [templates, foundation, purpose, principles, boundaries]
---

# Foundation Templates

Templates for the Foundation zone. Fixed structure templates for the overview, purpose, principles, and boundaries documents that capture system intent.

---

## Archetypes

| Template | Use When |
|----------|----------|
| **10-foundation-overview.md** | Creating the Foundation zone entry point |
| **20-purpose.md** | Documenting why the system exists |
| **30-principles.md** | Capturing decision-making heuristics |
| **40-boundaries.md** | Defining what the system won't do |

Foundation has a fixed structure. These four documents are always present and don't vary by project type.

## File Tree

```
10-foundation/
├── 00-overview.md              (this file)
├── 10-foundation-overview.md   Foundation zone entry point
├── 20-purpose.md               Why the system exists
├── 30-principles.md            Decision-making heuristics
└── 40-boundaries.md            What the system won't do
```

## Contents

### [10-foundation-overview.md](10-foundation-overview.md)
Template for `docs/00-foundation/00-overview.md`. Entry point for the Foundation zone with links to purpose, principles, and boundaries.

### [20-purpose.md](20-purpose.md)
Template for `docs/00-foundation/10-purpose.md`. Documents why the system exists, the problem it solves, and who benefits.

### [30-principles.md](30-principles.md)
Template for `docs/00-foundation/20-principles.md`. Decision-making heuristics that apply everywhere in the codebase.

### [40-boundaries.md](40-boundaries.md)
Template for `docs/00-foundation/30-boundaries.md`. Explicit non-goals, accepted constraints, and out-of-scope features.
