# Research Plan: Orchestrator Patterns for Deterministic Claude Code Config

## Research Question

How can patterns from the Orchestrator 3 Stream system (PostgreSQL-backed state, WebSocket streaming, ADW workflows) be applied to Claude Code config to make state management more deterministic?

## Investigation Strategy

This research compares two systems:
1. **Orchestrator 3 Stream**: A multi-agent orchestration system with database-backed state, hooks, and workflow tracking
2. **Claude Code Config (Session Skill)**: A file-based session system with spec/plan/build workflow and state.json tracking

The goal is to identify **portable patterns** that improve determinism without requiring full infrastructure changes.

## Subtasks

| ID | Objective | Boundaries | Status |
|----|-----------|------------|--------|
| 001 | Analyze Orchestrator DB schema and state models for deterministic patterns | Focus on models and schema, not UI/frontend code | pending |
| 002 | Understand Claude Code session state.json structure and current update patterns | Focus on state management, not skill workflows | pending |
| 003 | Investigate ADW workflows for deterministic step execution patterns | Focus on workflow orchestration, not specific implementation details | pending |
| 004 | Examine hook systems in both codebases for observability patterns | Focus on event capture and logging, not TTS or notification hooks | pending |
| 005 | Identify integration patterns and trade-offs for applying Orchestrator concepts to Claude Code config | Focus on practical applicability, not full database migration | pending |

## Success Criteria

- **SC1**: Can map Orchestrator DB models to Claude Code session state concepts
- **SC2**: Can identify which Orchestrator patterns apply vs. require infrastructure
- **SC3**: Can provide concrete integration patterns for hooks, state, and workflows
- **SC4**: Can assess trade-offs of file-based vs. database-backed state

## Key Files to Examine

### Orchestrator System
- `reference/orchestrator-agent-with-adws/apps/orchestrator_db/models.py` - Database models
- `reference/orchestrator-agent-with-adws/apps/orchestrator_3_stream/backend/modules/orch_database_models.py` - Pydantic models
- `reference/orchestrator-agent-with-adws/apps/orchestrator_3_stream/backend/modules/orchestrator_service.py` - Service layer
- `reference/orchestrator-agent-with-adws/adws/adw_workflows/adw_plan_build.py` - ADW workflow example
- `reference/orchestrator-agent-with-adws/adws/adw_modules/adw_database.py` - ADW database ops
- `reference/orchestrator-agent-with-adws/understanding.md` - Architecture overview

### Claude Code Config
- `.claude/skills/session/SKILL.md` - Session skill overview
- `.claude/skills/session/spec/OVERVIEW.md` - Spec phase
- `.claude/skills/session/plan/OVERVIEW.md` - Plan phase
- `agents/sessions/*/state.json` - Example session states
- `.claude/hooks/logging/universal_hook_logger.py` - Hook logging

## Expected Outputs

A context report that provides:
1. Concept mapping between the two systems
2. Patterns that can be adopted (with/without database)
3. Specific recommendations for improving determinism
4. Trade-off analysis for different integration depths
