import pytest

from app.models.prediction import (
    MarketProbability,
    MatchPredictionResult,
    ScoreProbability,
)

from app.services.fixture_value_service import (
    UnsupportedMarketSelectionError,
    probability_for_selection,
)


def create_prediction() -> MatchPredictionResult:
    return MatchPredictionResult(
        home_team="Liverpool",
        away_team="Arsenal",
        home_expected_goals=2.0,
        away_expected_goals=1.2,
        total_expected_goals=3.2,

        home_win=MarketProbability(
            probability=0.58,
            fair_odds=1.7241,
        ),
        draw=MarketProbability(
            probability=0.22,
            fair_odds=4.5455,
        ),
        away_win=MarketProbability(
            probability=0.20,
            fair_odds=5.0,
        ),

        over_2_5=MarketProbability(
            probability=0.62,
            fair_odds=1.6129,
        ),
        under_2_5=MarketProbability(
            probability=0.38,
            fair_odds=2.6316,
        ),

        both_teams_to_score_yes=MarketProbability(
            probability=0.57,
            fair_odds=1.7544,
        ),
        both_teams_to_score_no=MarketProbability(
            probability=0.43,
            fair_odds=2.3256,
        ),

        most_likely_score=ScoreProbability(
            home_goals=2,
            away_goals=1,
            probability=0.12,
        ),

        score_probabilities=[],
    )


def test_maps_one_x_two_probabilities() -> None:
    prediction = create_prediction()

    home_probability = probability_for_selection(
        prediction=prediction,
        market="1X2",
        selection="Home Win",
    )

    draw_probability = probability_for_selection(
        prediction=prediction,
        market="Match Result",
        selection="Draw",
    )

    away_probability = probability_for_selection(
        prediction=prediction,
        market="1X2",
        selection="Away",
    )

    assert home_probability == pytest.approx(0.58)
    assert draw_probability == pytest.approx(0.22)
    assert away_probability == pytest.approx(0.20)


def test_maps_goals_and_btts_probabilities() -> None:
    prediction = create_prediction()

    over_probability = probability_for_selection(
        prediction=prediction,
        market="Goals",
        selection="Over 2.5",
    )

    btts_probability = probability_for_selection(
        prediction=prediction,
        market="BTTS",
        selection="Yes",
    )

    assert over_probability == pytest.approx(0.62)
    assert btts_probability == pytest.approx(0.57)


def test_rejects_unsupported_market() -> None:
    prediction = create_prediction()

    with pytest.raises(
        UnsupportedMarketSelectionError
    ):
        probability_for_selection(
            prediction=prediction,
            market="Corners",
            selection="Over 9.5",
        )