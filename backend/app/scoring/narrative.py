"""
Template-driven narrative generation.
Selects nuanced text based on score patterns, regret type, and key answer signals.
"""

from __future__ import annotations
from app.models import AnswerSet


def _n5(val: float) -> float:
    return max(0.0, min(1.0, (val - 1.0) / 4.0))


def _n10(val: float) -> float:
    return max(0.0, min(1.0, (val - 1.0) / 9.0))


def generate_narrative(
    a: AnswerSet,
    action: float,
    inaction: float,
    regret_type: str,
    overall: int,
    confidence: str,
) -> str:
    values_high = _n5(a.values_alignment) > 0.65
    growth_high = _n5(a.expected_growth) > 0.60
    prep_low = _n5(a.preparedness) < 0.45
    social_high = _n5(a.social_influence) > 0.60
    urgency_high = _n5(a.time_sensitivity) > 0.60
    motivation_genuine = a.motivation == "genuine_excitement"
    motivation_reactive = a.motivation in ("external_pressure", "escape")

    if confidence == "low":
        return (
            "Your answers contain enough variability that no single clear pattern emerges. "
            "This may mean the decision isn't fully formed yet, or that external noise is "
            "making it hard to hear your own thinking. That ambiguity is worth acknowledging — "
            "it's often a signal to slow down before committing. Before moving forward, "
            "consider separating what you genuinely want from what you feel expected to want."
        )

    if regret_type == "inaction":
        if overall >= 70:
            base = (
                "The pattern in your answers points toward a meaningful risk of long-term inaction regret. "
                "When a decision scores high on values alignment, growth potential, and self-assessed "
                "future regret, the cost of not acting tends to compound quietly over time. "
                "People in similar situations often describe the choice they didn't make as the one that "
                "stayed with them — not the one they tried and found difficult."
            )
            if prep_low:
                base += (
                    " That said, your preparedness score suggests some gaps worth closing. "
                    "The question may not be whether to act, but whether the conditions are right yet."
                )
            if social_high:
                base += (
                    " It's also worth noting that external pressure appears to be a factor. "
                    "Make sure this is genuinely your desire before proceeding."
                )
        else:
            base = (
                "Your answers lean toward inaction regret — the sense that not pursuing this "
                "path may feel more costly over time than trying it. This pattern is especially "
                "common when decisions involve real growth opportunities or meaningful values alignment. "
                "The hesitation you feel now is real, but it may not accurately predict how "
                "you'll feel looking back."
            )
            if urgency_high:
                base += " The time-sensitive nature of this opportunity adds weight to the inaction side."

    elif regret_type == "action":
        if overall >= 65:
            base = (
                "The pattern in your answers suggests meaningful caution is warranted before acting. "
                "Several factors — including your own short-term regret estimate and indicators around "
                "preparedness and motivation — point toward elevated action regret risk. "
                "This doesn't mean the decision is wrong, but it may suggest that the timing, "
                "conditions, or underlying reasons aren't quite fully formed yet."
            )
            if motivation_reactive:
                base += (
                    " Acting primarily to escape a current situation or meet others' expectations "
                    "is one of the most common sources of post-decision regret. "
                    "Clarity about what you're moving toward — not just away from — matters here."
                )
        else:
            base = (
                "Your answers lean slightly toward action regret, meaning acting may carry "
                "more near-term risk than not acting at this moment. "
                "This pattern is often seen when decisions feel externally pressured or when "
                "preparation isn't quite complete. It's not a verdict — it's an invitation to "
                "examine whether a small delay might shift the picture meaningfully."
            )

    elif regret_type == "mixed":
        base = (
            "You're in genuinely ambiguous territory, and that's worth sitting with. "
            "Your answers show real tension: meaningful upside to acting, meaningful risk in either direction. "
            "This kind of internal conflict often signals that the decision is genuinely significant — "
            "high stakes, personal, and worth taking seriously. "
            "The clearest path forward may not be a simple yes or no, "
            "but rather: under what conditions would I feel confident either way?"
        )
        if values_high and growth_high:
            base += (
                " What's notable is that both values alignment and growth potential score high, "
                "which typically favors action in the long run — even when the short term is uncertain."
            )
    else:
        base = (
            "Your answers don't produce a strong signal in either direction, which can itself be meaningful. "
            "Low-confidence results often reflect decisions that are still evolving, or situations where "
            "the available information isn't yet sufficient to form a clear picture. "
            "This isn't a failure of the process — it's useful data about where you are right now."
        )

    if motivation_genuine and regret_type != "action":
        base += (
            " One factor working in your favor: your motivation appears to be genuine desire "
            "rather than fear or external pressure. Decisions made from authentic intent tend "
            "to generate less regret regardless of outcome."
        )

    return base


def generate_future_message(a: AnswerSet, regret_type: str, overall: int) -> str:
    values_high = _n5(a.values_alignment) > 0.65
    growth_high = _n5(a.expected_growth) > 0.60
    prep_low = _n5(a.preparedness) < 0.45
    urgency_high = _n5(a.time_sensitivity) > 0.65

    if regret_type == "inaction":
        if overall >= 70:
            return (
                "The version of you who looks back on this moment years from now will likely "
                "care less about whether you succeeded, and more about whether you tried. "
                "The risk of acting is visible and feels real right now. "
                "The risk of not acting is quieter — but it has a way of becoming louder over time. "
                "You already know something important. Trust that."
            )
        return (
            "Your future self may look back on this crossroads with clarity you don't have right now. "
            "The discomfort of uncertainty often feels larger in the moment than it does in retrospect. "
            "Whatever you choose, choose it intentionally — not by default."
        )

    elif regret_type == "action":
        if prep_low:
            return (
                "The version of you who looks back will respect the caution you showed here. "
                "Rushing into something that doesn't feel quite ready rarely produces the outcome "
                "you're hoping for — and the short-term sting of waiting is almost always smaller "
                "than the long-term cost of acting before the conditions are right. "
                "Give yourself permission to slow down."
            )
        return (
            "Your future self may appreciate that you took the time to think this through carefully. "
            "There's real wisdom in recognizing when the moment isn't quite right. "
            "That clarity — about timing, readiness, and motivation — is worth something."
        )

    elif regret_type == "mixed":
        return (
            "The version of you looking back from five years out won't remember the uncertainty "
            "you feel right now — they'll remember what you did with it. "
            "You're not being asked to be certain. You're being asked to be intentional. "
            "The decision you'll regret least is the one you made with full honesty about "
            "what you want, what you fear, and what you're actually ready for."
        )

    return (
        "Whatever you decide, your future self will most appreciate that you paused to reflect "
        "rather than reacting. That kind of deliberate thinking is its own form of wisdom — "
        "and it tends to produce better decisions, regardless of which direction you choose."
    )


def generate_reflections(a: AnswerSet, regret_type: str) -> list[str]:
    questions = []
    values_high = _n5(a.values_alignment) > 0.60
    prep_low = _n5(a.preparedness) < 0.45
    social_high = _n5(a.social_influence) > 0.55
    motivation_reactive = a.motivation in ("external_pressure", "escape")
    urgency_high = _n5(a.time_sensitivity) > 0.60

    if regret_type == "inaction":
        questions.append(
            "If you imagine yourself five years from now, having not acted — what do you see?"
        )
        if values_high:
            questions.append(
                "How much of your identity and values is tied to this direction? "
                "What does it cost to keep them unexpressed?"
            )
        questions.append(
            "What would need to be true — about your readiness, circumstances, or clarity — "
            "for you to feel confident moving forward?"
        )

    elif regret_type == "action":
        questions.append(
            "If you strip away the external pressure and others' expectations, "
            "what does your own honest read of this decision say?"
        )
        if prep_low:
            questions.append(
                "What specific preparation gap, if closed, would meaningfully change "
                "how you feel about this decision?"
            )
        questions.append(
            "Is there a version of this path that's slower, smaller, or more reversible "
            "that still moves you in the direction you want?"
        )

    elif regret_type in ("mixed", "low_confidence"):
        questions.append(
            "What would you need to know or feel to have genuine clarity here — "
            "not just resolution, but actual confidence?"
        )
        questions.append(
            "Are you leaning toward action or inaction right now? "
            "And is that lean coming from wisdom or from discomfort?"
        )

    if social_high:
        questions.append(
            "If no one whose opinion matters to you would ever find out what you decided, "
            "what would you choose?"
        )

    if motivation_reactive:
        questions.append(
            "What are you actually moving toward — not just away from? "
            "Can you articulate it clearly?"
        )

    if urgency_high:
        questions.append(
            "Is the time pressure real and external, or partly self-imposed? "
            "Would waiting 30 days actually close the window — or does it just feel that way?"
        )

    # Always include at least one universal question and cap at 5
    if len(questions) < 3:
        questions.append(
            "In a year from now, what's the story you most want to be able to tell about this moment?"
        )

    return questions[:5]
