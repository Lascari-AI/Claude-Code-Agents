# Research System

On-demand research for understanding code and gathering context.

---

## Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RESEARCH SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Research is triggered ON-DEMAND, not automatically.                        │
│                                                                             │
│  Single command with two modes:                                             │
│  • /research [query] — Standalone, creates ephemeral session                │
│  • /research [query] --session=X — Attaches to existing session             │
│                                                                             │
│  Dynamically assesses complexity and spawns subagents iteratively.          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Entry Points

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESEARCH ENTRY POINTS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  /research [query]                                                    │ │
│  │  Standalone research - creates ephemeral session for traceability     │ │
│  │                                                                       │ │
│  │  Example:                                                             │ │
│  │  /research How does the authentication system work?                   │ │
│  │  /research How do I add a new API endpoint? --style=cookbook          │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  /research [query] --session=X --phase=X --triggered-by=X             │ │
│  │  Session-attached - stores in existing session's research/            │ │
│  │                                                                       │ │
│  │  Example:                                                             │ │
│  │  /research How does auth work? --session=2026-01-12_feature           │ │
│  │    --phase=spec --triggered-by="Need to understand before planning"   │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Complexity-Based Subagent Scaling

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DYNAMIC COMPLEXITY ASSESSMENT                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Subagent count adapts based on exploration findings (1-15 range):          │
│                                                                             │
│  ┌─────────────┬───────────┬───────────────────────────────────────────┐   │
│  │ SIMPLE      │ 1-2       │ Single file/module, focused question      │   │
│  │             │ subagents │ Grep hits in one area                     │   │
│  ├─────────────┼───────────┼───────────────────────────────────────────┤   │
│  │ MEDIUM      │ 3-5       │ Multiple related modules                  │   │
│  │             │ subagents │ Component interactions                    │   │
│  ├─────────────┼───────────┼───────────────────────────────────────────┤   │
│  │ COMPLEX     │ 5-10      │ Cross-cutting concerns                    │   │
│  │             │ subagents │ Multiple systems/architectures            │   │
│  └─────────────┴───────────┴───────────────────────────────────────────┘   │
│                                                                             │
│  Iterative: If gaps detected after batch, spawn more (up to MAX=15)         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Report Styles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REPORT STYLES                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Style is inferred from question phrasing OR specified with --style=X      │
│                                                                             │
│  ┌─────────────┬────────────────────────────────────────────────────────┐  │
│  │ cookbook    │ "How do I do X?"                                       │  │
│  │             │ → Step-by-step guidance with patterns to follow        │  │
│  │             │                                                        │  │
│  │             │ Triggers: "How do I...", "How would I...",             │  │
│  │             │           "Show me how to...", "What's the pattern..." │  │
│  ├─────────────┼────────────────────────────────────────────────────────┤  │
│  │ understanding│ "How does X work?" (DEFAULT)                          │  │
│  │             │ → Explain architecture and design                      │  │
│  │             │                                                        │  │
│  │             │ Triggers: "How does X work?", "Explain how...",        │  │
│  │             │           "What happens when...", "How is X structured?"│  │
│  ├─────────────┼────────────────────────────────────────────────────────┤  │
│  │ context     │ "What do I need to know for X?"                        │  │
│  │             │ → Information for planning/decision-making             │  │
│  │             │                                                        │  │
│  │             │ Triggers: "What do I need to know...",                 │  │
│  │             │           "What would be affected if...",              │  │
│  │             │           "Before I implement X..."                    │  │
│  └─────────────┴────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Research Flow

```
                         Research Request
                               │
                               ▼
                    ┌─────────────────────┐
                    │  1. Parse Arguments │
                    │  - query            │
                    │  - style            │
                    │  - session (if any) │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  2. Initialize      │
                    │  - Create session   │
                    │    (if standalone)  │
                    │  - Create research/ │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  3. Explore         │
                    │  - Tree structure   │
                    │  - Glob for files   │
                    │  - Grep for terms   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  4. Clarify?        │
                    │  (optional - ask    │
                    │   if ambiguous)     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  5. Assess          │
                    │  Complexity         │
                    │  (simple/medium/    │
                    │   complex)          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  6. Create Plan     │
                    │  (subtasks with     │
                    │   objective +       │
                    │   boundaries)       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 │
    ┌─────────────────┐                         │
    │  7. Spawn       │                         │
    │  Subagents      │◄────────────────────────┤
    │  (parallel)     │                         │
    └────────┬────────┘                         │
             │                                  │
             ▼                                  │
    ┌─────────────────┐                         │
    │  8. Evaluate    │     gaps found          │
    │  Coverage       │─────────────────────────┘
    │  (gap detect)   │     (iterate)
    └────────┬────────┘
             │ no gaps / max reached
             ▼
    ┌─────────────────┐
    │  9. Spawn       │
    │  Report Writer  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────┐
    │  10. Update Session │
    │  (research artifact)│
    └─────────────────────┘
```

---

## Artifacts

```
Standalone research (/research):
agents/sessions/{research-session-id}/
├── state.json                    # Ephemeral session state
├── spec.md                       # Auto-generated from question
└── research/
    └── {research-id}/
        ├── state.json            # Research metadata + iterations
        ├── report.md             # Final report
        └── subagents/
            ├── subagent_001.json
            ├── subagent_002.json
            └── ...               # Count varies by complexity

Session-attached research (/research --session=X):
agents/sessions/{parent-session-id}/
├── state.json                    # Parent session (updated with artifact ref)
├── spec.md
└── research/
    └── {research-id}/
        ├── state.json            # Includes: phase, triggered_by, iterations
        ├── report.md             # Findings
        └── subagents/
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/research [query]` | Standalone research (creates ephemeral session) |
| `/research [query] --session=X --phase=X --triggered-by=X` | Session-attached research |

### Optional Flags

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--style` | `cookbook`, `understanding`, `context` | inferred | Report format |
| `--session` | session ID | (none) | Attach to existing session |
| `--phase` | `spec`, `plan`, `debug` | (required with --session) | Which phase triggered research |
| `--triggered-by` | reason string | (required with --session) | Why research is needed |

---

*Draft - expand with subagent coordination details*
