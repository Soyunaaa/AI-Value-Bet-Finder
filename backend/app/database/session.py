from collections.abc import AsyncIterator
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings
from app.database.base import Base


settings = get_settings()

# session.py is located at:
# backend/app/database/session.py
#
# parents[2] therefore points to:
# backend/
BACKEND_DIRECTORY = (
    Path(__file__).resolve().parents[2]
)

DATABASE_DIRECTORY = (
    BACKEND_DIRECTORY / "database"
)


def ensure_database_directory() -> None:
    if not settings.database_url.startswith(
        "sqlite"
    ):
        return

    DATABASE_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )


# Create the directory before SQLAlchemy attempts
# to open the SQLite database file.
ensure_database_directory()


engine = create_async_engine(
    settings.database_url,
    echo=False,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def initialize_database() -> None:
    from app.database.models import elo  # noqa: F401
    from app.database.models import league_statistics  # noqa: F401
    from app.database.models import match  # noqa: F401
    from app.database.models import prediction_history  # noqa: F401
    from app.database.models import team_statistics  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )


async def close_database() -> None:
    await engine.dispose()


async def get_database_session(
) -> AsyncIterator[AsyncSession]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()