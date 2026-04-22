'use client'

import { motion } from 'framer-motion'
import type { TopDriver } from '../../types'

interface DriverCardProps {
  driver: TopDriver
  index: number
}

const DIRECTION_CONFIG = {
  increases_action_regret: {
    label: '↑ Action regret',
    color: 'text-amber-600',
    bar: 'bg-amber-400',
    bg: 'bg-amber-50',
    border: 'border-amber-100',
  },
  increases_inaction_regret: {
    label: '↑ Inaction regret',
    color: 'text-violet-600',
    bar: 'bg-violet-500',
    bg: 'bg-violet-50',
    border: 'border-violet-100',
  },
  decreases_regret: {
    label: '↓ Reduces regret',
    color: 'text-emerald-600',
    bar: 'bg-emerald-500',
    bg: 'bg-emerald-50',
    border: 'border-emerald-100',
  },
}

export function DriverCard({ driver, index }: DriverCardProps) {
  const config = DIRECTION_CONFIG[driver.direction]

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 * index, duration: 0.35 }}
      className={`rounded-xl border p-4 ${config.bg} ${config.border}`}
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="font-semibold text-slate-800 text-sm">{driver.factor}</div>
        <span className={`text-xs font-semibold whitespace-nowrap ${config.color}`}>
          {config.label}
        </span>
      </div>
      {/* Weight bar */}
      <div className="h-1.5 bg-white/70 rounded-full mb-2 overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${config.bar}`}
          initial={{ width: 0 }}
          animate={{ width: `${driver.weight}%` }}
          transition={{ delay: 0.15 * index + 0.3, duration: 0.6, ease: 'easeOut' }}
        />
      </div>
      <p className="text-xs text-slate-600 leading-relaxed">{driver.explanation}</p>
    </motion.div>
  )
}
