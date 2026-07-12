from pydantic import BaseModel, Field

from app.models.market_evaluation import (
    MarketEvaluationResult,
)


class MatchedOddsEvent(BaseModel):
    odds_event_id: str
    sport_key: str

    home_team: str
    away_team: str

    match_score: float = Field(
        ge=0,
        le=1,
    )


class AutomaticFixtureValueResult(BaseModel):
    fixture_id: int

    home_team: str
    away_team: str
    competition: str

    matched_event: MatchedOddsEvent

    model_confidence: float

    home_expected_goals: float
    away_expected_goals: float

    evaluation: MarketEvaluationResult

    odds_requests_remaining: int | None = None