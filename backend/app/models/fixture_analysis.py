from pydantic import BaseModel, Field

from app.models.football import FootballFixture
from app.models.prediction import MatchPredictionResult
from app.models.team_strength import TeamStrengthRating
from app.models.elo import FixtureEloSummary

class TeamFormSummary(BaseModel):
    team_id: int
    team_name: str
    matches_used: int

    wins: int
    draws: int
    losses: int

    goals_scored: int
    goals_conceded: int

    average_goals_scored: float = Field(ge=0)
    average_goals_conceded: float = Field(ge=0)
    points_per_game: float = Field(ge=0)


class FixtureAnalysisResult(BaseModel):
    fixture: FootballFixture

    home_form: TeamFormSummary
    away_form: TeamFormSummary

    home_strength: TeamStrengthRating
    away_strength: TeamStrengthRating

    elo: FixtureEloSummary
    
    home_expected_goals: float = Field(ge=0)
    away_expected_goals: float = Field(ge=0)
  
    prediction: MatchPredictionResult

    confidence: float = Field(ge=0, le=100)
    reasons: list[str]