from app.database.models.team_statistics import (
    TeamStatisticsRecord,
)
from app.services.team_statistics_builder import (
    TeamAccumulator,
    add_team_result,
    apply_accumulator,
    safe_average,
)


def test_safe_average() -> None:
    assert safe_average(10, 5) == 2
    assert safe_average(10, 0) == 0


def test_accumulates_home_win() -> None:
    accumulator = TeamAccumulator(
        team_id=1,
        team_name="Arsenal",
        competition_code="PL",
        competition_name="Premier League",
    )

    add_team_result(
        accumulator=accumulator,
        scored=3,
        conceded=1,
        is_home=True,
    )

    assert accumulator.matches_played == 1
    assert accumulator.wins == 1
    assert accumulator.home_wins == 1
    assert accumulator.goals_scored == 3
    assert accumulator.results == ["W"]


def test_applies_statistics_to_record() -> None:
    accumulator = TeamAccumulator(
        team_id=1,
        team_name="Arsenal",
        competition_code="PL",
        competition_name="Premier League",
    )

    add_team_result(
        accumulator=accumulator,
        scored=2,
        conceded=0,
        is_home=True,
    )

    add_team_result(
        accumulator=accumulator,
        scored=1,
        conceded=1,
        is_home=False,
    )

    record = TeamStatisticsRecord(
        team_id=1,
        team_name="Arsenal",
        competition_code="PL",
        competition_name="Premier League",
    )

    apply_accumulator(
        record=record,
        accumulator=accumulator,
    )

    assert record.matches_played == 2
    assert record.wins == 1
    assert record.draws == 1
    assert record.points_per_game == 2
    assert record.last_five_form == "WD"