---
description: Run an interactive interview session using the interview agent framework
argument-hint: [questions-file | session-id | "sample"]
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion
model: opus
---

# Interview Runner

This command launches the interview agent to conduct a structured interview session.

## Input: `$1`

Parse the argument to determine session context:

| Input | Action |
|-------|--------|
| `"sample"` | Load sample questions from `interview_agent/questions/sample_questions.json` |
| Path ending in `.json` | Load questions from that file |
| Existing session ID | Resume from `agents/interview_sessions/$1/state.json` |
| Empty | Prompt user to choose sample or provide file path |

## Execution

1. **Load the Agent**: Read `interview_agent/agent.md` to understand your full capabilities and workflow
2. **Determine Context**: Parse `$1` as described above
3. **Execute the Agent**: Follow the agent.md workflow phases:
   - INITIALIZE the session (new or resume)
   - Run the interview loop (ASK → WAIT → ANALYZE → DECIDE → UPDATE)
   - FINALIZE when complete

## Key Reminders

- **One question at a time**: Never ask multiple questions in one message
- **Wait for responses**: After asking a question, stop and wait for the user to respond
- **Atomic state updates**: Update state.json after every exchange
- **Session directory**: All files go in `agents/interview_sessions/{session_id}/`

## If `$1` is Empty

Use AskUserQuestion to offer:
- "Use sample questions (recommended for testing)"
- "Provide path to questions JSON file"

Then proceed based on their choice.

## Begin

Read `interview_agent/agent.md` now, then execute the interview workflow based on the parsed `$1` value.
