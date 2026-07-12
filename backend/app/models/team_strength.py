from pydantic import BaseModel, Field


class TeamStrengthRating(BaseModel):
    team_id: int
    team_name: str

    matches_used: int

    attack_rating: float = Field(ge=0, le=100)
    defence_rating: float = Field(ge=0, le=100)
    form_rating: float = Field(ge=0, le=100)
    overall_rating: float = Field(ge=0, le=100)

    average_goals_scored: float = Field(ge=0)
    average_goals_conceded: float = Field(ge=0)
    points_per_game: float = Field(ge=0)

    home_average_scored: float = Field(ge=0)
    home_average_conceded: float = Field(ge=0)

    away_average_scored: float = Field(ge=0)
    away_average_conceded: float = Field(ge=0)