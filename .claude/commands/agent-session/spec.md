---
description: Enter spec mode to define requirements and goals before implementation planning
argument-hint: [topic | session-id | finalize] [description]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
model: opus
---

# Spec Mode

Enter spec mode to define WHAT you want to build before planning HOW to build it.

## Skill Reference

Read the agent-session skill for templates and full documentation:
- Skill: `.claude/skills/agent-session/SKILL.md`
- Templates: `.claude/skills/agent-session/templates/`
- Working directory: `agents/sessions/`

## Variables

```
$1 = Primary argument (session-id, topic, or "finalize")
$2 = Optional additional context or description
SESSIONS_DIR = agents/sessions
TEMPLATES_DIR = .claude/skills/agent-session/templates
```

## Instructions

Parse `$1` and follow the linear flow:

1. **`$1 = "finalize"`**: Jump to finalization phase for active session
2. **`$1` matches existing session ID**: Load that session (check `SESSIONS_DIR/$1/state.json`)
3. **`$1` is a topic string**: Create a new session with `$1` as topic, `$2` as optional description
4. **`$1` is empty**: Create a new session (prompt user for topic)

Then proceed through: Initialize → Question-driven exploration → Finalize (on user approval)

## Core Principles

Spec mode is:
- **Almost read-only** - Only writes to the session directory
- **Question-driven** - Asks clarifying questions to understand the problem
- **Focused on WHAT and WHY** - Not implementation details (that's plan mode)
- **Iterative** - Refines understanding through conversation

<workflows>
    <workflow name="spec_flow">
        <description>Linear flow from session resolution through finalization</description>
        <phase name="1_parse_inputs">
            <description>Parse positional arguments to determine session context</description>
            <inputs>
                - `$1`: Primary argument - one of:
                    - "finalize" → trigger finalization
                    - existing session ID → load that session
                    - topic string → create new session
                    - empty → prompt for topic
                - `$2`: Optional description/context for new sessions
            </inputs>
        </phase>
        <phase name="2_resolve_session">
            <description>Either load existing session or create new one</description>
            <branch condition="$1 matches existing session ID">
                <action>Load existing session</action>
                <steps>
                    <step id="1">Check if SESSIONS_DIR/$1/state.json exists</step>
                    <step id="2">Load state.json from SESSIONS_DIR/$1/</step>
                    <step id="3">Read current spec.md to restore context</step>
                    <step id="4">Review open_questions from state</step>
                </steps>
                <on_failure>Session not found → fall through to create new session</on_failure>
            </branch>
            <branch condition="$1 is topic string OR $1 is empty">
                <action>Create new session</action>
                <steps>
                    <step id="1">If $1 is empty, prompt user for topic</step>
                    <step id="2">Generate session_id: {YYYY-MM-DD}_{topic-slug}_{6-char-random-id}</step>
                    <step id="3">Create directory structure:
                        ```bash
                        mkdir -p SESSIONS_DIR/{session_id}/research
                        mkdir -p SESSIONS_DIR/{session_id}/context/diagrams
                        mkdir -p SESSIONS_DIR/{session_id}/context/notes
                        ```
                    </step>
                    <step id="4">Initialize state.json with:
                        - current_phase: "spec"
                        - phases.spec.status: "draft"
                        - phases.spec.started_at: now()
                        - topic: $1 (or prompted value)
                        - description: $2 (if provided)
                    </step>
                    <step id="5">Create initial spec.md from TEMPLATES_DIR/spec.md</step>
                    <step id="6">Write active_session.json to SESSIONS_DIR with current session_id</step>
                </steps>
            </branch>
        </phase>
        <phase name="3_initialize">
            <description>Prepare session state for interaction</description>
            <steps>
                <step id="1">Confirm session is loaded and active</step>
                <step id="2">Display session status to user (new or resumed)</step>
                <step id="3">If resuming, summarize current understanding from spec.md</step>
                <step id="4">If resuming, list open questions from state.json</step>
            </steps>
        </phase>
        <phase name="4_question_driven_exploration">
            <description>The core interaction loop during spec mode</description>
            <principles>
                - Ask ONE focused question at a time
                - Explain WHY you're asking
                - After each answer, update spec.md incrementally
                - Surface assumptions explicitly
                - Use diagrams when they clarify understanding
                - Track open questions in state.json
            </principles>
            <question_categories>
                <category name="problem_space">
                    - What problem are we solving?
                    - Who experiences this problem?
                    - What's the current workaround?
                    - What triggers the need for this?
                </category>
                <category name="goals">
                    - What does success look like?
                    - How will we know we're done?
                    - What's the minimum viable version?
                </category>
                <category name="constraints">
                    - What can't change?
                    - What dependencies exist?
                    - What's the timeline?
                    - Are there technical constraints?
                </category>
                <category name="scope">
                    - What's explicitly NOT included?
                    - What could be a future phase?
                    - What's the priority order?
                </category>
                <category name="context">
                    - How does this fit with existing systems?
                    - Are there similar implementations to reference?
                    - Who else is involved in this decision?
                </category>
            </question_categories>
            <after_each_answer>
                1. Acknowledge understanding
                2. Update relevant section in spec.md
                3. Note any decisions made (add to key_decisions)
                4. Identify if new questions emerged (add to open_questions)
                5. Remove answered questions from open_questions
                6. Ask next question OR summarize progress
            </after_each_answer>
            <exit_condition>User signals readiness to finalize OR all key questions answered</exit_condition>
        </phase>
        <phase name="5_finalize">
            <description>Complete and lock the spec for planning phase</description>
            <trigger>User approval (explicit request or confirmation prompt)</trigger>
            <steps>
                <step id="1">Review spec.md for completeness</step>
                <step id="2">Ensure required sections are present:
                    - Overview
                    - High-level goals
                    - Mid-level goals
                </step>
                <step id="3">Ask user to confirm finalization</step>
                <step id="4">Update state.json:
                    - phases.spec.status: "finalized"
                    - phases.spec.finalized_at: now()
                </step>
                <step id="5">Add finalization header to spec.md</step>
                <step id="6">Report: "Spec finalized. Ready for `/plan` phase."</step>
            </steps>
            <on_incomplete>List missing required sections and continue exploration</on_incomplete>
        </phase>
    </workflow>
</workflows>

<templates>
    <location>TEMPLATES_DIR/spec.md</location>
    <description>Read the spec template from the templates directory when creating new sessions</description>
    <variables>
        - {{TOPIC}}: Session topic from $1
        - {{SESSION_ID}}: Generated session ID
        - {{DATE}}: Current date
        - {{INITIAL_UNDERSTANDING}}: Initial context from $2 or conversation
    </variables>
</templates>

<active_session_tracking>
File: agents/sessions/active_session.json
```json
{
  "session_id": "current-active-session-id",
  "path": "agents/sessions/{session_id}",
  "activated_at": "timestamp"
}
```

This file tracks which session is currently active, allowing:
- `/spec` to resume the active session automatically
- `/plan` to automatically pick up the finalized spec
- Quick status checks
</active_session_tracking>

<behavior_constraints>
DURING SPEC MODE:
- DO NOT write code to non-session directories
- DO NOT create implementation plans (that's plan mode)
- DO NOT make architecture decisions (focus on WHAT not HOW)
- DO read codebase files for context
- DO create diagrams in session/context/diagrams/
- DO update spec.md after each meaningful exchange
- DO track questions and decisions in state.json

ALLOWED WRITES:
- agents/sessions/{session_id}/**  (all session files)
- agents/sessions/active_session.json
</behavior_constraints>

<user_output>
    <scenario name="new_session" trigger="Creating a new spec session">
```markdown
## Spec Session Started

**Session ID**: `{session_id}`
**Topic**: {topic}
**Location**: `agents/sessions/{session_id}/`

I'll help you clarify what you want to build. I'll ask questions to understand
the problem, goals, and constraints before we move to planning.

{First question based on the topic}
```

    </scenario>
    <scenario name="resume_session" trigger="Loading an existing session">
```markdown
## Spec Session Resumed

**Session ID**: `{session_id}`
**Topic**: {topic}
**Status**: {spec_status}

### Current Understanding
{Brief summary of spec.md}

### Open Questions
{List from state.json}

{Continue with next question or ask where to focus}
```
    </scenario>

    <scenario name="finalize" trigger="User approves spec finalization">
```markdown
## Spec Finalized

**Session ID**: `{session_id}`
**Topic**: {topic}

### Summary
{High-level and mid-level goals}

### Ready for Planning
The spec is now ready for the planning phase. Use `/plan` to begin
implementation planning, which will use this spec as its foundation.

**Spec Location**: `agents/sessions/{session_id}/spec.md`
```
    </scenario>
</user_output>

<error_handling>
    <scenario name="No Arguments">
        Prompt user for a topic to begin a new spec session.
    </scenario>
    <scenario name="Session ID Not Found">
        Inform user the session wasn't found, offer to create a new session instead.
    </scenario>
    <scenario name="Finalize Without Required Content">
        List missing required sections and continue question-driven exploration.
    </scenario>
    <scenario name="No Active Session for Finalize">
        Inform user no active session exists, prompt for session ID or topic.
    </scenario>
</error_handling>
