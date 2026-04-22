from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.orm import Decision, Result
from app.models import AssessmentSummary, CalculationResult, TopDriver

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.get("", response_model=list[AssessmentSummary])
async def list_assessments(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[AssessmentSummary]:
    """Return recent assessments ordered newest-first."""
    stmt = (
        select(Result, Decision)
        .join(Decision, Result.decision_id == Decision.id)
        .order_by(Result.created_at.desc())
        .limit(min(limit, 100))
        .offset(offset)
    )
    rows = await db.execute(stmt)
    out = []
    for result_row, decision_row in rows.all():
        out.append(
            AssessmentSummary(
                id=result_row.id,
                decision_id=decision_row.id,
                created_at=result_row.created_at.isoformat(),
                decision_text=decision_row.decision_text,
                category=decision_row.category,
                overall_score=result_row.overall_score,
                likely_regret_type=result_row.likely_regret_type,
                confidence_level=result_row.confidence_level,
            )
        )
    return out


@router.get("/{result_id}", response_model=CalculationResult)
async def get_assessment(result_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> CalculationResult:
    """Retrieve a previously computed assessment by result ID."""
    stmt = (
        select(Result, Decision)
        .join(Decision, Result.decision_id == Decision.id)
        .where(Result.id == result_id)
    )
    row = await db.execute(stmt)
    pair = row.first()
    if pair is None:
        raise HTTPException(status_code=404, detail="Assessment not found")

    result_row, decision_row = pair
    drivers = [TopDriver(**d) for d in result_row.top_drivers]

    return CalculationResult(
        id=result_row.id,
        decision_id=decision_row.id,
        overall_score=result_row.overall_score,
        short_term_regret=result_row.short_term_regret,
        long_term_regret=result_row.long_term_regret,
        action_regret_raw=result_row.action_regret_raw,
        inaction_regret_raw=result_row.inaction_regret_raw,
        likely_regret_type=result_row.likely_regret_type,
        confidence_level=result_row.confidence_level,
        top_drivers=drivers,
        narrative_summary=result_row.narrative_summary,
        future_you_message=result_row.future_you_message,
        reflection_questions=result_row.reflection_questions,
        disclaimer=result_row.disclaimer,
    )
