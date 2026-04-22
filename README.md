# Future Regret Calculator

A structured reflection tool that helps you think through meaningful life decisions by estimating short-term and long-term regret using behavioral heuristics.

---

## Stack choices

| Layer | Choice | Why |
|---|---|---|
| Backend | **FastAPI** (Python) | Best-in-class API ergonomics, automatic Pydantic validation, instant OpenAPI docs, minimal boilerplate |
| Frontend | **React 18 + TypeScript + Vite** | Fastest iteration, full TypeScript safety, excellent ecosystem for polished UI |
| Styling | **Tailwind CSS** | Utility-first, rapid design iteration, consistent spacing, no CSS file sprawl |
| Animations | **Framer Motion** | Production-quality spring animations with minimal effort |
| Charts | **Recharts** | Lightweight, composable, React-native charting |
| State | **Zustand** | Minimal footprint, zero boilerplate, perfect for single-flow apps |
| Persistence | **None** | Results are computed on demand. No user accounts needed. No data to store. Re-running is trivial. |

---

## Architecture

```
frontend (React/Vite :5173)
        ↓  POST /api/v1/calculate
backend (FastAPI :8000)
        ↓  pure Python scoring engine
        ↑  returns CalculationResult JSON
```

The scoring engine is fully stateless. Every request contains all inputs. The backend computes action regret, inaction regret, temporal splits, confidence, top drivers, and narrative — then returns structured JSON. No database required.

---

## Project structure

```
future_regret_calculator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + CORS
│   │   ├── models.py            # Pydantic request/response schemas
│   │   ├── routers/
│   │   │   └── calculate.py     # POST /calculate, GET /questions
│   │   └── scoring/
│   │       ├── constants.py     # Named weights — tune here
│   │       ├── engine.py        # Core scoring logic
│   │       └── narrative.py     # Narrative + reflection generation
│   ├── tests/
│   │   └── test_scoring.py      # Pytest: bounds, structure, behavioral logic, seeds
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/client.ts        # Axios API wrapper
│   │   ├── components/
│   │   │   ├── questionnaire/   # CategorySelector, QuestionStep
│   │   │   ├── results/         # ScoreDisplay, DriverCard, RegretChart
│   │   │   └── ui/              # Button, Card, ProgressBar, SliderInput
│   │   ├── data/questions.ts    # Question definitions + seed scenarios
│   │   ├── pages/               # LandingPage, QuestionnairePage, ResultsPage
│   │   ├── store/useAppStore.ts # Zustand global state
│   │   └── types/index.ts       # Shared TypeScript types
│   ├── package.json
│   └── vite.config.ts           # Dev proxy → backend :8000
└── README.md
```

---

## Setup & Run

### Prerequisites

- Python 3.10+
- Node.js 18+
- (Optional) SSH key configured for GitHub

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

The Vite dev server proxies `/api/*` to the backend at `localhost:8000`, so no CORS issues during development.

### 3. Run tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

---

## Sample API request

```bash
curl -X POST http://localhost:8000/api/v1/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_text": "Should I quit my job to start my own business?",
    "category": "career",
    "answers": {
      "importance": 9,
      "reversibility": "difficult",
      "time_sensitivity": 4,
      "preparedness": 3,
      "values_alignment": 5,
      "motivation": "genuine_excitement",
      "inaction_regret": 8,
      "action_regret_short": 5,
      "historical_pattern": "too_slow",
      "support_system": 3,
      "expected_growth": 5,
      "social_influence": 2
    }
  }'
```

### Sample response

```json
{
  "overall_score": 68,
  "short_term_regret": 45,
  "long_term_regret": 79,
  "action_regret_raw": 42,
  "inaction_regret_raw": 74,
  "likely_regret_type": "inaction",
  "confidence_level": "high",
  "top_drivers": [
    {
      "factor": "Strong Values Alignment",
      "weight": 92,
      "direction": "increases_inaction_regret",
      "explanation": "When a path aligns deeply with your values, the cost of not taking it tends to compound quietly over time."
    },
    {
      "factor": "High Growth Potential",
      "weight": 88,
      "direction": "increases_inaction_regret",
      "explanation": "Decisions with significant growth potential tend to generate more long-term regret when avoided."
    }
  ],
  "narrative_summary": "The pattern in your answers points toward a meaningful risk of long-term inaction regret...",
  "future_you_message": "The version of you who looks back on this moment years from now will likely care less about whether you succeeded, and more about whether you tried...",
  "reflection_questions": [
    "If you imagine yourself five years from now, having not acted — what do you see?",
    "How much of your identity and values is tied to this direction?",
    "What would need to be true for you to feel confident moving forward?"
  ],
  "disclaimer": "This tool is designed for personal reflection only..."
}
```

---

## Scoring model

All weights are named constants in `backend/app/scoring/constants.py` — tune them independently without touching engine logic.

**Two primary scores are computed:**

- **Action regret** (risk of regretting IF you act): driven by preparedness, motivation type, social pressure, reversibility, historical pattern, self-assessment
- **Inaction regret** (risk of regretting if you DON'T act): driven by self-assessment, values alignment, expected growth, importance, time sensitivity, historical pattern

**Derived scores:**

- **Short-term regret** = weighted toward action disruption + time-sensitive urgency
- **Long-term regret** = weighted toward inaction/opportunity cost × values/growth premium
- **Overall score** = combined risk metric (dominant direction + recessive + temporal average)

**Regret type logic:**

| Condition | Type |
|---|---|
| `\|inaction - action\| < 10` | `mixed` |
| `inaction > action + 10` | `inaction` |
| `action > inaction + 10` | `action` |
| confidence = low | `low_confidence` |

**Confidence** decreases with: high social influence, close action/inaction scores, reactive motivation.

---

## Seed demo scenarios

| Decision | Expected behavior |
|---|---|
| Quit job for own business | Inaction regret dominant, long-term > short-term |
| Move cities for opportunity | Moderate, likely inaction |
| Go back to school | Elevated, likely inaction with prep caveat |
| End a relationship (under pressure) | Action regret dominant |
| Impulsive large purchase | Action regret dominant |

---

## Git + GitHub

### Initial setup

```bash
# From project root
git init
git remote add origin git@github.com:Kelvyn2012/future_regret_calculator.git

# First commit
git add .
git commit -m "Initial project setup: architecture, gitignore, README"
git push -u origin main
```

### Milestone commits

```bash
# After backend
git add backend/
git commit -m "Add Python backend: FastAPI, scoring engine, narrative, tests"
git push

# After frontend
git add frontend/
git commit -m "Add React/TypeScript frontend: landing, questionnaire, results pages"
git push

# After final polish
git add .
git commit -m "Finalize MVP: scoring tuning, UX polish, integration"
git push
```

### SSH key setup (if needed)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub   # paste this into GitHub → Settings → SSH Keys
ssh -T git@github.com       # verify connection
```

---

## Future improvements

1. **Compare two decisions** — submit two sets of answers and show side-by-side results
2. **Local result history** — save last 5 results to localStorage with timestamps
3. **Export/share** — generate a shareable PDF or link summary
4. **Dark mode** — already using Tailwind, just needs a theme toggle
5. **Decision journal** — let users annotate and revisit decisions over time
6. **Category-specific questions** — tailor a subset of questions for career vs. relationship vs. financial
7. **Calibration feedback** — let users mark outcomes months later to improve model accuracy
8. **Confidence interval visualization** — show score bands rather than point estimates

---

## Disclaimer

This tool is designed for personal reflection only. It does not predict the future, provide professional advice, or account for the full complexity of your situation. For decisions involving health, finances, legal matters, or mental wellbeing, please consult a qualified professional.
