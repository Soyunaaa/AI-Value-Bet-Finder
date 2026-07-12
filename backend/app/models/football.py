from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class MatchStatus(StrEnum):
    scheduled = "SCHEDULED"
    timed = "TIMED"
    in_play = "IN_PLAY"
    paused = "PAUSED"
    finished = "FINISHED"
    postponed = "POSTPONED"
    suspended = "SUSPENDED"
    cancelled = "CANCELLED"
    unknown = "UNKNOWN"


class FootballTeam(BaseModel):
    id: int
    name: str
    short_name: str | None = None
    tla: str | None = None
    crest: str | None = None


class FootballCompetition(BaseModel):
    id: int
    code: str
    name: str
    emblem: str | None = None


class FootballScore(BaseModel):
    home: int | None = None
    away: int | None = None


class FootballFixture(BaseModel):
    id: int
    utc_date: datetime
    status: MatchStatus
    matchday: int | None = None

    competition: FootballCompetition
    home_team: FootballTeam
    away_team: FootballTeam

    full_time: FootballScore
    half_time: FootballScore