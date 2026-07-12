from abc import ABC, abstractmethod

from app.models.odds import (
    OddsEventResponse,
    OddsResponse,
)


class OddsProvider(ABC):
    @abstractmethod
    async def get_odds(
        self,
        *,
        sport_key: str,
        regions: list[str],
        markets: list[str],
        bookmakers: list[str] | None = None,
    ) -> OddsResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_event_odds(
        self,
        *,
        sport_key: str,
        event_id: str,
        regions: list[str],
        markets: list[str],
        bookmakers: list[str] | None = None,
    ) -> OddsEventResponse:
        raise NotImplementedError