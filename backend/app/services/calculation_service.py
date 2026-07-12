from app.models.calculation import (
    MarginRemovalRequest,
    MarginRemovalResult,
    ValueCalculationRequest,
    ValueCalculationResult,
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
    remove_proportional_margin,
)


def calculate_value(
    request: ValueCalculationRequest,
) -> ValueCalculationResult:
    implied_probability = (
        decimal_odds_to_probability(
            request.bookmaker_odds
        )
    )

    fair_odds = probability_to_fair_odds(
        request.model_probability
    )

    expected_value = calculate_expected_value(
        model_probability=request.model_probability,
        decimal_odds=request.bookmaker_odds,
    )

    probability_edge = calculate_probability_edge(
        model_probability=request.model_probability,
        implied_probability=implied_probability,
    )

    full_kelly_fraction = (
        calculate_full_kelly_fraction(
            decimal_odds=request.bookmaker_odds,
            model_probability=request.model_probability,
        )
    )

    recommended_kelly_fraction = (
        calculate_fractional_kelly(
            full_kelly_fraction=full_kelly_fraction,
            multiplier=request.kelly_fraction,
        )
    )

    recommended_stake = calculate_kelly_stake(
        bankroll=request.bankroll,
        kelly_fraction=recommended_kelly_fraction,
    )

    return ValueCalculationResult(
        bookmaker_odds=request.bookmaker_odds,
        model_probability=request.model_probability,
        implied_probability=round(
            implied_probability,
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
        probability_edge=round(
            probability_edge,
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


def remove_bookmaker_margin(
    request: MarginRemovalRequest,
) -> list[MarginRemovalResult]:
    odds = [
        selection.odds
        for selection in request.selections
    ]

    fair_probabilities = remove_proportional_margin(
        odds
    )

    results: list[MarginRemovalResult] = []

    for selection, fair_probability in zip(
        request.selections,
        fair_probabilities,
        strict=True,
    ):
        raw_probability = (
            decimal_odds_to_probability(
                selection.odds
            )
        )

        results.append(
            MarginRemovalResult(
                name=selection.name,
                odds=selection.odds,
                raw_probability=round(
                    raw_probability,
                    6,
                ),
                fair_probability=round(
                    fair_probability,
                    6,
                ),
                fair_odds=round(
                    probability_to_fair_odds(
                        fair_probability
                    ),
                    4,
                ),
            )
        )

    return results