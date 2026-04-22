"""
Vercel serverless entry point.

Adds backend/ to sys.path so 'app.*' imports resolve, then re-exports
the FastAPI ASGI app. Vercel's Python runtime picks up `app` automatically.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app  # noqa: F401, E402 — re-exported as ASGI handler
