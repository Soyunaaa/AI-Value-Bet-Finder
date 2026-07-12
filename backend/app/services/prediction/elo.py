from collections import defaultdict
from datetime import datetime

from app.models.elo import (
    FixtureEloSummary,
    TeamEloRating,
)
from app.models.football import FootballFixture
from app.services.prediction.league_calibration import (
    get_league_calibration,
)

INITIAL_ELO = 1500.0
K_FACTOR = 28.0


# A result loses half its weighting every 120 days.
RECENCY_HALF_LIFE_DAYS = 120.0

# Prevent older matches becoming completely irrelevant.
MINIMUM_RECENCY_WEIGHT = 0.20


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    return max(minimum, min(value, maximum))


def expected_score(
    *,
    rating: float,
    opponent_rating: float,
) -> float:
    return 1 / (
        1
        + 10
        ** (
            (opponent_rating - rating)
            / 400
        )
    )


def match_result_score(
    *,
    goals_for: int,
    goals_against: int,
) -> float:
    if goals_for > goals_against:
        return 1.0

    if goals_for == goals_against:
        return 0.5

    return 0.0


def goal_difference_multiplier(
    goal_difference: int,
) -> float:
    difference = abs(goal_difference)

    if difference <= 1:
        return 1.0

    if difference == 2:
        return 1.5

    return min(
        1.75
        + (difference - 3) * 0.125,
        2.5,
    )


def recency_weight(
    *,
    match_date: datetime,
    as_of: datetime,
) -> float:
    """
    Return a time-decay multiplier.

    A match played today receives a weight near 1.0.
    A match 120 days old receives a weight of 0.5.
    """
    age_seconds = (
        as_of - match_date
    ).total_seconds()

    age_days = max(
        age_seconds / 86_400,
        0,
    )

    weight = 0.5 ** (
        age_days / RECENCY_HALF_LIFE_DAYS
    )

    return clamp(
        weight,
        MINIMUM_RECENCY_WEIGHT,
        1.0,
    )


def build_fixture_elo(
    *,
    home_team_id: int,
    home_team_name: str,
    away_team_id: int,
    away_team_name: str,
    matches: list[FootballFixture],
    as_of: datetime,
    competition_code: str | None = None,
) -> FixtureEloSummary:
    calibration = get_league_calibration(
        competition_code
    )

    home_advantage_elo = (
        calibration.elo_home_advantage
    )
    ratings: defaultdict[int, float] = defaultdict(
        lambda: INITIAL_ELO
    )

    matches_processed: defaultdict[
        int,
        int,
    ] = defaultdict(int)

    # Both team-history calls can contain the same match.
    unique_matches = {
        match.id: match
        for match in matches
        if match.utc_date < as_of
    }

    ordered_matches = sorted(
        unique_matches.values(),
        key=lambda match: match.utc_date,
    )

    for match in ordered_matches:
        home_goals = match.full_time.home
        away_goals = match.full_time.away

        if (
            home_goals is None
            or away_goals is None
        ):
            continue

        match_home_id = match.home_team.id
        match_away_id = match.away_team.id

        home_rating = ratings[
            match_home_id
        ]

        away_rating = ratings[
            match_away_id
        ]

        adjusted_home_rating = (
            home_rating
            + home_advantage_elo
        )

        expected_home = expected_score(
            rating=adjusted_home_rating,
            opponent_rating=away_rating,
        )

        expected_away = 1 - expected_home

        actual_home = match_result_score(
            goals_for=home_goals,
            goals_against=away_goals,
        )

        actual_away = 1 - actual_home

        goal_multiplier = (
            goal_difference_multiplier(
                home_goals - away_goals
            )
        )

        time_multiplier = recency_weight(
            match_date=match.utc_date,
            as_of=as_of,
        )

        effective_k = (
            K_FACTOR
            * goal_multiplier
            * time_multiplier
        )

        # Opponent strength is already represented by
        # actual_score - expected_score.
        home_change = (
            effective_k
            * (
                actual_home
                - expected_home
            )
        )

        away_change = (
            effective_k
            * (
                actual_away
                - expected_away
            )
        )

        ratings[
            match_home_id
        ] += home_change

        ratings[
            match_away_id
        ] += away_change

        matches_processed[
            match_home_id
        ] += 1

        matches_processed[
            match_away_id
        ] += 1

    home_rating = ratings[
        home_team_id
    ]

    away_rating = ratings[
        away_team_id
    ]

    expected_home = expected_score(
        rating=(
            home_rating
            + home_advantage_elo
        ),
        opponent_rating=away_rating,
    )

    expected_away = 1 - expected_home

    return FixtureEloSummary(
        home=TeamEloRating(
            team_id=home_team_id,
            team_name=home_team_name,
            rating=round(
                home_rating,
                1,
            ),
            matches_processed=(
                matches_processed[
                    home_team_id
                ]
            ),
        ),
        away=TeamEloRating(
            team_id=away_team_id,
            team_name=away_team_name,
            rating=round(
                away_rating,
                1,
            ),
            matches_processed=(
                matches_processed[
                    away_team_id
                ]
            ),
        ),
        rating_difference=round(
            home_rating - away_rating,
            1,
        ),
        expected_home_score=round(
            expected_home,
            4,
        ),
        expected_away_score=round(
            expected_away,
            4,
        ),
    )