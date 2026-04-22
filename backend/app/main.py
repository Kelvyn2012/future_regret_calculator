from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import calculate

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app = FastAPI(
    title="Future Regret Calculator API",
    description="Heuristic scoring engine for reflective decision-making.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculate.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "service": "future-regret-calculator"}
