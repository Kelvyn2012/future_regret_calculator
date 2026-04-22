import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import { useAppStore } from '../store/useAppStore'
import { QUESTIONS, SEED_SCENARIOS } from '../data/questions'
import { calculateRegret } from '../api/client'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { ProgressBar } from '../components/ui/ProgressBar'
import { CategorySelector } from '../components/questionnaire/CategorySelector'
import { QuestionStep } from '../components/questionnaire/QuestionStep'
import type { AnswerSet, Category } from '../types'

// Steps: 0=decision_text, 1=category, 2–13=questions[0..11]
const TOTAL_QUESTION_STEPS = QUESTIONS.length
const TOTAL_STEPS = 2 + TOTAL_QUESTION_STEPS // text + category + 12 questions

export function QuestionnairePage() {
  const navigate = useNavigate()
  const store = useAppStore()
  const [step, setStep] = useState(0)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const progress = step === 0 ? 0 : step === 1 ? 1 : step - 1
  const progressTotal = TOTAL_STEPS - 2

  function getDefaultForQuestion(q: (typeof QUESTIONS)[0]): AnswerSet[keyof AnswerSet] {
    if (q.type === 'slider') return (q.default ?? q.min ?? 1) as AnswerSet[keyof AnswerSet]
    return (q.options?.[0]?.value ?? '') as AnswerSet[keyof AnswerSet]
  }

  function currentAnswer(q: (typeof QUESTIONS)[0]) {
    const v = store.answers[q.id]
    return v !== undefined ? v : getDefaultForQuestion(q)
  }

  function canAdvance(): boolean {
    if (step === 0) return store.decisionText.trim().length >= 5
    if (step === 1) return store.category !== null
    const qIndex = step - 2
    const q = QUESTIONS[qIndex]
    const val = store.answers[q.id]
    if (q.type === 'slider') {
      const v = val !== undefined ? (val as number) : (q.default as number)
      return v !== undefined
    }
    return val !== undefined
  }

  async function handleNext() {
    setError('')
    if (step < 2 + TOTAL_QUESTION_STEPS - 1) {
      // Ensure slider defaults are set when advancing past a slider question
      if (step >= 2) {
        const q = QUESTIONS[step - 2]
        if (store.answers[q.id] === undefined) {
          store.setAnswer(q.id, getDefaultForQuestion(q))
        }
      }
      setStep((s) => s + 1)
      return
    }

    // Final step: submit
    try {
      setLoading(true)
      const lastQ = QUESTIONS[TOTAL_QUESTION_STEPS - 1]
      if (store.answers[lastQ.id] === undefined) {
        store.setAnswer(lastQ.id, getDefaultForQuestion(lastQ))
      }

      // Fill any missing answers with defaults
      const fullAnswers: Record<string, AnswerSet[keyof AnswerSet]> = { ...store.answers }
      for (const q of QUESTIONS) {
        if (fullAnswers[q.id] === undefined) {
          fullAnswers[q.id] = getDefaultForQuestion(q)
        }
      }

      const result = await calculateRegret({
        decision_text: store.decisionText,
        category: store.category!,
        answers: fullAnswers as unknown as AnswerSet,
      })
      store.setResult(result)
      navigate('/results')
    } catch (e: any) {
      const msg = e?.response?.data?.detail ?? 'Something went wrong. Please try again.'
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg))
    } finally {
      setLoading(false)
    }
  }

  function handleBack() {
    if (step === 0) {
      navigate('/')
    } else {
      setStep((s) => s - 1)
    }
  }

  const isLastStep = step === 1 + TOTAL_QUESTION_STEPS

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="border-b border-slate-100 bg-white sticky top-0 z-10">
        <div className="max-w-2xl mx-auto px-6 h-16 flex items-center gap-4">
          <button
            onClick={() => navigate('/')}
            className="text-sm font-semibold text-slate-500 hover:text-slate-800 flex items-center gap-1.5 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Future Regret Calculator
          </button>
          {step >= 2 && (
            <div className="flex-1">
              <ProgressBar current={step - 1} total={TOTAL_QUESTION_STEPS} />
            </div>
          )}
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 flex items-center justify-center px-6 py-10">
        <div className="w-full max-w-2xl">
          <Card elevated className="p-8">
            <AnimatePresence mode="wait">
              {step === 0 && (
                <motion.div
                  key="decision"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <div>
                    <h2 className="text-xl font-semibold text-slate-800">
                      What decision are you thinking through?
                    </h2>
                    <p className="mt-2 text-sm text-slate-500">
                      Write it in plain language. Frame it as a question you're asking yourself.
                    </p>
                  </div>
                  <textarea
                    value={store.decisionText}
                    onChange={(e) => store.setDecisionText(e.target.value)}
                    placeholder="e.g. Should I quit my job to start my own business?"
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl border-2 border-slate-100 focus:border-brand-400 focus:outline-none text-slate-800 placeholder-slate-300 resize-none text-sm transition-colors"
                    autoFocus
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey && canAdvance()) {
                        e.preventDefault()
                        handleNext()
                      }
                    }}
                  />
                  <div>
                    <p className="text-xs text-slate-400 mb-2 font-medium">Or start with an example:</p>
                    <div className="flex flex-wrap gap-2">
                      {SEED_SCENARIOS.map((s) => (
                        <button
                          key={s}
                          type="button"
                          onClick={() => store.setDecisionText(s)}
                          className="text-xs px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-brand-100 hover:text-brand-700 text-slate-600 transition-colors"
                        >
                          {s.replace('Should I ', '').replace('?', '')}
                        </button>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}

              {step === 1 && (
                <motion.div
                  key="category"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                >
                  <CategorySelector
                    value={store.category}
                    onChange={(cat: Category) => store.setCategory(cat)}
                  />
                </motion.div>
              )}

              {step >= 2 && (
                <QuestionStep
                  key={`q-${step}`}
                  question={QUESTIONS[step - 2]}
                  value={currentAnswer(QUESTIONS[step - 2])}
                  onChange={(val) => store.setAnswer(QUESTIONS[step - 2].id, val)}
                />
              )}
            </AnimatePresence>

            {error && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 px-4 py-3 rounded-xl bg-rose-50 border border-rose-100 text-sm text-rose-600"
              >
                {error}
              </motion.div>
            )}

            <div className="mt-8 flex items-center justify-between gap-4">
              <Button variant="ghost" size="md" onClick={handleBack}>
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
                </svg>
                {step === 0 ? 'Home' : 'Back'}
              </Button>

              <Button
                size="md"
                onClick={handleNext}
                disabled={!canAdvance()}
                loading={loading}
              >
                {isLastStep ? (
                  <>
                    Calculate
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </>
                ) : (
                  <>
                    Continue
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </>
                )}
              </Button>
            </div>
          </Card>

          {/* Step indicator */}
          <div className="mt-6 flex justify-center gap-1.5">
            {Array.from({ length: TOTAL_STEPS }, (_, i) => (
              <div
                key={i}
                className={`rounded-full transition-all duration-300 ${
                  i === step
                    ? 'w-6 h-1.5 bg-brand-500'
                    : i < step
                    ? 'w-1.5 h-1.5 bg-brand-300'
                    : 'w-1.5 h-1.5 bg-slate-200'
                }`}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
