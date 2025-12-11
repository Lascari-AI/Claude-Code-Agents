---
description: Gain a full understanding of the research system to improve its design and implementation
---

# Prime Research System

Read all the research system documentation to understand its architecture, workflow, and agent coordination.

## Read

.claude/commands/research.md
.claude/agents/research/research-subagent.md
.claude/agents/research/report-writer.md

## Report

Summarize your understanding of the research system including:

1. **Architecture Overview**: How the orchestrator, subagents, and report-writer coordinate
2. **Workflow Phases**: The step-by-step process from request to final report
3. **Directory Structure**: How sessions, queries, findings, and reports are organized
4. **State Management**: How state.json tracks progress across all phases
5. **Parallel Execution**: How subagents run concurrently and write findings independently
6. **Report Synthesis**: How findings are combined into a comprehensive final report
7. **Potential Improvements**: Identify areas where the system could be enhanced
