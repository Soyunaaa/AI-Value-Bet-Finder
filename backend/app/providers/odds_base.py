from abc import ABC, abstractmethod

from app.models.odds import OddsResponse


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