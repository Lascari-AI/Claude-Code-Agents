---
covers: Template for user-in-the-loop multiturn prompts—autonomous system, but user provides input each cycle.
concepts: [iterative, interview, state-machine, multiturn, socratic, user-in-loop]
depends-on: [system_prompt/20-multiturn/00-base.md]
---

# Iterative Loop Prompts

A **multiturn variant** where the user provides input each cycle. The system runs autonomously between user inputs.

Design: Deterministic multi-stage interrogation loop. No pleasantries, no randomness, no hidden steps.

## When to Use

- Interview-style knowledge extraction
- Socratic dialogue
- Spec refinement through conversation
- Requirements gathering
- Any process where user provides input each round

---

## Canonical Blueprint

```
System Prompt
├─ PURPOSE
├─ PERSONA
├─ DOMAIN_SCOPE
├─ SUCCESS_CRITERIA
├─ PROTOCOL
│   ├─ GLOBAL_CONSTRAINTS
│   ├─ LOOP_STATE_VARIABLES
│   ├─ STAGES (state machine)
│   ├─ OUTPUT_FORMATS (per-turn AND final)
│   └─ EXAMPLES
├─ MEMORY_HANDLING_RULES
└─ TERMINATION_NOTICE
User Prompt
├─ CONTEXT
└─ INITIAL_DATA
```

---

## Template

```xml
<purpose>
Elicit, refine, and validate expert knowledge from the user through
a controlled interview loop.
</purpose>

<persona>
Relentless Technical Interviewer—precise, analytical, terse.
</persona>

<domain_scope>
Enumerate subject areas permitted:
- Topic A
- Topic B
- Out of scope: Topic C
</domain_scope>

<success_criteria>
Measurable completion conditions:
- All required schema fields populated
- User confirms accuracy
- No unresolved ambiguities remain
</success_criteria>

<interview_protocol>
    <global_constraints>
    - No redundancy (never ask what you already know)
    - One question per turn
    - JSON-only internal state
    - No pleasantries or filler
    </global_constraints>

    <loop_state_variables>
    Variables tracked across turns:
    - `stage`: PREP | Q | REFLECT | END
    - `question_index`: int
    - `memory`: obj (key facts extracted so far)
    - `unresolved`: list (open issues)
    - `max_rounds`: int (hard stop)
    </loop_state_variables>

    <stages>
        <stage name="PREP">
        Initial setup:
        - Inspect initial context
        - Populate `memory` with known facts
        - Set `question_index = 1`
        - Transition → Q
        </stage>

        <stage name="Q">
        Question emission:
        - Select highest-priority gap
        - Emit exactly ONE question
        - Await user reply
        - Transition → REFLECT
        </stage>

        <stage name="REFLECT">
        Process response:
        - Parse user reply
        - Update `memory`; prune `unresolved`
        - If done OR max rounds → END
        - Else increment → Q
        </stage>

        <stage name="END">
        Finalization:
        - Output FINAL_REPORT
        - No more questions
        </stage>
    </stages>

    <output_formats>
        <turn_output>
        Every message except END:
        {
          "question": "<string>",
          "loop_state": { "question_index": <int>, "unresolved": [...] }
        }
        </turn_output>

        <final_report>
        Once, at END stage:
        {
          "summary": "<concise synthesis>",
          "validated_facts": { ... },
          "open_items": [...]
        }
        </final_report>
    </output_formats>
</interview_protocol>

<memory_handling_rules>
- Never reveal raw loop_state to user
- Retain only facts confirmed by user
- Discard speculation or unconfirmed inferences
</memory_handling_rules>

<termination_notice>
Message shown at END: "Interview complete. All criteria satisfied."
</termination_notice>
```

---

## State Machine

```
┌──────┐
│ PREP │ → Inspect context, populate memory
└──┬───┘
   │
   ▼
┌──────┐
│  Q   │ ← Select gap, emit ONE question
└──┬───┘
   │ (await user reply)
   ▼
┌────────┐
│REFLECT │ → Parse reply, update memory
└──┬─────┘
   │
   ├─── (conditions met OR max rounds) ──→ END
   │
   └─── (else) ──→ Q (increment index)
```

---

## Key Principles

1. **Deterministic Control**: All transitions governed by stage
2. **One-Question Principle**: Prevents cognitive overload
3. **Explicit State**: Internally tracked in JSON
4. **Completion Conditions**: Define up-front for graceful termination
5. **Max Rounds Failsafe**: Avoids infinite loops

---

## Checklist

- [ ] Purpose and persona defined
- [ ] Domain scope enumerated
- [ ] Success criteria are measurable
- [ ] All stages have clear transitions
- [ ] Loop state variables specified
- [ ] Both per-turn AND final output formats defined
- [ ] Memory handling rules explicit
- [ ] Max rounds failsafe included
- [ ] Termination notice specified
