from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from app.models.automatic_fixture_value import (
    AutomaticFixtureValueResult,
)

from app.providers.football_data import (
    FootballDataApiError,
)

from app.providers.the_odds_api import (
    OddsApiError,
)

from app.services.automatic_fixture_value_service import (
    AutomaticFixtureValueService,
    FixtureOddsMatchError,
    NoUsableOddsError,
    get_automatic_fixture_value_service,
)


router = APIRouter(
    prefix="/automatic-fixture-value",
    tags=["Automatic Fixture Value"],
)


@router.get(
    "/{fixture_id}",
    response_model=AutomaticFixtureValueResult,
)
async def evaluate_automatic_fixture_value(
    fixture_id: int,
    sport_key: str = Query(
        description=(
            "The Odds API sport key, such as "
            "soccer_epl."
        ),
    ),
    region: str = Query(
        default="eu",
    ),
    bankroll: float = Query(
        default=1000,
        gt=0,
    ),
    kelly_fraction: float = Query(
        default=0.25,
        gt=0,
        le=1,
    ),
    minimum_expected_value: float = Query(
        default=0.05,
    ),
    service: AutomaticFixtureValueService = Depends(
        get_automatic_fixture_value_service
    ),
) -> AutomaticFixtureValueResult:
    try:
        return await service.evaluate_fixture(
            fixture_id=fixture_id,
            sport_key=sport_key,
            region=region,
            bankroll=bankroll,
            kelly_fraction=kelly_fraction,
            minimum_expected_value=(
                minimum_expected_value
            ),
        )

    except FixtureOddsMatchError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except NoUsableOddsError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except (
        FootballDataApiError,
        OddsApiError,
    ) as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc