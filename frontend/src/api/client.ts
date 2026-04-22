import axios from 'axios'
import type { DecisionInput, CalculationResult } from '../types'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export async function calculateRegret(input: DecisionInput): Promise<CalculationResult> {
  const { data } = await api.post<CalculationResult>('/calculate', input)
  return data
}
