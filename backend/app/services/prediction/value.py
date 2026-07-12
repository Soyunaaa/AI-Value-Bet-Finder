def decimal_odds_to_probability(
    decimal_odds: float,
) -> float:
    if decimal_odds <= 1:
        raise ValueError(
            "Decimal odds must be greater than 1."
        )

    return 1 / decimal_odds


def probability_to_fair_odds(
    probability: float,
) -> float:
    if probability <= 0 or probability > 1:
        raise ValueError(
            "Probability must be greater than 0 and at most 1."
        )

    return 1 / probability


def calculate_probability_edge(
    *,
    model_probability: float,
    implied_probability: float,
) -> float:
    return model_probability - implied_probability


def calculate_expected_value(
    *,
    model_probability: float,
    decimal_odds: float,
) -> float:
    return model_probability * decimal_odds - 1


def remove_proportional_margin(
    odds: list[float],
) -> list[float]:
    if len(odds) < 2:
        raise ValueError(
            "At least two selections are required."
        )

    raw_probabilities = [
        decimal_odds_to_probability(price)
        for price in odds
    ]

    overround = sum(raw_probabilities)

    if overround <= 0:
        raise ValueError(
            "The calculated overround must be positive."
        )

    return [
        probability / overround
        for probability in raw_probabilities
    ]