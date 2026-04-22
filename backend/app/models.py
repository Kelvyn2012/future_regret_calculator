import uuid
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Annotated

CATEGORIES = Literal[
    "career", "relationship", "education", "financial", "lifestyle", "health", "other"
]

REVERSIBILITY_OPTIONS = Literal["very_easy", "somewhat", "difficult", "nearly_impossible"]

MOTIVATION_OPTIONS = Literal[
    "genuine_excitement", "fomo", "external_pressure", "practical_necessity", "escape"
]

HISTORICAL_PATTERN_OPTIONS = Literal["too_fast", "too_slow", "balanced", "rarely"]

REGRET_TYPES = Literal["action", "inaction", "mixed", "low_confidence"]
CONFIDENCE_LEVELS = Literal["low", "medium", "high"]
DRIVER_DIRECTIONS = Literal["increases_action_regret", "increases_inaction_regret", "decreases_regret"]


class AnswerSet(BaseModel):
    importance: Annotated[int, Field(ge=1, le=10)]
    reversibility: REVERSIBILITY_OPTIONS
    time_sensitivity: Annotated[int, Field(ge=1, le=5)]
    preparedness: Annotated[int, Field(ge=1, le=5)]
    values_alignment: Annotated[int, Field(ge=1, le=5)]
    motivation: MOTIVATION_OPTIONS
    inaction_regret: Annotated[int, Field(ge=1, le=10)]
    action_regret_short: Annotated[int, Field(ge=1, le=10)]
    historical_pattern: HISTORICAL_PATTERN_OPTIONS
    support_system: Annotated[int, Field(ge=1, le=5)]
    expected_growth: Annotated[int, Field(ge=1, le=5)]
    social_influence: Annotated[int, Field(ge=1, le=5)]


class DecisionInput(BaseModel):
    decision_text: str = Field(min_length=5, max_length=500)
    category: CATEGORIES
    answers: AnswerSet

    @field_validator("decision_text")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()


class TopDriver(BaseModel):
    factor: str
    weight: int = Field(ge=0, le=100)
    direction: DRIVER_DIRECTIONS
    explanation: str


class CalculationResult(BaseModel):
    id: uuid.UUID | None = None          # result row id (set after DB persist)
    decision_id: uuid.UUID | None = None  # decision row id
    overall_score: int = Field(ge=0, le=100)
    short_term_regret: int = Field(ge=0, le=100)
    long_term_regret: int = Field(ge=0, le=100)
    action_regret_raw: int = Field(ge=0, le=100)
    inaction_regret_raw: int = Field(ge=0, le=100)
    likely_regret_type: REGRET_TYPES
    confidence_level: CONFIDENCE_LEVELS
    top_drivers: list[TopDriver]
    narrative_summary: str
    future_you_message: str
    reflection_questions: list[str]
    disclaimer: str


class AssessmentSummary(BaseModel):
    """Lightweight row returned by the history endpoint."""

    id: uuid.UUID
    decision_id: uuid.UUID
    created_at: str
    decision_text: str
    category: str
    overall_score: int
    likely_regret_type: REGRET_TYPES
    confidence_level: CONFIDENCE_LEVELS

    model_config = {"from_attributes": True}
