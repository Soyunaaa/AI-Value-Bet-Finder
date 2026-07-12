from app.models.team_strength import TeamStrengthRating


HOME_ADVANTAGE_MULTIPLIER = 1.08
MINIMUM_EXPECTED_GOALS = 0.2
MAXIMUM_EXPECTED_GOALS = 4.5


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    return max(minimum, min(value, maximum))


def elo_goal_multiplier(
    elo_difference: float,
) -> float:
    adjustment = clamp(
        elo_difference / 800,
        -0.15,
        0.15,
    )

    return 1 + adjustment


def estimate_expected_goals(
    *,
    attacking_team: TeamStrengthRating,
    defending_team: TeamStrengthRating,
    venue_attack_average: float,
    opponent_venue_conceding_average: float,
    home_advantage: bool,
    elo_difference: float = 0,
) -> float:
    recent_attack_component = (
        attacking_team.average_goals_scored
    )

    opponent_defence_component = (
        defending_team.average_goals_conceded
    )

    venue_component = (
        venue_attack_average
        + opponent_venue_conceding_average
    ) / 2

    rating_component = (
        attacking_team.attack_rating
        + (100 - defending_team.defence_rating)
    ) / 200

    expected_goals = (
        recent_attack_component * 0.30
        + opponent_defence_component * 0.25
        + venue_component * 0.30
        + rating_component * 1.35 * 0.15
    )

    expected_goals *= elo_goal_multiplier(
        elo_difference
    )

    if home_advantage:
        expected_goals *= HOME_ADVANTAGE_MULTIPLIER

    return round(
        clamp(
            expected_goals,
            MINIMUM_EXPECTED_GOALS,
            MAXIMUM_EXPECTED_GOALS,
        ),
        3,
    )