from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.models.fixture_value import (
    FixtureValueRequest,
    FixtureValueResult,
)

from app.providers.football_data import (
    FootballDataApiError,
)

from app.services.fixture_value_service import (
    FixtureValueService,
    UnsupportedMarketSelectionError,
    get_fixture_value_service,
)


router = APIRouter(
    prefix="/fixture-value",
    tags=["Fixture Value"],
)


@router.post(
    "/{fixture_id}",
    response_model=FixtureValueResult,
)
async def evaluate_fixture_value(
    fixture_id: int,
    request: FixtureValueRequest,
    service: FixtureValueService = Depends(
        get_fixture_value_service
    ),
) -> FixtureValueResult:
    try:
        return await service.evaluate_fixture(
            fixture_id=fixture_id,
            request=request,
        )

    except UnsupportedMarketSelectionError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except FootballDataApiError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc