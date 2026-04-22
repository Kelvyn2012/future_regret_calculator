"""SQLAlchemy ORM models — separate from Pydantic models in app/models.py."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Decision(Base):
    """Stores the raw user input for each assessment."""

    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    decision_text: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)

    # Answer columns — mirrors AnswerSet exactly
    importance: Mapped[int] = mapped_column(Integer, nullable=False)
    reversibility: Mapped[str] = mapped_column(String(30), nullable=False)
    time_sensitivity: Mapped[int] = mapped_column(Integer, nullable=False)
    preparedness: Mapped[int] = mapped_column(Integer, nullable=False)
    values_alignment: Mapped[int] = mapped_column(Integer, nullable=False)
    motivation: Mapped[str] = mapped_column(String(30), nullable=False)
    inaction_regret: Mapped[int] = mapped_column(Integer, nullable=False)
    action_regret_short: Mapped[int] = mapped_column(Integer, nullable=False)
    historical_pattern: Mapped[str] = mapped_column(String(20), nullable=False)
    support_system: Mapped[int] = mapped_column(Integer, nullable=False)
    expected_growth: Mapped[int] = mapped_column(Integer, nullable=False)
    social_influence: Mapped[int] = mapped_column(Integer, nullable=False)

    result: Mapped["Result"] = relationship("Result", back_populates="decision", uselist=False, cascade="all, delete-orphan")


class Result(Base):
    """Stores the computed scoring output for each assessment."""

    __tablename__ = "results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    short_term_regret: Mapped[int] = mapped_column(Integer, nullable=False)
    long_term_regret: Mapped[int] = mapped_column(Integer, nullable=False)
    action_regret_raw: Mapped[int] = mapped_column(Integer, nullable=False)
    inaction_regret_raw: Mapped[int] = mapped_column(Integer, nullable=False)
    likely_regret_type: Mapped[str] = mapped_column(String(20), nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(10), nullable=False)
    top_drivers: Mapped[list] = mapped_column(JSONB, nullable=False)
    narrative_summary: Mapped[str] = mapped_column(Text, nullable=False)
    future_you_message: Mapped[str] = mapped_column(Text, nullable=False)
    reflection_questions: Mapped[list] = mapped_column(JSONB, nullable=False)
    disclaimer: Mapped[str] = mapped_column(Text, nullable=False)

    decision: Mapped["Decision"] = relationship("Decision", back_populates="result")
