from fastapi import APIRouter

from app.models.market_evaluation import (
    MarketEvaluationRequest,
    MarketEvaluationResult,
)

from app.services.market_evaluation_service import (
    evaluate_markets,
)


router = APIRouter(
    prefix="/market-evaluation",
    tags=["Market Evaluation"],
)


@router.post(
    "",
    response_model=MarketEvaluationResult,
)
def evaluate_market_prices(
    request: MarketEvaluationRequest,
) -> MarketEvaluationResult:
    return evaluate_markets(request)