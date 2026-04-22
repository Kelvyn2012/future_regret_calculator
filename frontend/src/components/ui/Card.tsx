import type { HTMLAttributes } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  elevated?: boolean
}

export function Card({ elevated, className = '', children, ...props }: CardProps) {
  return (
    <div
      className={`bg-white rounded-2xl ${
        elevated
          ? 'shadow-xl shadow-slate-200/60'
          : 'shadow-sm shadow-slate-200/80 border border-slate-100'
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}
