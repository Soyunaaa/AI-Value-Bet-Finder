from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.match import MatchRecord
from app.database.session import get_database_session
from app.models.database import (
    DatabaseStatus,
    EloBuildResult,
    EloHistoryResponse,
    FixtureSyncResult,
    TeamEloResponse,
    TeamStatisticsBuildResult,
    TeamStatisticsResponse,
)
from app.providers.football_data import FootballDataApiError
from app.services.database_service import get_database_status
from app.services.fixture_sync_service import (
    FixtureSyncService,
    get_fixture_sync_service,
)
from app.services.persistent_elo_service import (
    PersistentEloService,
    get_persistent_elo_service,
)
from app.services.team_statistics_builder import (
    TeamStatisticsBuilder,
    get_team_statistics_builder,
)
from app.services.team_statistics_service import (
    get_competition_team_statistics,
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


@router.post(
    "/statistics/rebuild/{competition_code}",
    response_model=TeamStatisticsBuildResult,
)
async def rebuild_team_statistics(
    competition_code: str,
    session: AsyncSession = Depends(
        get_database_session
    ),
    builder: TeamStatisticsBuilder = Depends(
        get_team_statistics_builder
    ),
) -> TeamStatisticsBuildResult:
    try:
        return await builder.rebuild_competition(
            session=session,
            competition_code=competition_code,
        )

    except SQLAlchemyError as exc:
        await session.rollback()

        raise HTTPException(
            status_code=503,
            detail="Team statistics rebuild failed.",
        ) from exc


@router.get(
    "/statistics/{competition_code}",
    response_model=list[
        TeamStatisticsResponse
    ],
)
async def read_team_statistics(
    competition_code: str,
    session: AsyncSession = Depends(
        get_database_session
    ),
) -> list[TeamStatisticsResponse]:
    try:
        return await get_competition_team_statistics(
            session=session,
            competition_code=competition_code,
        )

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to read team statistics."
            ),
        ) from exc


@router.get(
    "/debug/match-statuses",
)
async def debug_match_statuses(
    session: AsyncSession = Depends(
        get_database_session
    ),
) -> list[dict[str, int | str]]:
    statement = (
        select(
            MatchRecord.status,
            func.count(MatchRecord.id),
        )
        .group_by(
            MatchRecord.status
        )
        .order_by(
            MatchRecord.status
        )
    )

    result = await session.execute(
        statement
    )

    return [
        {
            "status": status,
            "count": count,
        }
        for status, count in result.all()
    ]


@router.post(
    "/elo/rebuild/{competition_code}",
    response_model=EloBuildResult,
)
async def rebuild_competition_elo(
    competition_code: str,
    session: AsyncSession = Depends(
        get_database_session
    ),
    service: PersistentEloService = Depends(
        get_persistent_elo_service
    ),
) -> EloBuildResult:
    try:
        return await service.rebuild_competition(
            session=session,
            competition_code=competition_code,
        )

    except SQLAlchemyError as exc:
        await session.rollback()

        raise HTTPException(
            status_code=503,
            detail="Elo rebuild failed.",
        ) from exc


@router.get(
    "/elo/{competition_code}",
    response_model=list[
        TeamEloResponse
    ],
)
async def read_competition_elo(
    competition_code: str,
    session: AsyncSession = Depends(
        get_database_session
    ),
    service: PersistentEloService = Depends(
        get_persistent_elo_service
    ),
) -> list[TeamEloResponse]:
    try:
        return await service.get_competition_ratings(
            session=session,
            competition_code=competition_code,
        )

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to read Elo ratings.",
        ) from exc


@router.get(
    "/elo/{competition_code}/{team_id}/history",
    response_model=list[
        EloHistoryResponse
    ],
)
async def read_team_elo_history(
    competition_code: str,
    team_id: int,
    session: AsyncSession = Depends(
        get_database_session
    ),
    service: PersistentEloService = Depends(
        get_persistent_elo_service
    ),
) -> list[EloHistoryResponse]:
    try:
        return await service.get_team_history(
            session=session,
            competition_code=competition_code,
            team_id=team_id,
        )

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to read Elo history.",
        ) from exc