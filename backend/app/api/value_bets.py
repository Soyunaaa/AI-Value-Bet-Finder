from fastapi import APIRouter, HTTPException

from app.models.value_bet import ValueBet
from app.services.value_bet_service import (
    get_value_bet_by_id,
    list_value_bets,
)


router = APIRouter(
    prefix="/value-bets",
    tags=["Value Bets"],
)


@router.get("", response_model=list[ValueBet])
def get_all_value_bets() -> list[ValueBet]:
    return list_value_bets()


@router.get("/{bet_id}", response_model=ValueBet)
def get_value_bet(bet_id: int) -> ValueBet:
    bet = get_value_bet_by_id(bet_id)

    if bet is None:
        raise HTTPException(
            status_code=404,
            detail="Value bet not found",
        )

    return bet