export type Category =
  | 'career'
  | 'relationship'
  | 'education'
  | 'financial'
  | 'lifestyle'
  | 'health'
  | 'other'

export type Reversibility = 'very_easy' | 'somewhat' | 'difficult' | 'nearly_impossible'
export type Motivation =
  | 'genuine_excitement'
  | 'fomo'
  | 'external_pressure'
  | 'practical_necessity'
  | 'escape'
export type HistoricalPattern = 'too_fast' | 'too_slow' | 'balanced' | 'rarely'
export type RegretType = 'action' | 'inaction' | 'mixed' | 'low_confidence'
export type ConfidenceLevel = 'low' | 'medium' | 'high'
export type DriverDirection =
  | 'increases_action_regret'
  | 'increases_inaction_regret'
  | 'decreases_regret'

export interface AnswerSet {
  importance: number
  reversibility: Reversibility
  time_sensitivity: number
  preparedness: number
  values_alignment: number
  motivation: Motivation
  inaction_regret: number
  action_regret_short: number
  historical_pattern: HistoricalPattern
  support_system: number
  expected_growth: number
  social_influence: number
}

export interface DecisionInput {
  decision_text: string
  category: Category
  answers: AnswerSet
}

export interface TopDriver {
  factor: string
  weight: number
  direction: DriverDirection
  explanation: string
}

export interface CalculationResult {
  overall_score: number
  short_term_regret: number
  long_term_regret: number
  action_regret_raw: number
  inaction_regret_raw: number
  likely_regret_type: RegretType
  confidence_level: ConfidenceLevel
  top_drivers: TopDriver[]
  narrative_summary: string
  future_you_message: string
  reflection_questions: string[]
  disclaimer: string
}

export interface QuestionOption {
  value: string
  label: string
  description?: string
}

export interface Question {
  id: keyof AnswerSet
  text: string
  description?: string
  type: 'slider' | 'choice'
  options?: QuestionOption[]
  min?: number
  max?: number
  minLabel?: string
  maxLabel?: string
  default?: number | string
}
