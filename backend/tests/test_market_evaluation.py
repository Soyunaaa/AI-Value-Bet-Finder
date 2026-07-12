import pytest

from app.models.market_evaluation import (
    MarketEvaluationRequest,
    MarketSelectionInput,
)

from app.services.market_evaluation_service import (
    evaluate_markets,
)


def test_only_positive_value_selections_returned() -> None:
    request = MarketEvaluationRequest(
        fixture_id=12345,
        bankroll=1000,
        kelly_fraction=0.25,
        minimum_expected_value=0,
        selections=[
            MarketSelectionInput(
                market="1X2",
                selection="Home Win",
                bookmaker="Pinnacle",
                bookmaker_odds=2.20,
                model_probability=0.58,
            ),
            MarketSelectionInput(
                market="1X2",
                selection="Draw",
                bookmaker="Pinnacle",
                bookmaker_odds=3.20,
                model_probability=0.22,
            ),
            MarketSelectionInput(
                market="1X2",
                selection="Away Win",
                bookmaker="Pinnacle",
                bookmaker_odds=3.50,
                model_probability=0.20,
            ),
        ],
    )

    result = evaluate_markets(request)

    assert result.selections_evaluated == 3
    assert result.positive_value_count == 1

    positive_selection = (
        result.positive_value_selections[0]
    )

    assert (
        positive_selection.selection
        == "Home Win"
    )

    assert (
        positive_selection.expected_value
        == pytest.approx(
            0.276,
            abs=0.000001,
        )
    )


def test_minimum_ev_filter() -> None:
    request = MarketEvaluationRequest(
        bankroll=500,
        kelly_fraction=0.25,
        minimum_expected_value=0.10,
        selections=[
            MarketSelectionInput(
                market="Goals",
                selection="Over 2.5",
                bookmaker="Bet365",
                bookmaker_odds=1.90,
                model_probability=0.55,
            ),
            MarketSelectionInput(
                market="BTTS",
                selection="Yes",
                bookmaker="Betfair",
                bookmaker_odds=2.10,
                model_probability=0.60,
            ),
        ],
    )

    result = evaluate_markets(request)

    assert result.positive_value_count == 1

    assert (
        result.positive_value_selections[0]
        .selection
        == "Yes"
    )


def test_results_sorted_by_expected_value() -> None:
    request = MarketEvaluationRequest(
        selections=[
            MarketSelectionInput(
                market="Goals",
                selection="Over 2.5",
                bookmaker="Pinnacle",
                bookmaker_odds=2.00,
                model_probability=0.56,
            ),
            MarketSelectionInput(
                market="Corners",
                selection="Over 9.5",
                bookmaker="Bet365",
                bookmaker_odds=2.20,
                model_probability=0.58,
            ),
        ],
    )

    result = evaluate_markets(request)

    assert result.positive_value_count == 2

    first = result.positive_value_selections[0]
    second = result.positive_value_selections[1]

    assert (
        first.expected_value
        >= second.expected_value
    )