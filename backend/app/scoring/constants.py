# Weights for action regret (probability/severity of regretting IF you act)
ACTION_WEIGHTS: dict[str, float] = {
    "self_assessment": 0.28,    # user's own estimate is most predictive
    "preparedness": 0.22,       # low prep is a strong predictor of post-action regret
    "motivation": 0.16,         # acting from pressure/fear vs. genuine intent
    "social_pressure": 0.12,    # external influence reduces authenticity of choice
    "reversibility": 0.11,      # harder to undo → higher stakes → more weight
    "historical_pattern": 0.11, # past pattern of regretting fast moves
}

# Weights for inaction regret (probability/severity of regretting IF you do NOT act)
INACTION_WEIGHTS: dict[str, float] = {
    "self_assessment": 0.30,    # user's own sense of future regret from not acting
    "values_alignment": 0.22,   # acting against values → long-term resentment
    "expected_growth": 0.16,    # growth opportunities compound; missing them compounds too
    "importance": 0.14,         # higher stakes = more weight to inaction regret
    "time_sensitivity": 0.10,   # closing window raises cost of inaction
    "historical_pattern": 0.08, # past pattern of regretting passivity
}

# Motivation type → action regret multiplier [0, 1]
MOTIVATION_ACTION_REGRET: dict[str, float] = {
    "genuine_excitement": 0.10,   # acting from real desire → lowest action regret risk
    "practical_necessity": 0.25,  # necessity-driven → still your choice, low regret
    "fomo": 0.52,                 # fear of missing out → often feels hollow later
    "escape": 0.65,               # fleeing current situation, not running toward something
    "external_pressure": 0.72,    # others pushing you → least authentic → highest regret risk
}

# Historical pattern → action regret tendency [0, 1]
HISTORICAL_PATTERN_ACTION: dict[str, float] = {
    "too_fast": 0.72,   # pattern of rushing → more action regret likely
    "balanced": 0.42,
    "rarely": 0.32,
    "too_slow": 0.20,   # pattern of over-deliberating → less action regret
}

# Historical pattern → inaction regret tendency [0, 1]
HISTORICAL_PATTERN_INACTION: dict[str, float] = {
    "too_slow": 0.76,   # pattern of waiting too long → more inaction regret likely
    "balanced": 0.44,
    "rarely": 0.50,     # no strong pattern → slight inaction lean (status quo bias)
    "too_fast": 0.20,   # pattern of acting quickly → less inaction regret
}

# Reversibility → numeric score [0, 1] (higher = more reversible)
REVERSIBILITY_SCORES: dict[str, float] = {
    "very_easy": 0.90,
    "somewhat": 0.62,
    "difficult": 0.30,
    "nearly_impossible": 0.08,
}

DISCLAIMER_TEXT = (
    "This tool is designed for personal reflection only. It does not predict the future, "
    "provide professional advice, or account for the full complexity of your situation. "
    "For decisions involving your health, finances, legal matters, or mental wellbeing, "
    "please consult a qualified professional. Your future is not determined by any score."
)
