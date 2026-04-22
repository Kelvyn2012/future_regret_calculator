"""
Transparent heuristic scoring engine for the Future Regret Calculator.

Two primary scores are computed independently:
  - action_regret:   likelihood/severity of regretting the decision IF you act
  - inaction_regret: likelihood/severity of regretting the decision IF you do NOT act

These feed into:
  - short_term_regret: dominated by disruption of acting (near-term anxiety/doubt)
  - long_term_regret:  dominated by opportunity cost and values misalignment from not acting
  - overall_score:     combined risk metric
  - likely_regret_type, confidence_level, top_drivers
"""

from __future__ import annotations

from app.models import AnswerSet, CalculationResult, TopDriver
from app.scoring.constants import (
    ACTION_WEIGHTS,
    INACTION_WEIGHTS,
    MOTIVATION_ACTION_REGRET,
    HISTORICAL_PATTERN_ACTION,
    HISTORICAL_PATTERN_INACTION,
    REVERSIBILITY_SCORES,
    DISCLAIMER_TEXT,
)
from app.scoring.narrative import generate_narrative, generate_future_message, generate_reflections


def _n5(val: float) -> float:
    """Normalize a 1–5 value to [0, 1]."""
    return max(0.0, min(1.0, (val - 1.0) / 4.0))


def _n10(val: float) -> float:
    """Normalize a 1–10 value to [0, 1]."""
    return max(0.0, min(1.0, (val - 1.0) / 9.0))


def _clamp(val: float, lo: float = 0.0, hi: float = 100.0) -> int:
    return int(max(lo, min(hi, val)))


def _compute_action_regret(a: AnswerSet) -> float:
    """Return 0–100 representing regret risk from ACTING."""
    self_assessment = _n10(a.action_regret_short)
    unpreparedness = 1.0 - _n5(a.preparedness)
    motivation = MOTIVATION_ACTION_REGRET[a.motivation]
    social_pressure = _n5(a.social_influence)
    irreversibility = 1.0 - REVERSIBILITY_SCORES[a.reversibility]
    history = HISTORICAL_PATTERN_ACTION[a.historical_pattern]

    raw = (
        self_assessment * ACTION_WEIGHTS["self_assessment"]
        + unpreparedness * ACTION_WEIGHTS["preparedness"]
        + motivation * ACTION_WEIGHTS["motivation"]
        + social_pressure * ACTION_WEIGHTS["social_pressure"]
        + irreversibility * ACTION_WEIGHTS["reversibility"]
        + history * ACTION_WEIGHTS["historical_pattern"]
    )
    return raw * 100.0


def _compute_inaction_regret(a: AnswerSet) -> float:
    """Return 0–100 representing regret risk from NOT ACTING."""
    self_assessment = _n10(a.inaction_regret)
    values = _n5(a.values_alignment)
    growth = _n5(a.expected_growth)
    importance = _n10(a.importance)
    urgency = _n5(a.time_sensitivity)
    history = HISTORICAL_PATTERN_INACTION[a.historical_pattern]

    raw = (
        self_assessment * INACTION_WEIGHTS["self_assessment"]
        + values * INACTION_WEIGHTS["values_alignment"]
        + growth * INACTION_WEIGHTS["expected_growth"]
        + importance * INACTION_WEIGHTS["importance"]
        + urgency * INACTION_WEIGHTS["time_sensitivity"]
        + history * INACTION_WEIGHTS["historical_pattern"]
    )
    return raw * 100.0


def _compute_short_term(action: float, inaction: float, a: AnswerSet) -> int:
    """Short-term regret: primarily from disruption of acting + time-sensitive inaction."""
    urgency = _n5(a.time_sensitivity)
    low_support_stress = 1.0 - _n5(a.support_system)

    # Acting creates immediate disruption; missing a time-sensitive window also stings short-term
    score = (
        action * 0.60
        + inaction * 0.22 * urgency
        + low_support_stress * 18.0
    )
    return _clamp(score)


def _compute_long_term(action: float, inaction: float, a: AnswerSet) -> int:
    """Long-term regret: dominated by opportunity cost, values, growth."""
    values = _n5(a.values_alignment)
    growth = _n5(a.expected_growth)
    importance = _n10(a.importance)

    # Opportunity premium scales inaction regret upward for high-meaning decisions
    opp_premium = values * 0.35 + growth * 0.35 + importance * 0.30

    score = (
        inaction * (0.68 + 0.20 * opp_premium)
        + action * 0.22
    )
    return _clamp(score)


def _compute_overall(action: float, inaction: float, short: int, long: int) -> int:
    dominant = max(action, inaction)
    recessive = min(action, inaction)
    temporal_avg = (short + long) / 2.0
    overall = 0.48 * dominant + 0.22 * recessive + 0.30 * temporal_avg
    return _clamp(overall)


def _determine_regret_type(action: float, inaction: float, confidence: str) -> str:
    if confidence == "low":
        return "low_confidence"
    diff = inaction - action
    if abs(diff) < 10:
        return "mixed"
    return "inaction" if diff > 0 else "action"


def _compute_confidence(a: AnswerSet, action: float, inaction: float) -> str:
    social = _n5(a.social_influence)
    score_clarity = abs(action - inaction) / 100.0

    motivation_clarity_map = {
        "genuine_excitement": 0.90,
        "practical_necessity": 0.78,
        "fomo": 0.50,
        "escape": 0.40,
        "external_pressure": 0.28,
    }
    motivation_clarity = motivation_clarity_map[a.motivation]

    # High social pressure and low score separation both reduce confidence
    score = (1.0 - social) * 0.30 + score_clarity * 0.40 + motivation_clarity * 0.30
    if score >= 0.60:
        return "high"
    if score >= 0.35:
        return "medium"
    return "low"


def _compute_top_drivers(a: AnswerSet, action: float, inaction: float) -> list[TopDriver]:
    drivers: list[TopDriver] = []

    prep = _n5(a.preparedness)
    if prep < 0.45:
        drivers.append(TopDriver(
            factor="Low Preparedness",
            weight=_clamp((1.0 - prep) * 90),
            direction="increases_action_regret",
            explanation="Feeling underprepared is one of the strongest predictors of post-action regret. Strengthening your readiness may change this picture."
        ))

    values = _n5(a.values_alignment)
    if values > 0.60:
        drivers.append(TopDriver(
            factor="Strong Values Alignment",
            weight=_clamp(values * 92),
            direction="increases_inaction_regret",
            explanation="When a path aligns deeply with your values, the cost of not taking it tends to compound quietly over time."
        ))

    growth = _n5(a.expected_growth)
    if growth > 0.55:
        drivers.append(TopDriver(
            factor="High Growth Potential",
            weight=_clamp(growth * 88),
            direction="increases_inaction_regret",
            explanation="Decisions with significant growth potential tend to generate more long-term regret when avoided."
        ))

    reversibility = REVERSIBILITY_SCORES[a.reversibility]
    if reversibility < 0.40:
        drivers.append(TopDriver(
            factor="Low Reversibility",
            weight=_clamp((1.0 - reversibility) * 85),
            direction="increases_action_regret",
            explanation="Decisions that are difficult to undo carry higher stakes, which increases the cost of acting without full clarity."
        ))

    social = _n5(a.social_influence)
    if social > 0.60:
        drivers.append(TopDriver(
            factor="External Influence",
            weight=_clamp(social * 82),
            direction="increases_action_regret",
            explanation="Decisions made under heavy social pressure are more likely to feel inauthentic later, even when the outcome is positive."
        ))

    urgency = _n5(a.time_sensitivity)
    if urgency > 0.65:
        drivers.append(TopDriver(
            factor="Time Pressure",
            weight=_clamp(urgency * 80),
            direction="increases_inaction_regret",
            explanation="When an opportunity has a closing window, inaction carries a higher short-term price."
        ))

    motivation = a.motivation
    if motivation in ("external_pressure", "escape"):
        drivers.append(TopDriver(
            factor="Reactive Motivation",
            weight=70,
            direction="increases_action_regret",
            explanation="Acting primarily to escape a situation or satisfy others' expectations often leads to second-guessing the decision."
        ))
    elif motivation == "genuine_excitement":
        drivers.append(TopDriver(
            factor="Genuine Desire",
            weight=72,
            direction="decreases_regret",
            explanation="Acting from authentic excitement rather than fear or pressure significantly lowers regret risk in both directions."
        ))

    support = _n5(a.support_system)
    if support < 0.35:
        drivers.append(TopDriver(
            factor="Limited Support",
            weight=_clamp((1.0 - support) * 75),
            direction="increases_action_regret",
            explanation="Navigating major decisions without a strong support system amplifies short-term stress and can affect follow-through."
        ))

    # Sort by weight descending and return top 4
    drivers.sort(key=lambda d: d.weight, reverse=True)
    return drivers[:4]


def score_decision(input_data: "DecisionInput") -> CalculationResult:  # type: ignore[name-defined]
    """Entry point: compute a full CalculationResult from a DecisionInput."""
    from app.models import DecisionInput  # local import to avoid circular

    a = input_data.answers
    action = _compute_action_regret(a)
    inaction = _compute_inaction_regret(a)
    short = _compute_short_term(action, inaction, a)
    long_ = _compute_long_term(action, inaction, a)
    overall = _compute_overall(action, inaction, short, long_)
    confidence = _compute_confidence(a, action, inaction)
    regret_type = _determine_regret_type(action, inaction, confidence)
    drivers = _compute_top_drivers(a, action, inaction)

    narrative = generate_narrative(a, action, inaction, regret_type, overall, confidence)
    future_msg = generate_future_message(a, regret_type, overall)
    reflections = generate_reflections(a, regret_type)

    return CalculationResult(
        overall_score=overall,
        short_term_regret=short,
        long_term_regret=long_,
        action_regret_raw=_clamp(action),
        inaction_regret_raw=_clamp(inaction),
        likely_regret_type=regret_type,
        confidence_level=confidence,
        top_drivers=drivers,
        narrative_summary=narrative,
        future_you_message=future_msg,
        reflection_questions=reflections,
        disclaimer=DISCLAIMER_TEXT,
    )
