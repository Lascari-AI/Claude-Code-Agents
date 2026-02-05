# End-to-End Flow

How a user request flows through the entire system, from intent to implementation to documentation.

---

## Core Model: Modes + Agents

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MODES VS AGENTS                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  MODES (Interactive, run in main session)                                   │
│  ─────────────────────────────────────────                                  │
│  • SPEC MODE: Interactive interview, captures intent                        │
│  • PLAN MODE: Progressive design, user approves structure                   │
│                                                                             │
│  Modes run in the main Claude session with the user.                        │
│  They can spawn agents for background work.                                 │
│                                                                             │
│  AGENTS (Background, autonomous execution)                                  │
│  ─────────────────────────────────────────                                  │
│  • research-agent: Investigate codebase (spawned by modes)                  │
│  • task-breakdown-agent: Generate IDK actions (spawned by plan mode)        │
│  • checkpoint-agent: Execute a full checkpoint                              │
│  • task-agent: Execute a single task (spawned by checkpoint-agent)          │
│  • docs-agent: Update documentation (spawned by checkpoint-agent)           │
│                                                                             │
│  Agents run in background, report back via state files.                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The Complete Picture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    COMPLETE SYSTEM FLOW                                         │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  USER: "Add dark mode support"                                                                  │
│          │                                                                                      │
│          │ /session:spec                                                                        │
│          │ creates session: agents/sessions/2026-01-26_dark-mode/                               │
│          ▼                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  SPEC MODE (Interactive - main session)                                                   ║  │
│  ║                                                                                           ║  │
│  ║  Main Claude session conducts interview with user.                                        ║  │
│  ║                                                                                           ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │  Interview Loop                                                                     │  ║  │
│  ║  │  • Ask question ─────────────────────────────────▶ User answers                     │  ║  │
│  ║  │  • Process answer                                                                   │  ║  │
│  ║  │  • Atomic save (spec.md + state.json)                                               │  ║  │
│  ║  │  • Repeat until complete                                                            │  ║  │
│  ║  └───────────────────────────────────────────────────────────────┬─────────────────────┘  ║  │
│  ║                                                                  │                        ║  │
│  ║  Can spawn research-agent if needed:                             │                        ║  │
│  ║  ┌─────────────────────┐                                         │                        ║  │
│  ║  │  research-agent     │◀── "How does auth currently work?"      │                        ║  │
│  ║  │  (background)       │                                         │                        ║  │
│  ║  │  ─────────────────  │                                         │                        ║  │
│  ║  │  Explores codebase  │──▶ Returns findings to spec mode        │                        ║  │
│  ║  └─────────────────────┘                                         │                        ║  │
│  ║                                                                  │                        ║  │
│  ║  Output: spec.md finalized                                       │                        ║  │
│  ╚══════════════════════════════════════════════════════════════════╪════════════════════════╝  │
│                                                                     │                           │
│          ┌──────────────────────────────────────────────────────────┘                           │
│          │ /session:plan                                                                        │
│          ▼                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  PLAN MODE (Interactive → Background)                                                     ║  │
│  ║                                                                                           ║  │
│  ║  Progressive detail with DECREASING user involvement:                                     ║  │
│  ║                                                                                           ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │  TIER 1: Checkpoints                                        ◀── USER APPROVAL       │  ║  │
│  ║  │  ─────────────────────────────────────────────────────────────────────────────────  │  ║  │
│  ║  │  Main session (plan mode) generates checkpoint outline from spec.                   │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  "Here are 3 checkpoints:"                                                          │  ║  │
│  ║  │  • CP1: Foundation (theme provider setup)                                           │  ║  │
│  ║  │  • CP2: Features (color tokens, toggle)                                             │  ║  │
│  ║  │  • CP3: Polish (persistence, system preference)                                     │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  User: "Looks good" ✓                                                               │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                           │                                               ║  │
│  ║                                           ▼                                               ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │  TIER 2: Task Groups                                        ◀── USER APPROVAL       │  ║  │
│  ║  │  ─────────────────────────────────────────────────────────────────────────────────  │  ║  │
│  ║  │  Main session breaks each checkpoint into task groups.                              │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  "CP1 has 3 task groups:"                                                           │  ║  │
│  ║  │  • Group 1: Create ThemeProvider component                                          │  ║  │
│  ║  │  • Group 2: Define color tokens (light/dark)                                        │  ║  │
│  ║  │  • Group 3: Create toggle component                                                 │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  User: "Looks good" ✓                                                               │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                           │                                               ║  │
│  ║                                           ▼                                               ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │  TIER 3: Individual Tasks + IDK Actions                 ◀── BACKGROUND (no approval)│  ║  │
│  ║  │  ─────────────────────────────────────────────────────────────────────────────────  │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  User has approved the structure. Task breakdown is straightforward.                │  ║  │
│  ║  │  Main session spawns task-breakdown-agent(s) to fill in details.                    │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐          │  ║  │
│  ║  │  │ task-breakdown-agent│  │ task-breakdown-agent│  │ task-breakdown-agent│          │  ║  │
│  ║  │  │ (CP1 groups)        │  │ (CP2 groups)        │  │ (CP3 groups)        │          │  ║  │
│  ║  │  │                     │  │                     │  │                     │          │  ║  │
│  ║  │  │ For each group:     │  │ For each group:     │  │ For each group:     │          │  ║  │
│  ║  │  │ • Generate tasks    │  │ • Generate tasks    │  │ • Generate tasks    │          │  ║  │
│  ║  │  │ • Add IDK actions   │  │ • Add IDK actions   │  │ • Add IDK actions   │          │  ║  │
│  ║  │  │ • File references   │  │ • File references   │  │ • File references   │          │  ║  │
│  ║  │  └──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘          │  ║  │
│  ║  │             │                        │                        │                     │  ║  │
│  ║  │             └────────────────────────┼────────────────────────┘                     │  ║  │
│  ║  │                                      ▼                                              │  ║  │
│  ║  │                              plan.json updated                                      │  ║  │
│  ║  │                              (checkpoints → groups → tasks → IDK actions)           │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                                                                           ║  │
│  ║  Output: Complete plan.json ready for build                                               ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════════════════╝  │
│                                                                                                 │
│          ┌───────────────────────────────────────────────────────────────────────────────────┘  │
│          │ /session:build                                                                       │
│          ▼                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  BUILD PHASE (Agent-driven)                                                               ║  │
│  ║                                                                                           ║  │
│  ║  Main session spawns checkpoint-agent for each checkpoint.                                ║  │
│  ║  Each checkpoint-agent manages its own execution autonomously.                            ║  │
│  ║                                                                                           ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │                           CHECKPOINT 1                                              │  ║  │
│  ║  │  ┌─────────────────────────────────────────────────────────────────────────────┐    │  ║  │
│  ║  │  │  checkpoint-agent (CP1)                                                     │    │  ║  │
│  ║  │  │                                                                             │    │  ║  │
│  ║  │  │  Reads: plan.json (CP1: groups → tasks → IDK actions)                       │    │  ║  │
│  ║  │  │                                                                             │    │  ║  │
│  ║  │  │  Spawns task-agent for each task group (parallel or sequential):            │    │  ║  │
│  ║  │  │                                                                             │    │  ║  │
│  ║  │  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │    │  ║  │
│  ║  │  │  │  task-agent    │  │  task-agent    │  │  task-agent    │                 │    │  ║  │
│  ║  │  │  │  (Group 1)     │  │  (Group 2)     │  │  (Group 3)     │                 │    │  ║  │
│  ║  │  │  │                │  │                │  │                │                 │    │  ║  │
│  ║  │  │  │  Executes:     │  │  Executes:     │  │  Executes:     │                 │    │  ║  │
│  ║  │  │  │  • IDK actions │  │  • IDK actions │  │  • IDK actions │                 │    │  ║  │
│  ║  │  │  │  • File writes │  │  • File writes │  │  • File writes │                 │    │  ║  │
│  ║  │  │  │                │  │                │  │                │                 │    │  ║  │
│  ║  │  │  │  Reports back: │  │  Reports back: │  │  Reports back: │                 │    │  ║  │
│  ║  │  │  │  • What done   │  │  • What done   │  │  • What done   │                 │    │  ║  │
│  ║  │  │  │  • Files changed│ │  • Files changed│ │  • Files changed│                │    │  ║  │
│  ║  │  │  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘                 │    │  ║  │
│  ║  │  │          │                   │                   │                          │    │  ║  │
│  ║  │  │          └───────────────────┼───────────────────┘                          │    │  ║  │
│  ║  │  │                              ▼                                              │    │  ║  │
│  ║  │  │  Checkpoint-agent aggregates:                                               │    │  ║  │
│  ║  │  │  ├─▶ Collects task-agent reports                                            │    │  ║  │
│  ║  │  │  ├─▶ Runs verification (tests)                                              │    │  ║  │
│  ║  │  │  ├─▶ Spawns docs-agent (if changes warrant docs)                            │    │  ║  │
│  ║  │  │  │   ┌─────────────────────┐                                                │    │  ║  │
│  ║  │  │  │   │  docs-agent         │                                                │    │  ║  │
│  ║  │  │  │   │  • Assess changes   │                                                │    │  ║  │
│  ║  │  │  │   │  • Update L2/L3 docs│                                                │    │  ║  │
│  ║  │  │  │   │  • Add L4/L5 headers│                                                │    │  ║  │
│  ║  │  │  │   └─────────────────────┘                                                │    │  ║  │
│  ║  │  │  ├─▶ Creates commit for checkpoint                                          │    │  ║  │
│  ║  │  │  └─▶ Reports back to main session                                           │    │  ║  │
│  ║  │  └─────────────────────────────────────────────────────────────────────────────┘    │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                           │                                               ║  │
│  ║                                           ▼                                               ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │                           CHECKPOINT 2                                              │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  checkpoint-agent (CP2)                                                             │  ║  │
│  ║  │  └─▶ task-agents (groups) ─▶ aggregate ─▶ verify ─▶ docs-agent ─▶ commit            │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                           │                                               ║  │
│  ║                                           ▼                                               ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────────────────────┐  ║  │
│  ║  │                           CHECKPOINT 3                                              │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  │  checkpoint-agent (CP3)                                                             │  ║  │
│  ║  │  └─▶ task-agents (groups) ─▶ aggregate ─▶ verify ─▶ docs-agent ─▶ commit            │  ║  │
│  ║  │                                                                                     │  ║  │
│  ║  └─────────────────────────────────────────────────────────────────────────────────────┘  ║  │
│  ║                                                                                           ║  │
│  ║  Output: Code changes + doc updates + commits (one per checkpoint)                        ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════════════════╝  │
│                                                                                                 │
│          ┌───────────────────────────────────────────────────────────────────────────────────┘  │
│          ▼                                                                                      │
│  ┌───────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  SESSION COMPLETE                                                                         │  │
│  │                                                                                           │  │
│  │  Artifacts:                                                                               │  │
│  │  • agents/sessions/2026-01-26_dark-mode/spec.md                                           │  │
│  │  • agents/sessions/2026-01-26_dark-mode/plan.json                                         │  │
│  │  • agents/sessions/2026-01-26_dark-mode/state.json (complete)                             │  │
│  │  • 3 git commits (one per checkpoint, includes doc updates)                               │  │
│  │  • Updated docs/10-codebase/...                                                           │  │
│  └───────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Spawning Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT SPAWNING HIERARCHY                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  MAIN SESSION (modes)                                                       │
│  │                                                                          │
│  ├─── SPEC MODE                                                             │
│  │    └─── research-agent (on-demand, when understanding needed)            │
│  │                                                                          │
│  ├─── PLAN MODE                                                             │
│  │    └─── task-breakdown-agent (background, after tier 2 approval)         │
│  │         └─── one per checkpoint, runs in parallel                        │
│  │                                                                          │
│  └─── BUILD                                                                 │
│       └─── checkpoint-agent (one per checkpoint, sequential)                │
│            │                                                                │
│            ├─── task-agent (one per task group, can be parallel)            │
│            │                                                                │
│            └─── docs-agent (after task-agents complete, if needed)          │
│                                                                             │
│  Each agent reports back via state files.                                   │
│  Parent waits for children, aggregates results.                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Plan Mode Detail: Tier Progression

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PLAN MODE TIERS                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TIER 1: CHECKPOINTS                                                        │
│  ───────────────────────────────────────────────────────────────────────    │
│  Who: Main session (plan mode)                                              │
│  What: High-level checkpoint outline                                        │
│  Approval: USER REQUIRED                                                    │
│                                                                             │
│  plan.json after Tier 1:                                                    │
│  {                                                                          │
│    "checkpoints": [                                                         │
│      { "id": 1, "title": "Foundation", "goal": "..." },                     │
│      { "id": 2, "title": "Features", "goal": "..." },                       │
│      { "id": 3, "title": "Polish", "goal": "..." }                          │
│    ]                                                                        │
│  }                                                                          │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  TIER 2: TASK GROUPS                                                        │
│  ───────────────────────────────────────────────────────────────────────    │
│  Who: Main session (plan mode)                                              │
│  What: Groups within each checkpoint                                        │
│  Approval: USER REQUIRED                                                    │
│                                                                             │
│  plan.json after Tier 2:                                                    │
│  {                                                                          │
│    "checkpoints": [                                                         │
│      {                                                                      │
│        "id": 1, "title": "Foundation",                                      │
│        "groups": [                                                          │
│          { "id": "1.1", "title": "ThemeProvider component" },               │
│          { "id": "1.2", "title": "Color tokens" },                          │
│          { "id": "1.3", "title": "Toggle component" }                       │
│        ]                                                                    │
│      },                                                                     │
│      ...                                                                    │
│    ]                                                                        │
│  }                                                                          │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  TIER 3: TASKS + IDK ACTIONS                                                │
│  ───────────────────────────────────────────────────────────────────────    │
│  Who: task-breakdown-agent (background, spawned by main session)            │
│  What: Individual tasks with IDK actions                                    │
│  Approval: NONE (runs in background)                                        │
│                                                                             │
│  Why no approval: User already approved the structure (checkpoints +        │
│  groups). Task breakdown is mechanical - filling in implementation          │
│  details that are straightforward given the group definitions.              │
│                                                                             │
│  plan.json after Tier 3:                                                    │
│  {                                                                          │
│    "checkpoints": [                                                         │
│      {                                                                      │
│        "id": 1, "title": "Foundation",                                      │
│        "groups": [                                                          │
│          {                                                                  │
│            "id": "1.1", "title": "ThemeProvider component",                 │
│            "tasks": [                                                       │
│              {                                                              │
│                "id": "1.1.1",                                               │
│                "description": "Create ThemeContext",                        │
│                "actions": [                                                 │
│                  { "type": "create", "file": "src/theme/context.ts" },      │
│                  { "type": "idk", "decision": "Context vs Zustand?" }       │
│                ]                                                            │
│              },                                                             │
│              ...                                                            │
│            ]                                                                │
│          },                                                                 │
│          ...                                                                │
│        ]                                                                    │
│      },                                                                     │
│      ...                                                                    │
│    ]                                                                        │
│  }                                                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Build Phase Detail: Checkpoint Execution

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         CHECKPOINT EXECUTION                               │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Main session spawns checkpoint-agent for CP1                              │
│                                                                            │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  checkpoint-agent (CP1)                                               │ │
│  │                                                                       │ │
│  │  1. READ plan.json for CP1 details                                    │ │
│  │     └─ groups, tasks, IDK actions                                     │ │
│  │                                                                       │ │
│  │  2. SPAWN task-agents for each group                                  │ │
│  │     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                   │ │
│  │     │ task-agent  │ │ task-agent  │ │ task-agent  │                   │ │
│  │     │ (1.1)       │ │ (1.2)       │ │ (1.3)       │                   │ │
│  │     │             │ │             │ │             │                   │ │
│  │     │ Executes:   │ │ Executes:   │ │ Executes:   │                   │ │
│  │     │ - Tasks     │ │ - Tasks     │ │ - Tasks     │                   │ │
│  │     │ - Actions   │ │ - Actions   │ │ - Actions   │                   │ │
│  │     │ - Resolves  │ │ - Resolves  │ │ - Resolves  │                   │ │
│  │     │   IDKs      │ │   IDKs      │ │   IDKs      │                   │ │
│  │     │             │ │             │ │             │                   │ │
│  │     │ Writes:     │ │ Writes:     │ │ Writes:     │                   │ │
│  │     │ state file  │ │ state file  │ │ state file  │                   │ │
│  │     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘                   │ │
│  │            │               │               │                          │ │
│  │            └───────────────┼───────────────┘                          │ │
│  │                            ▼                                          │ │
│  │  3. WAIT for all task-agents to complete                              │ │
│  │                                                                       │ │
│  │  4. AGGREGATE results                                                 │ │
│  │     └─ Collect: files changed, decisions made, issues encountered     │ │
│  │                                                                       │ │
│  │  5. VERIFY checkpoint                                                 │ │
│  │     └─ Run tests                                                      │ │
│  │     └─ Check for errors                                               │ │
│  │                                                                       │ │
│  │  6. DOCS (if changes warrant)                                         │ │
│  │     └─ Spawn docs-agent                                               │ │
│  │        ┌─────────────────────┐                                        │ │
│  │        │  docs-agent         │                                        │ │
│  │        │  - Assess changes   │                                        │ │
│  │        │  - Update L2/L3     │                                        │ │
│  │        │  - Add L4/L5        │                                        │ │
│  │        └─────────────────────┘                                        │ │
│  │                                                                       │ │
│  │  7. COMMIT                                                            │ │
│  │     └─ One commit for entire checkpoint                               │ │
│  │     └─ Includes code + docs                                           │ │
│  │                                                                       │ │
│  │  8. REPORT back to main session                                       │ │
│  │     └─ Update state.json with checkpoint completion                   │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                            │
│  Main session receives report, spawns checkpoint-agent for CP2...          │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Hook Events Throughout Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HOOK EVENT TIMELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SESSION START                                                              │
│  │                                                                          │
│  ├─▶ SessionStart hook                                                      │
│  │   └─ Initialize session, load project context                           │
│  │                                                                          │
│  ├─▶ SPEC MODE (main session, no SubagentStart)                            │
│  │   │                                                                      │
│  │   ├─▶ research-agent spawned (if needed)                                │
│  │   │   ├─▶ SubagentStart hook                                            │
│  │   │   └─▶ SubagentStop hook                                             │
│  │   │                                                                      │
│  │   └─▶ PostToolUse hooks (Write spec.md)                                 │
│  │                                                                          │
│  ├─▶ PLAN MODE (main session, no SubagentStart)                            │
│  │   │                                                                      │
│  │   ├─▶ Tier 1 & 2: No agents, just main session                          │
│  │   │                                                                      │
│  │   └─▶ Tier 3: task-breakdown-agents spawned                             │
│  │       ├─▶ SubagentStart hook (per breakdown agent)                      │
│  │       └─▶ SubagentStop hook (per breakdown agent)                       │
│  │                                                                          │
│  ├─▶ BUILD PHASE                                                            │
│  │   │                                                                      │
│  │   └─▶ FOR EACH CHECKPOINT:                                              │
│  │       │                                                                  │
│  │       └─▶ SubagentStart hook (checkpoint-agent)                         │
│  │           │                                                              │
│  │           ├─▶ SubagentStart hook (task-agent, per group)                │
│  │           │   ├─▶ PostToolUse hooks (Write/Edit code)                   │
│  │           │   └─▶ SubagentStop hook                                     │
│  │           │                                                              │
│  │           ├─▶ SubagentStart hook (docs-agent, if needed)                │
│  │           │   ├─▶ PostToolUse hooks (Write docs)                        │
│  │           │   └─▶ SubagentStop hook                                     │
│  │           │                                                              │
│  │           └─▶ SubagentStop hook (checkpoint-agent)                      │
│  │               └─ Commit created, checkpoint complete                    │
│  │                                                                          │
│  └─▶ SessionEnd hook                                                        │
│      └─ Archive session, update index                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## State Transitions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STATE MACHINE                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────┐                                     │
│                         │   CREATED   │                                     │
│                         └──────┬──────┘                                     │
│                                │ /session:spec                              │
│                                ▼                                            │
│                         ┌─────────────┐                                     │
│                    ┌───▶│    SPEC     │◀───┐                                │
│                    │    │   (mode)    │    │                                │
│                    │    └──────┬──────┘    │                                │
│                    │           │           │                                │
│                    │ interrupt │ finalize  │ resume                         │
│                    │           ▼           │                                │
│                    │    ┌─────────────┐    │                                │
│                    └────│SPEC_PAUSED  │────┘                                │
│                         └──────┬──────┘                                     │
│                                │ /session:plan                              │
│                                ▼                                            │
│                         ┌─────────────┐                                     │
│                    ┌───▶│  PLAN_T1    │◀───┐                                │
│                    │    │ (checkpoints)│    │                               │
│                    │    └──────┬──────┘    │                                │
│                    │           │ approve   │                                │
│                    │           ▼           │ resume                         │
│                    │    ┌─────────────┐    │                                │
│                    └────│  PLAN_T2    │────┘                                │
│                         │ (groups)    │                                     │
│                         └──────┬──────┘                                     │
│                                │ approve                                    │
│                                ▼                                            │
│                         ┌─────────────┐                                     │
│                         │  PLAN_T3    │  ← Background agents               │
│                         │ (breakdown) │                                     │
│                         └──────┬──────┘                                     │
│                                │ all agents complete                        │
│                                ▼                                            │
│                         ┌─────────────┐                                     │
│                         │    BUILD    │                                     │
│                         └──────┬──────┘                                     │
│                                │                                            │
│                    ┌───────────┼───────────┐                                │
│                    ▼           │           ▼                                │
│             ┌───────────┐      │    ┌───────────┐                           │
│             │   ERROR   │      │    │ CP_DONE   │                           │
│             │(fix mode) │──────┘    └─────┬─────┘                           │
│             └───────────┘                 │ all CPs                         │
│                                           ▼                                 │
│                                    ┌─────────────┐                          │
│                                    │  COMPLETE   │                          │
│                                    └─────────────┘                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Plan Flow (Simplified)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      QUICK PLAN FLOW                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  USER: "Fix typo in README"                                                 │
│          │                                                                  │
│          ▼                                                                  │
│  ┌─────────────────────┐                                                    │
│  │  /session:quick-plan│                                                    │
│  │                     │                                                    │
│  │  Main session       │                                                    │
│  │  (haiku model)      │────▶ Auto-generates ~1 checkpoint plan            │
│  │                     │      (all tiers at once, no approval needed)      │
│  └──────────┬──────────┘                                                    │
│             │                                                               │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │  /session:build     │                                                    │
│  │                     │                                                    │
│  │  checkpoint-agent   │────▶ Executes single checkpoint                   │
│  └──────────┬──────────┘                                                    │
│             │                                                               │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │  User QA            │                                                    │
│  │  "Looks good?"      │                                                    │
│  └──────────┬──────────┘                                                    │
│             │                                                               │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │  Commit             │                                                    │
│  │  (docs update:      │                                                    │
│  │   likely skipped)   │                                                    │
│  └─────────────────────┘                                                    │
│                                                                             │
│  Total: ~2-3 minutes for simple fixes                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Agent Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENT SUMMARY                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AGENT                    SPAWNED BY           PURPOSE                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│  research-agent           spec/plan mode       Investigate codebase        │
│  task-breakdown-agent     plan mode (tier 3)   Generate tasks + IDK actions│
│  checkpoint-agent         build phase          Execute full checkpoint      │
│  task-agent               checkpoint-agent     Execute task group          │
│  docs-agent               checkpoint-agent     Update documentation        │
│                                                                             │
│  Key insight: Modes are interactive (main session).                         │
│               Agents are background (subagents).                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Files Touched Per Phase

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FILE ACCESS BY PHASE                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SPEC MODE                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  READS:                           WRITES:                            │   │
│  │  • docs/00-foundation/**          • agents/sessions/{id}/spec.md    │   │
│  │  • docs/10-codebase/**            • agents/sessions/{id}/state.json │   │
│  │  • src/** (via research-agent)    • research/*/report.md (if needed)│   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  PLAN MODE                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  READS:                           WRITES:                            │   │
│  │  • agents/sessions/{id}/spec.md   • agents/sessions/{id}/plan.json  │   │
│  │  • docs/10-codebase/**            • agents/sessions/{id}/state.json │   │
│  │  • src/** (exploration)                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  BUILD PHASE (checkpoint-agent + task-agents + docs-agent)                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  READS:                           WRITES:                            │   │
│  │  • agents/sessions/{id}/plan.json • src/** (implementation)         │   │
│  │  • src/** (context)               • tests/** (new tests)            │   │
│  │                                   • docs/10-codebase/** (L2/L3)     │   │
│  │                                   • src/** (L4/L5 headers)          │   │
│  │                                   • agents/sessions/{id}/state.json │   │
│  │                                   • git commits                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Error Recovery Patterns

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ERROR RECOVERY                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SPEC/PLAN INTERRUPTION                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Session closed mid-mode                                             │   │
│  │                                                                       │   │
│  │  Recovery: Re-invoke same command with session-id                    │   │
│  │  • Reads state.json for current tier/phase                           │   │
│  │  • Resumes from last atomic save                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TASK-AGENT FAILURE                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Task-agent encounters error during execution                        │   │
│  │                                                                       │   │
│  │  Recovery: checkpoint-agent handles                                  │   │
│  │  • Receives error report from task-agent                             │   │
│  │  • Can retry, skip, or escalate to user                              │   │
│  │  • Updates state with error details                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  CHECKPOINT-AGENT FAILURE                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Checkpoint verification fails (tests don't pass)                    │   │
│  │                                                                       │   │
│  │  Recovery: /session:build-interactive {session-id}                   │   │
│  │  • Main session enters fix-mode                                      │   │
│  │  • Collaborates with user to resolve                                 │   │
│  │  • Respawns checkpoint-agent after fix                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Draft - expand with parallel execution patterns and state file schemas*
