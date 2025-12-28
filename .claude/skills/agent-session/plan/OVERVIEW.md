# Plan Phase

Design HOW to implement the finalized spec using checkpoint-based planning.

## Purpose

The plan phase builds the **bridge** from current state to desired state:
- Analyzes existing codebase
- Designs checkpoint sequence
- Creates detailed tasks with IDK definitions
- Establishes testing strategy per checkpoint

## Prerequisites

- Finalized spec (`phases.spec.status: "finalized"` in state.json)
- Session in plan phase (`current_phase: "plan"`)

## Workflow

```
1. Load finalized spec + research
     ↓
2. Generate checkpoint outline (3-7 milestones)
     ↓
3. User confirms outline
     ↓
4. Detail checkpoint 1 tasks → User confirms
     ↓
5. Detail checkpoint 2 tasks → User confirms
     ↓
6. ... repeat for all checkpoints ...
     ↓
7. Finalize plan → Ready for build phase
```

## Key Concepts

### Checkpoints

Sequential milestones that incrementally move from current state to target state.

```json
{
  "id": 1,
  "title": "Implement Core Types",
  "goal": "Create foundational data types",
  "prerequisites": [],
  "status": "pending"
}
```

### Task Tranches

Parallelizable groups within a checkpoint. Tasks in a tranche can execute concurrently.

```json
{
  "id": "1.1",
  "goal": "Create base type definitions",
  "tasks": [...]
}
```

### Tasks

Units of work with full execution context. Uses IDK format for precise actions.

```json
{
  "id": "1.1.1",
  "title": "Define User type",
  "file_path": "src/types/user.ts",
  "action": "CREATE TYPE User: ...",
  "context": { "read_before": [...] }
}
```

## IDK Reference

Information-Dense Keywords for precise task definitions:

| Category | Keywords | File |
|----------|----------|------|
| **CRUD** | CREATE, UPDATE, DELETE | [idk/crud.md](idk/crud.md) |
| **Actions** | ADD, REMOVE, MOVE, REPLACE, MIRROR, MAKE, USE, APPEND | [idk/actions.md](idk/actions.md) |
| **Language** | VAR, FUNCTION, CLASS, TYPE, FILE, DEFAULT | [idk/language.md](idk/language.md) |
| **Location** | BEFORE, AFTER | [idk/location.md](idk/location.md) |
| **Refactoring** | REFACTOR, RENAME, SPLIT, MERGE, EXTRACT, INLINE, INSERT, WRAP | [idk/refactoring.md](idk/refactoring.md) |
| **Testing** | TEST, ASSERT, MOCK, VERIFY, CHECK | [idk/testing.md](idk/testing.md) |
| **Documentation** | COMMENT, DOCSTRING, ANNOTATE | [idk/documentation.md](idk/documentation.md) |

## File Context Tracking

Each checkpoint tracks beginning and ending file states:

```json
{
  "file_context": {
    "beginning": {
      "files": [{ "path": "...", "status": "exists" }],
      "tree": "ASCII tree visualization"
    },
    "ending": {
      "files": [{ "path": "...", "status": "new" }],
      "tree": "ASCII tree visualization"
    }
  }
}
```

## Testing Strategy

Each checkpoint includes verification approach:

```json
{
  "testing_strategy": {
    "approach": "Type checking and unit tests",
    "verification_steps": [
      "Run tsc --noEmit",
      "Run jest src/types/__tests__"
    ]
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/session:plan [session-id]` | Start/resume planning |
| `/session:plan [session-id] finalize` | Finalize plan for build |

## Outputs

- `plan.json` - Structured plan (source of truth)
- `plan.md` - Human-readable plan (generated)
- `state.json` - Updated with `plan_state`

## Templates

- [plan.json](templates/plan.json) - Plan structure template

## Reference

- [models.py](reference/models.py) - Pydantic models for type-safe plan structure

## Scripts

- [sync-plan-md.py](scripts/sync-plan-md.py) - Auto-generates plan.md from plan.json (triggered via PostToolUse hook)
