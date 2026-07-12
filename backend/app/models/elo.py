from pydantic import BaseModel, Field


class TeamEloRating(BaseModel):
    team_id: int
    team_name: str

    rating: float = Field(gt=0)
    matches_processed: int = Field(ge=0)


class FixtureEloSummary(BaseModel):
    home: TeamEloRating
    away: TeamEloRating

    rating_difference: float
    expected_home_score: float = Field(ge=0, le=1)
    expected_away_score: float = Field(ge=0, le=1)