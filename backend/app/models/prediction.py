from pydantic import BaseModel, Field


class MatchPredictionRequest(BaseModel):
    home_team: str
    away_team: str

    home_expected_goals: float = Field(ge=0, le=10)
    away_expected_goals: float = Field(ge=0, le=10)

    max_goals: int = Field(default=10, ge=5, le=15)


class MarketProbability(BaseModel):
    probability: float = Field(ge=0, le=1)
    fair_odds: float | None


class ScoreProbability(BaseModel):
    home_goals: int
    away_goals: int
    probability: float = Field(ge=0, le=1)


class MatchPredictionResult(BaseModel):
    home_team: str
    away_team: str

    home_expected_goals: float
    away_expected_goals: float
    total_expected_goals: float

    home_win: MarketProbability
    draw: MarketProbability
    away_win: MarketProbability

    over_2_5: MarketProbability
    under_2_5: MarketProbability

    both_teams_to_score_yes: MarketProbability
    both_teams_to_score_no: MarketProbability

    most_likely_score: ScoreProbability
    score_probabilities: list[ScoreProbability]