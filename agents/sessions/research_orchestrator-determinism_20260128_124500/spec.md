# Research: Applying Orchestrator Patterns for Deterministic State

**Question**: How can I take the patterns from the Orchestrator 3 Stream system (with its PostgreSQL-backed state management, WebSocket event streaming, and ADW workflows) and apply them to my Claude Code config to make state management more deterministic?

**Style**: context

**Core Problem**: Currently, agents update session state (state.json) directly, which can lead to inconsistent states, race conditions, or lost updates. The goal is to make state transitions more predictable and traceable.

**Key Areas to Investigate**:
1. How does Orchestrator 3 Stream manage state via database vs. file-based state.json?
2. What patterns from ADW workflows could improve session phase transitions?
3. How do hooks in the orchestrator system provide observability that could benefit the session skill?
4. What's the trade-off between full database vs. hybrid approaches for a Claude Code config?
