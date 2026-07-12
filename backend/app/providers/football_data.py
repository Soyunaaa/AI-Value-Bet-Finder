from datetime import date
from typing import Any

import httpx

from app.config import get_settings
from app.models.football import (
    FootballCompetition,
    FootballFixture,
    FootballScore,
    FootballTeam,
    MatchStatus,
)
from app.providers.base import FootballDataProvider


class FootballDataApiError(RuntimeError):
    pass


class FootballDataOrgProvider(FootballDataProvider):
    def __init__(self) -> None:
        settings = get_settings()

        self.base_url = (
            settings.football_data_base_url.rstrip("/")
        )
        self.api_key = settings.football_data_api_key

    async def get_matches(
        self,
        *,
        competition_code: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[FootballFixture]:
        if competition_code:
            path = (
                f"/competitions/"
                f"{competition_code.upper()}/matches"
            )
        else:
            path = "/matches"

        params: dict[str, str] = {}

        if date_from is not None:
            params["dateFrom"] = date_from.isoformat()

        if date_to is not None:
            params["dateTo"] = date_to.isoformat()

        payload = await self._get(path, params=params)

        raw_matches = payload.get("matches", [])

        if not isinstance(raw_matches, list):
            raise FootballDataApiError(
                "Football provider returned an invalid matches list."
            )

        return [
            self._map_fixture(raw_match)
            for raw_match in raw_matches
        ]
    async def get_match(
        self,
        match_id: int,
    ) -> FootballFixture:
        payload = await self._get(
            f"/matches/{match_id}"
        )

        return self._map_fixture(payload)

    async def get_team_matches(
        self,
        team_id: int,
        *,
        status: str = "FINISHED",
        limit: int = 10,
    ) -> list[FootballFixture]:
        payload = await self._get(
            f"/teams/{team_id}/matches",
            params={
                "status": status,
                "limit": str(limit),
            },
        )

        raw_matches = payload.get("matches", [])

        if not isinstance(raw_matches, list):
            raise FootballDataApiError(
                "Football provider returned an invalid "
                "team matches list."
            )

        return [
            self._map_fixture(raw_match)
            for raw_match in raw_matches
        ]
    async def _get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        headers = {
            "X-Auth-Token": self.api_key,
        }

        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=15.0,
            ) as client:
                response = await client.get(
                    path,
                    params=params,
                )
        except httpx.RequestError as exc:
            raise FootballDataApiError(
                "Unable to reach football-data.org."
            ) from exc

        if response.status_code == 401:
            raise FootballDataApiError(
                "The football-data.org API token is invalid."
            )

        if response.status_code == 403:
            raise FootballDataApiError(
                "Your football-data.org plan cannot access "
                "this resource."
            )

        if response.status_code == 429:
            raise FootballDataApiError(
                "The football-data.org request limit was reached."
            )

        if response.is_error:
            raise FootballDataApiError(
                "Football provider request failed with "
                f"status {response.status_code}."
            )

        result = response.json()

        if not isinstance(result, dict):
            raise FootballDataApiError(
                "Football provider returned invalid JSON."
            )

        return result

    def _map_fixture(
        self,
        raw_match: dict[str, Any],
    ) -> FootballFixture:
        competition = raw_match.get("competition", {})
        home_team = raw_match.get("homeTeam", {})
        away_team = raw_match.get("awayTeam", {})
        score = raw_match.get("score", {})

        full_time = score.get("fullTime") or {}
        half_time = score.get("halfTime") or {}

        raw_status = raw_match.get("status", "UNKNOWN")

        try:
            status = MatchStatus(raw_status)
        except ValueError:
            status = MatchStatus.unknown

        return FootballFixture(
            id=raw_match["id"],
            utc_date=raw_match["utcDate"],
            status=status,
            matchday=raw_match.get("matchday"),
            competition=FootballCompetition(
                id=competition["id"],
                code=competition.get("code", ""),
                name=competition.get("name", "Unknown"),
                emblem=competition.get("emblem"),
            ),
            home_team=FootballTeam(
                id=home_team["id"],
                name=home_team.get("name", "Unknown"),
                short_name=home_team.get("shortName"),
                tla=home_team.get("tla"),
                crest=home_team.get("crest"),
            ),
            away_team=FootballTeam(
                id=away_team["id"],
                name=away_team.get("name", "Unknown"),
                short_name=away_team.get("shortName"),
                tla=away_team.get("tla"),
                crest=away_team.get("crest"),
            ),
            full_time=FootballScore(
                home=full_time.get("home"),
                away=full_time.get("away"),
            ),
            half_time=FootballScore(
                home=half_time.get("home"),
                away=half_time.get("away"),
            ),
        )