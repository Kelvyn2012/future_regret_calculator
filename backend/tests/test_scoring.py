"""
Tests for the scoring engine.
Covers: score bounds, output structure, behavioral logic, and seed scenarios.
"""

import pytest
from app.models import AnswerSet, DecisionInput
from app.scoring.engine import (
    score_decision,
    _compute_action_regret,
    _compute_inaction_regret,
    _compute_short_term,
    _compute_long_term,
    _compute_overall,
    _compute_confidence,
    _compute_top_drivers,
    _determine_regret_type,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_answers(**overrides) -> AnswerSet:
    base = dict(
        importance=6,
        reversibility="somewhat",
        time_sensitivity=3,
        preparedness=3,
        values_alignment=3,
        motivation="genuine_excitement",
        inaction_regret=6,
        action_regret_short=4,
        historical_pattern="balanced",
        support_system=3,
        expected_growth=3,
        social_influence=2,
    )
    base.update(overrides)
    return AnswerSet(**base)


def make_input(decision_text="Should I make a change?", category="career", **answer_overrides) -> DecisionInput:
    return DecisionInput(
        decision_text=decision_text,
        category=category,
        answers=make_answers(**answer_overrides),
    )


# ---------------------------------------------------------------------------
# Score bounds
# ---------------------------------------------------------------------------

class TestScoreBounds:
    def test_overall_score_in_range(self):
        result = score_decision(make_input())
        assert 0 <= result.overall_score <= 100

    def test_short_term_in_range(self):
        result = score_decision(make_input())
        assert 0 <= result.short_term_regret <= 100

    def test_long_term_in_range(self):
        result = score_decision(make_input())
        assert 0 <= result.long_term_regret <= 100

    def test_action_raw_in_range(self):
        result = score_decision(make_input())
        assert 0 <= result.action_regret_raw <= 100

    def test_inaction_raw_in_range(self):
        result = score_decision(make_input())
        assert 0 <= result.inaction_regret_raw <= 100

    def test_extreme_high_scores_capped(self):
        inp = make_input(
            importance=10, preparedness=1, values_alignment=5, expected_growth=5,
            inaction_regret=10, action_regret_short=10, social_influence=5,
            motivation="external_pressure", time_sensitivity=5,
        )
        result = score_decision(inp)
        assert result.overall_score <= 100
        assert result.short_term_regret <= 100
        assert result.long_term_regret <= 100

    def test_extreme_low_scores_floored(self):
        inp = make_input(
            importance=1, preparedness=5, values_alignment=1, expected_growth=1,
            inaction_regret=1, action_regret_short=1, social_influence=1,
            motivation="genuine_excitement", time_sensitivity=1,
        )
        result = score_decision(inp)
        assert result.overall_score >= 0
        assert result.short_term_regret >= 0
        assert result.long_term_regret >= 0


# ---------------------------------------------------------------------------
# Output structure
# ---------------------------------------------------------------------------

class TestOutputStructure:
    def test_required_fields_present(self):
        result = score_decision(make_input())
        assert result.likely_regret_type in ("action", "inaction", "mixed", "low_confidence")
        assert result.confidence_level in ("low", "medium", "high")
        assert isinstance(result.top_drivers, list)
        assert isinstance(result.narrative_summary, str) and len(result.narrative_summary) > 20
        assert isinstance(result.future_you_message, str) and len(result.future_you_message) > 20
        assert isinstance(result.reflection_questions, list)
        assert 3 <= len(result.reflection_questions) <= 5
        assert isinstance(result.disclaimer, str) and len(result.disclaimer) > 20

    def test_top_drivers_structure(self):
        result = score_decision(make_input())
        for driver in result.top_drivers:
            assert hasattr(driver, "factor")
            assert hasattr(driver, "weight")
            assert hasattr(driver, "direction")
            assert hasattr(driver, "explanation")
            assert 0 <= driver.weight <= 100
            assert driver.direction in (
                "increases_action_regret",
                "increases_inaction_regret",
                "decreases_regret",
            )

    def test_at_most_four_drivers(self):
        result = score_decision(make_input())
        assert len(result.top_drivers) <= 4


# ---------------------------------------------------------------------------
# Behavioral logic
# ---------------------------------------------------------------------------

class TestBehavioralLogic:
    def test_high_values_alignment_increases_inaction_regret(self):
        low_values = _compute_inaction_regret(make_answers(values_alignment=1))
        high_values = _compute_inaction_regret(make_answers(values_alignment=5))
        assert high_values > low_values

    def test_low_preparedness_increases_action_regret(self):
        high_prep = _compute_action_regret(make_answers(preparedness=5))
        low_prep = _compute_action_regret(make_answers(preparedness=1))
        assert low_prep > high_prep

    def test_external_pressure_increases_action_regret(self):
        genuine = _compute_action_regret(make_answers(motivation="genuine_excitement"))
        pressure = _compute_action_regret(make_answers(motivation="external_pressure"))
        assert pressure > genuine

    def test_high_reversibility_reduces_action_regret(self):
        easy = _compute_action_regret(make_answers(reversibility="very_easy"))
        hard = _compute_action_regret(make_answers(reversibility="nearly_impossible"))
        assert easy < hard

    def test_high_time_pressure_increases_inaction_regret(self):
        low_urgency = _compute_inaction_regret(make_answers(time_sensitivity=1))
        high_urgency = _compute_inaction_regret(make_answers(time_sensitivity=5))
        assert high_urgency > low_urgency

    def test_high_social_influence_reduces_confidence(self):
        low_social = _compute_confidence(make_answers(social_influence=1), 60, 30)
        high_social = _compute_confidence(make_answers(social_influence=5), 60, 30)
        confidence_order = {"high": 2, "medium": 1, "low": 0}
        assert confidence_order[high_social] <= confidence_order[low_social]

    def test_regret_type_inaction_when_inaction_dominates(self):
        a = make_answers(
            inaction_regret=10, values_alignment=5, expected_growth=5,
            action_regret_short=2, preparedness=4, social_influence=1,
        )
        action = _compute_action_regret(a)
        inaction = _compute_inaction_regret(a)
        assert inaction > action + 10
        rtype = _determine_regret_type(action, inaction, "high")
        assert rtype == "inaction"

    def test_regret_type_action_when_action_dominates(self):
        a = make_answers(
            action_regret_short=10, preparedness=1, motivation="external_pressure",
            social_influence=5, reversibility="nearly_impossible",
            inaction_regret=2, values_alignment=1, expected_growth=1,
        )
        action = _compute_action_regret(a)
        inaction = _compute_inaction_regret(a)
        assert action > inaction + 10
        rtype = _determine_regret_type(action, inaction, "medium")
        assert rtype == "action"

    def test_mixed_when_scores_close(self):
        rtype = _determine_regret_type(50.0, 57.0, "high")
        assert rtype == "mixed"

    def test_low_confidence_when_high_social_pressure(self):
        a = make_answers(social_influence=5, motivation="external_pressure")
        result = score_decision(DecisionInput(
            decision_text="Unsure what to do",
            category="other",
            answers=a,
        ))
        assert result.confidence_level in ("low", "medium")


# ---------------------------------------------------------------------------
# Seed scenarios
# ---------------------------------------------------------------------------

class TestSeedScenarios:
    def _run(self, decision, category, **overrides) -> object:
        return score_decision(make_input(decision, category, **overrides))

    def test_quit_job_for_business_inaction_dominant(self):
        """High-stakes career move with strong values/growth → inaction regret likely."""
        result = self._run(
            "Should I quit my stable job to start my own business?",
            "career",
            importance=9,
            reversibility="difficult",
            time_sensitivity=4,
            preparedness=3,
            values_alignment=5,
            motivation="genuine_excitement",
            inaction_regret=8,
            action_regret_short=5,
            historical_pattern="too_slow",
            expected_growth=5,
            social_influence=2,
        )
        assert result.likely_regret_type in ("inaction", "mixed")
        assert result.long_term_regret >= result.short_term_regret

    def test_move_city_for_opportunity(self):
        """Relocation opportunity — moderate scores across the board."""
        result = self._run(
            "Should I move to another city for a new opportunity?",
            "lifestyle",
            importance=7,
            reversibility="somewhat",
            time_sensitivity=4,
            preparedness=3,
            values_alignment=4,
            motivation="genuine_excitement",
            inaction_regret=7,
            action_regret_short=4,
            historical_pattern="balanced",
            expected_growth=4,
            social_influence=2,
        )
        assert 0 <= result.overall_score <= 100

    def test_return_to_school(self):
        """Education decision under time sensitivity."""
        result = self._run(
            "Should I go back to school this year?",
            "education",
            importance=8,
            reversibility="difficult",
            time_sensitivity=3,
            preparedness=2,
            values_alignment=4,
            motivation="genuine_excitement",
            inaction_regret=7,
            action_regret_short=5,
            historical_pattern="too_slow",
            expected_growth=5,
            social_influence=3,
        )
        assert result.overall_score >= 40

    def test_end_relationship_external_pressure_high_action_regret(self):
        """Relationship ending under external pressure → action regret more likely."""
        result = self._run(
            "Should I end a relationship that no longer feels right?",
            "relationship",
            importance=9,
            reversibility="difficult",
            time_sensitivity=2,
            preparedness=3,
            values_alignment=2,
            motivation="external_pressure",
            inaction_regret=4,
            action_regret_short=8,
            historical_pattern="too_fast",
            expected_growth=2,
            social_influence=5,
        )
        assert result.likely_regret_type in ("action", "low_confidence")

    def test_impulsive_purchase_action_regret(self):
        """Low reversibility impulsive action → action regret."""
        result = self._run(
            "Should I buy a new car I can barely afford?",
            "financial",
            importance=4,
            reversibility="difficult",
            time_sensitivity=2,
            preparedness=1,
            values_alignment=2,
            motivation="fomo",
            inaction_regret=3,
            action_regret_short=8,
            historical_pattern="too_fast",
            expected_growth=1,
            social_influence=4,
        )
        assert result.action_regret_raw > result.inaction_regret_raw
