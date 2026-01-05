---
covers: Template for multiturn prompts submitted to autonomous systems—you direct, the system executes.
type: overview
concepts: [multiturn, autonomous, agent, skill, command, directive]
depends-on: [system_prompt/00-overview.md]
---

# Multiturn Prompts

You submit instructions. The system takes multiple turns autonomously.

This is for prompts where you're NOT controlling execution—you hand off to a system (Claude Code, background agent, autonomous pipeline) that runs on its own. The system decides what LLM calls to make, what tools to use, and when it's done.

**Key distinction**: You're directing an autonomous system, not orchestrating LLM calls yourself.
- **Single-Completion**: Your code controls the LLM, you process responses
- **Multiturn**: You submit to a system that runs autonomously across multiple turns

---

## When to Use

- Claude Code skills and commands
- Background agents and subagents
- Autonomous pipelines and workflows
- Any system that runs multiple turns on its own

For **user-in-the-loop** processes (user provides input each turn), see `10-iterative-loop.md`.

---

## Canonical Blueprint

```markdown
---
name: agent-name
description: What this agent does
tools: Read, Write, Glob, Grep, Task, ...
model: opus
---

<purpose>
Clear mission statement for this agent.
</purpose>

<variables>
CONFIGURABLE_PARAM = $ARGUMENTS
NUM_ITEMS = 3
</variables>

<input_format>
What this agent receives.
</input_format>

<output_protocol>
  <critical>
  What the agent MUST do with output.
  </critical>
</output_protocol>

<state_schema>
{
  "id": "session_id",
  "status": "initializing|processing|complete|failed",
  ...
}
</state_schema>

<workflow>
    <phase id="1" name="Initialize">
        <action>First action</action>
        <action>Second action</action>
    </phase>
    <phase id="2" name="Execute">
        <critical>Important constraint</critical>
        <action>Main work</action>
    </phase>
</workflow>

<principles>
  <principle name="Name">
      Explanation of the principle.
  </principle>
</principles>

<error_handling>
    <scenario name="Error Type">
        - How to handle it
    </scenario>
</error_handling>

<important_notes>
- Critical reminders
- Constraints
</important_notes>
```

---

## Key Sections

### Frontmatter (YAML)

```yaml
---
name: research-orchestrator
description: Coordinate parallel research investigations
argument-hint: [research question] [--style=cookbook|understanding|context]
allowed-tools: Bash, Task, Write, Read, Edit, Glob, Grep
model: opus
---
```

Required: `name`, `description`
Optional: `tools`, `model`, `argument-hint`, `color`

### Variables

```xml
<variables>
RESEARCH_REQUEST = $ARGUMENTS
NUM_SUBAGENTS = 3
OUTPUT_DIR = research_sessions/
</variables>
```

`$ARGUMENTS` receives command-line input.

### State Schema

```xml
<state_schema>
{
  "id": "session_id",
  "status": "initializing|researching|complete|failed",
  "created_at": "ISO_8601_timestamp",
  "subagents": [
    { "id": "001", "title": "Query Title", "status": "pending" }
  ]
}
</state_schema>
```

### Phased Workflow

```xml
<workflow>
    <phase id="1" name="Initialize">
        <action>Validate input</action>
        <action>Create directories</action>
    </phase>

    <phase id="2" name="Execute">
        <critical>
            Spawn ALL tasks in a SINGLE message with multiple parallel calls.
        </critical>
        <action>For each query, spawn subagent</action>
    </phase>

    <phase id="3" name="Finalize">
        <action>Spawn report writer</action>
        <action>Provide summary to user</action>
    </phase>
</workflow>
```

Use `<critical>` tags for must-not-violate constraints.

### Principles

```xml
<principles>
  <principle name="Incremental Updates">
      Update state file after EACH file examined.
  </principle>
  <principle name="Focused Investigation">
      Stay laser-focused on assigned objective.
  </principle>
</principles>
```

### Error Handling

```xml
<error_handling>
    <scenario name="Empty Request">
        Please provide a topic: `/command [your input]`
    </scenario>
    <scenario name="Subagent Failure">
        - Note failure in state
        - Continue with successful subagents
    </scenario>
</error_handling>
```

---

## Checklist

- [ ] Frontmatter includes name, description, tools
- [ ] Purpose clearly states mission
- [ ] Variables are configurable
- [ ] State schema defined for progress tracking
- [ ] Phases have clear actions
- [ ] `<critical>` tags mark must-not-violate constraints
- [ ] Error scenarios covered
- [ ] Parallel execution explicitly noted where applicable
