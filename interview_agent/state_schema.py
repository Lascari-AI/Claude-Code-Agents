"""
Interview Agent State Schema

Follows the iterative loop pattern from the prompt-writing framework:
- Atomic state updates after each exchange
- Dual tracking: state.json (machine) + transcript.md (human-readable)
- Research objective-driven progression
- One question per turn with follow-up tracking
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

# =============================================================================
# ENUMS - Status and Reason Tracking
# =============================================================================


class InterviewStatus(str, Enum):
    """Overall interview status."""

    INITIALIZING = "initializing"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class QuestionStatus(str, Enum):
    """Status of an individual question."""

    PENDING = "pending"  # Not yet asked
    ACTIVE = "active"  # Currently being asked (awaiting response)
    FOLLOW_UP = "follow_up"  # In follow-up mode
    SATISFIED = "satisfied"  # Research objective met
    SKIPPED = "skipped"  # User chose to skip
    NULL_ANSWER = "null_answer"  # User couldn't answer


class ResearchObjectiveStatus(str, Enum):
    """How well the research objective was satisfied."""

    NOT_STARTED = "not_started"
    PARTIAL = "partial"  # Some insight gained, but incomplete
    SATISFIED = "satisfied"  # Fully answered
    EXCEEDED = "exceeded"  # Got more than expected


class FollowUpReason(str, Enum):
    """Why a follow-up was asked."""

    OBJECTIVE_NOT_SATISFIED = "objective_not_satisfied"
    RESPONSE_UNCLEAR = "response_unclear"
    PROBE_DEEPER = "probe_deeper"  # Interesting thread to explore
    CLARIFY_CONTRADICTION = "clarify_contradiction"
    USER_HESITATION = "user_hesitation"  # Possible safety skip


class TransitionReason(str, Enum):
    """Why we moved to the next question."""

    OBJECTIVE_SATISFIED = "objective_satisfied"
    NULL_ANSWER = "null_answer"
    USER_SKIP = "user_skip"
    MAX_FOLLOW_UPS = "max_follow_ups"  # Hit follow-up limit


# =============================================================================
# EXCHANGE TRACKING - Each Q&A interaction
# =============================================================================


class Exchange(BaseModel):
    """
    A single exchange: question/follow-up asked + user response.
    The atomic unit of interview progression.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)

    # What was asked
    question_text: str
    is_follow_up: bool = False
    follow_up_reason: Optional[FollowUpReason] = None

    # User's response
    user_response: Optional[str] = None
    response_timestamp: Optional[datetime] = None

    # Analysis of response (populated by LLM)
    response_analysis: Optional["ResponseAnalysis"] = None


class ResponseAnalysis(BaseModel):
    """
    LLM analysis of a user response.
    Populated after each response via <ultrathink> evaluation.
    """

    # Did this response satisfy the research objective?
    objective_progress: ResearchObjectiveStatus

    # Key insights extracted from this response
    insights_extracted: List[str] = Field(default_factory=list)

    # Should we follow up or transition?
    recommendation: str  # "follow_up" or "transition"
    recommendation_reason: str

    # Confidence in the analysis (0.0 - 1.0)
    confidence: float = 0.8


# =============================================================================
# QUESTION STATE - Full tracking for each question
# =============================================================================


class QuestionState(BaseModel):
    """
    Complete state for a single interview question.
    Tracks all exchanges, insights, and research objective progress.
    """

    # Identity
    id: str
    order: int

    # The question itself
    base_question_text: str
    research_objective: str

    # Status tracking
    status: QuestionStatus = QuestionStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Research objective tracking
    objective_status: ResearchObjectiveStatus = ResearchObjectiveStatus.NOT_STARTED

    # All exchanges for this question (initial + follow-ups)
    exchanges: List[Exchange] = Field(default_factory=list)

    # Transition tracking
    transition_reason: Optional[TransitionReason] = None
    transition_message: Optional[str] = None  # Validation statement

    # Aggregated insights from all exchanges
    cumulative_insights: List[str] = Field(default_factory=list)

    # Follow-up tracking
    follow_up_count: int = 0
    max_follow_ups: int = 3  # Configurable limit

    def add_exchange(
        self,
        question_text: str,
        is_follow_up: bool = False,
        follow_up_reason: Optional[FollowUpReason] = None,
    ) -> Exchange:
        """Add a new exchange (question asked, awaiting response)."""
        exchange = Exchange(
            question_text=question_text,
            is_follow_up=is_follow_up,
            follow_up_reason=follow_up_reason,
        )
        self.exchanges.append(exchange)
        if is_follow_up:
            self.follow_up_count += 1
        return exchange

    def record_response(self, response: str, analysis: ResponseAnalysis) -> None:
        """Record user response and analysis for current exchange."""
        if self.exchanges:
            current = self.exchanges[-1]
            current.user_response = response
            current.response_timestamp = datetime.now()
            current.response_analysis = analysis

            # Aggregate insights
            self.cumulative_insights.extend(analysis.insights_extracted)

            # Update objective status
            self.objective_status = analysis.objective_progress


# =============================================================================
# INSIGHT/MEMORY - Extracted learnings
# =============================================================================


class Insight(BaseModel):
    """
    A single insight extracted from the interview.
    More structured than raw memory, linked to source.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str

    # Source tracking
    source_question_id: str
    source_exchange_id: str
    extracted_at: datetime = Field(default_factory=datetime.now)

    # Classification
    category: Optional[str] = None  # e.g., "motivation", "pain_point", "preference"
    importance: str = "medium"  # "low", "medium", "high", "critical"

    # Connections to other insights
    related_insight_ids: List[str] = Field(default_factory=list)


class InsightBank(BaseModel):
    """
    Collection of all insights from the interview.
    Replaces/enhances the memory bank concept.
    """

    insights: List[Insight] = Field(default_factory=list)

    # Categorized views
    by_category: Dict[str, List[str]] = Field(
        default_factory=dict
    )  # category -> insight IDs
    by_question: Dict[str, List[str]] = Field(
        default_factory=dict
    )  # question_id -> insight IDs

    # Summary (updated periodically)
    summary: Optional[str] = None
    last_summary_at: Optional[datetime] = None

    def add_insight(
        self,
        content: str,
        source_question_id: str,
        source_exchange_id: str,
        category: Optional[str] = None,
        importance: str = "medium",
    ) -> Insight:
        """Add a new insight and update indexes."""
        insight = Insight(
            content=content,
            source_question_id=source_question_id,
            source_exchange_id=source_exchange_id,
            category=category,
            importance=importance,
        )
        self.insights.append(insight)

        # Update indexes
        if category:
            if category not in self.by_category:
                self.by_category[category] = []
            self.by_category[category].append(insight.id)

        if source_question_id not in self.by_question:
            self.by_question[source_question_id] = []
        self.by_question[source_question_id].append(insight.id)

        return insight

    def get_high_importance(self) -> List[Insight]:
        """Get all high/critical importance insights."""
        return [i for i in self.insights if i.importance in ("high", "critical")]


# =============================================================================
# INTERVIEW STATE - Top-level state container
# =============================================================================


class InterviewConfig(BaseModel):
    """Configuration for the interview session."""

    max_follow_ups_per_question: int = 3
    max_total_exchanges: int = 50  # Safety limit
    auto_save_after_each_exchange: bool = True

    # LLM settings
    analysis_model: str = "gpt-4o"
    transition_model: str = "gemini-2.0-flash"

    # Behavior settings
    allow_user_skip: bool = True
    require_confirmation_on_complete: bool = True


class InterviewState(BaseModel):
    """
    Top-level interview state.

    This is the primary state file (state.json) that gets atomically
    updated after each exchange. Follows the iterative loop pattern.
    """

    # Session identity
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Interview metadata
    title: str
    context: str  # Background context for the interview

    # Status tracking
    status: InterviewStatus = InterviewStatus.INITIALIZING

    # Configuration
    config: InterviewConfig = Field(default_factory=InterviewConfig)

    # Question management
    questions: List[QuestionState] = Field(default_factory=list)
    current_question_index: int = 0

    # Insights/learnings accumulated
    insight_bank: InsightBank = Field(default_factory=InsightBank)

    # Progress metrics
    total_questions: int = 0
    completed_questions: int = 0
    total_exchanges: int = 0

    # Conversation history (for context in prompts)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)

    # Termination tracking
    termination_reason: Optional[str] = None
    completed_at: Optional[datetime] = None

    # ==========================================================================
    # State Machine Methods
    # ==========================================================================

    def get_current_question(self) -> Optional[QuestionState]:
        """Get the current active question."""
        if 0 <= self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def advance_to_next_question(self) -> Optional[QuestionState]:
        """Move to the next question. Returns None if interview complete."""
        self.current_question_index += 1
        self.completed_questions += 1

        if self.current_question_index >= len(self.questions):
            return None
        return self.get_current_question()

    def record_exchange(self, role: str, content: str) -> None:
        """Add to conversation history for context."""
        self.conversation_history.append(
            {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
        )
        self.total_exchanges += 1
        self.updated_at = datetime.now()

    def is_complete(self) -> bool:
        """Check if interview is finished."""
        return self.current_question_index >= len(self.questions) or self.status in (
            InterviewStatus.COMPLETED,
            InterviewStatus.FAILED,
        )

    def calculate_progress(self) -> float:
        """Calculate completion percentage."""
        if self.total_questions == 0:
            return 0.0
        return (self.completed_questions / self.total_questions) * 100

    # ==========================================================================
    # Atomic Update Method
    # ==========================================================================

    def atomic_update(self) -> None:
        """
        Mark state as updated. Call this after EVERY exchange.
        The actual file write happens in the storage layer.
        """
        self.updated_at = datetime.now()


# =============================================================================
# FACTORY FUNCTION - Create state from interview doc
# =============================================================================


def create_interview_state(
    title: str,
    context: str,
    questions: List[Dict[str, Any]],
    config: Optional[InterviewConfig] = None,
) -> InterviewState:
    """
    Factory function to create a new InterviewState from input questions.

    Args:
        title: Interview title
        context: Background context for the interview
        questions: List of question dicts with 'id', 'base_question_text',
                   'research_objective', 'order'
        config: Optional configuration overrides

    Returns:
        Initialized InterviewState ready for the interview loop
    """
    question_states = [
        QuestionState(
            id=q["id"],
            order=q["order"],
            base_question_text=q["base_question_text"],
            research_objective=q["research_objective"],
            max_follow_ups=config.max_follow_ups_per_question if config else 3,
        )
        for q in sorted(questions, key=lambda x: x["order"])
    ]

    return InterviewState(
        title=title,
        context=context,
        questions=question_states,
        total_questions=len(question_states),
        config=config or InterviewConfig(),
        status=InterviewStatus.INITIALIZING,
    )


# Update forward references
Exchange.model_rebuild()
QuestionState.model_rebuild()
