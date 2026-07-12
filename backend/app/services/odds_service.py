from app.config import get_settings
from app.models.odds import (
    OddsEventResponse,
    OddsResponse,
)
from app.providers.the_odds_api import (
    TheOddsApiProvider,
)


FEATURED_MARKETS = {
    "h2h",
    "spreads",
    "totals",
}

EVENT_MARKETS = {
    "h2h",
    "spreads",
    "totals",
    "btts",
    "draw_no_bet",
    "double_chance",
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

    def _validate_regions(
        self,
        regions: list[str],
    ) -> None:
        invalid_regions = (
            set(regions) - SUPPORTED_REGIONS
        )

        if invalid_regions:
            raise InvalidOddsRequestError(
                "Unsupported odds regions: "
                + ", ".join(
                    sorted(invalid_regions)
                )
            )

    def _validate_markets(
        self,
        *,
        markets: list[str],
        allowed_markets: set[str],
    ) -> None:
        invalid_markets = (
            set(markets) - allowed_markets
        )

        if invalid_markets:
            raise InvalidOddsRequestError(
                "Unsupported odds markets: "
                + ", ".join(
                    sorted(invalid_markets)
                )
            )

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

        self._validate_regions(selected_regions)

        self._validate_markets(
            markets=selected_markets,
            allowed_markets=FEATURED_MARKETS,
        )

        return await self.provider.get_odds(
            sport_key=sport_key,
            regions=selected_regions,
            markets=selected_markets,
            bookmakers=bookmakers,
        )

    async def get_event_odds(
        self,
        *,
        sport_key: str,
        event_id: str,
        regions: list[str] | None = None,
        markets: list[str] | None = None,
        bookmakers: list[str] | None = None,
    ) -> OddsEventResponse:
        selected_regions = (
            regions or [self.default_region]
        )

        selected_markets = markets or [
            "h2h",
            "totals",
            "btts",
        ]

        self._validate_regions(selected_regions)

        self._validate_markets(
            markets=selected_markets,
            allowed_markets=EVENT_MARKETS,
        )

        return await self.provider.get_event_odds(
            sport_key=sport_key,
            event_id=event_id,
            regions=selected_regions,
            markets=selected_markets,
            bookmakers=bookmakers,
        )


def get_odds_service() -> OddsService:
    return OddsService()