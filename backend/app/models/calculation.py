from pydantic import BaseModel, Field


class OddsSelection(BaseModel):
    name: str
    odds: float = Field(gt=1)


class MarginRemovalRequest(BaseModel):
    selections: list[OddsSelection]


class MarginRemovalResult(BaseModel):
    name: str
    odds: float
    raw_probability: float
    fair_probability: float
    fair_odds: float


class ValueCalculationRequest(BaseModel):
    bookmaker_odds: float = Field(gt=1)
    model_probability: float = Field(gt=0, le=1)
    bankroll: float = Field(default=1000, gt=0)
    kelly_fraction: float = Field(default=0.25, gt=0, le=1)


class ValueCalculationResult(BaseModel):
    bookmaker_odds: float
    model_probability: float
    implied_probability: float
    fair_odds: float
    expected_value: float
    probability_edge: float
    full_kelly_fraction: float
    recommended_kelly_fraction: float
    recommended_stake: float