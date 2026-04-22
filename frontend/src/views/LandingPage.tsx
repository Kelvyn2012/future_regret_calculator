'use client'

import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Button } from '../components/ui/Button'
import { SEED_SCENARIOS } from '../data/questions'
import { useAppStore } from '../store/useAppStore'

const STEPS = [
  {
    num: '01',
    title: 'Describe your decision',
    desc: 'Write it in plain language. No need to frame it perfectly.',
  },
  {
    num: '02',
    title: 'Answer 12 structured questions',
    desc: 'Sliders and choices designed around behavioral research on regret.',
  },
  {
    num: '03',
    title: 'Get a clear, honest reflection',
    desc: 'Scores, insights, top drivers, and a message from your future self.',
  },
]

export function LandingPage() {
  const router = useRouter()
  const setDecisionText = useAppStore((s) => s.setDecisionText)

  function startWithScenario(scenario: string) {
    setDecisionText(scenario)
    router.push('/assess')
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950 to-violet-950">
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage:
              'linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        <div className="relative max-w-4xl mx-auto px-6 py-24 sm:py-32 text-center">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
          >
            <div className="inline-flex items-center gap-2 bg-white/10 text-white/80 text-xs font-medium px-4 py-2 rounded-full mb-8 border border-white/10 backdrop-blur-sm">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Structured reflection tool · Not professional advice
            </div>
            <h1 className="text-4xl sm:text-6xl font-extrabold text-white leading-tight tracking-tight">
              How much will you regret
              <br />
              <span className="bg-gradient-to-r from-indigo-300 to-violet-300 bg-clip-text text-transparent">
                this decision?
              </span>
            </h1>
            <p className="mt-6 text-lg sm:text-xl text-white/70 max-w-2xl mx-auto leading-relaxed">
              A thoughtful, heuristic-based tool that helps you think through important decisions
              by estimating short-term and long-term regret — before you commit.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                onClick={() => router.push('/assess')}
                className="!bg-white !text-brand-700 hover:!bg-brand-50 !shadow-xl"
              >
                Start your assessment
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </Button>
              <Button
                size="lg"
                variant="ghost"
                className="!text-white/70 hover:!text-white hover:!bg-white/10"
                onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}
              >
                See how it works
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 1 }}
            className="mt-16 flex justify-center gap-6"
          >
            {[34, 71, 52].map((score, i) => (
              <div
                key={i}
                className="flex flex-col items-center gap-2 bg-white/5 border border-white/10 rounded-2xl px-5 py-4 backdrop-blur-sm"
              >
                <span className="text-3xl font-extrabold text-white/90">{score}</span>
                <span className="text-xs text-white/40 uppercase tracking-widest">
                  {i === 0 ? 'Short-term' : i === 1 ? 'Long-term' : 'Overall'}
                </span>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* How it works */}
      <section id="how-it-works" className="py-20 px-6 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-14"
        >
          <h2 className="text-3xl font-bold text-slate-900">How it works</h2>
          <p className="mt-3 text-slate-500 text-lg">Three simple steps. One clearer picture.</p>
        </motion.div>
        <div className="grid sm:grid-cols-3 gap-8">
          {STEPS.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15, duration: 0.5 }}
              className="flex flex-col gap-4"
            >
              <div className="w-12 h-12 rounded-2xl bg-brand-100 flex items-center justify-center">
                <span className="text-xs font-bold text-brand-600 tracking-widest">{step.num}</span>
              </div>
              <h3 className="font-semibold text-slate-800 text-lg">{step.title}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Example decisions */}
      <section className="py-16 px-6 bg-white border-y border-slate-100">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-10"
          >
            <h2 className="text-2xl font-bold text-slate-900">Try an example</h2>
            <p className="mt-2 text-slate-500">Real decisions people use this tool to think through.</p>
          </motion.div>
          <div className="grid sm:grid-cols-2 gap-3">
            {SEED_SCENARIOS.map((scenario, i) => (
              <motion.button
                key={scenario}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ y: -2 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => startWithScenario(scenario)}
                className="text-left p-5 rounded-xl border-2 border-slate-100 hover:border-brand-200 bg-white hover:bg-brand-50 transition-all duration-200 group"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-brand-100 flex items-center justify-center flex-shrink-0 group-hover:bg-brand-200 transition-colors">
                    <svg className="w-4 h-4 text-brand-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <span className="text-sm font-medium text-slate-700 group-hover:text-brand-700 transition-colors leading-snug">
                    {scenario}
                  </span>
                </div>
              </motion.button>
            ))}
          </div>
        </div>
      </section>

      {/* What you get */}
      <section className="py-20 px-6 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-2xl font-bold text-slate-900">What you&apos;ll receive</h2>
        </motion.div>
        <div className="grid sm:grid-cols-2 gap-4">
          {[
            { icon: '📊', title: 'Overall regret score', desc: 'A calibrated 0–100 risk metric.' },
            { icon: '⏱', title: 'Short vs. long-term split', desc: 'Near-term disruption vs. lifetime opportunity cost.' },
            { icon: '🔍', title: 'Top driving factors', desc: "Ranked explanations of what's shaping the result." },
            { icon: '✉️', title: 'A message from your future self', desc: 'Personalized, non-judgmental reflection.' },
            { icon: '💭', title: 'Reflection questions', desc: 'Prompts designed to deepen your own thinking.' },
            { icon: '🧭', title: 'Likely regret type', desc: 'Whether acting or not acting carries more risk.' },
          ].map((item, i) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
              className="flex gap-4 p-4 rounded-xl bg-white border border-slate-100 shadow-sm"
            >
              <span className="text-2xl flex-shrink-0">{item.icon}</span>
              <div>
                <div className="font-semibold text-slate-800 text-sm">{item.title}</div>
                <div className="text-xs text-slate-500 mt-0.5 leading-relaxed">{item.desc}</div>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-12 text-center"
        >
          <Button size="lg" onClick={() => router.push('/assess')}>
            Start your assessment
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </Button>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-8 px-6 text-center text-xs text-slate-400">
        <p className="max-w-2xl mx-auto leading-relaxed">
          Future Regret Calculator is a reflection tool only. It does not predict the future, provide
          professional advice, or replace the judgment of qualified professionals. For medical, legal,
          financial, or mental health decisions, please seek appropriate expert guidance.
        </p>
      </footer>
    </div>
  )
}
