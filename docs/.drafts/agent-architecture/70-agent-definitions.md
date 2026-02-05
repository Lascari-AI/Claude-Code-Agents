# Agent Definitions & Coordination

Specialized agents for each phase, their skills, and how they coordinate via session state and hooks.

---

## The Core Idea

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENT COORDINATION MODEL                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORCHESTRATOR (Main Claude Session)                                         │
│  • Interprets user intent                                                   │
│  • Routes to phase commands                                                 │
│  • Spawns specialized agents for execution                                  │
│  • Tracks progress via session state                                        │
│                                                                             │
│  SPECIALIZED AGENTS (Subagents)                                             │
│  • Each phase can spawn specialized agents                                  │
│  • Agents have restricted skill/tool access                                 │
│  • Communicate via session state files                                      │
│  • Tracked via hooks for observability                                      │
│                                                                             │
│  SESSION STATE (Coordination Mechanism)                                      │
│  • agents/sessions/{session-id}/state.json                                  │
│  • Single source of truth for phase tracking                                │
│  • All agents read/write to same state                                      │
│  • Hooks fire on state transitions                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Hierarchy

```
                              ┌───────────────────────────────────┐
                              │        MAIN ORCHESTRATOR          │
                              │        (Claude Session)           │
                              │                                   │
                              │  Skills: All session commands     │
                              │  Role: Route, coordinate, track   │
                              └───────────────┬───────────────────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              │                               │                               │
              ▼                               ▼                               ▼
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│     DOCS AGENTS          │    │    SESSION AGENTS        │    │    UTILITY AGENTS        │
├──────────────────────────┤    ├──────────────────────────┤    ├──────────────────────────┤
│ • interview-foundation   │    │ • spec-agent             │    │ • explore-agent          │
│ • interview-codebase     │    │ • plan-agent             │    │ • research-agent         │
│ • write-agent            │    │ • build-agent            │    │ • commit-agent           │
│ • annotate-agent         │    │ • quick-plan-agent       │    │                          │
│ • scaffold-agent         │    │                          │    │                          │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

---

## Agent Definitions

### Session Agents

These are the core workflow agents that execute spec/plan/build phases.

#### spec-agent

```yaml
# .claude/agents/spec-agent.yaml
---
name: spec-agent
description: |
  Conducts question-driven interviews to capture user intent.
  Writes to spec.md with atomic persistence after each exchange.

model: inherit  # Uses session's model

skills:
  - session  # Access to session state management

allowed-tools:
  - Read        # Read session state, existing docs
  - Write       # Write spec.md, state.json
  - Edit        # Update spec incrementally
  - Glob        # Find relevant files for context
  - Grep        # Search codebase for context
  - Task        # Spawn research if needed

hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/session-state-sync.sh'

context: |
  You are conducting a spec interview for session ${CLAUDE_SESSION_ID}.

  CRITICAL: After EVERY exchange, atomically save:
  - spec.md with updated content
  - state.json with updated open_questions, key_decisions

  Ask ONE focused question at a time. Capture WHY, not just WHAT.
---
```

**Purpose**: Interactive interviewing to capture intent
**Spawned by**: `/session:spec` command
**Outputs**: `spec.md`, `state.json` updates

---

#### plan-agent

```yaml
# .claude/agents/plan-agent.yaml
---
name: plan-agent
description: |
  Designs implementation plans with tiered checkpoints.
  Analyzes spec and codebase to create tracer-bullet checkpoints.

model: inherit

skills:
  - session
  - docs-framework  # Understands documentation structure

allowed-tools:
  - Read        # Read spec, codebase, docs
  - Write       # Write plan.json, plan.md
  - Edit        # Update plan incrementally
  - Glob        # Find files to modify
  - Grep        # Search patterns
  - Task        # Spawn research-agent for investigation

hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/plan-checkpoint-validate.sh'

context: |
  You are designing an implementation plan for session ${CLAUDE_SESSION_ID}.

  Key principles:
  - Tracer bullet: First checkpoint is thin end-to-end slice
  - Each checkpoint is self-contained and verifiable
  - Tasks use IDK format when uncertain
  - Tier-by-tier confirmation with user
---
```

**Purpose**: Design implementation strategy with checkpoints
**Spawned by**: `/session:plan` command
**Outputs**: `plan.json`, `plan.md`

---

#### build-agent

```yaml
# .claude/agents/build-agent.yaml
---
name: build-agent
description: |
  Executes checkpoints from the plan. Implements code changes,
  runs verification, tracks progress in session state.

model: inherit

skills:
  - session
  - git        # Commit conventions

allowed-tools:
  - Read        # Read plan, source files
  - Write       # Write new files
  - Edit        # Modify existing files
  - Bash        # Run tests, build commands
  - Glob        # Find files
  - Grep        # Search code

hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/build-scope-check.sh'
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: '"$CLAUDE_PROJECT_DIR"/.claude/hooks/build-task-complete.sh'
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Check if the current checkpoint is complete.
            Verify all tasks are done and tests pass.
            If incomplete, provide reason to continue.

context: |
  You are executing checkpoint ${CHECKPOINT_ID} for session ${CLAUDE_SESSION_ID}.

  Read the checkpoint from plan.json.
  Execute tasks in order.
  Run verification after each task.
  Update state.json with progress.

  COMMIT BOUNDARY: One checkpoint = one commit (at end of checkpoint).
---
```

**Purpose**: Execute implementation, verify, commit
**Spawned by**: `/session:build` or `/session:build-background`
**Outputs**: Code changes, git commits, state updates

---

#### quick-plan-agent

```yaml
# .claude/agents/quick-plan-agent.yaml
---
name: quick-plan-agent
description: |
  Fast planning for chores and bug fixes. Auto-generates
  a simple ~1 checkpoint plan without tier-by-tier confirmation.

model: haiku  # Speed optimized

skills:
  - session

allowed-tools:
  - Read
  - Write
  - Glob
  - Grep

context: |
  Generate a quick plan for: $ARGUMENTS

  This is a simple task. Create ~1 checkpoint with clear tasks.
  Skip tier-by-tier confirmation. User QAs at end.

  If task is too complex, escalate to full plan.
---
```

**Purpose**: Fast planning for simple tasks
**Spawned by**: `/session:quick-plan`
**Model**: Haiku (speed)

---

### Docs Agents

#### interview-foundation-agent

```yaml
# .claude/agents/interview-foundation-agent.yaml
---
name: interview-foundation-agent
description: |
  Curious exploration of what the project is trying to BE.
  Not a checklist - explores understanding through dialogue.

model: inherit

skills:
  - docs-framework

allowed-tools:
  - Read
  - Write
  - Edit

context: |
  You are exploring the FOUNDATION of this project.

  NOT a checklist. Curious exploration.

  Explore:
  - What is this trying to BE?
  - What should it do extremely well?
  - How does the user think about this?
  - What would feel "right" vs "wrong"?

  Let structure emerge from conversation.
  Output: docs/.drafts/foundation.interview.md
---
```

---

#### write-agent

```yaml
# .claude/agents/write-agent.yaml
---
name: write-agent
description: |
  Generates documentation from interview transcripts or session changes.
  Follows docs-framework standards for L1-L5 documentation.

model: inherit

skills:
  - docs-framework  # Full docs standards

allowed-tools:
  - Read        # Read interviews, source code
  - Write       # Write documentation
  - Edit        # Update existing docs
  - Glob        # Find files
  - Grep        # Search for patterns

context: |
  Generate documentation following the docs-framework standards.

  For Foundation: Use whatever structure emerged from interview.
  For Codebase: Follow L1-L6 hierarchy.

  Always include:
  - YAML frontmatter (covers, concepts)
  - 00-overview.md for every directory
  - Inline code references
---
```

---

### Utility Agents

#### research-agent

```yaml
# .claude/agents/research-agent.yaml
---
name: research-agent
description: |
  Investigates codebase to answer questions. Can run in light mode
  (single agent) or full mode (parallel subagents).

model: haiku  # Fast for exploration

skills: []  # Pure research, no session management

allowed-tools:
  - Read
  - Glob
  - Grep
  - Task        # Spawn research-subagents in full mode
  - WebFetch    # External documentation
  - WebSearch   # Find relevant resources

context: |
  Research mode: ${RESEARCH_MODE:-light}
  Style: ${RESEARCH_STYLE:-understanding}

  Investigate: $ARGUMENTS

  Document findings incrementally.
  Write report.md in appropriate style.
---
```

---

#### explore-agent

```yaml
# .claude/agents/explore-agent.yaml
---
name: explore-agent
description: |
  Fast, read-only codebase exploration. Used for quick context
  gathering without modification capabilities.

model: haiku

allowed-tools:
  - Read
  - Glob
  - Grep

# No write tools - pure exploration
---
```

---

## Hook Configuration

### Session Tracking Hooks

```json
// .claude/settings.json
{
  "hooks": {
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/track-agent-start.sh"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/track-agent-stop.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-file-changed.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Scripts

```bash
#!/bin/bash
# .claude/hooks/track-agent-start.sh
# Called when a subagent spawns

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id')
AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type')

# Log to session tracking
echo "{\"event\":\"agent_start\",\"agent_id\":\"$AGENT_ID\",\"type\":\"$AGENT_TYPE\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
  >> "$CLAUDE_PROJECT_DIR/agents/sessions/$SESSION_ID/agent-log.jsonl"
```

```bash
#!/bin/bash
# .claude/hooks/track-agent-stop.sh
# Called when a subagent finishes

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
AGENT_ID=$(echo "$INPUT" | jq -r '.agent_id')

echo "{\"event\":\"agent_stop\",\"agent_id\":\"$AGENT_ID\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
  >> "$CLAUDE_PROJECT_DIR/agents/sessions/$SESSION_ID/agent-log.jsonl"
```

---

## State-Based Coordination

### Session State as Communication Channel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STATE-BASED COORDINATION                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Agents don't communicate directly. They communicate via state files.       │
│                                                                             │
│  ORCHESTRATOR                    SESSION STATE                              │
│       │                               │                                     │
│       │ ── spawns ──▶ SPEC-AGENT     │                                     │
│       │                   │           │                                     │
│       │                   │──writes──▶│ state.json (phase: "spec")          │
│       │                   │           │ spec.md                             │
│       │                               │                                     │
│       │ ◀── reads state ──────────────│                                     │
│       │    (spec complete?)           │                                     │
│       │                               │                                     │
│       │ ── spawns ──▶ PLAN-AGENT     │                                     │
│       │                   │           │                                     │
│       │                   │──reads───▶│ spec.md                             │
│       │                   │──writes──▶│ plan.json, state.json               │
│       │                               │                                     │
│       │ ◀── reads state ──────────────│                                     │
│       │    (plan complete?)           │                                     │
│       │                               │                                     │
│       │ ── spawns ──▶ BUILD-AGENT    │                                     │
│                           │           │                                     │
│                           │──reads───▶│ plan.json                           │
│                           │──writes──▶│ state.json (checkpoint progress)    │
│                                       │                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### State Schema for Coordination

```json
// agents/sessions/{session-id}/state.json
{
  "session_id": "2026-01-26_feature-x",
  "created_at": "2026-01-26T10:00:00Z",
  "updated_at": "2026-01-26T14:30:00Z",

  "current_phase": "build",  // spec | plan | build | docs | complete
  "phase_history": [
    {"phase": "spec", "started": "...", "completed": "..."},
    {"phase": "plan", "started": "...", "completed": "..."},
    {"phase": "build", "started": "...", "completed": null}
  ],

  "active_agents": [
    {"agent_id": "abc123", "type": "build-agent", "started": "..."}
  ],

  "checkpoints": {
    "total": 3,
    "completed": 1,
    "current": 2,
    "details": [
      {"id": 1, "status": "completed", "commit": "abc123"},
      {"id": 2, "status": "in_progress", "tasks_done": 2, "tasks_total": 5},
      {"id": 3, "status": "pending"}
    ]
  },

  "artifacts": {
    "spec": "spec.md",
    "plan": "plan.json",
    "research": ["research/001/report.md"]
  }
}
```

---

## Skill Assignments Summary

| Agent | Skills | Tools | Model |
|-------|--------|-------|-------|
| **spec-agent** | session | Read, Write, Edit, Glob, Grep, Task | inherit |
| **plan-agent** | session, docs-framework | Read, Write, Edit, Glob, Grep, Task | inherit |
| **build-agent** | session, git | Read, Write, Edit, Bash, Glob, Grep | inherit |
| **quick-plan-agent** | session | Read, Write, Glob, Grep | haiku |
| **interview-foundation-agent** | docs-framework | Read, Write, Edit | inherit |
| **write-agent** | docs-framework | Read, Write, Edit, Glob, Grep | inherit |
| **research-agent** | - | Read, Glob, Grep, Task, WebFetch, WebSearch | haiku |
| **explore-agent** | - | Read, Glob, Grep | haiku |

---

## Implementation Phases

### Phase 1: Core Session Agents
- [ ] spec-agent definition
- [ ] plan-agent definition
- [ ] build-agent definition
- [ ] Session state schema

### Phase 2: Hooks & Tracking
- [ ] SubagentStart/Stop hooks
- [ ] State sync hooks
- [ ] Agent logging

### Phase 3: Docs Agents
- [ ] interview-foundation-agent
- [ ] write-agent
- [ ] annotate-agent

### Phase 4: Research System
- [ ] research-agent
- [ ] research-subagent
- [ ] report-writer integration

---

## Open Questions

- [ ] How do we handle agent failures mid-checkpoint?
- [ ] Should agents have access to previous agent transcripts?
- [ ] How granular should hook tracking be?
- [ ] Background vs foreground execution patterns?
- [ ] UI layer integration (future)?

---

*Draft - expand with detailed agent configurations and hook implementations*
