---
description: Run an interactive interview session using the interview agent framework
argument-hint: [questions-file | session-id | "sample"]
allowed-tools: Read, Write, Edit, Glob, AskUserQuestion
model: opus
---

# Interview Mode

Conduct an interactive interview session, asking questions one at a time and adapting based on responses.

## Variables

```
$1 = Primary argument:
     - Path to questions JSON file → Start new interview with those questions
     - Existing session ID → Resume that interview
     - "sample" → Use built-in sample questions for testing
     - Empty → Prompt user for questions file or use sample

SESSIONS_DIR = agents/interview_sessions
QUESTIONS_DIR = agents/interview_agent/questions
```

## Instructions

Parse `$1` to determine session context:

1. **`$1` is "sample"**: Load sample questions from `QUESTIONS_DIR/sample_questions.json`
2. **`$1` is a file path**: Load questions from that JSON file
3. **`$1` matches existing session ID**: Resume that session from `SESSIONS_DIR/$1/state.json`
4. **`$1` is empty**: Use AskUserQuestion to offer sample questions or custom file path

Then proceed through: Initialize → Question Loop → Finalize

## Core Principles

Interview mode is:
- **Conversational** - Natural dialogue, not interrogation
- **Research-objective driven** - Each question has a purpose
- **Adaptive** - Follow-ups based on response analysis
- **Persistent** - State saved after every exchange
- **One question at a time** - Never multiple questions in one turn

<workflow>
    <phase id="1" name="Parse Inputs">
        <description>Determine session context from arguments</description>
        <steps>
            <step id="1">Check if $1 is "sample" → use sample questions</step>
            <step id="2">Check if $1 is a file path ending in .json → load that file</step>
            <step id="3">Check if SESSIONS_DIR/$1/state.json exists → resume session</step>
            <step id="4">If $1 is empty, prompt user with AskUserQuestion:
                - "Use sample questions (recommended for testing)"
                - "Provide path to questions JSON file"
            </step>
        </steps>
    </phase>

    <phase id="2" name="Initialize Session">
        <branch condition="Starting new interview">
            <steps>
                <step id="1">Generate session_id: {YYYY-MM-DD}_{interview-slug}_{6-char-id}</step>
                <step id="2">Create directory: SESSIONS_DIR/{session_id}/</step>
                <step id="3">Load questions from JSON file</step>
                <step id="4">Create initial state.json with:
                    - session_id
                    - title from questions file
                    - context from questions file
                    - questions array with research objectives
                    - status: "in_progress"
                    - current_question_index: 0
                </step>
                <step id="5">Create empty transcript.md for human-readable record</step>
                <step id="6">Display session start message</step>
            </steps>
        </branch>
        <branch condition="Resuming existing session">
            <steps>
                <step id="1">Load state.json from SESSIONS_DIR/$1/</step>
                <step id="2">Display resume message with current progress</step>
                <step id="3">Show where we left off (current question, any pending follow-up)</step>
            </steps>
        </branch>
    </phase>

    <phase id="3" name="Interview Loop">
        <description>The core iterative interview process</description>

        <critical>
        This is an interactive loop. After each question, WAIT for user response.
        Do NOT auto-generate responses or continue without user input.
        </critical>

        <loop_structure>
            1. ASK: Present one question (initial or follow-up)
            2. WAIT: User responds in chat
            3. ANALYZE: Evaluate response against research objective
            4. DECIDE: Follow-up for depth OR transition to next question
            5. UPDATE: Save state.json and transcript.md atomically
            6. REPEAT: Until all questions complete
        </loop_structure>

        <asking_questions>
            <initial_question>
                - Present the base question text naturally
                - Set question status to "active"
                - Record in transcript.md
            </initial_question>

            <follow_up_question>
                <trigger>Response analysis recommends follow-up AND follow_up_count < max_follow_ups</trigger>
                <approach>
                    - Reference something specific from their response
                    - Probe the "why" behind the "what"
                    - Keep it conversational
                    - Explain briefly why you're asking
                </approach>
                <constraints>
                    - ONE question only
                    - Must connect to their previous answer
                    - Open-ended (no yes/no questions)
                </constraints>
            </follow_up_question>
        </asking_questions>

        <analyzing_responses>
            <ultrathink>
            After each user response, analyze deeply:

            1. RESEARCH OBJECTIVE CHECK
               - Does this response address the research objective?
               - What specific aspects are now answered?
               - What gaps remain?

            2. INSIGHT EXTRACTION
               - What concrete learnings can we extract?
               - Note powerful quotes verbatim
               - Distinguish facts vs opinions vs emotions

            3. DEPTH ASSESSMENT
               - Surface-level or genuine depth?
               - Did they explain "why" or just "what"?

            4. FOLLOW-UP VALUE
               - Would probing add significant value?
               - What specific aspect to explore?
               - Have we hit diminishing returns?

            5. USER STATE
               - Engaged or fatigued?
               - Any signals to skip or move on?
            </ultrathink>

            <output>
                objective_progress: "not_started" | "partial" | "satisfied" | "exceeded"
                insights: [list of extracted insights]
                recommendation: "follow_up" | "transition"
                recommendation_reason: "why this is the right next step"
            </output>
        </analyzing_responses>

        <transitions>
            <trigger>Analysis recommends transition OR max follow-ups reached OR user skip</trigger>
            <approach>
                1. Validate: Acknowledge something specific they shared
                2. Bridge: Create natural connection to next topic
                3. Ask: Present the next question
            </approach>
            <constraints>
                - Keep validation brief (1 sentence)
                - Don't over-summarize what they said
                - Make the transition feel natural
            </constraints>
        </transitions>

        <state_updates>
            <critical>Update state after EVERY exchange - never batch</critical>
            <updates>
                - Add exchange to current question's exchanges[]
                - Update question objective_status
                - Add insights to insight_bank
                - Append to conversation_history
                - Update transcript.md
                - Set updated_at timestamp
            </updates>
        </state_updates>
    </phase>

    <phase id="4" name="Finalize">
        <trigger>All questions completed (current_question_index >= total_questions)</trigger>
        <steps>
            <step id="1">Generate completion message:
                - Thank the participant
                - Highlight 2-3 key insights
                - Confirm interview is complete
            </step>
            <step id="2">Update state.json:
                - status: "completed"
                - completed_at: now()
            </step>
            <step id="3">Generate summary section in transcript.md</step>
            <step id="4">Report session location and key stats</step>
        </steps>
    </phase>
</workflow>

## Question File Format

Questions JSON files should follow this structure:

```json
{
  "title": "Interview Title",
  "context": "Background context for the interview",
  "questions": [
    {
      "id": "q1",
      "order": 1,
      "base_question_text": "The question to ask",
      "research_objective": "What we're trying to learn from this question"
    }
  ]
}
```

## State File Structure

State is tracked in `SESSIONS_DIR/{session_id}/state.json`:

```json
{
  "session_id": "2025-01-05_user-research_abc123",
  "title": "Interview Title",
  "status": "in_progress",
  "current_question_index": 0,
  "questions": [
    {
      "id": "q1",
      "status": "active",
      "objective_status": "partial",
      "exchanges": [
        {
          "question_text": "What was asked",
          "user_response": "What they said",
          "is_follow_up": false
        }
      ]
    }
  ],
  "insight_bank": {
    "insights": [
      {"content": "Key learning", "importance": "high"}
    ]
  }
}
```

## Behavior Constraints

DURING INTERVIEW MODE:
- DO NOT ask multiple questions at once
- DO NOT generate fake user responses
- DO NOT skip waiting for user input
- DO NOT make judgments about answers - stay neutral
- DO validate and acknowledge each response
- DO extract insights from every substantive response
- DO save state after EVERY exchange
- DO respect user signals to skip questions
- DO keep transitions natural and conversational

ALLOWED WRITES:
- agents/interview_sessions/{session_id}/**

## User Output Scenarios

<scenario name="new_session">
```markdown
## Interview Started

**Session ID**: `{session_id}`
**Title**: {title}
**Questions**: {total_questions}
**Location**: `agents/interview_sessions/{session_id}/`

---

I'll be asking you {total_questions} questions, one at a time. Take your time
with each response - I'm interested in your genuine thoughts and experiences.

Let's begin:

**{first_question_text}**
```
</scenario>

<scenario name="resume_session">
```markdown
## Interview Resumed

**Session ID**: `{session_id}`
**Title**: {title}
**Progress**: {completed}/{total} questions

### Where We Left Off
{current question and context}

---

{Continue with current question or follow-up}
```
</scenario>

<scenario name="after_response">
```markdown
{Validation of their response - reference something specific}

{If transitioning: bridge + next question}
{If follow-up: targeted follow-up question with brief explanation}
```
</scenario>

<scenario name="interview_complete">
```markdown
## Interview Complete

Thank you for sharing your experiences with me today.

### Key Insights
{2-3 most important learnings}

### Session Details
- **Session ID**: `{session_id}`
- **Questions Completed**: {total}
- **Total Exchanges**: {exchange_count}
- **Transcript**: `agents/interview_sessions/{session_id}/transcript.md`
- **State**: `agents/interview_sessions/{session_id}/state.json`

Your responses have been saved and can be reviewed in the transcript.
```
</scenario>

## Error Handling

<scenario name="Questions File Not Found">
    Inform user the file wasn't found. Offer to use sample questions or provide a different path.
</scenario>

<scenario name="Invalid Questions Format">
    Show what's missing or malformed. Provide the expected format.
</scenario>

<scenario name="Session Not Found">
    Inform user the session wasn't found. List available sessions or offer to start new.
</scenario>

<scenario name="User Wants to Skip">
    Acknowledge gracefully: "No problem - let's move on."
    Update state with skip reason and transition to next question.
</scenario>
