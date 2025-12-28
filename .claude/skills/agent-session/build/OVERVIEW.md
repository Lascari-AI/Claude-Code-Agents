# Build Phase

Execute the plan checkpoint by checkpoint with verification, spawning dedicated agents per checkpoint.

## Purpose

The build phase executes the planned transformation:
- Spawns checkpoint agents for clean context per checkpoint
- Follows checkpoints sequentially with verification
- Tracks progress in state.json for pause/resume capability
- Captures implementation learnings in DevNotes
- Allows user-in-loop validation after each checkpoint

## Prerequisites

- Finalized plan (`phases.plan.status: "finalized"` in state.json)
- Session in build phase (`current_phase: "build"`)

## Workflow

```
1. Parse arguments ($1=session, $2=checkpoint, $3=tranche)
     ↓
2. Load session (state.json, plan.json, dev-notes.json)
     ↓
3. Determine target
     ├── Auto-discover from plan_state
     ├── Explicit checkpoint ($2)
     └── Explicit tranche ($2.$3)
     ↓
4. Spawn checkpoint agent (Task tool)
     ├── Assemble context (checkpoint, spec goals, prior DevNotes)
     ├── Execute tasks in tranches
     └── Return results + DevNotes
     ↓
5. Run verification steps
     ├── Pass → Mark complete, continue
     └── Fail → User decides: override or pause
     ↓
6. Update state (plan_state, dev-notes.json)
     ↓
7. Report to user, wait for confirmation
     ↓
8. Repeat for next checkpoint or complete build
```

## Execution Model

### Checkpoint Agents

Each checkpoint spawns a dedicated agent via the Task tool:
- **Clean context**: Agent starts fresh with only relevant information
- **Self-contained**: All needed context included in prompt
- **Focused**: Only executes tasks for that checkpoint

Agent receives:
- Checkpoint goal and tasks from plan.json
- Relevant spec goals
- Prior DevNotes that might affect this work
- File context (beginning/ending state)

### Task Execution

For each task within the checkpoint agent:
1. Load pre-read context from `task.context.read_before`
2. Execute action using IDK commands
3. Verify file changes match expectations
4. Track any deviations as DevNotes

### Checkpoint Verification

After all tasks complete:
1. Run `testing_strategy.verification_steps`
2. Compare actual files to `file_context.ending`
3. If verification fails:
   - User can **override** (continues with DevNote documenting decision)
   - User can **pause** (partial completion, exact position saved)

## State Tracking

The `plan_state` in state.json tracks progress:

```json
{
  "plan_state": {
    "status": "in_progress",
    "current_checkpoint": 2,
    "current_tranche": "2.1",
    "current_task": "2.1.3",
    "checkpoints_completed": [1],
    "last_updated": "2025-12-24T12:00:00Z",
    "summary": "Completed checkpoint 1. Working on checkpoint 2, task 2.1.3."
  }
}
```

## DevNotes

DevNotes capture implementation learnings in `dev-notes.json`:

```json
{
  "notes": [
    {
      "id": "dn-001",
      "timestamp": "2025-12-28T12:00:00Z",
      "scope": { "type": "task", "ref": "1.2.3" },
      "category": "deviation",
      "content": "Used async/await instead of callbacks as planned"
    }
  ]
}
```

### Categories

| Category | When to Use |
|----------|-------------|
| `deviation` | Did something different than planned |
| `discovery` | Found something affecting current/future work |
| `decision` | Made a choice during implementation |
| `blocker` | Encountered something preventing progress |
| `resolution` | How a blocker was resolved |

### Scope Types

- `task` - Note about a specific task (ref: task ID like "1.2.3")
- `checkpoint` - Note about entire checkpoint (ref: checkpoint ID like "1")
- `session` - Session-wide note (ref: null)

## Commands

```
/session:build [session-id] [checkpoint] [tranche]

Arguments:
  $1 = session-id   (required)
  $2 = checkpoint   (optional - specific checkpoint number)
  $3 = tranche      (optional - specific tranche id)
```

### Examples

| Command | Description |
|---------|-------------|
| `/session:build my-session` | Auto-discover next checkpoint |
| `/session:build my-session 2` | Execute checkpoint 2 |
| `/session:build my-session 2 2.1` | Execute only tranche 2.1 |

## Error Handling

### Partial Completion

Errors are treated like a pause:
- Track exact position (checkpoint, tranche, task)
- Update plan_state with current progress
- Add DevNote capturing what went wrong
- Resume picks up exactly where stopped

### Verification Failure

When verification fails:
1. Present failure details to user
2. Offer options:
   - **Override**: Continue anyway (adds DevNote documenting override)
   - **Pause**: Stop to fix issue manually

## Completion

Session is complete when:
- [x] All checkpoints executed
- [x] All verification steps pass (or overridden)
- [x] `phases.build.status` set to "completed"
- [x] `current_phase` set to "complete"

## Outputs

- Working code (per plan)
- Updated `state.json` with completion status
- `dev-notes.json` with implementation learnings

## Templates

- [dev-notes.json](templates/dev-notes.json) - DevNotes template with schema
