---
covers: Patterns for dynamic context assembly using Python formatters to construct user prompts at runtime.
type: overview
concepts: [user-prompt, python, formatter, dynamic-context, xml-tags, sliding-window]
---

# User Prompt Formatting (Python)

Dynamic context assembly that pairs with any system prompt.

## The Power of Statelessness

LLMs are stateless—they have no memory, no context, nothing. Each request starts fresh.

This is actually a **superpower**: you have complete control over everything the model sees. Instead of relying on the classic user/assistant message format, you can construct the entire user prompt as a single, carefully structured document. The model reads it the same way—it doesn't know the difference.

This means you can:
- Inject runtime context exactly where it matters
- Control the narrative flow of information
- Layer context from static → dynamic → conversational
- Format everything with semantic XML for clarity

**Core Insight**: System prompt stays STATIC. User prompt owns the DYNAMIC context window.

---

## When to Use

- Any system prompt that needs runtime context
- Single-task prompts with variable inputs
- Agentic systems with state tracking
- Conversation history management

## Output Format

**Python functions** that take state objects and return formatted strings.

---

## Core Pattern

```python
def format_user_prompt(context: Dict[str, Any], messages: List[Dict[str, Any]]) -> str:
    """
    Format the complete user prompt with all dynamic context.
    """
    prompt = "Analyze the context below and generate your response:\n\n"

    # Layer 1: Temporal grounding
    prompt += format_date_context(...)

    # Layer 2: Static reference data
    prompt += format_background_knowledge(...)  # <background_knowledge_base>

    # Layer 3: Constraints/requirements
    prompt += format_requirements(...)  # <requirements>

    # Layer 4: Decision-relevant data
    prompt += format_pricing_info(...)  # <pricing_information>

    # Layer 5: Situational context
    prompt += format_call_context(...)  # <call_context>

    # Layer 6: State accumulated so far
    prompt += format_collected_data(...)  # <collected_data>

    # Layer 7: History + analysis
    prompt += format_history(...)  # <history>

    # Layer 8: Recent conversation (sliding window)
    prompt += format_conversation_history(messages, max=20)

    # Final instruction
    prompt += "\nGenerate your response..."
    return prompt
```

---

## Modular Formatter Pattern

Each context type gets its own function:

```python
def format_requirements_context(requirements: Dict[str, Any]) -> str:
    """Format requirements for the prompt."""
    if not requirements:
        return ""

    sections = []

    if requirements.get("min_weight") or requirements.get("max_weight"):
        weight_sections = []
        if requirements.get("min_weight"):
            weight_sections.append(f"\t\t<min_weight>{requirements['min_weight']}</min_weight>")
        if requirements.get("max_weight"):
            weight_sections.append(f"\t\t<max_weight>{requirements['max_weight']}</max_weight>")
        sections.append(f"\t<weight_restrictions>\n{chr(10).join(weight_sections)}\n\t</weight_restrictions>")

    if not sections:
        return ""

    return f"<requirements>\n{chr(10).join(sections)}\n</requirements>"
```

---

## XML Tag Conventions

```xml
<!-- Semantic wrapper tags -->
<background_knowledge_base>
    <entity_information>
        <entity_id>123</entity_id>
    </entity_information>
</background_knowledge_base>

<!-- Hierarchical nesting -->
<requirements>
    <weight_restrictions>
        <min_weight>1000</min_weight>
        <max_weight>45000</max_weight>
    </weight_restrictions>
</requirements>

<!-- Conversation history with role attribution -->
<recent_conversation_history>
    <message role='user'>User message here</message>
    <message role='assistant'>Assistant response here</message>
</recent_conversation_history>

<!-- Runtime directive injection -->
<active_directives>
    <background_directive priority="INTERRUPT">
        Critical instruction that must be addressed immediately.
    </background_directive>
</active_directives>
```

---

## Conversation History Formatter

```python
def format_recent_conversation_history(
    messages: List[Dict[str, Any]], max_messages: int = 20
) -> str:
    """Format recent conversation history with sliding window."""
    formatted_messages = []

    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        if role == "system":
            continue
        elif role == "user":
            formatted_messages.append(f"\t<message role='user'>{content}</message>")
        elif role == "assistant":
            if "tool_calls" in msg:
                continue
            formatted_messages.append(f"\t<message role='assistant'>{content}</message>")

    # Apply sliding window
    if len(formatted_messages) > max_messages:
        formatted_messages = formatted_messages[-max_messages:]
        formatted_messages.insert(0, "\t<!-- Older history truncated -->")

    return (
        "<recent_conversation_history>\n"
        + "\n".join(formatted_messages)
        + "\n</recent_conversation_history>\n"
    )
```

---

## Layering Order (Recommended)

1. **Temporal grounding** - Current date/time
2. **Static reference data** - Background knowledge
3. **Constraints/requirements** - Rules and restrictions
4. **Decision-relevant data** - Pricing, estimates
5. **Situational context** - Session-specific info
6. **Accumulated state** - Data collected so far
7. **History/analysis** - Rate history, analysis
8. **Conversation history** - Recent messages (sliding window)
9. **End instruction** - Brief task reminder

---

## Key Principles

1. **Modular Formatters**: Each context type has its own function
2. **XML Semantic Tags**: Descriptive, hierarchical tags
3. **Conditional Inclusion**: Only include sections if data exists
4. **Sliding Window**: Limit conversation history
5. **Directive Injection**: Runtime insertions via `<active_directives>`
6. **End Instruction**: Brief reminder of the task

---

## Checklist

- [ ] Each context type has its own formatter function
- [ ] XML tags are semantic and descriptive
- [ ] Conditional inclusion prevents empty sections
- [ ] Conversation history has sliding window
- [ ] Directive injection point is before conversation history
- [ ] End instruction reminds of task
