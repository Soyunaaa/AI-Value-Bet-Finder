def calculate_full_kelly_fraction(
    *,
    decimal_odds: float,
    model_probability: float,
) -> float:
    if decimal_odds <= 1:
        raise ValueError(
            "Decimal odds must be greater than 1."
        )

    if model_probability <= 0 or model_probability > 1:
        raise ValueError(
            "Model probability must be greater than 0 "
            "and at most 1."
        )

    net_odds = decimal_odds - 1
    losing_probability = 1 - model_probability

    kelly_fraction = (
        net_odds * model_probability
        - losing_probability
    ) / net_odds

    return max(kelly_fraction, 0)


def calculate_fractional_kelly(
    *,
    full_kelly_fraction: float,
    multiplier: float = 0.25,
) -> float:
    if full_kelly_fraction < 0:
        raise ValueError(
            "Full Kelly fraction cannot be negative."
        )

    if multiplier <= 0 or multiplier > 1:
        raise ValueError(
            "Kelly multiplier must be greater than 0 "
            "and at most 1."
        )

    return full_kelly_fraction * multiplier


def calculate_kelly_stake(
    *,
    bankroll: float,
    kelly_fraction: float,
) -> float:
    if bankroll <= 0:
        raise ValueError(
            "Bankroll must be greater than 0."
        )

    if kelly_fraction < 0:
        raise ValueError(
            "Kelly fraction cannot be negative."
        )

    return bankroll * kelly_fraction