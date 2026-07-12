import pytest

from app.services.prediction.kelly import (
    calculate_fractional_kelly,
    calculate_full_kelly_fraction,
    calculate_kelly_stake,
)

from app.services.prediction.value import (
    calculate_expected_value,
    calculate_probability_edge,
    decimal_odds_to_probability,
    probability_to_fair_odds,
    remove_proportional_margin,
)


def test_probability_and_fair_odds() -> None:
    implied_probability = (
        decimal_odds_to_probability(2.0)
    )

    fair_odds = probability_to_fair_odds(
        implied_probability
    )

    assert implied_probability == pytest.approx(0.5)
    assert fair_odds == pytest.approx(2.0)


def test_positive_expected_value() -> None:
    expected_value = calculate_expected_value(
        model_probability=0.58,
        decimal_odds=2.05,
    )

    edge = calculate_probability_edge(
        model_probability=0.58,
        implied_probability=1 / 2.05,
    )

    assert expected_value == pytest.approx(
        0.189,
        abs=0.000001,
    )

    assert edge > 0


def test_margin_removed_probabilities_total_one() -> None:
    fair_probabilities = remove_proportional_margin(
        [2.10, 3.40, 3.60]
    )

    assert sum(fair_probabilities) == pytest.approx(
        1.0,
        abs=0.000001,
    )


def test_quarter_kelly_stake() -> None:
    full_kelly = calculate_full_kelly_fraction(
        decimal_odds=2.05,
        model_probability=0.58,
    )

    quarter_kelly = calculate_fractional_kelly(
        full_kelly_fraction=full_kelly,
        multiplier=0.25,
    )

    stake = calculate_kelly_stake(
        bankroll=1000,
        kelly_fraction=quarter_kelly,
    )

    assert full_kelly == pytest.approx(
        0.18,
        abs=0.000001,
    )

    assert quarter_kelly == pytest.approx(
        0.045,
        abs=0.000001,
    )

    assert stake == pytest.approx(45.0)