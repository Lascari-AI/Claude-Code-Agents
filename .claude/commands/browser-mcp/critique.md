---
allowed-tools: Read, Write, Bash, browser_navigate, browser_go_back, browser_go_forward, browser_snapshot, browser_click, browser_hover, browser_type, browser_select_option, browser_press_key, browser_wait, browser_get_console_logs, browser_screenshot
description: Start design critique workflow with Jony Ive lens
arguments: "Optional focus area or specific element to critique"
---

focus = $ARGUMENTS

# Design Critique

Read and execute the design critique workflow:

1. Read `.claude/skills/browser-mcp/SKILL.md` for context on Browser MCP tools
2. Read `.claude/skills/browser-mcp/references/design-principles.md` for the Jony Ive lens and evaluation criteria
3. Read `.claude/skills/browser-mcp/workflows/critique.md` for the workflow phases
4. Execute the workflow, starting with Context_Gathering phase

**Focus area (if provided)**: {focus}

Follow the workflow phases in order. Remember: this produces analysis, not implementation. Confirm context with user before proceeding with critique.
