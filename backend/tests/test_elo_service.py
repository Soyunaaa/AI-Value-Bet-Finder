from datetime import (
    UTC,
    datetime,
    timedelta,
)

import pytest

from app.models.football import (
    FootballCompetition,
    FootballFixture,
    FootballScore,
    FootballTeam,
    MatchStatus,
)

from app.services.prediction.elo import (
    INITIAL_ELO,
    build_fixture_elo,
    expected_score,
    recency_weight,
)


AS_OF = datetime(
    2026,
    8,
    20,
    15,
    0,
    tzinfo=UTC,
)


def create_match(
    *,
    match_id: int,
    home_id: int,
    home_name: str,
    away_id: int,
    away_name: str,
    home_goals: int,
    away_goals: int,
    days_ago: int,
) -> FootballFixture:
    return FootballFixture(
        id=match_id,
        utc_date=(
            AS_OF
            - timedelta(days=days_ago)
        ),
        status=MatchStatus.finished,
        matchday=1,
        competition=FootballCompetition(
            id=1,
            code="PL",
            name="Premier League",
        ),
        home_team=FootballTeam(
            id=home_id,
            name=home_name,
        ),
        away_team=FootballTeam(
            id=away_id,
            name=away_name,
        ),
        full_time=FootballScore(
            home=home_goals,
            away=away_goals,
        ),
        half_time=FootballScore(),
    )


def test_equal_ratings_have_equal_expectation() -> None:
    probability = expected_score(
        rating=INITIAL_ELO,
        opponent_rating=INITIAL_ELO,
    )

    assert probability == pytest.approx(
        0.5
    )


def test_recent_match_has_more_weight() -> None:
    recent_weight = recency_weight(
        match_date=(
            AS_OF
            - timedelta(days=5)
        ),
        as_of=AS_OF,
    )

    old_weight = recency_weight(
        match_date=(
            AS_OF
            - timedelta(days=240)
        ),
        as_of=AS_OF,
    )

    assert recent_weight > old_weight
    assert recent_weight <= 1
    assert old_weight >= 0.20


def test_winning_team_gains_elo() -> None:
    matches = [
        create_match(
            match_id=1,
            home_id=10,
            home_name="Home",
            away_id=20,
            away_name="Away",
            home_goals=3,
            away_goals=0,
            days_ago=5,
        )
    ]

    result = build_fixture_elo(
        home_team_id=10,
        home_team_name="Home",
        away_team_id=20,
        away_team_name="Away",
        matches=matches,
        as_of=AS_OF,
    )

    assert (
        result.home.rating
        > INITIAL_ELO
    )

    assert (
        result.away.rating
        < INITIAL_ELO
    )

    assert (
        result.expected_home_score
        > result.expected_away_score
    )


def test_recent_win_changes_rating_more() -> None:
    recent_match = create_match(
        match_id=1,
        home_id=10,
        home_name="Home",
        away_id=20,
        away_name="Away",
        home_goals=2,
        away_goals=0,
        days_ago=5,
    )

    old_match = create_match(
        match_id=2,
        home_id=10,
        home_name="Home",
        away_id=20,
        away_name="Away",
        home_goals=2,
        away_goals=0,
        days_ago=240,
    )

    recent_result = build_fixture_elo(
        home_team_id=10,
        home_team_name="Home",
        away_team_id=20,
        away_team_name="Away",
        matches=[recent_match],
        as_of=AS_OF,
    )

    old_result = build_fixture_elo(
        home_team_id=10,
        home_team_name="Home",
        away_team_id=20,
        away_team_name="Away",
        matches=[old_match],
        as_of=AS_OF,
    )

    assert (
        recent_result.home.rating
        > old_result.home.rating
    )


def test_duplicate_matches_not_processed_twice() -> None:
    match = create_match(
        match_id=1,
        home_id=10,
        home_name="Home",
        away_id=20,
        away_name="Away",
        home_goals=2,
        away_goals=1,
        days_ago=5,
    )

    result = build_fixture_elo(
        home_team_id=10,
        home_team_name="Home",
        away_team_id=20,
        away_team_name="Away",
        matches=[
            match,
            match,
        ],
        as_of=AS_OF,
    )

    assert (
        result.home.matches_processed
        == 1
    )

    assert (
        result.away.matches_processed
        == 1
    )


def test_future_matches_are_ignored() -> None:
    future_match = create_match(
        match_id=1,
        home_id=10,
        home_name="Home",
        away_id=20,
        away_name="Away",
        home_goals=5,
        away_goals=0,
        days_ago=-2,
    )

    result = build_fixture_elo(
        home_team_id=10,
        home_team_name="Home",
        away_team_id=20,
        away_team_name="Away",
        matches=[future_match],
        as_of=AS_OF,
    )

    assert (
        result.home.rating
        == INITIAL_ELO
    )

    assert (
        result.away.rating
        == INITIAL_ELO
    )

    assert (
        result.home.matches_processed
        == 0
    )