from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from app.models.football import FootballFixture
from app.providers.football_data import (
    FootballDataApiError,
)
from app.services.football_service import (
    FootballService,
    get_football_service,
)


router = APIRouter(
    prefix="/football",
    tags=["Football"],
)


@router.get(
    "/matches",
    response_model=list[FootballFixture],
)
async def get_matches(
    competition: str | None = Query(
        default=None,
        min_length=2,
        max_length=10,
        description=(
            "Competition code such as PL, PD, BL1, SA or CL."
        ),
    ),
    date_from: date | None = None,
    date_to: date | None = None,
    service: FootballService = Depends(
        get_football_service
    ),
) -> list[FootballFixture]:
    if (
        date_from is not None
        and date_to is not None
        and date_from > date_to
    ):
        raise HTTPException(
            status_code=422,
            detail="date_from cannot be after date_to.",
        )

    try:
        return await service.get_matches(
            competition_code=competition,
            date_from=date_from,
            date_to=date_to,
        )
    except FootballDataApiError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc