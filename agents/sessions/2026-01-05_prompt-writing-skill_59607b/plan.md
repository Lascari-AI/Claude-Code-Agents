# Implementation Plan

> **Session**: `2026-01-05_prompt-writing-skill_59607b`
> **Status**: Complete
> **Spec**: [./spec.md](./spec.md)
> **Created**: 2026-01-05
> **Updated**: 2026-01-05

---

## Overview

- **Checkpoints**: 5 (0 complete)
- **Total Tasks**: 8

## ⬜ Checkpoint 1: Foundation: Overview + Base Template

**Goal**: Create the entry point (00-overview.md) and canonical base template (10-base-template.md) as the foundational layer. This is the minimal end-to-end structure—a user can read overview, understand routing, and access the base template.

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `system_prompt/00-overview.md` | 📄 exists | Entry point with routing + embedded template |
| Before | `system_prompt/10-single-completion.md` | 📄 exists | Single-completion pattern |
| Before | `system_prompt/20-multiturn/00-base.md` | 📄 exists | Multi-turn base |
| Before | `system_prompt/20-multiturn/10-iterative-loop.md` | 📄 exists | Iterative loop |
| After | `system_prompt/00-overview.md` | 📝 modified | Entry point + routing only (template extracted) |
| After | `system_prompt/10-base-template.md` | ✨ new | Canonical XML structure |

**Projected Structure**:
```
system_prompt/
├── 00-overview.md (refactored)
├── 10-base-template.md (new)
├── 10-single-completion.md
└── 20-multiturn/
    ├── 00-base.md
    └── 10-iterative-loop.md
```

### Testing Strategy

**Approach**: Manual navigation test

**Verification Steps**:
- [ ] `Read 00-overview.md and verify it routes to base-template and workflow-design`
- [ ] `Read 10-base-template.md and verify it contains the canonical XML template`

### ⬜ Task Group 1.1: Create Base Template File

**Objective**: Extract the canonical XML structure from 00-overview.md into a dedicated 10-base-template.md file that serves as the copy-and-adapt reference.

#### ⬜ Task 1.1.1: Create base-template.md file

**File**: `system_prompt/10-base-template.md`

**Description**: Create the canonical base template file with YAML frontmatter, title, intro, canonical structure tree, reference XML template, and quick reference section.

**Context to Load**:
- `system_prompt/00-overview.md` (lines 79-293) - Source for canonical structure and reference template

**Actions**:
- ⬜ **1.1.1.1**: CREATE FILE system_prompt/10-base-template.md: ADD YAML frontmatter (covers: 'Canonical XML structure for all instruction artifacts', type: 'template', concepts: [base-template, xml-structure, purpose, knowledge, goal, workflow], depends-on: [system_prompt/00-overview.md]). ADD Title '# Base Template'. ADD intro paragraph: standalone canonical structure reference. ADD Section '## Canonical Structure': MIRROR tree diagram from 00-overview.md. ADD Section '## Reference Template': EXTRACT XML code block from 00-overview.md (preserve inline documentation). ADD Section '## Quick Reference': ADD table summarizing key sections. (`system_prompt/10-base-template.md`)

### ⬜ Task Group 1.2: Refactor Overview File

**Objective**: Transform 00-overview.md into a focused entry point that routes to base-template and workflow-design sections. Remove the embedded canonical template (now in 10-base-template.md).

#### ⬜ Task 1.2.1: Refactor overview to entry point

**File**: `system_prompt/00-overview.md`

**Description**: Transform overview into focused entry point: keep What This Covers, Key Distinction, Choosing Your Pattern; remove Canonical Structure and Reference Template (now in 10-base-template.md); update Instruction Types routing table; add reference to base-template.

**Context to Load**:
- `system_prompt/00-overview.md` - Full file - identify sections to keep vs remove

**Depends On**: Tasks 1.1.1

**Actions**:
- ⬜ **1.2.1.1**: UPDATE system_prompt/00-overview.md: REMOVE Section '## Canonical Structure' (the tree diagram). REMOVE Section '## Reference Template' (the entire XML code block). ADD reference link after 'Key Distinction' section: 'For the canonical XML structure, see [Base Template](10-base-template.md)'. UPDATE Section '## Instruction Types' table: keep routing to single-completion and multiturn, add row for base-template reference. (`system_prompt/00-overview.md`)

---

## ⬜ Checkpoint 2: Workflow Design Core: Overview + Base Principles

**Goal**: Create the 20-workflow-design/ folder with its overview and base principles file. Establishes workflow design as the central discipline with core theory that applies to all patterns.

**Prerequisites**: Checkpoints 1

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `system_prompt/00-overview.md` | 📄 exists | Refactored entry point |
| Before | `system_prompt/10-base-template.md` | 📄 exists | Canonical XML structure |
| After | `system_prompt/20-workflow-design/00-overview.md` | ✨ new | Introduces workflow design discipline |
| After | `system_prompt/20-workflow-design/10-base.md` | ✨ new | Core principles for all workflows |

**Projected Structure**:
```
system_prompt/
├── 00-overview.md
├── 10-base-template.md
└── 20-workflow-design/
    ├── 00-overview.md (new)
    └── 10-base.md (new)
```

### Testing Strategy

**Approach**: Manual navigation test

**Verification Steps**:
- [ ] `Navigate from 00-overview.md to 20-workflow-design/00-overview.md`
- [ ] `Verify 00-overview.md explains patterns and routes correctly`
- [ ] `Verify 10-base.md contains core principles applicable to all patterns`

### ⬜ Task Group 2.1: Create Workflow Design Overview

**Objective**: Create 20-workflow-design/00-overview.md introducing workflow design as the central discipline. Explain the single-completion vs multi-turn split and how to navigate the pattern files.

#### ⬜ Task 2.1.1: Create workflow-design overview file

**File**: `system_prompt/20-workflow-design/00-overview.md`

**Description**: Create overview file with core insight ('workflow IS the product'), fundamental split table (single-completion vs multi-turn), pattern navigation guide, and choosing your pattern section.

**Context to Load**:
- `spec.md` (lines 30-50) - Core insight and key distinction
- `system_prompt/00-overview.md` (lines 40-75) - Existing key distinction content

**Actions**:
- ⬜ **2.1.1.1**: CREATE FILE system_prompt/20-workflow-design/00-overview.md: ADD YAML frontmatter (covers: 'Workflow design as the central discipline', type: 'overview', concepts: [workflow-design, steps, phases, single-completion, multi-turn]). ADD Title '# Workflow Design'. ADD Section '## Core Insight': 'The workflow IS the product'. ADD Section '## The Fundamental Split': table comparing single-completion vs multi-turn (structure, execution, state, output). ADD Section '## Pattern Navigation': guide to 20-single-completion.md and 30-multi-turn/. ADD Section '## Choosing Your Pattern': decision guidance. (`system_prompt/20-workflow-design/00-overview.md`)

### ⬜ Task Group 2.2: Create Base Principles File

**Objective**: Create 20-workflow-design/10-base.md as the dense reference for core workflow principles that apply to ALL patterns (XML structure, steps vs phases, constraint localization, critical tags, etc.).

#### ⬜ Task 2.2.1: Create base principles file

**File**: `system_prompt/20-workflow-design/10-base.md`

**Description**: Create dense reference file with: steps vs phases distinction, constraint localization, output format vs protocol, critical tags usage, error handling patterns, principles sections, general rules.

**Context to Load**:
- `spec.md` (lines 106-132) - Steps vs Phases, workflow design principles
- `system_prompt/10-single-completion.md` - Existing patterns for steps and constraints
- `system_prompt/20-multiturn/00-base.md` - Existing patterns for phases, state, critical tags

**Depends On**: Tasks 2.1.1

**Actions**:
- ⬜ **2.2.1.1**: CREATE FILE system_prompt/20-workflow-design/10-base.md: ADD YAML frontmatter (covers: 'Core workflow design principles', type: 'reference'). ADD Title '# Workflow Design: Base Principles'. ADD Section '## Steps vs Phases': internal vs external execution. ADD Section '## Constraint Localization': global vs step-specific. ADD Section '## Output Format vs Protocol': structure vs delivery. ADD Section '## Using <critical> Tags': must-not-violate constraints. ADD Section '## Error Handling Patterns': scenario-based. ADD Section '## Principles Sections': named principles. ADD Section '## General Rules': numbered emphasis rules. (`system_prompt/20-workflow-design/10-base.md`)

---

## ⬜ Checkpoint 3: Single-Completion Pattern

**Goal**: Create 20-workflow-design/20-single-completion.md covering thinking-window execution pattern with <steps> structure. Validates the pattern documentation approach.

**Prerequisites**: Checkpoints 2

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `system_prompt/20-workflow-design/00-overview.md` | 📄 exists | Workflow design overview |
| Before | `system_prompt/20-workflow-design/10-base.md` | 📄 exists | Base principles |
| Before | `system_prompt/10-single-completion.md` | 📄 exists | Existing full template |
| After | `system_prompt/20-workflow-design/20-single-completion.md` | ✨ new | Single-completion workflow pattern |

**Projected Structure**:
```
system_prompt/20-workflow-design/
├── 00-overview.md
├── 10-base.md
└── 20-single-completion.md (new)
```

### Testing Strategy

**Approach**: Manual navigation and content verification

**Verification Steps**:
- [ ] `Navigate from 20-workflow-design/00-overview.md to 20-single-completion.md`
- [ ] `Verify file covers <steps> structure, internal reasoning, no external state`
- [ ] `Verify examples are appropriate for thinking-window execution`

### ⬜ Task Group 3.1: Create Single-Completion Pattern File

**Objective**: Create 20-workflow-design/20-single-completion.md documenting the thinking-window execution pattern using <steps> structure. Focuses on workflow design for internal reasoning without external state.

#### ⬜ Task 3.1.1: Create single-completion workflow pattern file

**File**: `system_prompt/20-workflow-design/20-single-completion.md`

**Description**: Create single-completion pattern doc: when to use, <steps> structure, internal reasoning scaffold, no external state, step anatomy (name, description, constraints), examples (classification, extraction, generation).

**Context to Load**:
- `system_prompt/10-single-completion.md` - Existing template content to draw from
- `spec.md` (lines 106-120) - Steps definition and characteristics

**Actions**:
- ⬜ **3.1.1.1**: CREATE FILE system_prompt/20-workflow-design/20-single-completion.md: ADD YAML frontmatter (covers: 'Thinking-window workflow pattern', type: 'pattern'). ADD Title '# Single-Completion Workflows'. ADD Section '## When to Use': your code controls execution. ADD Section '## The <steps> Structure': internal reasoning scaffold. ADD Section '## Step Anatomy': name, description, constraints. ADD Section '## No External State': single response output. ADD Section '## Examples': classification, extraction, generation. ADD Section '## Template Reference': link to 10-base-template.md. (`system_prompt/20-workflow-design/20-single-completion.md`)

---

## ⬜ Checkpoint 4: Multi-Turn Base Pattern

**Goal**: Create 30-multi-turn/00-base.md covering external state execution with <phases> structure, state schemas, and output protocols. Core multi-turn pattern.

**Prerequisites**: Checkpoints 2

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `system_prompt/20-workflow-design/00-overview.md` | 📄 exists | Workflow design overview |
| Before | `system_prompt/20-workflow-design/20-single-completion.md` | 📄 exists | Single-completion pattern |
| Before | `system_prompt/20-multiturn/00-base.md` | 📄 exists | Existing multi-turn base |
| After | `system_prompt/20-workflow-design/30-multi-turn/00-base.md` | ✨ new | Multi-turn base workflow pattern |

**Projected Structure**:
```
system_prompt/20-workflow-design/
├── 00-overview.md
├── 10-base.md
├── 20-single-completion.md
└── 30-multi-turn/
    └── 00-base.md (new)
```

### Testing Strategy

**Approach**: Manual navigation and content verification

**Verification Steps**:
- [ ] `Navigate from 20-workflow-design/00-overview.md to 30-multi-turn/00-base.md`
- [ ] `Verify file covers <phases> structure, state schemas, output protocols`
- [ ] `Verify examples reference research agents or similar autonomous systems`

### ⬜ Task Group 4.1: Create Multi-Turn Base Pattern File

**Objective**: Create 20-workflow-design/30-multi-turn/00-base.md documenting the external state execution pattern using <phases> structure. Covers state schema design, output protocols, and autonomous execution.

#### ⬜ Task 4.1.1: Create multi-turn base workflow pattern file

**File**: `system_prompt/20-workflow-design/30-multi-turn/00-base.md`

**Description**: Create multi-turn base pattern doc: when to use (autonomous execution), <phases> structure, state schema design, output protocol, phase anatomy (id, name, actions, critical), examples (research agents, report writers).

**Context to Load**:
- `system_prompt/20-multiturn/00-base.md` - Existing template content
- `.claude/agents/research/report-writer.md` - Real multi-turn agent example
- `spec.md` (lines 106-132) - Phases definition

**Actions**:
- ⬜ **4.1.1.1**: CREATE FILE system_prompt/20-workflow-design/30-multi-turn/00-base.md: ADD YAML frontmatter (covers: 'External state workflow pattern', type: 'pattern'). ADD Title '# Multi-Turn Workflows'. ADD Section '## When to Use': autonomous system execution. ADD Section '## The <phases> Structure': external execution flow. ADD Section '## State Schema Design': explicit JSON state. ADD Section '## Output Protocol': where to write, incremental updates. ADD Section '## Phase Anatomy': id, name, actions, critical tags. ADD Section '## Examples': research-subagent, report-writer. ADD Section '## Template Reference': link to 20-multiturn/00-base.md. (`system_prompt/20-workflow-design/30-multi-turn/00-base.md`)

---

## ⬜ Checkpoint 5: Multi-Turn Techniques: Iterative Loop + Parallel Agents

**Goal**: Complete the multi-turn section with technique files: 10-iterative-loop.md (user-in-the-loop) and 20-parallel-agents.md (subagent spawning). Full documentation set complete.

**Prerequisites**: Checkpoints 4

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `system_prompt/20-workflow-design/30-multi-turn/00-base.md` | 📄 exists | Multi-turn base pattern |
| Before | `system_prompt/20-multiturn/10-iterative-loop.md` | 📄 exists | Existing iterative loop template |
| After | `system_prompt/20-workflow-design/30-multi-turn/10-iterative-loop.md` | ✨ new | Iterative loop technique |
| After | `system_prompt/20-workflow-design/30-multi-turn/20-parallel-agents.md` | ✨ new | Parallel agents technique |

**Projected Structure**:
```
system_prompt/20-workflow-design/30-multi-turn/
├── 00-base.md
├── 10-iterative-loop.md (new)
└── 20-parallel-agents.md (new)
```

### Testing Strategy

**Approach**: Manual navigation and content verification

**Verification Steps**:
- [ ] `Navigate from 30-multi-turn/00-base.md to both technique files`
- [ ] `Verify iterative-loop covers state machine, per-turn output, memory handling`
- [ ] `Verify parallel-agents covers orchestrator pattern, subagent state, coordination`

### ⬜ Task Group 5.1: Create Iterative Loop Technique File

**Objective**: Create 20-workflow-design/30-multi-turn/10-iterative-loop.md documenting the user-in-the-loop technique. State machine stages, per-turn output, memory handling, max rounds failsafe.

#### ⬜ Task 5.1.1: Create iterative loop technique file

**File**: `system_prompt/20-workflow-design/30-multi-turn/10-iterative-loop.md`

**Description**: Create iterative loop technique doc: when to use (user input each cycle), state machine stages (PREP→Q→REFLECT→END), per-turn and final output formats, memory handling rules, max rounds failsafe, examples (spec interviews, requirements).

**Context to Load**:
- `system_prompt/20-multiturn/10-iterative-loop.md` - Existing template content
- `spec.md` (lines 186-198) - Iterative loop characteristics

**Actions**:
- ⬜ **5.1.1.1**: CREATE FILE system_prompt/20-workflow-design/30-multi-turn/10-iterative-loop.md: ADD YAML frontmatter (covers: 'User-in-the-loop technique', type: 'technique'). ADD Title '# Iterative Loop Technique'. ADD Section '## When to Use': user provides input each cycle. ADD Section '## State Machine Stages': PREP→Q→REFLECT→END. ADD Section '## Output Formats': per-turn format + final report format. ADD Section '## Memory Handling': retain confirmed facts, discard speculation. ADD Section '## Max Rounds Failsafe': prevent infinite loops. ADD Section '## Examples': spec interviews, requirements gathering. (`system_prompt/20-workflow-design/30-multi-turn/10-iterative-loop.md`)

### ⬜ Task Group 5.2: Create Parallel Agents Technique File

**Objective**: Create 20-workflow-design/30-multi-turn/20-parallel-agents.md documenting the subagent spawning technique. Orchestrator pattern, subagent state files, coordination, synthesis.

#### ⬜ Task 5.2.1: Create parallel agents technique file

**File**: `system_prompt/20-workflow-design/30-multi-turn/20-parallel-agents.md`

**Description**: Create parallel agents technique doc: when to use (spawn subagents), orchestrator pattern, subagent state files, coordination (spawn, wait, collect), synthesis/report writing, examples (research system).

**Context to Load**:
- `.claude/agents/research/report-writer.md` - Real orchestrator example
- `.claude/agents/research/research-subagent.md` - Real subagent example
- `spec.md` (lines 199-204) - Parallel agents characteristics

**Actions**:
- ⬜ **5.2.1.1**: CREATE FILE system_prompt/20-workflow-design/30-multi-turn/20-parallel-agents.md: ADD YAML frontmatter (covers: 'Subagent spawning technique', type: 'technique'). ADD Title '# Parallel Agents Technique'. ADD Section '## When to Use': spawn subagents with own state. ADD Section '## Orchestrator Pattern': coordinate multiple subagents. ADD Section '## Subagent State Files': each subagent maintains state. ADD Section '## Coordination': spawn, wait, collect results. ADD Section '## Synthesis': report writing from collected results. ADD Section '## Examples': research system orchestrator. (`system_prompt/20-workflow-design/30-multi-turn/20-parallel-agents.md`)

---

---
*Auto-generated from plan.json on 2026-01-05 13:27*