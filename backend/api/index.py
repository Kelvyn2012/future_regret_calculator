"""
Vercel serverless entry point for the backend project.

When Vercel deploys with Root Directory = backend/, the project root
is backend/ itself, so `app.main` is directly importable — no sys.path
manipulation required.
"""

from app.main import app  # noqa: F401 — re-exported as the ASGI handler
