import axios from 'axios'
import type { DecisionInput, CalculationResult } from '../types'

// NEXT_PUBLIC_API_URL is the deployed backend base URL (no trailing slash).
// Set it in .env.local for local dev, and in Vercel project settings for production.
const api = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_URL ?? ''}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
})

export async function calculateRegret(input: DecisionInput): Promise<CalculationResult> {
  const { data } = await api.post<CalculationResult>('/calculate', input)
  return data
}
