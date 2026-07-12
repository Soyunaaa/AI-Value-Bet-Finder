from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.models.fixture_analysis import (
    FixtureAnalysisResult,
)

from app.providers.football_data import (
    FootballDataApiError,
)

from app.services.fixture_analysis_service import (
    FixtureAnalysisService,
    get_fixture_analysis_service,
)


router = APIRouter(
    prefix="/fixture-analysis",
    tags=["Fixture Analysis"],
)


@router.get(
    "/{fixture_id}",
    response_model=FixtureAnalysisResult,
)
async def analyse_fixture(
    fixture_id: int,
    service: FixtureAnalysisService = Depends(
        get_fixture_analysis_service
    ),
) -> FixtureAnalysisResult:
    try:
        return await service.analyse_fixture(
            fixture_id
        )
    except FootballDataApiError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc