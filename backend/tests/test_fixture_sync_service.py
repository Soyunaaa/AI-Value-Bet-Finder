from datetime import (
    UTC,
    datetime,
)

from app.database.models.match import (
    MatchRecord,
)
from app.models.football import (
    FootballCompetition,
    FootballFixture,
    FootballScore,
    FootballTeam,
    MatchStatus,
)
from app.services.fixture_sync_service import (
    create_match_record,
    fixture_has_changed,
    update_match_record,
)


def create_fixture(
    *,
    status: MatchStatus = (
        MatchStatus.scheduled
    ),
    home_score: int | None = None,
    away_score: int | None = None,
) -> FootballFixture:
    return FootballFixture(
        id=123456,
        utc_date=datetime(
            2026,
            8,
            15,
            15,
            0,
            tzinfo=UTC,
        ),
        status=status,
        matchday=1,
        competition=FootballCompetition(
            id=2021,
            code="PL",
            name="Premier League",
        ),
        home_team=FootballTeam(
            id=1,
            name="Arsenal",
        ),
        away_team=FootballTeam(
            id=2,
            name="Chelsea",
        ),
        full_time=FootballScore(
            home=home_score,
            away=away_score,
        ),
        half_time=FootballScore(),
    )


def test_creates_match_record_from_fixture() -> None:
    fixture = create_fixture()

    record = create_match_record(
        fixture
    )

    assert (
        record.provider_match_id
        == fixture.id
    )

    assert record.competition_code == "PL"
    assert record.home_team_name == "Arsenal"
    assert record.away_team_name == "Chelsea"


def test_unchanged_fixture_is_detected() -> None:
    fixture = create_fixture()

    record = create_match_record(
        fixture
    )

    assert not fixture_has_changed(
        record=record,
        fixture=fixture,
    )


def test_finished_score_is_detected_as_change() -> None:
    scheduled_fixture = create_fixture()

    record = create_match_record(
        scheduled_fixture
    )

    finished_fixture = create_fixture(
        status=MatchStatus.finished,
        home_score=2,
        away_score=1,
    )

    assert fixture_has_changed(
        record=record,
        fixture=finished_fixture,
    )


def test_updates_existing_match_record() -> None:
    record = create_match_record(
        create_fixture()
    )

    finished_fixture = create_fixture(
        status=MatchStatus.finished,
        home_score=3,
        away_score=1,
    )

    update_match_record(
        record=record,
        fixture=finished_fixture,
    )

    assert record.status == "FINISHED"
    assert record.home_score == 3
    assert record.away_score == 1