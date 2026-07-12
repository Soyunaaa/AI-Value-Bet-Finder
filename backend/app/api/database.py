from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.session import (
    get_database_session,
)
from app.models.database import (
    DatabaseStatus,
    FixtureSyncResult,
)
from app.providers.football_data import (
    FootballDataApiError,
)
from app.services.database_service import (
    get_database_status,
)
from app.services.fixture_sync_service import (
    FixtureSyncService,
    get_fixture_sync_service,
)


router = APIRouter(
    prefix="/database",
    tags=["Database"],
)


@router.get(
    "/status",
    response_model=DatabaseStatus,
)
async def database_status(
    session: AsyncSession = Depends(
        get_database_session
    ),
) -> DatabaseStatus:
    try:
        return await get_database_status(
            session
        )
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="The database is unavailable.",
        ) from exc


@router.post(
    "/sync/competition/{competition_code}",
    response_model=FixtureSyncResult,
)
async def sync_competition_fixtures(
    competition_code: str,
    date_from: date | None = Query(
        default=None,
    ),
    date_to: date | None = Query(
        default=None,
    ),
    session: AsyncSession = Depends(
        get_database_session
    ),
    service: FixtureSyncService = Depends(
        get_fixture_sync_service
    ),
) -> FixtureSyncResult:
    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                "date_from cannot be after "
                "date_to."
            ),
        )

    try:
        return await service.sync_competition(
            session=session,
            competition_code=competition_code,
            date_from=date_from,
            date_to=date_to,
        )

    except FootballDataApiError as exc:
        await session.rollback()

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    except SQLAlchemyError as exc:
        await session.rollback()

        raise HTTPException(
            status_code=503,
            detail=(
                "The database synchronization "
                "failed."
            ),
        ) from exc