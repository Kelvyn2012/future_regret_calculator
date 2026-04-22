import { create } from 'zustand'
import type { Category, AnswerSet, CalculationResult } from '../types'

interface AppState {
  decisionText: string
  category: Category | null
  answers: Partial<AnswerSet>
  result: CalculationResult | null
  currentStep: number

  setDecisionText: (text: string) => void
  setCategory: (category: Category) => void
  setAnswer: <K extends keyof AnswerSet>(key: K, value: AnswerSet[K]) => void
  setResult: (result: CalculationResult) => void
  setCurrentStep: (step: number) => void
  reset: () => void
}

const initialState = {
  decisionText: '',
  category: null as Category | null,
  answers: {} as Partial<AnswerSet>,
  result: null as CalculationResult | null,
  currentStep: 0,
}

export const useAppStore = create<AppState>((set) => ({
  ...initialState,

  setDecisionText: (text) => set({ decisionText: text }),
  setCategory: (category) => set({ category }),
  setAnswer: (key, value) =>
    set((state) => ({ answers: { ...state.answers, [key]: value } })),
  setResult: (result) => set({ result }),
  setCurrentStep: (step) => set({ currentStep: step }),
  reset: () => set(initialState),
}))
