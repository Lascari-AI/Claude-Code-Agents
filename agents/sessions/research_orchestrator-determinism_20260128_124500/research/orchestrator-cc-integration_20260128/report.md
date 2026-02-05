# Context: Applying Orchestrator 3 Stream Patterns to Claude Code Config for Deterministic State Management

**Session**: orchestrator-cc-integration_20260128
**Generated**: 2026-01-28T12:55:00Z

---

## Summary

This research examines how patterns from the Orchestrator 3 Stream system (a PostgreSQL-backed, multi-agent orchestration platform) can be applied to the Claude Code config's file-based session system to increase determinism. The core insight is that determinism in the Orchestrator comes primarily from **architectural patterns** rather than just database infrastructure.

The Orchestrator achieves determinism through: (1) Pydantic models with Literal type status fields enforced by database CHECK constraints, (2) append-only logging for complete audit trails, (3) step lifecycle tracking with explicit start/end boundaries and duration metrics, and (4) atomic state updates with WebSocket broadcasting for observability.

The Claude Code config already has foundational elements that parallel these patterns: state.json tracks session phases and plan execution, universal_hook_logger.py writes append-only JSONL logs, and Pydantic models exist for plan structures. However, state updates currently rely on the agent using Edit tool calls without schema validation, and there is no explicit step boundary logging. The integration path focuses on **enhancing existing patterns** rather than adding database infrastructure.

---

## Affected Areas

### Primary Impact

| File/Component | Role | Why It's Affected |
|----------------|------|-------------------|
| `.claude/skills/session/spec/templates/state.json` | Session state structure | Would gain Pydantic validation and explicit status transitions |
| `.claude/hooks/logging/universal_hook_logger.py` | Event logging | Would gain event categorization and sequence numbers |
| `.claude/skills/session/plan/reference/models.py` | Plan Pydantic models | Already exists; extend pattern to state.json validation |
| `.claude/commands/session/*.md` | Phase commands | Would integrate phase boundary logging |

### Secondary Impact

| File/Component | Role | Potential Effect |
|----------------|------|------------------|
| `.claude/settings.json` | Hook configuration | May add new hooks for phase transitions |
| `agents/sessions/*/state.json` | Existing sessions | Could be validated against new schema |
| `.claude/skills/session/build/OVERVIEW.md` | Build documentation | Would document checkpoint timing tracking |

---

## Key Systems Involved

### Orchestrator Database Models

**Location**: `reference/orchestrator-agent-with-adws/apps/orchestrator_db/models.py`

**Relevance**: These models demonstrate how to enforce deterministic state through Pydantic with Literal types, achieving state machine semantics without a database.

**Key Points**:
- Status fields use `Literal['idle', 'executing', 'waiting', 'blocked', 'complete']` for compile-time type safety
- Field validators handle UUID conversion, Decimal-to-float conversion, and JSON parsing automatically
- `AiDeveloperWorkflow` model tracks step progress: `current_step`, `total_steps`, `completed_steps`, `error_step`, `error_message`
- All models have `created_at`/`updated_at` timestamps for audit trails

**File**: `reference/orchestrator-agent-with-adws/apps/orchestrator_db/models.py:338-390`
```python
class AiDeveloperWorkflow(BaseModel):
    """
    Tracks AI Developer Workflow executions in the system.

    Maps to: ai_developer_workflows table
    """
    id: UUID
    orchestrator_agent_id: Optional[UUID] = None
    adw_name: str
    workflow_type: str
    description: Optional[str] = None
    status: Literal['pending', 'in_progress', 'completed', 'failed', 'cancelled'] = 'pending'
    current_step: Optional[str] = None
    total_steps: int = 0
    completed_steps: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    error_step: Optional[str] = None
    error_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
```

### ADW Step Execution Pattern

**Location**: `reference/orchestrator-agent-with-adws/adws/adw_workflows/adw_plan_build.py`

**Relevance**: This workflow demonstrates the deterministic step execution pattern that could be adapted for session phase transitions.

**Key Points**:
- Steps defined as constants: `STEP_PLAN = "plan"`, `STEP_BUILD = "build"`, `TOTAL_STEPS = 2`
- Each step follows: create agent -> `log_step_start` -> update status to in_progress -> execute -> `log_step_end`
- Duration tracked per-step using `time.time()` with `duration_ms` calculation
- Sequential orchestration with early exit on failure
- Final status states: 'completed', 'failed', 'cancelled' with timestamps

**File**: `reference/orchestrator-agent-with-adws/adws/adw_workflows/adw_plan_build.py:388-446`
```python
async def run_plan_step(
    adw_id: str,
    orchestrator_agent_id: str,
    prompt: str,
    working_dir: str,
    model: str = ModelName.OPUS.value,
) -> tuple[bool, str | None, str | None]:
    """Run the /plan step."""
    step_start_time = time.time()

    # Create agent record upfront (name includes ADW ID for uniqueness)
    agent_id = await create_agent(
        orchestrator_agent_id=orchestrator_agent_id,
        name=f"plan-{adw_id[:8]}",
        model=model,
        working_dir=working_dir,
        adw_id=adw_id,
        adw_step=STEP_PLAN,
    )

    # Update agent status to executing (broadcast status change)
    await update_agent(agent_id=agent_id, status="executing", old_status="idle")

    # Log step start
    await log_step_start(
        adw_id=adw_id,
        adw_step=STEP_PLAN,
        agent_id=agent_id,
        payload={"prompt": prompt, "model": model},
        summary=f"Starting plan step for: {prompt[:100]}...",
    )

    # Update ADW status
    await update_adw_status(
        adw_id=adw_id,
        status="in_progress",
        current_step=STEP_PLAN,
    )
```

### Step Logging Module

**Location**: `reference/orchestrator-agent-with-adws/adws/adw_modules/adw_logging.py`

**Relevance**: This module provides the step boundary logging functions that enable deterministic replay and debugging.

**Key Points**:
- `log_step_start` writes event with `event_category="adw_step"`, `event_type="StepStart"`
- `log_step_end` includes status ('success', 'failed', 'skipped') and optional `duration_ms`
- All functions write to database AND broadcast via WebSocket
- Resilient design: WebSocket failures are silently ignored, workflow continues

**File**: `reference/orchestrator-agent-with-adws/adws/adw_modules/adw_logging.py:94-194`
```python
async def log_step_start(
    adw_id: str,
    adw_step: str,
    agent_id: Optional[str] = None,
    payload: Optional[dict[str, Any]] = None,
    summary: Optional[str] = None,
) -> str:
    """
    Log the start of an ADW step.
    Writes to database AND broadcasts via WebSocket for real-time updates.
    """
    default_summary = f"Step '{adw_step}' started"

    log_id = await write_agent_log(
        adw_id=adw_id,
        adw_step=adw_step,
        event_category="adw_step",
        event_type="StepStart",
        content=f"StepStart: {adw_step}",
        agent_id=agent_id,
        payload=payload,
        summary=summary or default_summary,
    )

    # Broadcast step change via WebSocket (fails silently if unavailable)
    await ws_broadcast_adw_step_change(
        adw_id=adw_id,
        step=adw_step,
        event_type="StepStart",
        payload=payload,
    )

    return log_id
```

### Claude Code Universal Hook Logger

**Location**: `.claude/hooks/logging/universal_hook_logger.py`

**Relevance**: This is the existing event logging foundation in Claude Code config that can be enhanced with the patterns from the Orchestrator.

**Key Points**:
- Already implements append-only JSONL logging (event sourcing pattern)
- Logs organized by session_id and hook_event_name
- Directory structure: `agents/logging/hook_logs/{session_id}/{hook_name}.jsonl`
- Non-blocking errors - failures don't stop hook execution

**File**: `.claude/hooks/logging/universal_hook_logger.py:1-69`
```python
#!/usr/bin/env uv run
"""
Universal Hook Logger - Claude Code Hook
Logs all hook payloads to session-specific JSONL files
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def create_log_entry(input_data: dict) -> dict:
    """Create enriched log entry with timestamp and full payload."""
    return {"timestamp": datetime.now().isoformat(), "payload": input_data}


def write_log_entry(session_id: str, hook_name: str, log_entry: dict) -> None:
    """Write log entry to appropriate JSONL file."""
    # Use CLAUDE_PROJECT_DIR if available, otherwise use cwd
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

    # Create directory structure relative to project root (within agents/logging/)
    log_dir = Path(project_dir) / "agents" / "logging" / "hook_logs" / session_id
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create hook-specific log file
    log_file = log_dir / f"{hook_name}.jsonl"

    # Append to JSONL file
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### Claude Code Session State Template

**Location**: `.claude/skills/session/spec/templates/state.json`

**Relevance**: This is the current state structure that would be enhanced with Pydantic validation and explicit status transitions.

**Key Points**:
- Tracks session_id, topic, description, granularity, parent_session
- Phases object with spec/plan/build, each with status and timestamps
- plan_state tracks checkpoint execution progress
- Arrays for commits, research_artifacts, doc_updates

**File**: `.claude/skills/session/spec/templates/state.json:14-36`
```json
"current_phase": "spec",
"phases": {
  "spec": {
    "_status_values": ["draft", "finalized", "finalized_complete"],
    "_status_notes": {
      "draft": "Spec in progress, not yet complete",
      "finalized": "Spec complete, ready for plan phase",
      "finalized_complete": "Spec complete, no plan needed"
    },
    "status": "draft",
    "started_at": "{{CREATED_AT}}",
    "finalized_at": null
  },
  "plan": {
    "status": null,
    "started_at": null,
    "finalized_at": null
  },
  "build": {
    "status": null,
    "started_at": null,
    "completed_at": null
  }
}
```

### Claude Code Plan State Model

**Location**: `.claude/skills/session/plan/reference/models.py`

**Relevance**: Demonstrates that Pydantic models already exist in the Claude Code config for type-safe structures; the pattern can be extended to state.json.

**Key Points**:
- `PlanState` model with `Literal["not_started", "in_progress", "complete"]` status
- Tracks current_checkpoint, current_task_group, current_task
- checkpoints_completed as list of integers
- last_updated and summary fields for progress tracking

**File**: `.claude/skills/session/plan/reference/models.py:173-191`
```python
class PlanState(BaseModel):
    """Tracks plan execution progress in state.json."""

    status: Literal["not_started", "in_progress", "complete"] = Field(
        default="not_started"
    )
    current_checkpoint: Optional[int] = Field(
        None, description="Currently executing checkpoint"
    )
    current_task_group: Optional[str] = Field(
        None, description="Currently executing task group ID"
    )
    current_task: Optional[str] = Field(None, description="Currently executing task ID")
    checkpoints_completed: list[int] = Field(default_factory=list)
    last_updated: Optional[datetime] = None
    summary: Optional[str] = Field(
        None, description="Brief progress summary for quick resume"
    )
```

---

## Constraints & Invariants

### Architecture Differences

| Constraint | Source | Implication |
|------------|--------|-------------|
| Claude Code uses file-based state | `.claude/skills/session/SKILL.md` | No ACID transactions; atomic writes require write-to-temp-then-rename pattern |
| Orchestrator uses PostgreSQL + SDK | `reference/orchestrator-agent-with-adws/understanding.md` | Database features (indexes, constraints) not directly portable |
| State updates via Edit tool | `.claude/commands/session/spec.md` | No automated validation; relies on agent following instructions |
| Single-agent per session assumption | `.claude/skills/session/SKILL.md` | No concurrent write handling needed |

### Existing Patterns

**Pattern**: Atomic Persistence
**Used in**: `.claude/commands/session/spec.md`, `.claude/commands/session/build.md`
**Expectation**: Update state.json after EVERY user exchange (spec) or after EACH task completion (build)

**Pattern**: Append-Only Logging
**Used in**: `.claude/hooks/logging/universal_hook_logger.py`
**Expectation**: Events are appended to JSONL files, never modified

**Pattern**: Pydantic for Type Safety
**Used in**: `.claude/skills/session/plan/reference/models.py`
**Expectation**: Complex structures defined with Pydantic models for validation

---

## Dependencies to Consider

### Upstream (Things This Depends On)

| Dependency | Location | Notes |
|------------|----------|-------|
| Pydantic v2 | Python dependency | Required for field validators and Literal types |
| Claude Code hooks | `.claude/settings.json` | Execution environment for logging hooks |
| Session skill | `.claude/skills/session/` | Defines lifecycle phases and state structure |

### Downstream (Things That Depend On This)

| Dependent | Location | Impact of Changes |
|-----------|----------|-------------------|
| Session commands | `.claude/commands/session/*.md` | Would need to integrate phase boundary logging |
| Existing sessions | `agents/sessions/*/state.json` | May need migration if schema changes |
| Research system | `.claude/agents/research/` | Uses session structure for research sessions |

---

## Configuration & Environment

| Config | Location | Purpose |
|--------|----------|---------|
| Hook definitions | `.claude/settings.json` | Defines which hooks run on which events |
| Session templates | `.claude/skills/session/spec/templates/` | Initial state.json structure |
| Plan models | `.claude/skills/session/plan/reference/models.py` | Pydantic definitions for plan structures |

---

## Prior Art

### Existing Pydantic Models in Claude Code Config

The plan system already uses Pydantic models for type-safe structures.

**File**: `.claude/skills/session/plan/reference/models.py:54-78`
```python
class Action(BaseModel):
    """File-scoped atomic operation within a task."""

    id: str = Field(..., description="Hierarchical ID, e.g., '1.1.1.1'")
    command: str = Field(..., description="IDK-formatted command")
    file: str = Field(..., description="Target file path")
    status: TaskStatus = Field(default="pending")


class Task(BaseModel):
    """A unit of work within a task group."""

    id: str = Field(..., description="Hierarchical ID, e.g., '1.1.1'")
    title: str = Field(..., description="Short one-sentence summary (max)")
    file_path: str = Field(..., description="Primary file this task operates on")
    description: str = Field(..., description="Detailed description of what to do")
    context: TaskContext = Field(default_factory=TaskContext)
    depends_on: list[str] = Field(
        default_factory=list, description="Task IDs that must complete before this task"
    )
    status: TaskStatus = Field(default="pending")
    actions: list[Action] = Field(
        default_factory=list, description="Atomic operations to perform"
    )
```

**Lesson**: The pattern of using Literal types for status fields (`TaskStatus = Literal["pending", "in_progress", "complete", "blocked"]`) is already established in the codebase.

### Existing Real Session State

A completed session demonstrates the actual state tracking in practice.

**File**: `agents/sessions/2026-01-12_agent-session-overhaul_k9m2x7/state.json:132-179`
```json
"commits": [
  {
    "checkpoint_id": 1,
    "sha": "2d22684f1ab4e25eef03d18561cf60f91cd27678",
    "message": "checkpoint-1: Session directory structure & initialization script",
    "created_at": "2026-01-14T01:00:00Z"
  },
  {
    "checkpoint_id": 2,
    "sha": "2a57982",
    "message": "checkpoint-2: Research integration - unified session-based research",
    "created_at": "2026-01-14T02:30:00Z"
  }
],
"plan_state": {
  "status": "complete",
  "checkpoints_total": 6,
  "checkpoints_detailed": 6,
  "checkpoints_completed": [1, 2, 3, 4, 5, 6],
  "current_checkpoint": null,
  "current_task_group": null,
  "current_task": null,
  "last_updated": "2026-01-14T06:30:00Z"
}
```

**Lesson**: The structure already tracks checkpoint progress and links commits to checkpoints. What's missing is checkpoint timing (started_at, completed_at per checkpoint) and phase transition logging.

---

## Concept Mapping: Orchestrator to Claude Code

| Orchestrator Concept | Claude Code Equivalent | Gap Analysis |
|---------------------|----------------------|--------------|
| `AiDeveloperWorkflow.status` | `state.json.phases.{phase}.status` | CC has status but no Literal type enforcement |
| `AiDeveloperWorkflow.current_step` | `state.json.current_phase` | Equivalent |
| `AiDeveloperWorkflow.completed_steps` | `state.json.plan_state.checkpoints_completed` | Equivalent (array vs counter) |
| `AiDeveloperWorkflow.started_at` | `state.json.phases.{phase}.started_at` | Equivalent |
| `AiDeveloperWorkflow.error_message/error_step` | Not tracked | Gap: no error tracking per phase |
| `AiDeveloperWorkflow.duration_seconds` | Not tracked | Gap: no duration tracking |
| `AgentLog` with entry_index | `hook_logs/*.jsonl` lines | CC uses implicit ordering; could add sequence numbers |
| `log_step_start`/`log_step_end` | Not implemented | Gap: no explicit phase boundary logging |
| Hook factory pattern | Hook scripts in `.claude/hooks/` | Equivalent mechanism |

---

## Integration Patterns: Tiered Implementation

### Tier 1: Immediate Wins (Minimal Change)

**Pattern**: Atomic File Writes for state.json
```python
import json
import tempfile
from pathlib import Path

def atomic_write_state(state_path: Path, state_data: dict) -> None:
    """Write state.json atomically to prevent corruption."""
    state_path = Path(state_path)
    with tempfile.NamedTemporaryFile(
        mode='w',
        dir=state_path.parent,
        delete=False,
        suffix='.tmp'
    ) as tf:
        json.dump(state_data, tf, indent=2)
        temp_path = Path(tf.name)
    temp_path.rename(state_path)  # Atomic on POSIX
```
**Benefit**: Prevents state.json corruption if write fails mid-way.

**Pattern**: Event Categorization in JSONL Logs
```python
def create_log_entry(input_data: dict) -> dict:
    """Create enriched log entry with event categorization."""
    hook_name = input_data.get("hook_event_name", "Unknown")

    # Categorize events
    if hook_name in ("PreToolUse", "PostToolUse"):
        category = "tool"
    elif hook_name == "UserPromptSubmit":
        category = "prompt"
    elif hook_name in ("Stop", "SubagentStop"):
        category = "lifecycle"
    else:
        category = "other"

    return {
        "timestamp": datetime.now().isoformat(),
        "sequence": get_next_sequence(),  # Add ordering
        "category": category,
        "payload": input_data
    }
```
**Benefit**: Enables filtered log viewing and swimlane-style visualization.

### Tier 2: Medium Effort (Schema Validation)

**Pattern**: Pydantic Models for state.json
```python
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

PhaseStatus = Literal["draft", "finalized", "finalized_complete"]
PlanStatus = Literal["not_started", "in_progress", "complete"]
BuildStatus = Literal["not_started", "in_progress", "complete", "failed"]

class PhaseState(BaseModel):
    status: Optional[PhaseStatus] = None
    started_at: Optional[datetime] = None
    finalized_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None  # Add error tracking

class SessionState(BaseModel):
    session_id: str
    created_at: datetime
    updated_at: datetime
    topic: str
    description: str
    granularity: Literal["project", "feature", "sub_feature"] = "feature"
    parent_session: Optional[str] = None
    current_phase: Literal["spec", "plan", "build", "docs", "complete"]
    phases: dict[str, PhaseState]
    # ... rest of fields
```
**Benefit**: Type safety, automatic validation, clear contracts for state updates.

**Pattern**: Checkpoint Timing in plan_state
```python
class CheckpointTiming(BaseModel):
    checkpoint_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    status: Literal["pending", "in_progress", "complete", "failed"] = "pending"

class EnhancedPlanState(BaseModel):
    status: Literal["not_started", "in_progress", "complete"] = "not_started"
    current_checkpoint: Optional[int] = None
    checkpoint_timings: list[CheckpointTiming] = Field(default_factory=list)
    # ... rest of fields
```
**Benefit**: Duration tracking per checkpoint enables performance profiling.

### Tier 3: Future Consideration (If Cross-Session Queries Needed)

**Pattern**: SQLite for Session Index
```python
import sqlite3
from pathlib import Path

def index_session(session_path: Path, db_path: Path = Path("agents/sessions.db")):
    """Index session metadata in SQLite for querying."""
    state = json.loads((session_path / "state.json").read_text())

    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT OR REPLACE INTO sessions
        (session_id, topic, status, created_at, completed_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        state["session_id"],
        state["topic"],
        state["phases"]["build"]["status"] or state["current_phase"],
        state["created_at"],
        state["phases"]["build"].get("completed_at")
    ))
    conn.commit()
```
**Benefit**: Enables queries like "find all completed sessions this week" without reading every state.json.
**Trade-off**: Adds complexity; only valuable if cross-session queries become a frequent need.

---

## Trade-off Analysis

### Complexity vs. Determinism

| Approach | Complexity | Determinism Gain |
|----------|------------|------------------|
| Atomic file writes | Minimal | Medium - prevents corruption |
| Event categorization | Low | Medium - enables filtered replay |
| Pydantic validation | Medium | High - enforces valid states |
| Checkpoint timing | Medium | Medium - enables debugging |
| SQLite index | High | Low - only for cross-session queries |

### File Portability vs. Database Power

The Claude Code config currently benefits from:
- **Git-friendly**: Session directories can be committed, branched, diffed
- **Human-readable**: JSON files can be inspected directly
- **Portable**: Copy a session directory to share it

Adding database infrastructure would sacrifice these benefits. The recommended approach is to **keep files as primary storage** and only use SQLite if cross-session querying becomes critical.

### Agent Simplicity vs. Observability

The Orchestrator logs everything with AI summarization. This provides excellent observability but adds cost and complexity. For Claude Code:
- **Current**: Raw payloads logged to JSONL
- **Recommended**: Add event categorization and sequence numbers
- **Deferred**: AI summarization (add when needed, not proactively)

---

## Open Questions

- Should checkpoint timing be tracked in state.json or in a separate timing.json file?
- How should state.json schema migrations be handled for existing sessions?
- Is there value in creating a state validation hook that runs on SessionStart?
- Should phase boundary logging create entries in state.json or only in hook logs?

---

## Recommended Next Steps

1. **Implement atomic file writes** for state.json updates (immediate reliability win)
2. **Add sequence numbers and event categories** to universal_hook_logger.py (enables filtered viewing)
3. **Create SessionState Pydantic model** mirroring state.json structure (validates agent updates)
4. **Add checkpoint timing fields** to plan_state (started_at, completed_at, duration_ms per checkpoint)
5. **Create phase transition logging** functions similar to log_step_start/log_step_end
6. **Evaluate SQLite** after 3-6 months based on whether cross-session queries are needed

---

## File Reference

| File | Relevance | Key Content |
|------|-----------|-------------|
| `reference/orchestrator-agent-with-adws/apps/orchestrator_db/models.py` | Critical | Pydantic models with Literal status fields |
| `reference/orchestrator-agent-with-adws/adws/adw_workflows/adw_plan_build.py` | Critical | Step execution pattern with logging |
| `reference/orchestrator-agent-with-adws/adws/adw_modules/adw_logging.py` | High | Step boundary logging functions |
| `.claude/hooks/logging/universal_hook_logger.py` | High | Current JSONL logging implementation |
| `.claude/skills/session/spec/templates/state.json` | High | Session state structure |
| `.claude/skills/session/plan/reference/models.py` | High | Existing Pydantic models for plans |
| `agents/sessions/2026-01-12_agent-session-overhaul_k9m2x7/state.json` | Medium | Real session state example |

---

## Research Methodology

### Research Plan

**Source**: [research-plan.md](./research-plan.md)

**Planned Execution**:
- 5 subtasks investigating: DB schema/models, session state.json, ADW workflows, hook systems, integration patterns
- Success criteria: concept mapping, pattern identification, integration patterns, trade-off analysis

**Actual Execution**:
- 5 subagents completed as planned
- All 4 success criteria met
- No deviations from plan

### Success Criteria Completion

| Criteria | Status | Evidence |
|----------|--------|----------|
| SC1: Map Orchestrator DB models to CC session state | Met | Concept Mapping table above |
| SC2: Identify which patterns apply vs. require infrastructure | Met | Tiered Implementation section |
| SC3: Provide concrete integration patterns | Met | Code snippets in Tier 1-3 patterns |
| SC4: Assess trade-offs of file-based vs. database-backed | Met | Trade-off Analysis section |

### Queries Investigated

| ID | Title | Objective |
|----|-------|-----------|
| 001 | Orchestrator DB Schema and State Models Analysis | Analyze database models for deterministic patterns |
| 002 | Claude Code Session State.json Structure | Understand current state management |
| 003 | ADW Workflow Deterministic Step Execution | Investigate step execution patterns |
| 004 | Hook Systems for Observability | Examine hook systems in both codebases |
| 005 | Integration Patterns and Trade-offs | Identify practical integration approaches |

### Files Examined

28 files examined across 5 subagents, including:
- Orchestrator: models.py, adw_plan_build.py, adw_logging.py, database.py, hooks.py
- Claude Code: universal_hook_logger.py, state.json template, models.py, SKILL.md, settings.json
- Real session data: 2 complete session state.json files
