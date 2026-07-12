from typing import Any

import httpx

from app.config import get_settings
from app.models.odds import (
    OddsBookmaker,
    OddsEvent,
    OddsEventResponse,
    OddsMarket,
    OddsOutcome,
    OddsQuota,
    OddsResponse,
)
from app.providers.odds_base import OddsProvider


class OddsApiError(RuntimeError):
    pass


class TheOddsApiProvider(OddsProvider):
    def __init__(self) -> None:
        settings = get_settings()

        self.base_url = (
            settings.odds_api_base_url.rstrip("/")
        )
        self.api_key = settings.odds_api_key

    async def get_odds(
        self,
        *,
        sport_key: str,
        regions: list[str],
        markets: list[str],
        bookmakers: list[str] | None = None,
    ) -> OddsResponse:
        response = await self._request(
            path=f"/sports/{sport_key}/odds",
            regions=regions,
            markets=markets,
            bookmakers=bookmakers,
        )

        payload = response.json()

        if not isinstance(payload, list):
            raise OddsApiError(
                "The odds provider returned an invalid events list."
            )

        return OddsResponse(
            events=[
                self._map_event(event)
                for event in payload
            ],
            quota=self._map_quota(response),
        )

    async def get_event_odds(
        self,
        *,
        sport_key: str,
        event_id: str,
        regions: list[str],
        markets: list[str],
        bookmakers: list[str] | None = None,
    ) -> OddsEventResponse:
        response = await self._request(
            path=(
                f"/sports/{sport_key}/events/"
                f"{event_id}/odds"
            ),
            regions=regions,
            markets=markets,
            bookmakers=bookmakers,
        )

        payload = response.json()

        if not isinstance(payload, dict):
            raise OddsApiError(
                "The odds provider returned invalid event JSON."
            )

        return OddsEventResponse(
            event=self._map_event(payload),
            quota=self._map_quota(response),
        )

    async def _request(
        self,
        *,
        path: str,
        regions: list[str],
        markets: list[str],
        bookmakers: list[str] | None,
    ) -> httpx.Response:
        params = {
            "apiKey": self.api_key,
            "markets": ",".join(markets),
            "oddsFormat": "decimal",
            "dateFormat": "iso",
        }

        if bookmakers:
            params["bookmakers"] = ",".join(
                bookmakers
            )
        else:
            params["regions"] = ",".join(regions)

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=20.0,
            ) as client:
                response = await client.get(
                    path,
                    params=params,
                )
        except httpx.RequestError as exc:
            raise OddsApiError(
                "Unable to reach The Odds API."
            ) from exc

        if response.status_code == 401:
            raise OddsApiError(
                "The Odds API key is invalid."
            )

        if response.status_code == 404:
            raise OddsApiError(
                "The requested odds event was not found."
            )

        if response.status_code == 422:
            detail = self._extract_error(response)

            raise OddsApiError(
                f"The odds request was invalid: {detail}"
            )

        if response.status_code == 429:
            raise OddsApiError(
                "The Odds API request quota or rate limit "
                "has been reached."
            )

        if response.is_error:
            detail = self._extract_error(response)

            raise OddsApiError(
                "The odds provider returned status "
                f"{response.status_code}: {detail}"
            )

        return response

    @staticmethod
    def _extract_error(
        response: httpx.Response,
    ) -> str:
        try:
            body = response.json()

            if isinstance(body, dict):
                return str(
                    body.get("message")
                    or body.get("error")
                    or body
                )
        except ValueError:
            pass

        return response.text or "Unknown error"

    @staticmethod
    def _header_int(
        response: httpx.Response,
        name: str,
    ) -> int | None:
        raw_value = response.headers.get(name)

        if raw_value is None:
            return None

        try:
            return int(raw_value)
        except ValueError:
            return None

    def _map_quota(
        self,
        response: httpx.Response,
    ) -> OddsQuota:
        return OddsQuota(
            requests_remaining=self._header_int(
                response,
                "x-requests-remaining",
            ),
            requests_used=self._header_int(
                response,
                "x-requests-used",
            ),
            requests_last=self._header_int(
                response,
                "x-requests-last",
            ),
        )

    def _map_event(
        self,
        raw_event: dict[str, Any],
    ) -> OddsEvent:
        return OddsEvent(
            id=str(raw_event["id"]),
            sport_key=raw_event["sport_key"],
            sport_title=raw_event["sport_title"],
            commence_time=raw_event["commence_time"],
            home_team=raw_event["home_team"],
            away_team=raw_event["away_team"],
            bookmakers=[
                self._map_bookmaker(bookmaker)
                for bookmaker in raw_event.get(
                    "bookmakers",
                    [],
                )
            ],
        )

    def _map_bookmaker(
        self,
        raw_bookmaker: dict[str, Any],
    ) -> OddsBookmaker:
        return OddsBookmaker(
            key=raw_bookmaker["key"],
            title=raw_bookmaker["title"],
            last_update=raw_bookmaker.get(
                "last_update"
            ),
            markets=[
                self._map_market(market)
                for market in raw_bookmaker.get(
                    "markets",
                    [],
                )
            ],
        )

    def _map_market(
        self,
        raw_market: dict[str, Any],
    ) -> OddsMarket:
        return OddsMarket(
            key=raw_market["key"],
            last_update=raw_market["last_update"],
            outcomes=[
                OddsOutcome(
                    name=outcome["name"],
                    price=outcome["price"],
                    point=outcome.get("point"),
                    description=outcome.get(
                        "description"
                    ),
                )
                for outcome in raw_market.get(
                    "outcomes",
                    [],
                )
            ],
        )