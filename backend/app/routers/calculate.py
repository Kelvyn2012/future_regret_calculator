from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.models import DecisionInput, CalculationResult
from app.scoring.engine import score_decision

router = APIRouter(tags=["calculate"])


@router.post("/calculate", response_model=CalculationResult)
def calculate(input_data: DecisionInput) -> CalculationResult:
    try:
        return score_decision(input_data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Scoring error: {str(exc)}") from exc


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
