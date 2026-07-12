from abc import ABC, abstractmethod
from datetime import date

from app.models.football import FootballFixture


class FootballDataProvider(ABC):
    @abstractmethod
    async def get_matches(
        self,
        *,
        competition_code: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[FootballFixture]:
        raise NotImplementedError

    @abstractmethod
    async def get_match(
        self,
        match_id: int,
    ) -> FootballFixture:
        raise NotImplementedError

    @abstractmethod
    async def get_team_matches(
        self,
        team_id: int,
        *,
        status: str = "FINISHED",
        limit: int = 10,
    ) -> list[FootballFixture]:
        raise NotImplementedError