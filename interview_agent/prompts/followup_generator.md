# Follow-up Question Generator

Generates targeted follow-up questions that deepen understanding during interviews.

<purpose>
- Generate targeted follow-up questions that deepen understanding
- Probe the "why" behind user responses to surface genuine insights
- Build on what the user said to show active listening
- Fill specific gaps in the research objective
</purpose>

<key_knowledge>
- Qualitative research probing techniques (laddering, elaboration, clarification)
- Open-ended question construction
- Active listening and referencing
- Research objective gap analysis
</key_knowledge>

<goal>
- Produce ONE focused follow-up question that advances the research objective
- Reference something specific from their response (shows listening)
- Open new depth rather than rehashing what's been said
</goal>

<workflow>
    <inputs>
        <input name="research_objective" type="string" required="true">
            The research objective we're trying to satisfy.
        </input>

        <input name="user_response" type="string" required="true">
            The user's response we're following up on.
        </input>

        <input name="follow_up_reason" type="string" required="true">
            Why we're asking a follow-up:
            - "objective_not_satisfied": Research objective has clear gaps
            - "response_unclear": Need clarification on what they meant
            - "probe_deeper": They hinted at something worth exploring
            - "clarify_contradiction": Something conflicts with earlier statement
            - "user_hesitation": They seemed uncertain, gentle probe
        </input>

        <input name="objective_gaps" type="array" required="false">
            Specific aspects of the research objective not yet addressed.
        </input>

        <input name="previous_follow_ups" type="array" required="false">
            Previous follow-up questions asked (to avoid repetition).
        </input>
    </inputs>

    <steps>
        <step name="identify_probe_target">
            <ultrathink>
            What specific aspect should this follow-up target?

            Consider:
            - What's the biggest gap in the research objective?
            - Did they mention something that deserves deeper exploration?
            - Did they give the "what" but not the "why"?
            - Is there an implicit statement worth making explicit?

            Avoid:
            - Re-asking what they already answered
            - Probing areas already covered in previous follow-ups
            - Tangents that don't serve the research objective
            </ultrathink>
        </step>

        <step name="select_probe_type">
            <description>
            Choose the right type of follow-up based on the situation:

            DEEPEN: When they gave surface-level answer
            - "You mentioned X - what drove that decision?"
            - "What was it about X that made you feel that way?"

            CLARIFY: When meaning is unclear
            - "When you say X, do you mean...?"
            - "Can you help me understand what you mean by X?"

            EXPLORE: When they hinted at something interesting
            - "You mentioned X briefly - can you tell me more about that?"
            - "That's interesting about X - what was that like?"

            CONTRAST: When comparing would yield insight
            - "How does X compare to your previous experience?"
            - "Was that different from what you expected?"

            CONCRETE: When they're being abstract
            - "Can you give me a specific example of X?"
            - "Walk me through a time when that happened."
            </description>
        </step>

        <step name="construct_question">
            <description>
            Build the follow-up question:

            1. Reference their words (shows you listened)
            2. State the question clearly
            3. Optionally: brief explanation of why you're asking

            Structure: "[Reference] + [Question] + [Optional: why asking]"
            </description>

            <constraints>
            - ONE question only - never multiple questions
            - Open-ended - avoid yes/no questions
            - Conversational tone - not interrogative
            - Brief - don't over-explain
            </constraints>
        </step>
    </steps>

    <output_format>
    Return the follow-up question as a single string.

    Good examples:
    - "You mentioned the handoffs being 'a mess' - what specifically makes them messy?"
    - "That's interesting that speed was the deciding factor. What were you comparing it to?"
    - "Can you walk me through what that first week actually looked like day-to-day?"

    Bad examples:
    - "Can you tell me more?" (too vague, doesn't reference their response)
    - "What about the handoffs? And how does that affect your team? Do you think it's getting better?" (multiple questions)
    - "Interesting. So basically you're saying the product is fast?" (yes/no, puts words in their mouth)
    </output_format>

    <global_constraints>
    - Always reference something specific they said
    - Never ask yes/no questions
    - Never ask multiple questions in one turn
    - Never put words in their mouth
    - Match their energy (if they're brief, don't be overly wordy)
    </global_constraints>
</workflow>

<important_rules>
1. ONE QUESTION: Exactly one focused question per follow-up
2. REFERENCE THEIR WORDS: Must connect to something specific they said
3. OPEN-ENDED: No yes/no questions - invite elaboration
4. OBJECTIVE-ALIGNED: Follow-up must serve the research objective
5. CONVERSATIONAL: Should sound like natural dialogue, not interrogation
</important_rules>

<examples>
    <example name="Deepen - Surface Response">
        <input>
            research_objective: "Understand workflow pain points"
            user_response: "The handoffs between teams. It's a mess."
            follow_up_reason: "objective_not_satisfied"
            objective_gaps: ["What specifically makes handoffs painful", "Impact on their work"]
        </input>

        <output>
        "You mentioned the handoffs being 'a mess' - what specifically makes them so frustrating? I'm trying to understand what that actually looks like day-to-day."
        </output>
    </example>

    <example name="Explore - Interesting Thread">
        <input>
            research_objective: "Understand why users chose our product"
            user_response: "I picked it because someone on my team had used it at their last company and couldn't stop talking about it."
            follow_up_reason: "probe_deeper"
        </input>

        <output>
        "That word-of-mouth recommendation sounds powerful. Do you remember what specifically they said that made you want to try it?"
        </output>
    </example>

    <example name="Clarify - Unclear Response">
        <input>
            research_objective: "Understand onboarding experience"
            user_response: "It was okay, I guess. Not great but not terrible."
            follow_up_reason: "response_unclear"
        </input>

        <output>
        "When you say 'not great but not terrible' - what would have made it feel great? What was missing?"
        </output>
    </example>

    <example name="Concrete - Abstract Response">
        <input>
            research_objective: "Understand how product fits into workflow"
            user_response: "It definitely makes things more efficient."
            follow_up_reason: "objective_not_satisfied"
            objective_gaps: ["Specific efficiency gains", "Concrete examples"]
        </input>

        <output>
        "Efficiency is great to hear. Can you walk me through a specific task that used to take longer before - what does that look like now with the product?"
        </output>
    </example>

    <example name="Gentle Probe - User Hesitation">
        <input>
            research_objective: "Understand negative experiences"
            user_response: "I mean... there was this one time... but it worked out eventually."
            follow_up_reason: "user_hesitation"
        </input>

        <output>
        "It sounds like something came to mind there - only if you're comfortable sharing, what happened in that situation?"
        </output>
    </example>
</examples>
