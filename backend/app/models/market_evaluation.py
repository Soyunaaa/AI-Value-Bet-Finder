from pydantic import BaseModel, Field


class MarketSelectionInput(BaseModel):
    market: str = Field(min_length=1)
    selection: str = Field(min_length=1)
    bookmaker: str = Field(min_length=1)

    bookmaker_odds: float = Field(gt=1)
    model_probability: float = Field(gt=0, le=1)


class MarketEvaluationRequest(BaseModel):
    fixture_id: int | None = Field(default=None, gt=0)

    bankroll: float = Field(default=1000, gt=0)

    kelly_fraction: float = Field(
        default=0.25,
        gt=0,
        le=1,
    )

    minimum_expected_value: float = Field(
        default=0,
        description=(
            "Minimum expected value expressed as a decimal. "
            "For example, 0.05 means 5%."
        ),
    )

    selections: list[MarketSelectionInput] = Field(
        min_length=1,
    )


class PositiveValueSelection(BaseModel):
    fixture_id: int | None

    market: str
    selection: str
    bookmaker: str

    bookmaker_odds: float
    model_probability: float
    implied_probability: float
    probability_edge: float

    fair_odds: float
    expected_value: float

    full_kelly_fraction: float
    recommended_kelly_fraction: float
    recommended_stake: float


class MarketEvaluationResult(BaseModel):
    fixture_id: int | None

    selections_evaluated: int
    positive_value_count: int

    minimum_expected_value: float

    positive_value_selections: list[
        PositiveValueSelection
    ]