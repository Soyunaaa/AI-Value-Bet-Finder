from datetime import datetime

from pydantic import BaseModel, Field


class OddsOutcome(BaseModel):
    name: str
    price: float = Field(gt=1)
    point: float | None = None


class OddsMarket(BaseModel):
    key: str
    last_update: datetime
    outcomes: list[OddsOutcome]


class OddsBookmaker(BaseModel):
    key: str
    title: str
    last_update: datetime
    markets: list[OddsMarket]


class OddsEvent(BaseModel):
    id: str
    sport_key: str
    sport_title: str
    commence_time: datetime

    home_team: str
    away_team: str

    bookmakers: list[OddsBookmaker]


class OddsQuota(BaseModel):
    requests_remaining: int | None = None
    requests_used: int | None = None
    requests_last: int | None = None


class OddsResponse(BaseModel):
    events: list[OddsEvent]
    quota: OddsQuota