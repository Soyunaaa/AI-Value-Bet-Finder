from collections import defaultdict
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.match import MatchRecord
from app.database.models.team_statistics import (
    TeamStatisticsRecord,
)
from app.models.database import (
    TeamStatisticsBuildResult,
)


@dataclass
class TeamAccumulator:
    team_id: int
    team_name: str
    competition_code: str
    competition_name: str

    matches_played: int = 0

    wins: int = 0
    draws: int = 0
    losses: int = 0

    goals_scored: int = 0
    goals_conceded: int = 0

    home_matches: int = 0
    home_wins: int = 0
    home_draws: int = 0
    home_losses: int = 0
    home_goals_scored: int = 0
    home_goals_conceded: int = 0

    away_matches: int = 0
    away_wins: int = 0
    away_draws: int = 0
    away_losses: int = 0
    away_goals_scored: int = 0
    away_goals_conceded: int = 0

    results: list[str] = field(
        default_factory=list
    )


def safe_average(
    total: int,
    matches: int,
) -> float:
    if matches <= 0:
        return 0.0

    return round(
        total / matches,
        3,
    )


def add_team_result(
    *,
    accumulator: TeamAccumulator,
    scored: int,
    conceded: int,
    is_home: bool,
) -> None:
    accumulator.matches_played += 1
    accumulator.goals_scored += scored
    accumulator.goals_conceded += conceded

    if scored > conceded:
        result = "W"
        accumulator.wins += 1
    elif scored == conceded:
        result = "D"
        accumulator.draws += 1
    else:
        result = "L"
        accumulator.losses += 1

    accumulator.results.append(result)

    if is_home:
        accumulator.home_matches += 1
        accumulator.home_goals_scored += scored
        accumulator.home_goals_conceded += conceded

        if result == "W":
            accumulator.home_wins += 1
        elif result == "D":
            accumulator.home_draws += 1
        else:
            accumulator.home_losses += 1

        return

    accumulator.away_matches += 1
    accumulator.away_goals_scored += scored
    accumulator.away_goals_conceded += conceded

    if result == "W":
        accumulator.away_wins += 1
    elif result == "D":
        accumulator.away_draws += 1
    else:
        accumulator.away_losses += 1


def apply_accumulator(
    *,
    record: TeamStatisticsRecord,
    accumulator: TeamAccumulator,
) -> None:
    points = (
        accumulator.wins * 3
        + accumulator.draws
    )

    record.team_name = accumulator.team_name
    record.competition_name = (
        accumulator.competition_name
    )

    record.matches_played = (
        accumulator.matches_played
    )

    record.wins = accumulator.wins
    record.draws = accumulator.draws
    record.losses = accumulator.losses

    record.goals_scored = (
        accumulator.goals_scored
    )

    record.goals_conceded = (
        accumulator.goals_conceded
    )

    record.home_matches = (
        accumulator.home_matches
    )

    record.home_wins = accumulator.home_wins
    record.home_draws = accumulator.home_draws
    record.home_losses = accumulator.home_losses

    record.home_goals_scored = (
        accumulator.home_goals_scored
    )

    record.home_goals_conceded = (
        accumulator.home_goals_conceded
    )

    record.away_matches = (
        accumulator.away_matches
    )

    record.away_wins = accumulator.away_wins
    record.away_draws = accumulator.away_draws
    record.away_losses = accumulator.away_losses

    record.away_goals_scored = (
        accumulator.away_goals_scored
    )

    record.away_goals_conceded = (
        accumulator.away_goals_conceded
    )

    record.points_per_game = safe_average(
        points,
        accumulator.matches_played,
    )

    record.average_goals_scored = safe_average(
        accumulator.goals_scored,
        accumulator.matches_played,
    )

    record.average_goals_conceded = safe_average(
        accumulator.goals_conceded,
        accumulator.matches_played,
    )

    record.home_average_scored = safe_average(
        accumulator.home_goals_scored,
        accumulator.home_matches,
    )

    record.home_average_conceded = safe_average(
        accumulator.home_goals_conceded,
        accumulator.home_matches,
    )

    record.away_average_scored = safe_average(
        accumulator.away_goals_scored,
        accumulator.away_matches,
    )

    record.away_average_conceded = safe_average(
        accumulator.away_goals_conceded,
        accumulator.away_matches,
    )

    record.last_five_form = "".join(
        accumulator.results[-5:]
    )

    record.last_ten_form = "".join(
        accumulator.results[-10:]
    )


class TeamStatisticsBuilder:
    async def rebuild_competition(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
    ) -> TeamStatisticsBuildResult:
        normalized_code = (
            competition_code.upper()
        )

        match_statement = (
            select(MatchRecord)
            .where(
                MatchRecord.competition_code
                == normalized_code,
                MatchRecord.status
                == "FINISHED",
                MatchRecord.home_score.is_not(
                    None
                ),
                MatchRecord.away_score.is_not(
                    None
                ),
            )
            .order_by(
                MatchRecord.kickoff_utc.asc()
            )
        )

        match_result = await session.execute(
            match_statement
        )

        matches = list(
            match_result.scalars().all()
        )

        accumulators: dict[
            int,
            TeamAccumulator,
        ] = {}

        for match in matches:
            home_score = match.home_score
            away_score = match.away_score

            if (
                home_score is None
                or away_score is None
            ):
                continue

            if match.home_team_id not in accumulators:
                accumulators[
                    match.home_team_id
                ] = TeamAccumulator(
                    team_id=match.home_team_id,
                    team_name=match.home_team_name,
                    competition_code=(
                        match.competition_code
                    ),
                    competition_name=(
                        match.competition_name
                    ),
                )

            if match.away_team_id not in accumulators:
                accumulators[
                    match.away_team_id
                ] = TeamAccumulator(
                    team_id=match.away_team_id,
                    team_name=match.away_team_name,
                    competition_code=(
                        match.competition_code
                    ),
                    competition_name=(
                        match.competition_name
                    ),
                )

            add_team_result(
                accumulator=accumulators[
                    match.home_team_id
                ],
                scored=home_score,
                conceded=away_score,
                is_home=True,
            )

            add_team_result(
                accumulator=accumulators[
                    match.away_team_id
                ],
                scored=away_score,
                conceded=home_score,
                is_home=False,
            )

        existing_statement = select(
            TeamStatisticsRecord
        ).where(
            TeamStatisticsRecord.competition_code
            == normalized_code
        )

        existing_result = await session.execute(
            existing_statement
        )

        existing_records = {
            record.team_id: record
            for record in (
                existing_result.scalars().all()
            )
        }

        created = 0
        updated = 0

        for team_id, accumulator in (
            accumulators.items()
        ):
            record = existing_records.get(
                team_id
            )

            if record is None:
                record = TeamStatisticsRecord(
                    team_id=team_id,
                    team_name=(
                        accumulator.team_name
                    ),
                    competition_code=(
                        normalized_code
                    ),
                    competition_name=(
                        accumulator
                        .competition_name
                    ),
                )

                session.add(record)
                created += 1
            else:
                updated += 1

            apply_accumulator(
                record=record,
                accumulator=accumulator,
            )

        await session.commit()

        return TeamStatisticsBuildResult(
            competition_code=normalized_code,
            matches_processed=len(matches),
            teams_created=created,
            teams_updated=updated,
            teams_total=len(accumulators),
        )


def get_team_statistics_builder(
) -> TeamStatisticsBuilder:
    return TeamStatisticsBuilder()