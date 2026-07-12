from datetime import datetime

from pydantic import BaseModel, Field


class PredictionSnapshotSaveResult(BaseModel):
    snapshot_id: int
    provider_match_id: int
    model_version: str

    created: bool
    captured_at: datetime


class PredictionSnapshotResponse(BaseModel):
    id: int

    provider_match_id: int
    model_version: str

    competition_code: str
    competition_name: str

    kickoff_utc: datetime

    home_team_id: int
    home_team_name: str

    away_team_id: int
    away_team_name: str

    home_expected_goals: float = Field(ge=0)
    away_expected_goals: float = Field(ge=0)

    home_win_probability: float = Field(
        ge=0,
        le=1,
    )
    draw_probability: float = Field(
        ge=0,
        le=1,
    )
    away_win_probability: float = Field(
        ge=0,
        le=1,
    )

    over_2_5_probability: float = Field(
        ge=0,
        le=1,
    )
    under_2_5_probability: float = Field(
        ge=0,
        le=1,
    )

    btts_yes_probability: float = Field(
        ge=0,
        le=1,
    )
    btts_no_probability: float = Field(
        ge=0,
        le=1,
    )

    most_likely_home_goals: int = Field(ge=0)
    most_likely_away_goals: int = Field(ge=0)

    confidence: float = Field(
        ge=0,
        le=100,
    )

    home_elo: float
    away_elo: float

    goal_environment: float
    home_advantage_multiplier: float
    elo_home_advantage: float

    captured_at: datetime


class PredictionGradingResult(BaseModel):
    competition_code: str | None = None

    snapshots_checked: int = Field(ge=0)
    predictions_graded: int = Field(ge=0)
    predictions_already_graded: int = Field(ge=0)
    predictions_waiting_for_result: int = Field(ge=0)


class PredictionPerformanceSummary(BaseModel):
    competition_code: str | None = None
    model_version: str | None = None

    predictions_graded: int = Field(ge=0)

    correct_outcomes: int = Field(ge=0)
    outcome_accuracy: float = Field(ge=0, le=1)

    exact_scores: int = Field(ge=0)
    exact_score_rate: float = Field(ge=0, le=1)

    average_brier_score: float = Field(ge=0)
    average_log_loss: float = Field(ge=0)

    over_2_5_results: int = Field(ge=0)
    btts_results: int = Field(ge=0)