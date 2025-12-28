# Build Phase

Execute the plan checkpoint by checkpoint with verification.

## Purpose

The build phase executes the planned transformation:
- Follows checkpoints sequentially
- Verifies each checkpoint before proceeding
- Allows course correction if issues arise
- Tracks progress in state.json

## Prerequisites

- Finalized plan (`phases.plan.status: "finalized"` in state.json)
- Session in build phase (`current_phase: "build"`)

## Workflow

```
1. Load plan.json
     ↓
2. Execute Checkpoint 1
     ├── Complete Tranche 1.1 tasks
     ├── Complete Tranche 1.2 tasks
     └── Run verification steps
     ↓
3. Verify checkpoint state
     ├── Good → Save checkpoint, continue
     └── Issues → Adjust remaining tasks
     ↓
4. Execute Checkpoint 2
     ↓
5. ... repeat for all checkpoints ...
     ↓
6. Complete build → Session done
```

## Execution Model

### Task Execution

For each task:
1. Load pre-read context from `task.context.read_before`
2. Execute action using IDK commands
3. Verify file changes match expectations
4. Mark task complete in plan_state

### Checkpoint Verification

After each checkpoint:
1. Run `testing_strategy.verification_steps`
2. Compare actual files to `file_context.ending`
3. Document any deviations
4. Adjust remaining checkpoints if needed

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

## Commands

| Command | Description |
|---------|-------------|
| `/session:build [session-id]` | Start/resume build |
| `/session:build [session-id] status` | Check build progress |

## Error Handling

When issues occur:

1. **Task Failure**:
   - Mark task blocked
   - Document issue in state
   - Determine if blocker or workaround needed

2. **Checkpoint Verification Failure**:
   - Document deviation
   - Assess impact on future checkpoints
   - Adjust remaining tasks if needed

3. **Critical Blocker**:
   - Pause build
   - Return to plan phase for revision
   - Update plan.json with learnings

## Completion

Session is complete when:
- [ ] All checkpoints executed
- [ ] All verification steps pass
- [ ] `phases.build.status` set to "completed"
- [ ] `current_phase` set to "complete"

## Outputs

- Working code (per plan)
- Updated `state.json` with completion status
- Build log in `context/build-log.md` (optional)
