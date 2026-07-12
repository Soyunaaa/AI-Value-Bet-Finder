import math

import pytest

from app.services.prediction_grading_service import (
    actual_outcome,
    brier_score_1x2,
    log_loss_1x2,
    predicted_outcome,
)


def test_actual_home_outcome() -> None:
    assert (
        actual_outcome(
            home_score=2,
            away_score=1,
        )
        == "HOME"
    )


def test_actual_draw_outcome() -> None:
    assert (
        actual_outcome(
            home_score=1,
            away_score=1,
        )
        == "DRAW"
    )


def test_predicted_outcome_uses_highest_probability(
) -> None:
    result = predicted_outcome(
        home_probability=0.51,
        draw_probability=0.27,
        away_probability=0.22,
    )

    assert result == "HOME"


def test_perfect_prediction_has_zero_brier() -> None:
    score = brier_score_1x2(
        home_probability=1.0,
        draw_probability=0.0,
        away_probability=0.0,
        outcome="HOME",
    )

    assert score == 0.0


def test_log_loss_uses_actual_probability() -> None:
    score = log_loss_1x2(
        home_probability=0.5,
        draw_probability=0.3,
        away_probability=0.2,
        outcome="HOME",
    )

    assert score == pytest.approx(
        -math.log(0.5),
        abs=1e-6,
    )