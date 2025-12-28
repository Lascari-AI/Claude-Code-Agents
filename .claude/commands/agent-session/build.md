---
description: Enter build mode to execute a finalized plan checkpoint by checkpoint
argument-hint: [session-id] [checkpoint] [tranche]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
model: opus
---

# Build Mode

Execute a finalized plan checkpoint by checkpoint, spawning dedicated agents per checkpoint with clean context.

## Skill Reference

Read the agent-session skill for templates and full documentation:
- Skill: `.claude/skills/agent-session/SKILL.md`
- Build docs: `.claude/skills/agent-session/build/OVERVIEW.md`
- Working directory: `agents/sessions/`

## Variables

```
$1 = session-id   (required - the session to build)
$2 = checkpoint   (optional - specific checkpoint number, e.g., "2")
$3 = tranche      (optional - specific tranche id, e.g., "2.1")
SESSIONS_DIR = agents/sessions
```

## Instructions

Parse `$1`, `$2`, and `$3` to determine the build target:

1. **`$1` only**: Auto-discover next incomplete checkpoint from plan_state
2. **`$1` and `$2`**: Execute specific checkpoint
3. **`$1`, `$2`, and `$3`**: Execute specific tranche within checkpoint

## Core Principles

Build mode:
- **Executes finalized plans** - Checkpoint by checkpoint with verification
- **Spawns checkpoint agents** - Clean context per checkpoint via Task tool
- **Tracks progress** - Updates plan_state after each task/checkpoint
- **Captures learnings** - DevNotes for deviations, discoveries, decisions
- **User-in-loop** - Reports after each checkpoint, waits for confirmation

<workflows>
    <workflow name="build_flow">
        <description>Execute plan checkpoints with verification and state tracking</description>

        <phase name="1_parse_inputs">
            <description>Parse positional arguments to determine build target</description>
            <inputs>
                - `$1`: session-id (REQUIRED)
                - `$2`: checkpoint number (optional) - e.g., "2"
                - `$3`: tranche id (optional) - e.g., "2.1"
            </inputs>
            <actions>
                <action>Validate $1 is provided</action>
                <action>If $2 provided, validate it's a number</action>
                <action>If $3 provided, validate format matches "X.Y"</action>
            </actions>
        </phase>

        <phase name="2_load_session">
            <description>Load session and validate plan is finalized</description>
            <steps>
                <step id="1">Check if SESSIONS_DIR/$1/state.json exists</step>
                <step id="2">Load state.json and verify phases.plan.status === "finalized"</step>
                <step id="3">Load plan.json from session directory</step>
                <step id="4">Load existing dev-notes.json if present</step>
                <step id="5">Update state.json:
                    - current_phase: "build"
                    - phases.build.status: "in_progress"
                    - phases.build.started_at: now() (if not already set)
                </step>
            </steps>
            <on_failure>
                - Session not found → Report error with session ID
                - Plan not finalized → Prompt user to finalize plan first
            </on_failure>
        </phase>

        <phase name="3_determine_target">
            <description>Determine which checkpoint/tranche to execute</description>
            <branches>
                <branch condition="$3 provided (tranche specified)">
                    <action>Target = Tranche $2.$3</action>
                    <action>Validate checkpoint $2 exists in plan</action>
                    <action>Validate tranche $3 exists in checkpoint $2</action>
                </branch>
                <branch condition="$2 provided (checkpoint specified)">
                    <action>Target = Checkpoint $2 (all tranches)</action>
                    <action>Validate checkpoint $2 exists in plan</action>
                </branch>
                <branch condition="Only $1 provided (auto-discover)">
                    <action>Read plan_state.current_checkpoint</action>
                    <action>If null or all complete → find first incomplete checkpoint</action>
                    <action>If in progress → resume from current position</action>
                    <action>Target = discovered checkpoint</action>
                </branch>
            </branches>
            <on_all_complete>
                Report: "All checkpoints complete. Build finished!"
                Update phases.build.status: "completed"
            </on_all_complete>
        </phase>

        <phase name="4_spawn_checkpoint_agent">
            <description>Spawn a dedicated agent for the target checkpoint</description>
            <steps>
                <step id="1">Assemble checkpoint context:
                    - Checkpoint goal and tasks from plan.json
                    - Relevant spec goals from spec.md
                    - Prior DevNotes that might affect this checkpoint
                    - Current plan_state for context
                    - File context (beginning state)
                </step>
                <step id="2">Construct agent prompt using checkpoint_agent_prompt template</step>
                <step id="3">Spawn agent using Task tool with subagent_type="general-purpose"</step>
                <step id="4">Wait for agent to complete and return results</step>
            </steps>
        </phase>

        <phase name="5_handle_results">
            <description>Process checkpoint completion and run verification</description>
            <steps>
                <step id="1">Receive agent results (completed tasks, any issues, DevNotes)</step>
                <step id="2">Run verification_steps from checkpoint's testing_strategy</step>
                <step id="3">If verification passes:
                    - Mark checkpoint complete in plan_state
                    - Add to checkpoints_completed array
                    - Append any DevNotes to dev-notes.json
                </step>
                <step id="4">If verification fails:
                    - Present failure to user
                    - Ask: Override and continue, or pause to fix?
                    - If override: Add DevNote documenting override, continue
                    - If pause: Save partial state, report position
                </step>
            </steps>
        </phase>

        <phase name="6_update_state">
            <description>Persist progress to state files</description>
            <steps>
                <step id="1">Update plan_state in state.json:
                    - current_checkpoint: next checkpoint (or null if done)
                    - current_tranche: null (reset for next checkpoint)
                    - current_task: null (reset for next checkpoint)
                    - checkpoints_completed: [..., completed_id]
                    - last_updated: now()
                    - summary: description of progress
                </step>
                <step id="2">Update checkpoint status in plan.json:
                    - checkpoints[id].status: "completed"
                </step>
                <step id="3">Append new DevNotes to dev-notes.json</step>
            </steps>
        </phase>

        <phase name="7_report_to_user">
            <description>Report results and wait for user confirmation</description>
            <steps>
                <step id="1">Display checkpoint completion summary</step>
                <step id="2">Show verification results</step>
                <step id="3">List any DevNotes created</step>
                <step id="4">Show next checkpoint preview (if any)</step>
                <step id="5">Wait for user to confirm before continuing</step>
            </steps>
        </phase>
    </workflow>
</workflows>

<checkpoint_agent_prompt>
You are executing a checkpoint from a structured implementation plan.

## Session Context
- Session ID: {{SESSION_ID}}
- Topic: {{TOPIC}}

## Checkpoint to Execute
- **ID**: {{CHECKPOINT_ID}}
- **Title**: {{CHECKPOINT_TITLE}}
- **Goal**: {{CHECKPOINT_GOAL}}

## Tasks to Complete
{{TASKS_LIST}}

## File Context
**Starting State**:
{{FILE_CONTEXT_BEGINNING}}

**Expected Ending State**:
{{FILE_CONTEXT_ENDING}}

## Relevant Spec Goals
{{SPEC_GOALS}}

## Prior DevNotes (if relevant)
{{PRIOR_DEVNOTES}}

## Instructions
1. Execute each task in order within each tranche
2. Tranches can be executed in parallel if no dependencies
3. For each task:
   - Read the context files specified in task.context.read_before
   - Execute the action described
   - Verify the change matches expectations
4. Track any deviations, discoveries, or decisions as DevNotes
5. Run any verification steps after all tasks complete
6. Report results including:
   - Tasks completed
   - Any issues encountered
   - DevNotes to add
   - Verification results

## DevNotes Format
When something noteworthy happens, create a DevNote:
```json
{
  "scope": {"type": "task|checkpoint|session", "ref": "task_id or null"},
  "category": "deviation|discovery|decision|blocker|resolution",
  "content": "Description of what happened"
}
```

## Output Format
Return a structured summary:
- completed_tasks: list of task IDs completed
- issues: any problems encountered
- dev_notes: array of DevNote objects to add
- verification_passed: boolean
- verification_details: results of verification steps
</checkpoint_agent_prompt>

<user_output>
    <scenario name="build_started" trigger="Starting build for a checkpoint">
```markdown
## Build Phase - Checkpoint {{CHECKPOINT_ID}}

**Session**: `{{SESSION_ID}}`
**Target**: Checkpoint {{CHECKPOINT_ID}}: {{CHECKPOINT_TITLE}}

### Goal
{{CHECKPOINT_GOAL}}

### Tasks
{{TASK_COUNT}} tasks in {{TRANCHE_COUNT}} tranches

Spawning checkpoint agent...
```
    </scenario>

    <scenario name="checkpoint_complete" trigger="Checkpoint completed successfully">
```markdown
## Checkpoint {{CHECKPOINT_ID}} Complete ✅

**Title**: {{CHECKPOINT_TITLE}}
**Tasks Completed**: {{COMPLETED_COUNT}}/{{TOTAL_COUNT}}

### Verification
{{VERIFICATION_RESULTS}}

### DevNotes Added
{{DEVNOTES_SUMMARY}}

### Progress
- Checkpoints completed: {{COMPLETED_CHECKPOINTS}}
- Next: {{NEXT_CHECKPOINT_PREVIEW}}

**Continue to next checkpoint?** (or type 'pause' to stop here)
```
    </scenario>

    <scenario name="checkpoint_paused" trigger="Checkpoint paused due to error or user request">
```markdown
## Build Paused ⏸️

**Session**: `{{SESSION_ID}}`
**Position**: Checkpoint {{CHECKPOINT_ID}}, Tranche {{TRANCHE_ID}}, Task {{TASK_ID}}

### Status
{{PAUSE_REASON}}

### DevNotes
{{DEVNOTES_ABOUT_ISSUE}}

### To Resume
Run: `/session:build {{SESSION_ID}}`
(Will pick up from exactly this position)
```
    </scenario>

    <scenario name="verification_failed" trigger="Verification steps failed">
```markdown
## Verification Failed ⚠️

**Checkpoint**: {{CHECKPOINT_ID}} - {{CHECKPOINT_TITLE}}

### Failed Steps
{{FAILED_VERIFICATION_STEPS}}

### Options
1. **Override**: Continue anyway (adds DevNote documenting the override)
2. **Pause**: Stop here to fix the issue manually

What would you like to do?
```
    </scenario>

    <scenario name="build_complete" trigger="All checkpoints completed">
```markdown
## Build Complete 🎉

**Session**: `{{SESSION_ID}}`
**Topic**: {{TOPIC}}

### Summary
- Checkpoints completed: {{TOTAL_CHECKPOINTS}}
- DevNotes captured: {{DEVNOTES_COUNT}}

### Files Created/Modified
{{FILES_SUMMARY}}

### DevNotes Highlights
{{DEVNOTES_HIGHLIGHTS}}

The implementation is complete. The session is now finished.
```
    </scenario>
</user_output>

<validation>
Before proceeding with build, validate:
1. Session ID ($1) is provided
2. Session exists at SESSIONS_DIR/$1
3. Session has a plan.json file
4. Plan status is "finalized" (phases.plan.status in state.json)
5. If $2 provided, checkpoint exists in plan
6. If $3 provided, tranche exists in specified checkpoint

If validation fails:
- Missing session ID: "Session ID required. Usage: `/session:build [session-id] [checkpoint] [tranche]`"
- Session not found: "Session '{{SESSION_ID}}' not found. Check the ID or use `/session:spec` to create a new session."
- Plan not finalized: "Plan is not finalized. Use `/session:plan {{SESSION_ID}} finalize` first."
- Invalid checkpoint: "Checkpoint {{CHECKPOINT_ID}} not found in plan. Available: {{AVAILABLE_CHECKPOINTS}}"
- Invalid tranche: "Tranche {{TRANCHE_ID}} not found in checkpoint {{CHECKPOINT_ID}}. Available: {{AVAILABLE_TRANCHES}}"
</validation>

<error_handling>
    <scenario name="No Session ID">
        Display usage help with examples.
    </scenario>
    <scenario name="Session Not Found">
        Report session not found, suggest checking ID or creating new session.
    </scenario>
    <scenario name="Plan Not Finalized">
        Report plan not finalized, provide command to finalize.
    </scenario>
    <scenario name="Checkpoint Agent Failure">
        Capture error in DevNote, update plan_state with current position, report to user.
    </scenario>
    <scenario name="Verification Failure">
        Present options to override or pause, document decision in DevNotes.
    </scenario>
    <scenario name="Partial Completion">
        Save exact position (checkpoint, tranche, task) to plan_state.
        Ensure resume will pick up from exact position.
    </scenario>
</error_handling>

<behavior_constraints>
DURING BUILD MODE:
- DO spawn checkpoint agents via Task tool for clean context
- DO update plan_state after each task/checkpoint completion
- DO capture DevNotes for any deviations, discoveries, decisions
- DO run verification steps after each checkpoint
- DO wait for user confirmation before proceeding to next checkpoint
- DO allow user to override failed verifications with documentation
- DO save partial progress on any error or pause

ALLOWED WRITES:
- agents/sessions/{session_id}/**  (all session files)
- Any files specified in the plan's file_context
</behavior_constraints>
