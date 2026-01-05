---
covers: Template for prompts where your code controls LLM execution—you make the API call, you process the response.
concepts: [single-completion, api-call, orchestrated, classification, extraction]
depends-on: [system_prompt/00-overview.md]
---

# Single-Completion Prompts

Your code makes the LLM call. Your code processes the response. You control execution.

This is for prompts where YOU are orchestrating the LLM—calling the API from your application, handling the response, deciding what happens next. The LLM completes a task, but your code is in the driver's seat.

**Key distinction**: You control execution vs. handing off to an autonomous system.
- **Single-Completion**: Your code calls the LLM API, processes response, decides next steps
- **Workflow/Agent**: You submit to a system (Claude Code, background agent) that runs autonomously

Tool use is fine here—you can use structured outputs, function calling, etc. The distinction is about WHO controls the execution loop, not whether tools are involved.

---

## When to Use

- Your application calls the LLM API directly
- You process the response in your code
- You control the execution flow
- Examples:
  - Classification (sentiment, category, intent)
  - Data extraction (entities, fields, structured output)
  - Content generation (summaries, rewrites, translations)
  - Agentic loops where YOUR code orchestrates multiple LLM calls
  - Tool use where YOUR code handles the tool execution

## Output Format

1. **System Prompt** (Markdown+XML): Static instructions
2. **User Prompt Formatter** (Python): Dynamic context assembly

---

## Canonical Blueprint

```
System Prompt
├─ Purpose
│   ├─ Persona (optional)
│   └─ Mission
├─ Key Knowledge and Expertise
├─ Goal
├─ Background
├─ Mission Brief (transition checkpoint)
├─ Workflow
│   ├─ Overview
│   ├─ Expected Inputs
│   ├─ Steps
│   │   └─ step <name>
│   │       ├─ description
│   │       └─ [Optional] Constraints
│   ├─ Global Constraints
│   ├─ Output Format
│   └─ [Optional] Examples
User Prompt
├─ Re-iteration of Key Information
└─ User Inputs
```

---

## Template

```xml
<purpose>
Define the mission for this computational instance. Not "You are a [role]"—
instead, state the clear objective this instance exists to accomplish.

Example: "Analyze customer feedback to identify actionable product insights
that will guide the roadmap. Successful analysis directly impacts product
decisions."
</purpose>

<key_knowledge>
List specific competencies or knowledge domains to prioritize:
- Domain expertise relevant to the task
- Specific methodologies or frameworks
- Data types or formats to understand
</key_knowledge>

<goal>
The ultimate success condition. Strategic target, not procedural steps.

Example: "Produce a prioritized list of product improvements with supporting
evidence from customer feedback, ranked by impact and feasibility."
</goal>

<background>
The WHY—this is the differentiator between good and great prompts.

- Why does this task matter?
- What larger context does it operate within?
- What pain point does it solve?
- Who benefits from successful completion?
</background>

<mission_brief>
Brief recap of purpose, goal, and background—a transition checkpoint
before detailed workflow.
</mission_brief>

<workflow>
    <overview>
    Major phases at a glance. Primes the model for detailed steps.
    </overview>

    <expected_inputs>
    What data will be provided. How to handle variability.
    </expected_inputs>

    <steps>
        <step name="analyze_input">
            <description>
            What action to perform, how to do it, why it matters.
            Be specific—inject your expert methodology here.
            </description>
            <constraints>
            Rules for THIS step only. Localized, not global.
            </constraints>
        </step>

        <step name="generate_output">
            <description>
            Next action in the sequence. Build on previous step.
            </description>
        </step>
    </steps>

    <global_constraints>
    Rules that apply EVERYWHERE:
    - Overall tone and style
    - Ethical guidelines
    - Information to exclude
    </global_constraints>

    <output_format>
    Required structure of final output. JSON schema, XML structure,
    or detailed Markdown formatting instructions.
    </output_format>

    <examples>
    Optional input/output pairs demonstrating expected behavior.
    </examples>
</workflow>

<important_rules>
Critical constraints (numbered for emphasis):
1. Rule one
2. Rule two
3. Rule three
</important_rules>
```

---

## Common Optional Sections

| Section | Purpose |
|---------|---------|
| `<system_boundaries>` | Hard constraints, what NOT to do |
| `<*_strategy>` | Domain-specific tactics |
| `<*_evaluation>` | How to check/validate things |
| `<conversation_style>` | Tone, principles, anti-patterns |
| `<directive_handling>` | How to process runtime injections |

---

## Checklist

- [ ] Purpose defines mission (not generic role)
- [ ] Background explains WHY (the differentiator)
- [ ] Steps are explicit with methodology
- [ ] Constraints localized appropriately
- [ ] Output format clearly specified
- [ ] Examples included if complex
