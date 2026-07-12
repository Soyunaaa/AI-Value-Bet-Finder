from pydantic import BaseModel, Field


class BookmakerOdds(BaseModel):
    name: str
    odds: float = Field(gt=1)


class ValueBet(BaseModel):
    id: int
    match: str
    league: str
    home_team: str
    away_team: str
    kickoff: str

    market: str
    bookmaker: str

    odds: float = Field(gt=1)
    model_probability: float = Field(gt=0, le=1)
    implied_probability: float = Field(gt=0, le=1)
    probability_edge: float
    fair_odds: float = Field(gt=1)
    expected_value: float
    confidence: float = Field(ge=0, le=100)

    full_kelly_fraction: float = Field(ge=0)
    recommended_kelly_fraction: float = Field(ge=0)
    recommended_stake: float = Field(ge=0)

    attack_rating: float = Field(ge=0, le=100)
    defence_rating: float = Field(ge=0, le=100)
    goals_rating: float = Field(ge=0, le=100)
    corners_rating: float = Field(ge=0, le=100)
    cards_rating: float = Field(ge=0, le=100)

    home_xg: float = Field(ge=0)
    away_xg: float = Field(ge=0)
    expected_corners: float = Field(ge=0)
    expected_cards: float = Field(ge=0)

    weather: str
    team_news: str

    reasons: list[str]
    bookmaker_odds: list[BookmakerOdds]