from app.models.market_evaluation import (
    MarketEvaluationRequest,
    MarketEvaluationResult,
    PositiveValueSelection,
)

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
)


def evaluate_markets(
    request: MarketEvaluationRequest,
) -> MarketEvaluationResult:
    positive_selections: list[
        PositiveValueSelection
    ] = []

    for selection in request.selections:
        implied_probability = (
            decimal_odds_to_probability(
                selection.bookmaker_odds
            )
        )

        fair_odds = probability_to_fair_odds(
            selection.model_probability
        )

        probability_edge = (
            calculate_probability_edge(
                model_probability=(
                    selection.model_probability
                ),
                implied_probability=(
                    implied_probability
                ),
            )
        )

        expected_value = calculate_expected_value(
            model_probability=(
                selection.model_probability
            ),
            decimal_odds=selection.bookmaker_odds,
        )

        if (
            expected_value
            < request.minimum_expected_value
        ):
            continue

        full_kelly_fraction = (
            calculate_full_kelly_fraction(
                decimal_odds=(
                    selection.bookmaker_odds
                ),
                model_probability=(
                    selection.model_probability
                ),
            )
        )

        recommended_kelly_fraction = (
            calculate_fractional_kelly(
                full_kelly_fraction=(
                    full_kelly_fraction
                ),
                multiplier=request.kelly_fraction,
            )
        )

        recommended_stake = calculate_kelly_stake(
            bankroll=request.bankroll,
            kelly_fraction=(
                recommended_kelly_fraction
            ),
        )

        positive_selections.append(
            PositiveValueSelection(
                fixture_id=request.fixture_id,
                market=selection.market,
                selection=selection.selection,
                bookmaker=selection.bookmaker,
                bookmaker_odds=(
                    selection.bookmaker_odds
                ),
                model_probability=round(
                    selection.model_probability,
                    6,
                ),
                implied_probability=round(
                    implied_probability,
                    6,
                ),
                probability_edge=round(
                    probability_edge,
                    6,
                ),
                fair_odds=round(
                    fair_odds,
                    4,
                ),
                expected_value=round(
                    expected_value,
                    6,
                ),
                full_kelly_fraction=round(
                    full_kelly_fraction,
                    6,
                ),
                recommended_kelly_fraction=round(
                    recommended_kelly_fraction,
                    6,
                ),
                recommended_stake=round(
                    recommended_stake,
                    2,
                ),
            )
        )

    positive_selections.sort(
        key=lambda item: item.expected_value,
        reverse=True,
    )

    return MarketEvaluationResult(
        fixture_id=request.fixture_id,
        selections_evaluated=len(
            request.selections
        ),
        positive_value_count=len(
            positive_selections
        ),
        minimum_expected_value=(
            request.minimum_expected_value
        ),
        positive_value_selections=(
            positive_selections
        ),
    )