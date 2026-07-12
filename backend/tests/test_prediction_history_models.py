from datetime import UTC, datetime

from app.database.models.prediction_history import (
    PredictionResultRecord,
    PredictionSnapshotRecord,
)


def test_prediction_snapshot_can_be_created() -> None:
    snapshot = PredictionSnapshotRecord(
        provider_match_id=123456,
        model_version="v1",
        competition_code="PL",
        competition_name="Premier League",
        kickoff_utc=datetime(
            2026,
            8,
            15,
            15,
            0,
            tzinfo=UTC,
        ),
        home_team_id=1,
        home_team_name="Arsenal",
        away_team_id=2,
        away_team_name="Chelsea",
        home_expected_goals=1.75,
        away_expected_goals=1.12,
        home_win_probability=0.51,
        draw_probability=0.25,
        away_win_probability=0.24,
        over_2_5_probability=0.55,
        under_2_5_probability=0.45,
        btts_yes_probability=0.52,
        btts_no_probability=0.48,
        most_likely_home_goals=1,
        most_likely_away_goals=1,
        confidence=72.5,
        home_elo=1610,
        away_elo=1560,
        goal_environment=1.04,
        home_advantage_multiplier=1.07,
        elo_home_advantage=60,
    )

    assert snapshot.provider_match_id == 123456
    assert snapshot.model_version == "v1"
    assert snapshot.home_win_probability == 0.51
    assert snapshot.home_elo == 1610


def test_prediction_result_can_be_created() -> None:
    result = PredictionResultRecord(
        snapshot_id=1,
        home_score=2,
        away_score=1,
        actual_outcome="HOME",
        predicted_outcome="HOME",
        correct_outcome=True,
        over_2_5_result=True,
        btts_result=True,
        most_likely_score_correct=False,
        brier_score_1x2=0.18,
        log_loss_1x2=0.67,
    )

    assert result.actual_outcome == "HOME"
    assert result.correct_outcome is True
    assert result.over_2_5_result is True