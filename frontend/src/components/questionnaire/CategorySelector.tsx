import { motion } from 'framer-motion'
import { CATEGORIES } from '../../data/questions'
import type { Category } from '../../types'

interface CategorySelectorProps {
  value: Category | null
  onChange: (cat: Category) => void
}

export function CategorySelector({ value, onChange }: CategorySelectorProps) {
  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-xl font-semibold text-slate-800">What category best describes this decision?</h2>
        <p className="mt-2 text-sm text-slate-500">This helps contextualize the analysis.</p>
      </div>
      <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-4">
        {CATEGORIES.map((cat) => {
          const selected = value === cat.value
          return (
            <motion.button
              key={cat.value}
              type="button"
              whileTap={{ scale: 0.96 }}
              onClick={() => onChange(cat.value as Category)}
              className={`p-4 rounded-xl border-2 text-left transition-all duration-150 ${
                selected
                  ? 'border-brand-500 bg-brand-50 shadow-sm shadow-brand-100'
                  : 'border-slate-100 bg-white hover:border-brand-200 hover:bg-slate-50'
              }`}
            >
              <div className="text-2xl mb-2">{cat.icon}</div>
              <div className={`text-sm font-semibold ${selected ? 'text-brand-700' : 'text-slate-700'}`}>
                {cat.label}
              </div>
              <div className="text-xs text-slate-400 mt-0.5 leading-tight">{cat.description}</div>
            </motion.button>
          )
        })}
      </div>
    </div>
  )
}
