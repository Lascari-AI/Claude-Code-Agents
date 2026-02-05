# Research Plan Template

<purpose>
Documents the investigation strategy before research subagents are spawned.
Provides traceability and enables back-checking against planned objectives.
</purpose>

<template>
# Research Plan: {Research Question}

**Research ID**: {research_id}
**Session**: {session_id}
**Created**: {timestamp}
**Complexity Tier**: {simple|medium|complex}
**Estimated Subagents**: {count}

---

## Investigation Strategy

{2-4 sentences describing the overall approach to answering the research question.
What areas will be explored? What is the investigation philosophy?}

---

## Subtasks

| ID | Objective | Boundaries |
|----|-----------|------------|
| 001 | {Clear, focused investigation goal} | {What NOT to investigate} |
| 002 | {Objective} | {Boundaries} |
| ... | ... | ... |

---

## Success Criteria

The research will be considered complete when:

- [ ] {Criterion 1: Specific, measurable outcome}
- [ ] {Criterion 2: What must be understood/documented}
- [ ] {Criterion 3: Key question that must be answered}

---

## Gap Detection Checkpoints

After each iteration, validate:

1. **Coverage**: Are all subtask objectives addressed?
2. **Depth**: Is the understanding sufficient for the report style?
3. **Connections**: Are cross-references and dependencies mapped?
4. **Contradictions**: Are conflicting findings resolved?

---

## Notes

{Any additional context, constraints, or considerations for this investigation}
</template>

<generation_guidance>
When generating a research plan:

1. **Investigation Strategy**: Synthesize from exploration phase findings
   - What directories/files are relevant?
   - What patterns emerged from initial grep searches?
   - What is the scope of the investigation?

2. **Subtasks**: Decompose based on complexity tier
   - SIMPLE (1-2): Single focused area
   - MEDIUM (3-5): Multiple related components
   - COMPLEX (5-10): Cross-cutting concerns

3. **Success Criteria**: Derive from research question type
   - "How does X work?" → Must explain architecture and flow
   - "How do I do X?" → Must provide actionable patterns
   - "What do I need to know for X?" → Must map dependencies and constraints

4. **Boundaries**: Prevent overlap between subtasks
   - Each subtask should have clear non-overlapping scope
   - Boundaries prevent duplicate investigation
</generation_guidance>

<back_checking>
During gap detection (Phase 8), use this plan to:

1. Check each success criterion - is it met by current findings?
2. Verify each subtask objective was addressed
3. Track deviations from the original plan
4. Document which criteria required additional iterations

Update the plan execution trace in research state.json to maintain traceability.
</back_checking>
