# Onboarding Flow

How new projects get set up with the documentation system. The critical first step: understanding what this thing is trying to BE.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ONBOARDING FLOW                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Goal: Get from "new project" to "docbase ready" so sessions can begin     │
│                                                                             │
│  The FOUNDATION INTERVIEW is the critical first step.                       │
│  Everything else builds on understanding what we're building.               │
│                                                                             │
│  NEW PROJECT ──▶ INIT ──▶ FOUNDATION ──▶ SCAFFOLD ──▶ CODEBASE ──▶ READY   │
│                          INTERVIEW                                          │
│                          (critical)                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Why Foundation Comes First

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE UNDERSTANDING PROBLEM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Without understanding what the system is trying to BE:                     │
│  • Agents make decisions that feel "off"                                    │
│  • Code changes drift from the core idea                                    │
│  • Every session starts with re-explaining context                          │
│                                                                             │
│  With Foundation captured:                                                  │
│  • Agents understand the mental model                                       │
│  • Decisions align with what feels "right"                                  │
│  • The core idea guides every change                                        │
│                                                                             │
│  This is NOT a PRD. It's capturing how you think about what you're         │
│  building—so agents can think about it the same way.                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Flow

```
                         NEW PROJECT / USER
                               │
                               ▼
                    ┌─────────────────────┐
                    │  /docs:init         │
                    │  Initialize docs/   │
                    │                     │
                    │  Creates:           │
                    │  - docs/ structure  │
                    │  - 00-foundation/   │
                    │  - 10-codebase/     │
                    │  - 99-appendix/     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  /docs:interview-   │
                    │  foundation         │
                    │                     │
                    │  CURIOUS EXPLORATION│
                    │  - What is this     │
                    │    trying to BE?    │
                    │  - What should it   │
                    │    do extremely     │
                    │    well?            │
                    │  - How do you think │
                    │    about this?      │
                    │                     │
                    │  Structure emerges  │
                    │  from conversation  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  /docs:write        │
                    │  foundation         │
                    │                     │
                    │  Generate docs      │
                    │  using whatever     │
                    │  structure emerged: │
                    │  - Problem-focused  │
                    │  - Vision-focused   │
                    │  - Thinking-focused │
                    │  - Single narrative │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  /docs:scaffold     │
                    │                     │
                    │  Map source dirs    │
                    │  to doc sections:   │
                    │  - src/api/ → 10-api│
                    │  - src/ui/ → 20-ui  │
                    │  - etc.             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  /docs:interview-   │
                    │  codebase           │
                    │                     │
                    │  Per-section        │
                    │  knowledge extract: │
                    │  - What does this   │
                    │    section do?      │
                    │  - Key concepts?    │
                    │  - Important files? │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  /docs:write        │
                    │  [section]          │
                    │                     │
                    │  Generate L2/L3     │
                    │  documentation:     │
                    │  - Section overview │
                    │  - Concept docs     │
                    └──────────┬──────────┘
                               │
                               ▼
                      ┌───────────────┐
                      │  DOCBASE      │
                      │  READY        │
                      │               │
                      │  Can now run  │
                      │  sessions     │
                      └───────────────┘
```

---

## The Foundation Interview

The most important step. This is where we capture understanding.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FOUNDATION INTERVIEW                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  NOT a checklist. NOT forcing categories.                                   │
│  CURIOUS EXPLORATION of how you think about what you're building.           │
│                                                                             │
│  The agent explores:                                                        │
│  • What is this trying to BE? (not features—the core idea)                 │
│  • What should it do extremely well?                                        │
│  • How do you think about this problem?                                     │
│  • What would feel "right" vs. "wrong"?                                    │
│  • Who would love this? Who would hate it?                                  │
│  • What's adjacent but explicitly not this?                                 │
│                                                                             │
│  Structure emerges from conversation:                                       │
│  • Problem-focused → problem.md, landscape.md, approach.md                  │
│  • Vision-focused → vision.md, constraints.md, direction.md                 │
│  • Thinking-focused → context.md, ideas.md, decisions.md                    │
│  • Simple projects → single foundation.md                                   │
│                                                                             │
│  Output: docs/.drafts/foundation.interview.md                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Commands Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/docs:init` | Create docs/ directory structure | First time setup |
| `/docs:interview-foundation` | Explore understanding through dialogue | After init (CRITICAL) |
| `/docs:write foundation` | Generate foundation docs from interview | After foundation interview |
| `/docs:scaffold` | Map source to doc sections | After foundation complete |
| `/docs:interview-codebase [section]` | Extract knowledge for a section | Per-section |
| `/docs:write [section]` | Generate L2/L3 docs for section | After section interview |

---

## Artifacts Created

```
docs/
├── 00-foundation/
│   ├── 00-overview.md      # Foundation overview (always)
│   └── [structure varies]  # Whatever emerged from interview:
│       │                   #   - problem.md, vision.md, approach.md
│       │                   #   - OR: context.md, ideas.md, decisions.md
│       │                   #   - OR: single foundation.md
│       │                   #   - OR: purpose.md, principles.md, boundaries.md
│
├── 10-codebase/
│   ├── 00-overview.md      # Codebase architecture overview (L1)
│   ├── 10-{section}/       # Per-section documentation (L2)
│   │   ├── 00-overview.md  # Section overview
│   │   └── *.md            # Concept docs (L3)
│   └── ...
│
└── 99-appendix/
    └── 00-overview.md      # Setup guides, operational docs
```

---

## Target Project Scope

This onboarding flow is designed for:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TARGET SCOPE                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  GOOD FIT:                                                                  │
│  • Microservice-scale projects                                              │
│  • Projects with a core idea they want to nail                              │
│  • Focused tools or libraries                                               │
│  • Applications with clear boundaries                                       │
│                                                                             │
│  LESS SUITED FOR:                                                           │
│  • Multi-million line monoliths                                             │
│  • Projects without a coherent vision                                       │
│  • Codebases that do "everything"                                           │
│                                                                             │
│  The assumption: There IS a core idea. The software SHOULD do               │
│  something extremely well. Foundation captures that.                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Notes

- Foundation interview should happen FIRST—it informs everything else
- The interview is interactive: agent explores, developer articulates
- Structure emerges from conversation, not forced into categories
- Documentation quality depends on the quality of understanding captured
- Onboarding can be incremental (one section at a time after Foundation)

---

*Draft - expand with more detail on each step*
