import pytest

from app.services.persistent_elo_service import (
    calculate_elo_changes,
    result_labels,
    result_scores,
)


def test_home_win_result_values() -> None:
    home_score, away_score = result_scores(
        home_goals=2,
        away_goals=0,
    )

    home_label, away_label = result_labels(
        home_goals=2,
        away_goals=0,
    )

    assert home_score == 1.0
    assert away_score == 0.0
    assert home_label == "W"
    assert away_label == "L"


def test_draw_result_values() -> None:
    home_score, away_score = result_scores(
        home_goals=1,
        away_goals=1,
    )

    assert home_score == 0.5
    assert away_score == 0.5


def test_home_winner_gains_rating() -> None:
    changes = calculate_elo_changes(
        home_rating=1500,
        away_rating=1500,
        home_goals=2,
        away_goals=0,
        home_advantage_elo=60,
    )

    assert changes.home_change > 0
    assert changes.away_change < 0

    assert changes.home_change == pytest.approx(
        -changes.away_change
    )


def test_underdog_win_creates_larger_change() -> None:
    underdog_win = calculate_elo_changes(
        home_rating=1400,
        away_rating=1600,
        home_goals=1,
        away_goals=0,
        home_advantage_elo=60,
    )

    favourite_win = calculate_elo_changes(
        home_rating=1600,
        away_rating=1400,
        home_goals=1,
        away_goals=0,
        home_advantage_elo=60,
    )

    assert (
        underdog_win.home_change
        > favourite_win.home_change
    )