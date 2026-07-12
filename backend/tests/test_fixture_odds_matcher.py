from datetime import UTC, datetime

import pytest

from app.models.football import (
    FootballCompetition,
    FootballFixture,
    FootballScore,
    FootballTeam,
    MatchStatus,
)

from app.models.odds import OddsEvent

from app.services.fixture_odds_matcher import (
    event_match_score,
    find_best_odds_event,
    normalize_team_name,
)


def create_fixture() -> FootballFixture:
    return FootballFixture(
        id=123,
        utc_date=datetime(
            2026,
            8,
            15,
            15,
            0,
            tzinfo=UTC,
        ),
        status=MatchStatus.scheduled,
        matchday=1,
        competition=FootballCompetition(
            id=1,
            code="PL",
            name="Premier League",
        ),
        home_team=FootballTeam(
            id=10,
            name="Manchester United FC",
        ),
        away_team=FootballTeam(
            id=20,
            name="Arsenal FC",
        ),
        full_time=FootballScore(),
        half_time=FootballScore(),
    )


def create_odds_event(
    *,
    home_team: str,
    away_team: str,
) -> OddsEvent:
    return OddsEvent(
        id="odds-event-1",
        sport_key="soccer_epl",
        sport_title="EPL",
        commence_time=datetime(
            2026,
            8,
            15,
            15,
            0,
            tzinfo=UTC,
        ),
        home_team=home_team,
        away_team=away_team,
        bookmakers=[],
    )


def test_normalizes_team_names() -> None:
    assert normalize_team_name(
        "Manchester United FC"
    ) == "manchester united"

    assert normalize_team_name(
        "Arsenal F.C."
    ) == "arsenal"


def test_matching_event_scores_highly() -> None:
    fixture = create_fixture()

    event = create_odds_event(
        home_team="Manchester United",
        away_team="Arsenal",
    )

    score = event_match_score(
        fixture=fixture,
        odds_event=event,
    )

    assert score >= 0.95


def test_selects_best_event() -> None:
    fixture = create_fixture()

    wrong_event = create_odds_event(
        home_team="Chelsea",
        away_team="Liverpool",
    )

    correct_event = create_odds_event(
        home_team="Manchester United",
        away_team="Arsenal",
    )

    result = find_best_odds_event(
        fixture=fixture,
        events=[
            wrong_event,
            correct_event,
        ],
    )

    assert result is not None

    matched_event, score = result

    assert (
        matched_event.home_team
        == "Manchester United"
    )

    assert score >= 0.95