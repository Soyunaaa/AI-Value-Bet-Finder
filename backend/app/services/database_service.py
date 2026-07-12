from sqlalchemy import (
    func,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.match import (
    MatchRecord,
)
from app.models.database import (
    DatabaseStatus,
)


async def get_database_status(
    session: AsyncSession,
) -> DatabaseStatus:
    statement = select(
        func.count(MatchRecord.id)
    )

    result = await session.execute(
        statement
    )

    matches_stored = (
        result.scalar_one()
    )

    return DatabaseStatus(
        connected=True,
        database_type="SQLite",
        matches_stored=matches_stored,
    )