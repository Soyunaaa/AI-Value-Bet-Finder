from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from app.models.odds import OddsResponse

from app.providers.the_odds_api import (
    OddsApiError,
)

from app.services.odds_service import (
    InvalidOddsRequestError,
    OddsService,
    get_odds_service,
)


router = APIRouter(
    prefix="/odds",
    tags=["Odds"],
)


@router.get(
    "/{sport_key}",
    response_model=OddsResponse,
)
async def get_sport_odds(
    sport_key: str,
    regions: list[str] | None = Query(
        default=None,
        description=(
            "Bookmaker regions, for example eu or uk."
        ),
    ),
    markets: list[str] | None = Query(
        default=None,
        description=(
            "Featured markets: h2h, spreads, totals."
        ),
    ),
    bookmakers: list[str] | None = Query(
        default=None,
        description=(
            "Optional bookmaker keys. When supplied, "
            "these replace the region selection."
        ),
    ),
    service: OddsService = Depends(
        get_odds_service
    ),
) -> OddsResponse:
    try:
        return await service.get_odds(
            sport_key=sport_key,
            regions=regions,
            markets=markets,
            bookmakers=bookmakers,
        )

    except InvalidOddsRequestError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except OddsApiError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc