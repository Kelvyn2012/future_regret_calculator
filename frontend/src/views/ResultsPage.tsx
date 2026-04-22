'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { useAppStore } from '../store/useAppStore'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { ScoreArc, RegretTypeBadge } from '../components/results/ScoreDisplay'
import { DriverCard } from '../components/results/DriverCard'
import { RegretChart } from '../components/results/RegretChart'

export function ResultsPage() {
  const router = useRouter()
  const { result, decisionText, reset } = useAppStore()

  useEffect(() => {
    if (!result) router.push('/')
  }, [result, router])

  if (!result) return null

  function handleStartOver() {
    reset()
    router.push('/')
  }

  function handleEditAnswers() {
    router.push('/assess')
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="border-b border-slate-100 bg-white sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-6 h-16 flex items-center justify-between">
          <button
            onClick={handleStartOver}
            className="text-sm font-semibold text-slate-500 hover:text-slate-800 flex items-center gap-1.5 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Future Regret Calculator
          </button>
          <div className="flex gap-2">
            <Button variant="ghost" size="sm" onClick={handleEditAnswers}>
              Edit answers
            </Button>
            <Button variant="secondary" size="sm" onClick={handleStartOver}>
              New assessment
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-10 space-y-6 pb-20">
        {/* Decision label */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">
            Your decision
          </p>
          <h1 className="text-xl font-semibold text-slate-800 leading-snug">
            "{decisionText}"
          </h1>
        </motion.div>

        {/* Score hero card */}
        <Card elevated className="p-8">
          <div className="flex flex-col sm:flex-row items-center gap-8">
            {/* Overall score */}
            <div className="flex flex-col items-center gap-3">
              <ScoreArc
                score={result.overall_score}
                size={180}
                strokeWidth={14}
              />
              <div className="text-center">
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  Overall Regret Risk
                </div>
              </div>
            </div>

            {/* Short + long term + regret type */}
            <div className="flex-1 space-y-4 w-full">
              <div className="grid grid-cols-2 gap-3">
                <div className="text-center p-4 rounded-xl bg-slate-50">
                  <div className="text-3xl font-extrabold text-slate-800 tabular-nums">
                    {result.short_term_regret}
                  </div>
                  <div className="text-xs text-slate-500 font-medium mt-1">Short-term</div>
                  <div className="text-xs text-slate-400">Next 6 months</div>
                </div>
                <div className="text-center p-4 rounded-xl bg-slate-50">
                  <div className="text-3xl font-extrabold text-slate-800 tabular-nums">
                    {result.long_term_regret}
                  </div>
                  <div className="text-xs text-slate-500 font-medium mt-1">Long-term</div>
                  <div className="text-xs text-slate-400">5+ years out</div>
                </div>
              </div>

              <RegretTypeBadge
                type={result.likely_regret_type}
                confidence={result.confidence_level}
              />
            </div>
          </div>
        </Card>

        {/* Regret dimensions chart */}
        <Card className="p-6">
          <RegretChart result={result} />
        </Card>

        {/* Top drivers */}
        {result.top_drivers.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 className="text-sm font-semibold text-slate-600 uppercase tracking-wider mb-4">
              What's driving this
            </h2>
            <div className="grid sm:grid-cols-2 gap-3">
              {result.top_drivers.map((driver, i) => (
                <DriverCard key={driver.factor} driver={driver} index={i} />
              ))}
            </div>
          </motion.div>
        )}

        {/* Narrative summary */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className="p-6">
            <h2 className="text-sm font-semibold text-slate-600 uppercase tracking-wider mb-4">
              What this may suggest
            </h2>
            <p className="text-slate-700 leading-relaxed text-sm">{result.narrative_summary}</p>
          </Card>
        </motion.div>

        {/* Future you message */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35 }}
        >
          <div className="relative rounded-2xl overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-violet-900 to-indigo-950" />
            <div
              className="absolute inset-0 opacity-10"
              style={{
                backgroundImage:
                  'radial-gradient(circle at 20% 50%, rgba(255,255,255,0.15) 0%, transparent 50%)',
              }}
            />
            <div className="relative px-8 py-8">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                  <span className="text-sm">✉️</span>
                </div>
                <span className="text-xs font-semibold text-white/60 uppercase tracking-widest">
                  A message from your future self
                </span>
              </div>
              <blockquote className="text-white/90 text-sm leading-relaxed italic font-light">
                "{result.future_you_message}"
              </blockquote>
            </div>
          </div>
        </motion.div>

        {/* Reflection questions */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card className="p-6">
            <h2 className="text-sm font-semibold text-slate-600 uppercase tracking-wider mb-4">
              Questions to reflect on
            </h2>
            <ul className="space-y-3">
              {result.reflection_questions.map((q, i) => (
                <motion.li
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.45 + i * 0.08 }}
                  className="flex gap-3 items-start"
                >
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-brand-400 flex-shrink-0" />
                  <span className="text-sm text-slate-700 leading-relaxed">{q}</span>
                </motion.li>
              ))}
            </ul>
          </Card>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="rounded-xl bg-slate-100 border border-slate-200 px-5 py-4"
        >
          <div className="flex gap-3">
            <span className="text-slate-400 flex-shrink-0 mt-0.5">ℹ️</span>
            <p className="text-xs text-slate-500 leading-relaxed">{result.disclaimer}</p>
          </div>
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.55 }}
          className="flex flex-col sm:flex-row gap-3"
        >
          <Button size="lg" onClick={handleEditAnswers} className="flex-1">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit my answers
          </Button>
          <Button size="lg" variant="secondary" onClick={handleStartOver} className="flex-1">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            New assessment
          </Button>
        </motion.div>
      </main>
    </div>
  )
}
