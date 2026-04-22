# Future Regret Calculator

A structured reflection tool that helps you think through meaningful life decisions by estimating short-term and long-term regret using behavioral heuristics.

---

## Stack

| Layer | Choice |
|---|---|
| Backend | **FastAPI** (Python 3.12) + SQLAlchemy 2 async + Neon PostgreSQL |
| Frontend | **Next.js 14** (App Router) + React 18 + TypeScript |
| Styling | **Tailwind CSS** + Framer Motion + Recharts |
| State | **Zustand** |
| Deployment | **Vercel** (monorepo — two separate Vercel projects) |

---

## Monorepo structure

```
future_regret_calculator/
├── backend/                 # Vercel project #1 (Root Directory = backend)
│   ├── api/
│   │   └── index.py         # Vercel Python serverless entry point
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── db/              # SQLAlchemy ORM + async engine
│   │   ├── routers/         # calculate.py, assessments.py
│   │   └── scoring/         # constants.py, engine.py, narrative.py
│   ├── alembic/             # DB migrations
│   ├── tests/
│   ├── vercel.json
│   └── requirements.txt
└── frontend/                # Vercel project #2 (Root Directory = frontend)
    ├── src/
    │   ├── app/             # Next.js App Router (layout, pages)
    │   ├── views/           # LandingPage, QuestionnairePage, ResultsPage
    │   ├── components/      # ui/, questionnaire/, results/
    │   ├── api/client.ts
    │   ├── store/
    │   └── types/
    ├── next.config.js
    └── package.json
```

---

## Vercel deployment (monorepo)

### Backend project

1. Create a new Vercel project → import this repo
2. **Root Directory**: `backend`
3. **Framework Preset**: Other
4. Set environment variables:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Your Neon connection string (e.g. `postgresql://...?sslmode=require&channel_binding=require`) |
| `ALLOWED_ORIGINS` | Comma-separated frontend URLs (e.g. `https://your-frontend.vercel.app`) |

### Frontend project

1. Create a second Vercel project → import the same repo
2. **Root Directory**: `frontend`
3. **Framework Preset**: Next.js (auto-detected)
4. Set environment variables:

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | Your backend Vercel URL (e.g. `https://your-backend.vercel.app`) |

---

## Local development

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Neon PostgreSQL database (or any PostgreSQL instance)

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy and fill in env vars
cp .env.example .env
# Edit .env: set DATABASE_URL and ALLOWED_ORIGINS

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install

# Copy and fill in env vars
cp .env.local.example .env.local
# Edit .env.local: NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

App: http://localhost:3000

### 3. Tests

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

---

## API endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/calculate` | Submit answers, get regret scores |
| `GET` | `/api/v1/assessments` | List recent assessments |
| `GET` | `/api/v1/assessments/{id}` | Retrieve a single result |

---

## Scoring model

Two primary scores drive everything:

- **Action regret** — risk of regretting IF you act (preparedness, motivation type, reversibility, social pressure, historical pattern, self-assessment)
- **Inaction regret** — risk of regretting if you DON'T act (values alignment, expected growth, importance, time sensitivity, historical pattern, self-assessment)

Derived: **short-term regret**, **long-term regret**, **overall score**, **regret type**, **confidence level**, **top drivers**.

All weights are named constants in `backend/app/scoring/constants.py`.

---

## Disclaimer

This tool is for personal reflection only. It does not predict the future, provide professional advice, or replace qualified professionals. For decisions involving health, finances, legal matters, or mental wellbeing, please consult an appropriate expert.
