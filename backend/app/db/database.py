"""
Async SQLAlchemy engine and session factory.

The raw DATABASE_URL may use postgresql:// (libpq format) with query params
like sslmode and channel_binding that asyncpg doesn't accept in the URL.
We strip them and pass ssl via connect_args instead.
"""

from __future__ import annotations

import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

_raw_url: str = os.environ.get("DATABASE_URL", "")
if not _raw_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")


def _to_asyncpg_url(url: str) -> str:
    """Convert a standard postgresql:// URL to a postgresql+asyncpg:// URL.

    asyncpg does not accept sslmode/channel_binding as URL query params —
    it handles SSL via connect_args. So we strip the query string entirely.
    """
    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    # Strip everything after '?' — SSL is set via connect_args below
    if "?" in url:
        url = url.split("?")[0]
    return url


def _to_psycopg2_url(url: str) -> str:
    """Convert to a psycopg2 sync URL for Alembic migrations.

    Keeps sslmode=require but drops channel_binding which psycopg2 ignores.
    """
    import re

    url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
    url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    url = re.sub(r"[?&]channel_binding=[^&]*", "", url)
    url = re.sub(r"\?$|&$", "", url)
    # Ensure sslmode=require is present
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return url


ASYNC_DATABASE_URL: str = _to_asyncpg_url(_raw_url)
SYNC_DATABASE_URL: str = _to_psycopg2_url(_raw_url)

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    connect_args={"ssl": "require"},
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
