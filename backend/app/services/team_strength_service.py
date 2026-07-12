from app.models.football import FootballFixture
from app.models.team_strength import TeamStrengthRating


DEFAULT_GOALS_AVERAGE = 1.35
MAX_RATING_GOALS = 3.0
RECENT_MATCH_WEIGHT = 1.5


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    return max(minimum, min(value, maximum))


def normalize_goal_rating(
    goals: float,
) -> float:
    return clamp(
        goals / MAX_RATING_GOALS * 100,
        0,
        100,
    )


def calculate_form_rating(
    points_per_game: float,
) -> float:
    return clamp(
        points_per_game / 3 * 100,
        0,
        100,
    )


def build_team_strength(
    *,
    team_id: int,
    team_name: str,
    matches: list[FootballFixture],
) -> TeamStrengthRating:
    weighted_goals_scored = 0.0
    weighted_goals_conceded = 0.0
    weighted_points = 0.0
    total_weight = 0.0

    home_goals_scored = 0
    home_goals_conceded = 0
    home_matches = 0

    away_goals_scored = 0
    away_goals_conceded = 0
    away_matches = 0

    matches_used = 0

    valid_matches: list[tuple[int, int, bool]] = []

    for match in matches:
        home_score = match.full_time.home
        away_score = match.full_time.away

        if home_score is None or away_score is None:
            continue

        team_is_home = match.home_team.id == team_id
        team_is_away = match.away_team.id == team_id

        if not team_is_home and not team_is_away:
            continue

        if team_is_home:
            scored = home_score
            conceded = away_score

            home_goals_scored += scored
            home_goals_conceded += conceded
            home_matches += 1
        else:
            scored = away_score
            conceded = home_score

            away_goals_scored += scored
            away_goals_conceded += conceded
            away_matches += 1

        valid_matches.append(
            (scored, conceded, team_is_home)
        )

    # Provider results are normally returned newest first.
    for index, (
        scored,
        conceded,
        _,
    ) in enumerate(valid_matches):
        recency_factor = max(
            1.0,
            RECENT_MATCH_WEIGHT
            - index * 0.05,
        )

        if scored > conceded:
            points = 3
        elif scored == conceded:
            points = 1
        else:
            points = 0

        weighted_goals_scored += (
            scored * recency_factor
        )

        weighted_goals_conceded += (
            conceded * recency_factor
        )

        weighted_points += (
            points * recency_factor
        )

        total_weight += recency_factor
        matches_used += 1

    if matches_used == 0 or total_weight == 0:
        return TeamStrengthRating(
            team_id=team_id,
            team_name=team_name,
            matches_used=0,
            attack_rating=45,
            defence_rating=45,
            form_rating=45,
            overall_rating=45,
            average_goals_scored=DEFAULT_GOALS_AVERAGE,
            average_goals_conceded=DEFAULT_GOALS_AVERAGE,
            points_per_game=1.0,
            home_average_scored=DEFAULT_GOALS_AVERAGE,
            home_average_conceded=DEFAULT_GOALS_AVERAGE,
            away_average_scored=DEFAULT_GOALS_AVERAGE,
            away_average_conceded=DEFAULT_GOALS_AVERAGE,
        )

    average_goals_scored = (
        weighted_goals_scored / total_weight
    )

    average_goals_conceded = (
        weighted_goals_conceded / total_weight
    )

    points_per_game = (
        weighted_points / total_weight
    )

    attack_rating = normalize_goal_rating(
        average_goals_scored
    )

    # Fewer goals conceded produces a stronger rating.
    defence_rating = clamp(
        100
        - normalize_goal_rating(
            average_goals_conceded
        ),
        0,
        100,
    )

    form_rating = calculate_form_rating(
        points_per_game
    )

    overall_rating = (
        attack_rating * 0.40
        + defence_rating * 0.35
        + form_rating * 0.25
    )

    return TeamStrengthRating(
        team_id=team_id,
        team_name=team_name,
        matches_used=matches_used,
        attack_rating=round(
            attack_rating,
            1,
        ),
        defence_rating=round(
            defence_rating,
            1,
        ),
        form_rating=round(
            form_rating,
            1,
        ),
        overall_rating=round(
            overall_rating,
            1,
        ),
        average_goals_scored=round(
            average_goals_scored,
            3,
        ),
        average_goals_conceded=round(
            average_goals_conceded,
            3,
        ),
        points_per_game=round(
            points_per_game,
            3,
        ),
        home_average_scored=round(
            (
                home_goals_scored / home_matches
                if home_matches
                else average_goals_scored
            ),
            3,
        ),
        home_average_conceded=round(
            (
                home_goals_conceded / home_matches
                if home_matches
                else average_goals_conceded
            ),
            3,
        ),
        away_average_scored=round(
            (
                away_goals_scored / away_matches
                if away_matches
                else average_goals_scored
            ),
            3,
        ),
        away_average_conceded=round(
            (
                away_goals_conceded / away_matches
                if away_matches
                else average_goals_conceded
            ),
            3,
        ),
    )