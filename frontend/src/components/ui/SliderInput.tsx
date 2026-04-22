'use client'

interface SliderInputProps {
  value: number
  onChange: (val: number) => void
  min: number
  max: number
  minLabel?: string
  maxLabel?: string
}

export function SliderInput({ value, onChange, min, max, minLabel, maxLabel }: SliderInputProps) {
  const pct = ((value - min) / (max - min)) * 100

  return (
    <div className="w-full space-y-4">
      <div className="relative">
        <div className="flex items-center gap-3">
          <div className="flex-1 relative h-2 bg-slate-100 rounded-full">
            <div
              className="absolute left-0 top-0 h-full bg-gradient-to-r from-brand-500 to-violet-500 rounded-full transition-all duration-150"
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="min-w-[2.5rem] text-center">
            <span className="text-xl font-bold text-brand-600 tabular-nums">{value}</span>
          </div>
        </div>
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="absolute inset-0 w-full opacity-0 cursor-pointer h-8 -top-3"
          style={{ touchAction: 'none' }}
        />
      </div>
      {(minLabel || maxLabel) && (
        <div className="flex justify-between text-xs text-slate-400 font-medium px-0.5">
          <span>{minLabel}</span>
          <span>{maxLabel}</span>
        </div>
      )}
      {/* Tick marks */}
      <div className="flex justify-between px-0.5">
        {Array.from({ length: max - min + 1 }, (_, i) => i + min).map((tick) => (
          <button
            key={tick}
            type="button"
            onClick={() => onChange(tick)}
            className={`w-5 h-5 rounded-full text-xs font-medium transition-all duration-150 ${
              tick === value
                ? 'bg-brand-600 text-white scale-110 shadow-sm shadow-brand-200'
                : 'bg-slate-100 text-slate-400 hover:bg-brand-100 hover:text-brand-600'
            }`}
          >
            {tick}
          </button>
        ))}
      </div>
    </div>
  )
}
