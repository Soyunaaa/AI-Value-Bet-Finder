import pytest

from app.services.odds_service import (
    InvalidOddsRequestError,
    OddsService,
)


@pytest.mark.asyncio
async def test_rejects_invalid_odds_region() -> None:
    service = OddsService()

    with pytest.raises(
        InvalidOddsRequestError
    ):
        await service.get_odds(
            sport_key="soccer_epl",
            regions=["invalid"],
        )


@pytest.mark.asyncio
async def test_rejects_invalid_featured_market() -> None:
    service = OddsService()

    with pytest.raises(
        InvalidOddsRequestError
    ):
        await service.get_odds(
            sport_key="soccer_epl",
            markets=["corners"],
        )