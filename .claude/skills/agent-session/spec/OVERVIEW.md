# Spec Phase

Define WHAT to build and WHY using a question-driven approach.

## Purpose

The spec phase captures requirements, goals, and context **before** implementation planning. It answers:
- What problem are we solving?
- What does success look like?
- What are we explicitly NOT building?

## Prerequisites

- New session created with `/session:spec [topic]`
- Or resuming existing session with `/session:spec [session-id]`

## Workflow

```
1. User provides topic/context
     ↓
2. Ask clarifying questions
     ↓
3. Draft spec sections iteratively
     ↓
4. User reviews and refines
     ↓
5. Finalize spec → Ready for plan phase
```

## Key Principles

1. **Question-driven**: Ask questions to understand before documenting
2. **Almost read-only**: Only write to session directory files
3. **WHAT not HOW**: Focus on outcomes, not implementation
4. **Iterative refinement**: Spec evolves through conversation

## Spec Document Sections

| Section | Purpose |
|---------|---------|
| **Overview** | Brief understanding of the problem space |
| **Problem Statement** | What we're solving and why it matters |
| **Goals (High/Mid/Detailed)** | Hierarchical goals from north star to specifics |
| **Non-Goals** | Explicit exclusions to prevent scope creep |
| **Success Criteria** | Testable outcomes - how we know we're done |
| **Context & Background** | Prior art, existing systems, stakeholder input |
| **Key Decisions** | Important decisions with rationale and date |
| **Open Questions** | Questions needing answers (checkbox format) |
| **Diagrams** | Mermaid/ASCII visualizations |
| **Notes** | Working notes and considerations |

## Commands

| Command | Description |
|---------|-------------|
| `/session:spec [topic]` | Start new spec session |
| `/session:spec [session-id]` | Resume existing session |
| `/session:spec [session-id] finalize` | Finalize spec for planning |

## Outputs

- `spec.md` - Specification document
- `state.json` - Session state (updated)
- `research/` - Any research artifacts gathered

## Finalization Criteria

Before finalizing, ensure:
- [ ] Problem statement is clear
- [ ] High-level goals are defined
- [ ] Non-goals explicitly stated
- [ ] Success criteria are testable
- [ ] No critical open questions remain
- [ ] Key decisions are documented

## Templates

- [spec.md](templates/spec.md) - Specification template
- [state.json](templates/state.json) - Session state template
