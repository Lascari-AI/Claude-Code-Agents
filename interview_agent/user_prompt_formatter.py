"""
User Prompt Formatter for Interview Agent

Transforms InterviewState into structured XML context for LLM prompts.
Follows the modular formatter pattern from the prompt-writing framework:
- Each section has its own formatter function
- Build strings line-by-line with explicit tabs
- XML semantic tags for clear boundaries
- Conditional inclusion based on available data
"""

from typing import Any, Dict, List, Optional

# Import state schema (adjust path as needed)
from agents.interview_agent.state_schema import (
    Exchange,
    InsightBank,
    InterviewState,
)

# =============================================================================
# MAIN FORMATTER - Orchestrator Prompt
# =============================================================================


def format_interviewer_prompt(
    state: InterviewState,
    user_message: Optional[str] = None,
    max_history: int = 10,
    include_all_questions: bool = False,
) -> str:
    """
    Main formatter for the interviewer system prompt.

    Assembles all context sections into a structured XML user prompt.

    Args:
        state: The current InterviewState
        user_message: The user's latest response (None on first turn)
        max_history: Maximum conversation history entries to include
        include_all_questions: Whether to show all questions or just current

    Returns:
        Formatted XML string for the user prompt
    """
    prompt = ""

    # Interview context and metadata
    prompt += format_interview_context(state)

    # Current question with research objective
    prompt += format_current_question(state)

    # Exchange history for current question
    prompt += format_question_exchanges(state)

    # Accumulated insights (summary view)
    prompt += format_insight_summary(state.insight_bank)

    # Recent conversation history
    prompt += format_conversation_history(
        state.conversation_history, max_entries=max_history
    )

    # The new user message (if provided)
    if user_message:
        prompt += format_user_message(user_message)

    # Progress and status
    prompt += format_progress(state)

    # Task instruction
    prompt += format_task_instruction(state, user_message)

    return prompt


# =============================================================================
# SECTION FORMATTERS
# =============================================================================


def format_interview_context(state: InterviewState) -> str:
    """Format interview metadata and context."""
    fields = []
    fields.append(f"\t<session_id>{state.session_id}</session_id>")
    fields.append(f"\t<title>{state.title}</title>")
    fields.append(f"\t<status>{state.status.value}</status>")

    if state.context:
        # Escape any XML-like content in context
        escaped_context = _escape_xml(state.context)
        fields.append(f"\t<context>{escaped_context}</context>")

    return f"<interview>\n{_join_lines(fields)}\n</interview>\n\n"


def format_current_question(state: InterviewState) -> str:
    """Format the current question with its research objective."""
    question = state.get_current_question()

    if not question:
        return "<current_question>None - Interview complete</current_question>\n\n"

    fields = []
    fields.append(f"\t<id>{question.id}</id>")
    fields.append(f"\t<order>{question.order} of {state.total_questions}</order>")
    fields.append(
        f"\t<question_text>{_escape_xml(question.base_question_text)}</question_text>"
    )
    fields.append(
        f"\t<research_objective>{_escape_xml(question.research_objective)}</research_objective>"
    )
    fields.append(f"\t<status>{question.status.value}</status>")
    fields.append(
        f"\t<objective_status>{question.objective_status.value}</objective_status>"
    )
    fields.append(f"\t<follow_up_count>{question.follow_up_count}</follow_up_count>")
    fields.append(f"\t<max_follow_ups>{question.max_follow_ups}</max_follow_ups>")

    return f"<current_question>\n{_join_lines(fields)}\n</current_question>\n\n"


def format_question_exchanges(state: InterviewState) -> str:
    """Format the exchange history for the current question."""
    question = state.get_current_question()

    if not question or not question.exchanges:
        return ""

    exchanges = []
    for i, exchange in enumerate(question.exchanges):
        exchange_fields = []
        exchange_fields.append(
            f"\t\t<asked>{_escape_xml(exchange.question_text)}</asked>"
        )

        if exchange.is_follow_up:
            exchange_fields.append("\t\t<type>follow_up</type>")
            if exchange.follow_up_reason:
                exchange_fields.append(
                    f"\t\t<follow_up_reason>{exchange.follow_up_reason.value}</follow_up_reason>"
                )
        else:
            exchange_fields.append("\t\t<type>initial</type>")

        if exchange.user_response:
            exchange_fields.append(
                f"\t\t<response>{_escape_xml(exchange.user_response)}</response>"
            )

            if exchange.response_analysis:
                analysis = exchange.response_analysis
                analysis_fields = []
                analysis_fields.append(
                    f"\t\t\t<objective_progress>{analysis.objective_progress.value}</objective_progress>"
                )
                analysis_fields.append(
                    f"\t\t\t<recommendation>{analysis.recommendation}</recommendation>"
                )
                if analysis.insights_extracted:
                    insights = [
                        f"\t\t\t\t<insight>{_escape_xml(ins)}</insight>"
                        for ins in analysis.insights_extracted
                    ]
                    analysis_fields.append(
                        f"\t\t\t<insights>\n{_join_lines(insights)}\n\t\t\t</insights>"
                    )
                exchange_fields.append(
                    f"\t\t<analysis>\n{_join_lines(analysis_fields)}\n\t\t</analysis>"
                )
        else:
            exchange_fields.append("\t\t<response>AWAITING</response>")

        exchanges.append(
            f'\t<exchange num="{i + 1}">\n{_join_lines(exchange_fields)}\n\t</exchange>'
        )

    return f"<question_exchanges>\n{_join_lines(exchanges)}\n</question_exchanges>\n\n"


def format_insight_summary(insight_bank: InsightBank, max_insights: int = 10) -> str:
    """Format a summary of accumulated insights."""
    if not insight_bank.insights:
        return ""

    # Get most recent insights, prioritizing high importance
    high_priority = [
        i for i in insight_bank.insights if i.importance in ("high", "critical")
    ]
    other = [
        i for i in insight_bank.insights if i.importance not in ("high", "critical")
    ]

    # Combine with high priority first, limit total
    selected = (high_priority + other)[:max_insights]

    if not selected:
        return ""

    insight_lines = []
    for insight in selected:
        importance_marker = "*" if insight.importance in ("high", "critical") else ""
        category = f" [{insight.category}]" if insight.category else ""
        insight_lines.append(
            f'\t<insight importance="{insight.importance}"{' category="' + insight.category + '"' if insight.category else ""}>{importance_marker}{_escape_xml(insight.content)}</insight>'
        )

    header = f"\t<total_insights>{len(insight_bank.insights)}</total_insights>"
    if len(insight_bank.insights) > max_insights:
        header += f"\n\t<showing>Most recent {max_insights} (prioritizing high importance)</showing>"

    return f"<accumulated_insights>\n{header}\n{_join_lines(insight_lines)}\n</accumulated_insights>\n\n"


def format_conversation_history(
    history: List[Dict[str, str]], max_entries: int = 10
) -> str:
    """Format recent conversation history with sliding window."""
    if not history:
        return ""

    # Apply sliding window
    recent = history[-max_entries:] if len(history) > max_entries else history

    messages = []
    for msg in recent:
        role = msg.get("role", "user")
        content = _escape_xml(msg.get("content", ""))
        messages.append(f'\t<message role="{role}">{content}</message>')

    window_note = ""
    if len(history) > max_entries:
        window_note = (
            f"\t<!-- Showing last {max_entries} of {len(history)} messages -->\n"
        )

    return f"<conversation_history>\n{window_note}{_join_lines(messages)}\n</conversation_history>\n\n"


def format_user_message(message: str) -> str:
    """Format the latest user message prominently."""
    return (
        f"<latest_user_message>\n\t{_escape_xml(message)}\n</latest_user_message>\n\n"
    )


def format_progress(state: InterviewState) -> str:
    """Format interview progress metrics."""
    fields = []
    fields.append(
        f"\t<completed_questions>{state.completed_questions}</completed_questions>"
    )
    fields.append(f"\t<total_questions>{state.total_questions}</total_questions>")
    fields.append(
        f"\t<progress_percent>{state.calculate_progress():.1f}%</progress_percent>"
    )
    fields.append(f"\t<total_exchanges>{state.total_exchanges}</total_exchanges>")

    return f"<progress>\n{_join_lines(fields)}\n</progress>\n\n"


def format_task_instruction(state: InterviewState, user_message: Optional[str]) -> str:
    """Format the task instruction based on current state."""
    if state.is_complete():
        return "<task>Generate interview completion message. Thank the participant and summarize key insights.</task>\n"

    question = state.get_current_question()

    if not user_message:
        # First turn or starting new question
        if question and question.exchanges:
            return "<task>Continue the interview. A follow-up was asked but no response yet.</task>\n"
        return (
            "<task>Begin the interview by asking the first question naturally.</task>\n"
        )

    # User responded - need to evaluate and decide
    return "<task>Evaluate the user's response against the research objective. Decide whether to ask a follow-up or transition to the next question. Generate your response.</task>\n"


# =============================================================================
# SPECIALIZED FORMATTERS - For Sub-Prompts
# =============================================================================


def format_response_analyzer_prompt(
    research_objective: str,
    question_asked: str,
    user_response: str,
    exchange_history: Optional[List[Exchange]] = None,
    follow_up_count: int = 0,
    max_follow_ups: int = 3,
) -> str:
    """
    Format context for the response analyzer sub-prompt.

    Used when running response analysis as a separate LLM call.
    """
    prompt = ""

    # Research objective (critical context)
    prompt += f"<research_objective>\n\t{_escape_xml(research_objective)}\n</research_objective>\n\n"

    # The question that was asked
    prompt += (
        f"<question_asked>\n\t{_escape_xml(question_asked)}\n</question_asked>\n\n"
    )

    # The user's response to analyze
    prompt += f"<user_response>\n\t{_escape_xml(user_response)}\n</user_response>\n\n"

    # Previous exchanges for context (if any)
    if exchange_history and len(exchange_history) > 1:
        prev_exchanges = []
        for i, ex in enumerate(exchange_history[:-1]):  # Exclude current
            ex_fields = []
            ex_fields.append(f"\t\t<asked>{_escape_xml(ex.question_text)}</asked>")
            if ex.user_response:
                ex_fields.append(
                    f"\t\t<response>{_escape_xml(ex.user_response)}</response>"
                )
            prev_exchanges.append(
                f'\t<exchange num="{i + 1}">\n{_join_lines(ex_fields)}\n\t</exchange>'
            )

        prompt += f"<previous_exchanges>\n{_join_lines(prev_exchanges)}\n</previous_exchanges>\n\n"

    # Follow-up constraints
    prompt += f"<constraints>\n\t<follow_up_count>{follow_up_count}</follow_up_count>\n\t<max_follow_ups>{max_follow_ups}</max_follow_ups>\n</constraints>\n\n"

    # Task
    prompt += "<task>Analyze this response against the research objective. Return a ResponseAnalysis JSON object.</task>\n"

    return prompt


def format_transition_generator_prompt(
    user_response: str,
    transition_reason: str,
    next_question: str,
    key_insight: Optional[str] = None,
) -> str:
    """
    Format context for the transition generator sub-prompt.

    Used when generating transitions as a separate LLM call.
    """
    prompt = ""

    # User's response we're transitioning from
    prompt += f"<user_response>\n\t{_escape_xml(user_response)}\n</user_response>\n\n"

    # Why we're transitioning
    prompt += f"<transition_reason>{transition_reason}</transition_reason>\n\n"

    # Key insight to reference (if available)
    if key_insight:
        prompt += f"<key_insight>\n\t{_escape_xml(key_insight)}\n</key_insight>\n\n"

    # The next question to ask
    prompt += f"<next_question>\n\t{_escape_xml(next_question)}\n</next_question>\n\n"

    # Task
    prompt += "<task>Generate a natural transition: validate their response, bridge to the next topic, then ask the next question.</task>\n"

    return prompt


def format_followup_generator_prompt(
    research_objective: str,
    user_response: str,
    follow_up_reason: str,
    objective_gaps: Optional[List[str]] = None,
    previous_follow_ups: Optional[List[str]] = None,
) -> str:
    """
    Format context for the follow-up generator sub-prompt.

    Used when generating follow-ups as a separate LLM call.
    """
    prompt = ""

    # Research objective
    prompt += f"<research_objective>\n\t{_escape_xml(research_objective)}\n</research_objective>\n\n"

    # User's response to follow up on
    prompt += f"<user_response>\n\t{_escape_xml(user_response)}\n</user_response>\n\n"

    # Why we need a follow-up
    prompt += f"<follow_up_reason>{follow_up_reason}</follow_up_reason>\n\n"

    # Specific gaps to address
    if objective_gaps:
        gaps = [f"\t<gap>{_escape_xml(gap)}</gap>" for gap in objective_gaps]
        prompt += f"<objective_gaps>\n{_join_lines(gaps)}\n</objective_gaps>\n\n"

    # Previous follow-ups to avoid repetition
    if previous_follow_ups:
        prev = [f"\t<previous>{_escape_xml(q)}</previous>" for q in previous_follow_ups]
        prompt += (
            f"<previous_follow_ups>\n{_join_lines(prev)}\n</previous_follow_ups>\n\n"
        )

    # Task
    prompt += "<task>Generate ONE targeted follow-up question that builds on their response and advances the research objective.</task>\n"

    return prompt


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def _escape_xml(text: str) -> str:
    """Escape XML special characters in text."""
    if not text:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _join_lines(lines: List[str]) -> str:
    """Join lines with newlines."""
    return "\n".join(lines)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def format_from_dict(
    state_dict: Dict[str, Any], user_message: Optional[str] = None
) -> str:
    """
    Format prompt from a state dictionary (e.g., loaded from JSON).

    Convenience function for when you have raw dict instead of Pydantic model.
    """
    state = InterviewState(**state_dict)
    return format_interviewer_prompt(state, user_message)


def format_minimal_context(
    question_text: str,
    research_objective: str,
    user_response: Optional[str] = None,
) -> str:
    """
    Format minimal context for simple use cases.

    Use when you don't need full state tracking.
    """
    prompt = f"<question>\n\t{_escape_xml(question_text)}\n</question>\n\n"
    prompt += f"<research_objective>\n\t{_escape_xml(research_objective)}\n</research_objective>\n\n"

    if user_response:
        prompt += (
            f"<user_response>\n\t{_escape_xml(user_response)}\n</user_response>\n\n"
        )
        prompt += (
            "<task>Evaluate the response and decide: follow-up or transition?</task>\n"
        )
    else:
        prompt += "<task>Ask this question naturally to begin the interview.</task>\n"

    return prompt


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example: Create a sample state and format it
    from agents.interview_agent.state_schema import (
        create_interview_state,
    )

    # Sample questions
    questions = [
        {
            "id": "q1",
            "order": 1,
            "base_question_text": "Can you walk me through your first experience using our product?",
            "research_objective": "Understand initial impressions and onboarding experience",
        },
        {
            "id": "q2",
            "order": 2,
            "base_question_text": "What features do you find most valuable?",
            "research_objective": "Identify high-value features and why they resonate",
        },
    ]

    # Create state
    state = create_interview_state(
        title="User Research Interview",
        context="Understanding how users experience our product",
        questions=questions,
    )

    # Format for first turn (no user message yet)
    prompt = format_interviewer_prompt(state)
    print("=== First Turn (No User Message) ===")
    print(prompt)
    print()

    # Simulate user response
    user_msg = (
        "I signed up last week. The signup was easy but the dashboard was overwhelming."
    )
    prompt_with_response = format_interviewer_prompt(state, user_message=user_msg)
    print("=== With User Response ===")
    print(prompt_with_response)
