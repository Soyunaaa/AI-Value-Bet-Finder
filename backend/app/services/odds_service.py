from app.config import get_settings
from app.models.odds import OddsResponse
from app.providers.the_odds_api import (
    TheOddsApiProvider,
)


SUPPORTED_MARKETS = {
    "h2h",
    "spreads",
    "totals",
}

SUPPORTED_REGIONS = {
    "uk",
    "eu",
    "us",
    "us2",
    "au",
}


class InvalidOddsRequestError(ValueError):
    pass


class OddsService:
    def __init__(self) -> None:
        settings = get_settings()

        self.default_region = (
            settings.odds_api_default_region
        )
        self.provider = TheOddsApiProvider()

    async def get_odds(
        self,
        *,
        sport_key: str,
        regions: list[str] | None = None,
        markets: list[str] | None = None,
        bookmakers: list[str] | None = None,
    ) -> OddsResponse:
        selected_regions = (
            regions or [self.default_region]
        )

        selected_markets = markets or ["h2h"]

        invalid_regions = set(
            selected_regions
        ) - SUPPORTED_REGIONS

        if invalid_regions:
            raise InvalidOddsRequestError(
                "Unsupported odds regions: "
                + ", ".join(
                    sorted(invalid_regions)
                )
            )

        invalid_markets = set(
            selected_markets
        ) - SUPPORTED_MARKETS

        if invalid_markets:
            raise InvalidOddsRequestError(
                "Unsupported featured markets: "
                + ", ".join(
                    sorted(invalid_markets)
                )
            )

        return await self.provider.get_odds(
            sport_key=sport_key,
            regions=selected_regions,
            markets=selected_markets,
            bookmakers=bookmakers,
        )


def get_odds_service() -> OddsService:
    return OddsService()