import pytest

from app.services.prediction.league_calibration import (
    DEFAULT_CALIBRATION,
    get_league_calibration,
)


def test_returns_premier_league_calibration() -> None:
    calibration = get_league_calibration(
        "PL"
    )

    assert calibration.competition_code == "PL"
    assert calibration.goal_environment > 0
    assert (
        calibration.home_advantage_multiplier
        > 1
    )


def test_normalizes_lowercase_code() -> None:
    calibration = get_league_calibration(
        "bl1"
    )

    assert calibration.competition_code == "BL1"


def test_unknown_competition_uses_default() -> None:
    calibration = get_league_calibration(
        "UNKNOWN"
    )

    assert calibration == DEFAULT_CALIBRATION


def test_missing_competition_uses_default() -> None:
    calibration = get_league_calibration(
        None
    )

    assert calibration == DEFAULT_CALIBRATION


@pytest.mark.parametrize(
    "competition_code",
    [
        "PL",
        "PD",
        "BL1",
        "SA",
        "FL1",
        "CL",
    ],
)
def test_calibrations_are_within_safe_ranges(
    competition_code: str,
) -> None:
    calibration = get_league_calibration(
        competition_code
    )

    assert (
        0.85
        <= calibration.goal_environment
        <= 1.15
    )

    assert (
        1.0
        <= calibration.home_advantage_multiplier
        <= 1.15
    )

    assert (
        0
        <= calibration.elo_home_advantage
        <= 100
    )