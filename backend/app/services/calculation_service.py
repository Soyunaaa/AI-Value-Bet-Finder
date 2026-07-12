from app.models.calculation import (
    MarginRemovalRequest,
    MarginRemovalResult,
    ValueCalculationRequest,
    ValueCalculationResult,
)


def decimal_odds_to_probability(odds: float) -> float:
    return 1 / odds


def probability_to_fair_odds(probability: float) -> float:
    return 1 / probability


def calculate_expected_value(
    bookmaker_odds: float,
    model_probability: float,
) -> float:
    return model_probability * bookmaker_odds - 1


def calculate_kelly_fraction(
    bookmaker_odds: float,
    model_probability: float,
) -> float:
    net_odds = bookmaker_odds - 1
    losing_probability = 1 - model_probability

    kelly_fraction = (
        net_odds * model_probability - losing_probability
    ) / net_odds

    return max(kelly_fraction, 0)


def calculate_value(
    request: ValueCalculationRequest,
) -> ValueCalculationResult:
    implied_probability = decimal_odds_to_probability(
        request.bookmaker_odds
    )

    fair_odds = probability_to_fair_odds(
        request.model_probability
    )

    expected_value = calculate_expected_value(
        bookmaker_odds=request.bookmaker_odds,
        model_probability=request.model_probability,
    )

    probability_edge = (
        request.model_probability - implied_probability
    )

    full_kelly_fraction = calculate_kelly_fraction(
        bookmaker_odds=request.bookmaker_odds,
        model_probability=request.model_probability,
    )

    recommended_kelly_fraction = (
        full_kelly_fraction * request.kelly_fraction
    )

    recommended_stake = (
        request.bankroll * recommended_kelly_fraction
    )

    return ValueCalculationResult(
        bookmaker_odds=request.bookmaker_odds,
        model_probability=request.model_probability,
        implied_probability=round(implied_probability, 6),
        fair_odds=round(fair_odds, 4),
        expected_value=round(expected_value, 6),
        probability_edge=round(probability_edge, 6),
        full_kelly_fraction=round(full_kelly_fraction, 6),
        recommended_kelly_fraction=round(
            recommended_kelly_fraction,
            6,
        ),
        recommended_stake=round(recommended_stake, 2),
    )


def remove_bookmaker_margin(
    request: MarginRemovalRequest,
) -> list[MarginRemovalResult]:
    raw_probabilities = [
        decimal_odds_to_probability(selection.odds)
        for selection in request.selections
    ]

    total_probability = sum(raw_probabilities)

    return [
        MarginRemovalResult(
            name=selection.name,
            odds=selection.odds,
            raw_probability=round(raw_probability, 6),
            fair_probability=round(
                raw_probability / total_probability,
                6,
            ),
            fair_odds=round(
                1 / (raw_probability / total_probability),
                4,
            ),
        )
        for selection, raw_probability in zip(
            request.selections,
            raw_probabilities,
            strict=True,
        )
    ]