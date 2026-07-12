from fastapi import APIRouter

from app.models.prediction import (
    MatchPredictionRequest,
    MatchPredictionResult,
)

from app.services.prediction_service import predict_match


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


@router.post(
    "/match",
    response_model=MatchPredictionResult,
)
def predict_match_endpoint(
    request: MatchPredictionRequest,
) -> MatchPredictionResult:
    return predict_match(request)