import { motion } from 'framer-motion'
import { SliderInput } from '../ui/SliderInput'
import type { Question, AnswerSet } from '../../types'

interface QuestionStepProps {
  question: Question
  value: AnswerSet[keyof AnswerSet] | undefined
  onChange: (val: AnswerSet[keyof AnswerSet]) => void
}

export function QuestionStep({ question, value, onChange }: QuestionStepProps) {
  return (
    <motion.div
      key={question.id}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className="space-y-6"
    >
      <div>
        <h2 className="text-xl font-semibold text-slate-800 leading-snug">{question.text}</h2>
        {question.description && (
          <p className="mt-2 text-sm text-slate-500 leading-relaxed">{question.description}</p>
        )}
      </div>

      {question.type === 'slider' && (
        <SliderInput
          value={(value as number) ?? question.default ?? question.min!}
          onChange={(val) => onChange(val as AnswerSet[keyof AnswerSet])}
          min={question.min!}
          max={question.max!}
          minLabel={question.minLabel}
          maxLabel={question.maxLabel}
        />
      )}

      {question.type === 'choice' && (
        <div className="space-y-2.5">
          {question.options?.map((opt) => {
            const selected = value === opt.value
            return (
              <motion.button
                key={opt.value}
                type="button"
                whileTap={{ scale: 0.98 }}
                onClick={() => onChange(opt.value as AnswerSet[keyof AnswerSet])}
                className={`w-full text-left px-5 py-4 rounded-xl border-2 transition-all duration-150 ${
                  selected
                    ? 'border-brand-500 bg-brand-50 shadow-sm shadow-brand-100'
                    : 'border-slate-100 bg-white hover:border-brand-200 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`mt-0.5 w-4 h-4 rounded-full border-2 flex-shrink-0 transition-colors duration-150 ${
                      selected ? 'border-brand-500 bg-brand-500' : 'border-slate-300 bg-white'
                    }`}
                  >
                    {selected && (
                      <div className="w-full h-full rounded-full flex items-center justify-center">
                        <div className="w-1.5 h-1.5 rounded-full bg-white" />
                      </div>
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div
                      className={`font-medium text-sm ${selected ? 'text-brand-700' : 'text-slate-700'}`}
                    >
                      {opt.label}
                    </div>
                    {opt.description && (
                      <div className="mt-0.5 text-xs text-slate-400">{opt.description}</div>
                    )}
                  </div>
                </div>
              </motion.button>
            )
          })}
        </div>
      )}
    </motion.div>
  )
}
