from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.orm import Decision, Result
from app.models import CalculationResult, DecisionInput
from app.scoring.engine import score_decision

router = APIRouter(tags=["calculate"])


@router.post("/calculate", response_model=CalculationResult)
async def calculate(input_data: DecisionInput, db: AsyncSession = Depends(get_db)) -> CalculationResult:
    try:
        result = score_decision(input_data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Scoring error: {str(exc)}") from exc

    try:
        decision_row = Decision(
            decision_text=input_data.decision_text,
            category=input_data.category,
            **input_data.answers.model_dump(),
        )
        db.add(decision_row)
        await db.flush()  # get decision_row.id before inserting result

        result_row = Result(
            decision_id=decision_row.id,
            overall_score=result.overall_score,
            short_term_regret=result.short_term_regret,
            long_term_regret=result.long_term_regret,
            action_regret_raw=result.action_regret_raw,
            inaction_regret_raw=result.inaction_regret_raw,
            likely_regret_type=result.likely_regret_type,
            confidence_level=result.confidence_level,
            top_drivers=[d.model_dump() for d in result.top_drivers],
            narrative_summary=result.narrative_summary,
            future_you_message=result.future_you_message,
            reflection_questions=result.reflection_questions,
            disclaimer=result.disclaimer,
        )
        db.add(result_row)
        await db.commit()

        result.id = result_row.id
        result.decision_id = decision_row.id
    except Exception as exc:
        await db.rollback()
        # Don't fail the whole request if persistence fails — still return the result
        import logging
        logging.getLogger(__name__).error("DB persist failed: %s", exc)

    return result


@router.get("/questions")
def get_questions() -> dict:
    """Return question definitions so the frontend can optionally fetch them dynamically."""
    return {
        "questions": [
            {
                "id": "importance",
                "text": "How significant is this decision to your overall life path?",
                "description": "Consider how much it could change your trajectory.",
                "type": "slider",
                "min": 1, "max": 10,
                "minLabel": "Minor", "maxLabel": "Life-defining",
                "default": 5,
            },
            {
                "id": "reversibility",
                "text": "If this doesn't go as planned, how easily can you reverse course?",
                "description": "Think about practical, financial, and emotional costs of undoing it.",
                "type": "choice",
                "options": [
                    {"value": "very_easy", "label": "Very easily", "description": "Little lost if it doesn't work"},
                    {"value": "somewhat", "label": "With some effort", "description": "Possible but takes time/money"},
                    {"value": "difficult", "label": "Very difficult", "description": "Major disruption to unwind"},
                    {"value": "nearly_impossible", "label": "Nearly impossible", "description": "Effectively permanent"},
                ],
            },
            {
                "id": "time_sensitivity",
                "text": "How time-sensitive is this opportunity?",
                "description": "Would waiting significantly reduce or eliminate the option?",
                "type": "slider",
                "min": 1, "max": 5,
                "minLabel": "No urgency", "maxLabel": "Window closing fast",
                "default": 3,
            },
            {
                "id": "preparedness",
                "text": "How prepared are you — practically, financially, and emotionally?",
                "description": "Be honest: readiness is one of the strongest predictors of good outcomes.",
                "type": "slider",
                "min": 1, "max": 5,
                "minLabel": "Not ready", "maxLabel": "Fully prepared",
                "default": 3,
            },
            {
                "id": "values_alignment",
                "text": "How closely does this path align with your core values?",
                "description": "Would your future self recognize this as authentically you?",
                "type": "slider",
                "min": 1, "max": 5,
                "minLabel": "Misaligned", "maxLabel": "Deeply aligned",
                "default": 3,
            },
            {
                "id": "motivation",
                "text": "What best describes what's driving this decision right now?",
                "type": "choice",
                "options": [
                    {"value": "genuine_excitement", "label": "Genuine excitement", "description": "This feels right and I want it"},
                    {"value": "practical_necessity", "label": "Practical necessity", "description": "Circumstances make it the sensible choice"},
                    {"value": "fomo", "label": "Fear of missing out", "description": "Worried I'll regret not trying"},
                    {"value": "escape", "label": "Wanting to escape", "description": "Primarily motivated by leaving my current situation"},
                    {"value": "external_pressure", "label": "External pressure", "description": "Others expect or want me to do this"},
                ],
            },
            {
                "id": "inaction_regret",
                "text": "If you do NOT act, how likely are you to regret it 5+ years from now?",
                "description": "Imagine your future self looking back at this moment.",
                "type": "slider",
                "min": 1, "max": 10,
                "minLabel": "Very unlikely", "maxLabel": "Almost certain",
                "default": 5,
            },
            {
                "id": "action_regret_short",
                "text": "If you DO act, how likely are you to regret it within the first 6 months?",
                "description": "Think about adjustment period, doubt, and early consequences.",
                "type": "slider",
                "min": 1, "max": 10,
                "minLabel": "Very unlikely", "maxLabel": "Almost certain",
                "default": 5,
            },
            {
                "id": "historical_pattern",
                "text": "In past important decisions, you've most often regretted...",
                "type": "choice",
                "options": [
                    {"value": "too_fast", "label": "Acting too quickly", "description": "I've rushed into things I should have thought through"},
                    {"value": "too_slow", "label": "Waiting too long", "description": "I've hesitated past the right moment"},
                    {"value": "balanced", "label": "Roughly balanced", "description": "No strong pattern either way"},
                    {"value": "rarely", "label": "I rarely have major regrets", "description": "Decisions haven't often felt this significant"},
                ],
            },
            {
                "id": "support_system",
                "text": "How much support do you have — emotionally, financially, practically?",
                "description": "Who can you rely on if this gets hard?",
                "type": "slider",
                "min": 1, "max": 5,
                "minLabel": "On my own", "maxLabel": "Strong network",
                "default": 3,
            },
            {
                "id": "expected_growth",
                "text": "How much personal growth do you expect from taking this path?",
                "description": "Even if difficult, would this stretch and develop you meaningfully?",
                "type": "slider",
                "min": 1, "max": 5,
                "minLabel": "Little growth", "maxLabel": "Transformative",
                "default": 3,
            },
            {
                "id": "social_influence",
                "text": "How heavily is this decision being shaped by others' expectations?",
                "description": "Are you acting for yourself, or partly to satisfy someone else?",
                "type": "slider",
                "min": 1, "max": 5,
                "minLabel": "Entirely my own", "maxLabel": "Heavily influenced",
                "default": 2,
            },
        ]
    }
