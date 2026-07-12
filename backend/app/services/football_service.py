from datetime import date

from app.models.football import FootballFixture
from app.providers.football_data import (
    FootballDataOrgProvider,
)


class FootballService:
    def __init__(self) -> None:
        self.provider = FootballDataOrgProvider()

    async def get_matches(
        self,
        *,
        competition_code: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[FootballFixture]:
        return await self.provider.get_matches(
            competition_code=competition_code,
            date_from=date_from,
            date_to=date_to,
        )


def get_football_service() -> FootballService:
    return FootballService()