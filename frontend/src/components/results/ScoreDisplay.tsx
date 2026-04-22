import { motion } from 'framer-motion'

interface ScoreArcProps {
  score: number
  size?: number
  strokeWidth?: number
  label?: string
  sublabel?: string
  colorClass?: string
  strokeColor?: string
}

function getScoreStyle(score: number) {
  if (score <= 33) return { color: '#10b981', bg: 'bg-emerald-50', text: 'text-emerald-600', label: 'Low' }
  if (score <= 60) return { color: '#f59e0b', bg: 'bg-amber-50', text: 'text-amber-600', label: 'Moderate' }
  if (score <= 79) return { color: '#f97316', bg: 'bg-orange-50', text: 'text-orange-600', label: 'Elevated' }
  return { color: '#f43f5e', bg: 'bg-rose-50', text: 'text-rose-600', label: 'High' }
}

export function ScoreArc({
  score,
  size = 160,
  strokeWidth = 12,
  label,
  sublabel,
}: ScoreArcProps) {
  const style = getScoreStyle(score)
  const cx = size / 2
  const cy = size / 2
  const r = (size - strokeWidth * 2) / 2
  const circumference = Math.PI * r
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size / 2 + strokeWidth }}>
        <svg
          width={size}
          height={size / 2 + strokeWidth}
          viewBox={`0 0 ${size} ${size / 2 + strokeWidth}`}
        >
          {/* Track */}
          <path
            d={`M ${strokeWidth} ${size / 2} A ${r} ${r} 0 0 1 ${size - strokeWidth} ${size / 2}`}
            fill="none"
            stroke="#f1f5f9"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
          {/* Score arc */}
          <motion.path
            d={`M ${strokeWidth} ${size / 2} A ${r} ${r} 0 0 1 ${size - strokeWidth} ${size / 2}`}
            fill="none"
            stroke={style.color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.2, ease: 'easeOut', delay: 0.2 }}
          />
        </svg>
        {/* Score number centered in arc */}
        <div
          className="absolute bottom-0 left-0 right-0 flex flex-col items-center"
          style={{ paddingBottom: 4 }}
        >
          <motion.span
            className={`text-4xl font-extrabold tabular-nums ${style.text}`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.4 }}
          >
            {score}
          </motion.span>
          <span className={`text-xs font-semibold uppercase tracking-widest mt-0.5 ${style.text}`}>
            {style.label}
          </span>
        </div>
      </div>
      {label && <div className="text-sm font-semibold text-slate-700 text-center">{label}</div>}
      {sublabel && <div className="text-xs text-slate-400 text-center leading-tight">{sublabel}</div>}
    </div>
  )
}

interface RegretTypeBadgeProps {
  type: string
  confidence: string
}

const REGRET_TYPE_CONFIG = {
  inaction: {
    label: 'Inaction Regret',
    description: 'Your pattern suggests you may regret NOT acting more than acting.',
    color: 'bg-violet-100 text-violet-700 border-violet-200',
    icon: '→',
  },
  action: {
    label: 'Action Regret',
    description: 'Your pattern suggests the near-term risk of acting may outweigh inaction.',
    color: 'bg-amber-100 text-amber-700 border-amber-200',
    icon: '⟵',
  },
  mixed: {
    label: 'Mixed Signal',
    description: 'Both acting and not acting carry meaningful regret risk. This is genuinely complex.',
    color: 'bg-slate-100 text-slate-700 border-slate-200',
    icon: '⇌',
  },
  low_confidence: {
    label: 'Low Confidence',
    description: 'Not enough signal to distinguish a clear pattern. More clarity may help.',
    color: 'bg-slate-100 text-slate-600 border-slate-200',
    icon: '~',
  },
}

const CONFIDENCE_CONFIG = {
  high: { label: 'High confidence', color: 'bg-emerald-100 text-emerald-700' },
  medium: { label: 'Medium confidence', color: 'bg-amber-100 text-amber-700' },
  low: { label: 'Low confidence', color: 'bg-slate-100 text-slate-600' },
}

export function RegretTypeBadge({ type, confidence }: RegretTypeBadgeProps) {
  const config = REGRET_TYPE_CONFIG[type as keyof typeof REGRET_TYPE_CONFIG]
  const confConfig = CONFIDENCE_CONFIG[confidence as keyof typeof CONFIDENCE_CONFIG]

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4 }}
      className={`inline-flex flex-col gap-2 rounded-xl border px-5 py-4 ${config.color}`}
    >
      <div className="flex items-center gap-2">
        <span className="text-lg font-bold">{config.icon}</span>
        <span className="font-semibold text-sm">{config.label}</span>
        <span className={`ml-auto text-xs font-medium px-2 py-0.5 rounded-full ${confConfig.color}`}>
          {confConfig.label}
        </span>
      </div>
      <p className="text-xs leading-relaxed opacity-80">{config.description}</p>
    </motion.div>
  )
}
