---
covers: Patterns for dynamic context assembly using Python formatters to construct user prompts at runtime.
type: overview
concepts: [user-prompt, python, formatter, dynamic-context, xml-tags, state-management, modular]
---

# User Prompt Formatting (Python)

Transform external state into structured LLM completions using modular formatters.

---

## The Core Idea

You manage state externally (Redis, database, JSON file). When it's time to call the LLM, you transform that state into a formatted user prompt. The LLM receives just two things:

1. **System prompt** — Static instructions (what you built with the system prompt patterns)
2. **User prompt** — Your state, formatted with XML structure

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  External State │  →   │    Formatter    │  →   │  LLM Completion │
│  (JSON in DB)   │      │    (Python)     │      │  system + user  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

**Why XML?** Clear boundaries. The model knows exactly where each piece of context begins and ends. No ambiguity about structure.

**Why modular formatters?** State changes drastically. Each section gets its own helper function—vertical slices you can adjust independently without maintaining one giant string.

---

## Complete Example

### 1. External State (JSON)

This lives in your database, Redis, or state file:

```json
{
  "session_id": "abc-123",
  "customer": {
    "name": "Acme Corp",
    "tier": "enterprise",
    "account_age_days": 450
  },
  "request": {
    "type": "refund",
    "amount": 2500,
    "reason": "Service outage on Dec 15"
  },
  "conversation": [
    {"role": "user", "content": "I need a refund for the December outage"},
    {"role": "assistant", "content": "I can help with that. Let me look up your account."}
  ],
  "context": {
    "outage_confirmed": true,
    "outage_date": "2024-12-15",
    "affected_duration_hours": 4
  }
}
```

### 2. Modular Formatters (Python)

Each section gets its own function. Build strings line-by-line with explicit tabs—avoids Python interpreter indentation issues:

```python
def format_user_prompt(state: dict) -> str:
    """Main formatter - assembles sections from helper functions."""
    prompt = "Process this customer request:\n\n"

    prompt += format_customer(state.get("customer", {}))
    prompt += format_request(state.get("request", {}))
    prompt += format_verified_context(state.get("context", {}))
    prompt += format_conversation(state.get("conversation", []))

    prompt += "\nGenerate your response to the customer."
    return prompt


def format_customer(customer: dict) -> str:
    """Format customer information section."""
    if not customer:
        return ""

    fields = []
    if customer.get("name"):
        fields.append(f"\t<name>{customer['name']}</name>")
    if customer.get("tier"):
        fields.append(f"\t<tier>{customer['tier']}</tier>")
    if customer.get("account_age_days"):
        fields.append(f"\t<account_age_days>{customer['account_age_days']}</account_age_days>")

    if not fields:
        return ""

    return f"<customer>\n{chr(10).join(fields)}\n</customer>\n\n"


def format_request(request: dict) -> str:
    """Format the customer request section."""
    if not request:
        return ""

    fields = []
    if request.get("type"):
        fields.append(f"\t<type>{request['type']}</type>")
    if request.get("amount"):
        fields.append(f"\t<amount>{request['amount']}</amount>")
    if request.get("reason"):
        fields.append(f"\t<reason>{request['reason']}</reason>")

    if not fields:
        return ""

    return f"<request>\n{chr(10).join(fields)}\n</request>\n\n"


def format_verified_context(context: dict) -> str:
    """Format verified context - facts we've confirmed."""
    if not context:
        return ""

    fields = []
    if context.get("outage_confirmed") is not None:
        fields.append(f"\t<outage_confirmed>{context['outage_confirmed']}</outage_confirmed>")
    if context.get("outage_date"):
        fields.append(f"\t<outage_date>{context['outage_date']}</outage_date>")
    if context.get("affected_duration_hours"):
        fields.append(f"\t<affected_duration_hours>{context['affected_duration_hours']}</affected_duration_hours>")

    if not fields:
        return ""

    return f"<verified_context>\n{chr(10).join(fields)}\n</verified_context>\n\n"


def format_conversation(messages: list, max_messages: int = 20) -> str:
    """Format conversation history with sliding window."""
    if not messages:
        return ""

    # Apply sliding window
    recent = messages[-max_messages:] if len(messages) > max_messages else messages

    formatted = []
    for msg in recent:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        formatted.append(f"\t<message role='{role}'>{content}</message>")

    return f"<conversation_history>\n{chr(10).join(formatted)}\n</conversation_history>\n"
```

### 3. Rendered User Prompt

What the formatter produces:

```xml
Process this customer request:

<customer>
	<name>Acme Corp</name>
	<tier>enterprise</tier>
	<account_age_days>450</account_age_days>
</customer>

<request>
	<type>refund</type>
	<amount>2500</amount>
	<reason>Service outage on Dec 15</reason>
</request>

<verified_context>
	<outage_confirmed>True</outage_confirmed>
	<outage_date>2024-12-15</outage_date>
	<affected_duration_hours>4</affected_duration_hours>
</verified_context>

<conversation_history>
	<message role='user'>I need a refund for the December outage</message>
	<message role='assistant'>I can help with that. Let me look up your account.</message>
</conversation_history>

Generate your response to the customer.
```

### 4. Send to LLM

Simple completion with system + user using Mirascope:

```python
from mirascope import Messages, llm


@llm.call(
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    call_params={"temperature": 0.1, "max_tokens": 1024},
)
def customer_support_agent(system_prompt: str, user_prompt: str):
    return [
        Messages.System(content=system_prompt),
        Messages.User(content=user_prompt),
    ]


# Load state and call
state = redis.get(f"session:{session_id}")
response = customer_support_agent(
    system_prompt=SYSTEM_PROMPT,
    user_prompt=format_user_prompt(state),
)
```

That's it. Static system prompt + formatted state = completion.

---

## Advanced: Nested Structures

For deeply nested state, build inner sections first then wrap:

```python
def format_requirements(requirements: dict) -> str:
    """Format requirements with nested subsections."""
    if not requirements:
        return ""

    sections = []

    # Weight restrictions (nested)
    if requirements.get("min_weight") or requirements.get("max_weight"):
        weight_fields = []
        if requirements.get("min_weight"):
            weight_fields.append(f"\t\t<min_weight>{requirements['min_weight']} lbs</min_weight>")
        if requirements.get("max_weight"):
            weight_fields.append(f"\t\t<max_weight>{requirements['max_weight']} lbs</max_weight>")
        sections.append(f"\t<weight_restrictions>\n{chr(10).join(weight_fields)}\n\t</weight_restrictions>")

    # Commodity restrictions (list)
    if requirements.get("avoid_commodity"):
        items = requirements["avoid_commodity"]
        commodity_fields = [f"\t\t<type>{item}</type>" for item in items]
        sections.append(f"\t<avoid_commodity_types>\n{chr(10).join(commodity_fields)}\n\t</avoid_commodity_types>")

    if not sections:
        return ""

    return f"<requirements>\n{chr(10).join(sections)}\n</requirements>\n\n"
```

Produces:

```xml
<requirements>
	<weight_restrictions>
		<min_weight>1000 lbs</min_weight>
		<max_weight>45000 lbs</max_weight>
	</weight_restrictions>
	<avoid_commodity_types>
		<type>hazmat</type>
		<type>oversized</type>
	</avoid_commodity_types>
</requirements>
```

---

## Key Principles

1. **Modular Formatters** — Each context type has its own function
2. **Line-by-Line Building** — Use lists + `chr(10).join()`, explicit `\t` for tabs
3. **Conditional Inclusion** — Only include sections if data exists
4. **XML Semantic Tags** — Descriptive, hierarchical, clear boundaries
5. **Sliding Window** — Limit conversation history to prevent context overflow
6. **End Instruction** — Brief task reminder after all context