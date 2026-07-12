from datetime import datetime

from pydantic import BaseModel, Field


class DatabaseStatus(BaseModel):
    connected: bool
    database_type: str
    matches_stored: int


class TeamStatisticsBuildResult(BaseModel):
    competition_code: str

    matches_processed: int = Field(ge=0)
    teams_created: int = Field(ge=0)
    teams_updated: int = Field(ge=0)
    teams_total: int = Field(ge=0)


class EloBuildResult(BaseModel):
    competition_code: str

    matches_processed: int = Field(ge=0)
    teams_rated: int = Field(ge=0)
    history_rows_created: int = Field(ge=0)


class LeagueStatisticsBuildResult(BaseModel):
    competition_code: str
    matches_processed: int = Field(ge=0)
    statistics_created: bool


class FixtureSyncResult(BaseModel):
    competition_code: str

    fixtures_received: int = Field(ge=0)
    fixtures_inserted: int = Field(ge=0)
    fixtures_updated: int = Field(ge=0)
    fixtures_unchanged: int = Field(ge=0)

    total_matches_stored: int = Field(ge=0)

    statistics_rebuilt: bool
    statistics: TeamStatisticsBuildResult | None = None

    elo_rebuilt: bool
    elo: EloBuildResult | None = None

    league_statistics_rebuilt: bool
    league_statistics: (
        LeagueStatisticsBuildResult | None
    ) = None


class TeamStatisticsResponse(BaseModel):
    team_id: int
    team_name: str

    competition_code: str
    competition_name: str

    matches_played: int

    wins: int
    draws: int
    losses: int

    goals_scored: int
    goals_conceded: int

    points_per_game: float
    average_goals_scored: float
    average_goals_conceded: float

    home_average_scored: float
    home_average_conceded: float

    away_average_scored: float
    away_average_conceded: float

    last_five_form: str
    last_ten_form: str


class TeamEloResponse(BaseModel):
    team_id: int
    team_name: str
    competition_code: str

    rating: float
    matches_processed: int
    updated_at: datetime


class EloHistoryResponse(BaseModel):
    provider_match_id: int
    competition_code: str
    kickoff_utc: datetime

    team_id: int
    team_name: str

    opponent_team_id: int
    opponent_team_name: str

    venue: str
    result: str

    rating_before: float
    rating_after: float
    rating_change: float


class LeagueStatisticsResponse(BaseModel):
    competition_code: str
    competition_name: str

    matches_played: int

    average_goals: float
    average_home_goals: float
    average_away_goals: float

    home_win_rate: float
    draw_rate: float
    away_win_rate: float

    over_2_5_rate: float
    btts_rate: float

    goal_environment: float
    home_advantage_multiplier: float
    elo_home_advantage: float