from pydantic import BaseModel, Field

from app.models.market_evaluation import (
    MarketEvaluationResult,
)


class FixtureOddsInput(BaseModel):
    market: str = Field(min_length=1)
    selection: str = Field(min_length=1)
    bookmaker: str = Field(min_length=1)
    bookmaker_odds: float = Field(gt=1)


class FixtureValueRequest(BaseModel):
    bankroll: float = Field(
        default=1000,
        gt=0,
    )

    kelly_fraction: float = Field(
        default=0.25,
        gt=0,
        le=1,
    )

    minimum_expected_value: float = Field(
        default=0.05,
        description=(
            "Minimum EV expressed as a decimal. "
            "For example, 0.05 means 5%."
        ),
    )

    odds: list[FixtureOddsInput] = Field(
        min_length=1,
    )


class FixtureValueResult(BaseModel):
    fixture_id: int

    home_team: str
    away_team: str
    competition: str

    model_confidence: float

    home_expected_goals: float
    away_expected_goals: float

    evaluation: MarketEvaluationResult