from fastapi import APIRouter

from app.models.calculation import (
    MarginRemovalRequest,
    MarginRemovalResult,
    ValueCalculationRequest,
    ValueCalculationResult,
)

from app.services.calculation_service import (
    calculate_value,
    remove_bookmaker_margin,
)


router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


@router.post(
    "/value",
    response_model=ValueCalculationResult,
)
def calculate_value_endpoint(
    request: ValueCalculationRequest,
) -> ValueCalculationResult:
    return calculate_value(request)


@router.post(
    "/remove-margin",
    response_model=list[MarginRemovalResult],
)
def remove_margin_endpoint(
    request: MarginRemovalRequest,
) -> list[MarginRemovalResult]:
    return remove_bookmaker_margin(request)