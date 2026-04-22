'use client'

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ReferenceLine,
} from 'recharts'
import type { CalculationResult } from '../../types'

interface RegretChartProps {
  result: CalculationResult
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white border border-slate-100 rounded-xl shadow-lg px-4 py-3">
      <div className="text-xs text-slate-500 mb-1">{label}</div>
      <div className="text-xl font-bold text-slate-800">{payload[0].value}</div>
      <div className="text-xs text-slate-400">out of 100</div>
    </div>
  )
}

export function RegretChart({ result }: RegretChartProps) {
  const data = [
    {
      name: 'Action\nRegret',
      label: 'If you act',
      value: result.action_regret_raw,
      fill: '#f97316',
    },
    {
      name: 'Inaction\nRegret',
      label: "If you don't act",
      value: result.inaction_regret_raw,
      fill: '#8b5cf6',
    },
    {
      name: 'Short-term',
      label: 'Near-term risk',
      value: result.short_term_regret,
      fill: '#f59e0b',
    },
    {
      name: 'Long-term',
      label: 'Long-term risk',
      value: result.long_term_regret,
      fill: '#6366f1',
    },
  ]

  return (
    <div>
      <h3 className="text-sm font-semibold text-slate-600 uppercase tracking-wider mb-4">
        Regret dimensions
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} barSize={36} margin={{ top: 4, right: 4, bottom: 4, left: -20 }}>
          <XAxis
            dataKey="name"
            tick={{ fontSize: 11, fill: '#94a3b8', fontWeight: 500 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#cbd5e1' }} axisLine={false} tickLine={false} />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(99,102,241,0.05)', radius: 8 }} />
          <ReferenceLine y={50} stroke="#e2e8f0" strokeDasharray="4 4" />
          <Bar dataKey="value" radius={[6, 6, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={index} fill={entry.fill} opacity={0.85} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="grid grid-cols-2 gap-2 mt-3">
        {data.map((d) => (
          <div key={d.name} className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ background: d.fill }} />
            <span className="text-xs text-slate-500">{d.label}</span>
            <span className="ml-auto text-xs font-semibold text-slate-700 tabular-nums">{d.value}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
