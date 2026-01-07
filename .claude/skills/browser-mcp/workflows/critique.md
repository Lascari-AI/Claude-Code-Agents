---
covers: Design critique workflow using Browser MCP with Jony Ive lens
type: workflow
concepts: [design-critique, browser-mcp, jony-ive, multi-turn, screenshots]
---

# Design Critique Workflow

A structured design critique workflow that applies the Jony Ive lens to evaluate and improve visual design.

## Overview

This workflow enables thorough design critique by:
1. **Context Gathering** - Understanding what the app/page is for (confirmed with user)
2. **Visual Capture** - Screenshots across states and viewports
3. **Analysis** - Applying the Jony Ive perspective to identify issues
4. **Principles Check** - Evaluating against specific design guidelines
5. **Report** - Structured output with prioritized recommendations
6. **Refinement** - Iterating with user until satisfied
7. **Save** - Persisting the critique for handoff to implementation

**Key principle**: This is analysis-focused, not implementation. The output feeds into plan mode when ready to act on recommendations.

## Workflow

```xml
<workflow id="design-critique">
    <global_constraints>
        - Analysis-focused: produce critique report, not implementation
        - Must confirm context with user before critique begins
        - Apply Jony Ive lens: "Really think. Really, really think."
        - Reference design-principles.md for evaluation criteria
        - Save all artifacts to agents/design-sessions/{id}/
    </global_constraints>

    <phase id="1" name="Context_Gathering">
        <action>
            - Call `browser_snapshot` to see current URL and page state
        </action>
        <action>
            - Infer from visual + any available code:
              - Purpose of the app
              - Purpose of this specific page
              - What should a user accomplish here?
        </action>
        <action>
            - Present understanding: "Here's what I think this app/page is for..."
        </action>
        <action>
            - Wait for user confirmation or correction
            - Do NOT proceed to critique until context is confirmed
        </action>
    </phase>

    <phase id="2" name="Visual_Capture">
        <action>
            - Call `browser_screenshot` for current state
        </action>
        <action>
            - Navigate through different states/views if relevant
            - Capture key interactions and transitions
        </action>
        <action>
            - If responsive design matters, capture mobile viewport
            - Use browser_click on device toggle or resize as needed
        </action>
        <action>
            - Organize screenshots mentally for reference in analysis
        </action>
    </phase>

    <phase id="3" name="Analysis">
        <action>
            - Read SKILL_ROOT/references/design-principles.md for the Jony Ive lens
        </action>
        <action>
            - For each screen/state captured, examine:
              - What works well? (call these out — positive reinforcement)
              - What doesn't work? (specific, actionable)
              - What is confusing or unclear?
              - What feels redundant or unnecessary?
        </action>
        <action>
            - Apply "Would Steve Jobs smile at this?" test
        </action>
    </phase>

    <phase id="4" name="Principles_Check">
        <action>
            - Evaluate against specific guidelines from design-principles.md:
              - Icons vs emojis (clean icons preferred)
              - Padding/spacing (intentional, not cramped)
              - Aesthetic (sleek, premium, minimalist)
              - Color palette (cohesive, not random accents)
              - Responsive (elegant on both desktop and mobile)
        </action>
        <action>
            - Use evaluation questions:
              - First impression: premium or cheap?
              - Clarity: understandable in 5 seconds?
              - Economy: what can be removed?
              - Consistency: similar elements look/behave the same?
              - Hierarchy: clear what's most important?
        </action>
    </phase>

    <phase id="5" name="Report">
        <action>
            - Structure the critique report:
              ## Summary
              [1-2 sentences on overall impression]

              ## What Works
              [Positive elements to preserve]

              ## Issues Identified
              [Specific problems with evidence]

              ## Recommendations
              [Actionable improvements]

              ## Priority Order
              [What to fix first, second, third...]
        </action>
        <action>
            - Present report to user
        </action>
    </phase>

    <phase id="6" name="Refinement">
        <action>
            - Ask user: "Would you like me to examine anything else?"
        </action>
        <action>
            - Handle follow-up questions:
              - "What about this element?"
              - "Can you look at the mobile view?"
              - "How would you handle [specific component]?"
        </action>
        <action>
            - Continue until user is satisfied with the analysis
        </action>
    </phase>

    <phase id="7" name="Save">
        <action>
            - Generate unique session ID (timestamp-based)
        </action>
        <action>
            - Create directory: agents/design-sessions/{id}/
        </action>
        <action>
            - Save artifacts:
              - critique.md — The full critique report
              - context.md — Confirmed app/page purpose and goals
              - screenshots/ — Visual captures used in analysis (if applicable)
        </action>
        <action>
            - Present save location to user
            - Note: "When ready to implement, this can feed into plan mode"
        </action>
    </phase>
</workflow>
```
