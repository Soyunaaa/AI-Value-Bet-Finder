from math import exp, factorial

from app.models.prediction import (
    MarketProbability,
    MatchPredictionRequest,
    MatchPredictionResult,
    ScoreProbability,
)


def poisson_probability(
    expected_goals: float,
    goals: int,
) -> float:
    return (
        exp(-expected_goals)
        * expected_goals**goals
        / factorial(goals)
    )


def probability_to_fair_odds(
    probability: float,
) -> float | None:
    if probability <= 0:
        return None

    return round(1 / probability, 4)


def create_market_probability(
    probability: float,
) -> MarketProbability:
    rounded_probability = round(probability, 6)

    return MarketProbability(
        probability=rounded_probability,
        fair_odds=probability_to_fair_odds(
            rounded_probability
        ),
    )


def predict_match(
    request: MatchPredictionRequest,
) -> MatchPredictionResult:
    score_probabilities: list[ScoreProbability] = []

    home_win_probability = 0.0
    draw_probability = 0.0
    away_win_probability = 0.0

    over_2_5_probability = 0.0
    btts_yes_probability = 0.0

    for home_goals in range(request.max_goals + 1):
        home_probability = poisson_probability(
            request.home_expected_goals,
            home_goals,
        )

        for away_goals in range(request.max_goals + 1):
            away_probability = poisson_probability(
                request.away_expected_goals,
                away_goals,
            )

            score_probability = (
                home_probability * away_probability
            )

            score_probabilities.append(
                ScoreProbability(
                    home_goals=home_goals,
                    away_goals=away_goals,
                    probability=round(
                        score_probability,
                        8,
                    ),
                )
            )

            if home_goals > away_goals:
                home_win_probability += score_probability
            elif home_goals == away_goals:
                draw_probability += score_probability
            else:
                away_win_probability += score_probability

            if home_goals + away_goals >= 3:
                over_2_5_probability += score_probability

            if home_goals > 0 and away_goals > 0:
                btts_yes_probability += score_probability

    total_probability = sum(
        score.probability
        for score in score_probabilities
    )

    if total_probability <= 0:
        raise ValueError(
            "The score probability distribution is empty."
        )

    # The score grid is truncated at max_goals, so normalize
    # the probabilities back to a total of 1.
    home_win_probability /= total_probability
    draw_probability /= total_probability
    away_win_probability /= total_probability
    over_2_5_probability /= total_probability
    btts_yes_probability /= total_probability

    under_2_5_probability = (
        1 - over_2_5_probability
    )

    btts_no_probability = (
        1 - btts_yes_probability
    )

    normalized_scores = [
        ScoreProbability(
            home_goals=score.home_goals,
            away_goals=score.away_goals,
            probability=round(
                score.probability / total_probability,
                8,
            ),
        )
        for score in score_probabilities
    ]

    sorted_scores = sorted(
        normalized_scores,
        key=lambda score: score.probability,
        reverse=True,
    )

    most_likely_score = sorted_scores[0]

    return MatchPredictionResult(
        home_team=request.home_team,
        away_team=request.away_team,
        home_expected_goals=(
            request.home_expected_goals
        ),
        away_expected_goals=(
            request.away_expected_goals
        ),
        total_expected_goals=round(
            request.home_expected_goals
            + request.away_expected_goals,
            4,
        ),
        home_win=create_market_probability(
            home_win_probability
        ),
        draw=create_market_probability(
            draw_probability
        ),
        away_win=create_market_probability(
            away_win_probability
        ),
        over_2_5=create_market_probability(
            over_2_5_probability
        ),
        under_2_5=create_market_probability(
            under_2_5_probability
        ),
        both_teams_to_score_yes=(
            create_market_probability(
                btts_yes_probability
            )
        ),
        both_teams_to_score_no=(
            create_market_probability(
                btts_no_probability
            )
        ),
        most_likely_score=most_likely_score,
        score_probabilities=sorted_scores[:10],
    )