RECENT_MATCH_LIMIT = 10


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    return max(minimum, min(value, maximum))


def calculate_confidence(
    *,
    home_matches: int,
    away_matches: int,
    probability_strength: float,
) -> float:
    sample_score = min(
        (home_matches + away_matches)
        / (RECENT_MATCH_LIMIT * 2),
        1,
    )

    probability_score = min(
        abs(probability_strength - 0.5) * 2,
        1,
    )

    confidence = (
        sample_score * 55
        + probability_score * 30
        + 15
    )

    return round(
        clamp(confidence, 0, 100),
        1,
    )