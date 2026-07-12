from datetime import (
    UTC,
    datetime,
)

from app.database.models.match import (
    MatchRecord,
)
from app.models.football import (
    MatchStatus,
)
from app.services.match_history_service import (
    match_record_to_fixture,
)


def create_match_record() -> MatchRecord:
    return MatchRecord(
        provider_match_id=123456,
        competition_id=2021,
        competition_code="PL",
        competition_name="Premier League",
        matchday=1,
        kickoff_utc=datetime(
            2026,
            8,
            15,
            15,
            0,
            tzinfo=UTC,
        ),
        status="FINISHED",
        home_team_id=1,
        home_team_name="Arsenal",
        away_team_id=2,
        away_team_name="Chelsea",
        home_score=2,
        away_score=1,
    )


def test_converts_database_record_to_fixture() -> None:
    fixture = match_record_to_fixture(
        create_match_record()
    )

    assert fixture.id == 123456
    assert fixture.status == MatchStatus.finished
    assert fixture.competition.code == "PL"
    assert fixture.home_team.name == "Arsenal"
    assert fixture.away_team.name == "Chelsea"
    assert fixture.full_time.home == 2
    assert fixture.full_time.away == 1


def test_unknown_status_is_mapped_safely() -> None:
    record = create_match_record()
    record.status = "UNRECOGNIZED"

    fixture = match_record_to_fixture(
        record
    )

    assert fixture.status == MatchStatus.unknown