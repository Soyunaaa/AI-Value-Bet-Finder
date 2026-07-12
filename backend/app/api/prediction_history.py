from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import (
    get_database_session,
)
from app.models.prediction_history import (
    PredictionGradingResult,
    PredictionPerformanceSummary,
)
from app.services.prediction_grading_service import (
    PredictionGradingService,
    get_prediction_grading_service,
)


router = APIRouter(
    prefix="/prediction-history",
    tags=["Prediction History"],
)


@router.post(
    "/grade",
    response_model=PredictionGradingResult,
)
async def grade_predictions(
    competition_code: str | None = Query(
        default=None,
    ),
    session: AsyncSession = Depends(
        get_database_session
    ),
    service: PredictionGradingService = Depends(
        get_prediction_grading_service
    ),
) -> PredictionGradingResult:
    try:
        return await service.grade_pending_predictions(
            session=session,
            competition_code=competition_code,
        )

    except SQLAlchemyError as exc:
        await session.rollback()

        raise HTTPException(
            status_code=503,
            detail=(
                "Prediction grading failed."
            ),
        ) from exc


@router.get(
    "/performance",
    response_model=PredictionPerformanceSummary,
)
async def read_prediction_performance(
    competition_code: str | None = Query(
        default=None,
    ),
    model_version: str | None = Query(
        default=None,
    ),
    session: AsyncSession = Depends(
        get_database_session
    ),
    service: PredictionGradingService = Depends(
        get_prediction_grading_service
    ),
) -> PredictionPerformanceSummary:
    try:
        return await service.get_performance_summary(
            session=session,
            competition_code=competition_code,
            model_version=model_version,
        )

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to calculate prediction performance."
            ),
        ) from exc