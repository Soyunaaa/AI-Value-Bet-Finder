from app.models.prediction import MatchPredictionRequest
from app.services.prediction_service import predict_match


def test_prediction_probabilities_total_one() -> None:
    result = predict_match(
        MatchPredictionRequest(
            home_team="Liverpool",
            away_team="Arsenal",
            home_expected_goals=2.12,
            away_expected_goals=1.34,
        )
    )

    one_x_two_total = (
        result.home_win.probability
        + result.draw.probability
        + result.away_win.probability
    )

    goals_total = (
        result.over_2_5.probability
        + result.under_2_5.probability
    )

    btts_total = (
        result.both_teams_to_score_yes.probability
        + result.both_teams_to_score_no.probability
    )

    assert abs(one_x_two_total - 1) < 0.00001
    assert abs(goals_total - 1) < 0.00001
    assert abs(btts_total - 1) < 0.00001


def test_fair_odds_are_positive() -> None:
    result = predict_match(
        MatchPredictionRequest(
            home_team="Barcelona",
            away_team="Sevilla",
            home_expected_goals=2.31,
            away_expected_goals=0.86,
        )
    )

    assert result.home_win.fair_odds is not None
    assert result.home_win.fair_odds > 1
    assert result.over_2_5.fair_odds is not None
    assert result.over_2_5.fair_odds > 1