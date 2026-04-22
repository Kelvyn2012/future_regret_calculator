from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()  # no-op on Vercel (vars are injected); useful locally

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import calculate, assessments

_is_serverless = bool(os.getenv("VERCEL"))

# On Vercel the frontend and API share the same domain, so CORS is technically
# unnecessary for production — but we still set it for local dev and previews.
# VERCEL_URL is automatically injected by Vercel on every deployment.
_env_origins = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")
_vercel_url = os.getenv("VERCEL_URL")  # e.g. "your-project.vercel.app"
ALLOWED_ORIGINS = _env_origins + ([f"https://{_vercel_url}"] if _vercel_url else [])


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not _is_serverless:
        # Verify DB connectivity on local startup — skip on Vercel cold starts
        # to avoid adding latency to the first request.
        from app.db.database import engine
        async with engine.connect():
            pass
    yield
    from app.db.database import engine
    await engine.dispose()


app = FastAPI(
    title="Future Regret Calculator API",
    description="Heuristic scoring engine for reflective decision-making.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculate.router, prefix="/api/v1")
app.include_router(assessments.router, prefix="/api/v1")


@app.get("/health")
async def health():
    from app.db.database import engine
    from sqlalchemy import text
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as exc:
        db_status = f"error: {exc}"
    return {"status": "ok", "service": "future-regret-calculator", "db": db_status}
