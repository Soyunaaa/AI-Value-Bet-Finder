from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.league_statistics import (
    LeagueStatisticsRecord,
)
from app.database.models.match import MatchRecord
from app.models.database import (
    LeagueStatisticsBuildResult,
    LeagueStatisticsResponse,
)


REFERENCE_GOALS_PER_MATCH = 2.70


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    return max(
        minimum,
        min(value, maximum),
    )


def safe_rate(
    count: int,
    total: int,
) -> float:
    if total <= 0:
        return 0.0

    return round(
        count / total,
        4,
    )


def record_to_response(
    record: LeagueStatisticsRecord,
) -> LeagueStatisticsResponse:
    return LeagueStatisticsResponse(
        competition_code=record.competition_code,
        competition_name=record.competition_name,
        matches_played=record.matches_played,
        average_goals=record.average_goals,
        average_home_goals=(
            record.average_home_goals
        ),
        average_away_goals=(
            record.average_away_goals
        ),
        home_win_rate=record.home_win_rate,
        draw_rate=record.draw_rate,
        away_win_rate=record.away_win_rate,
        over_2_5_rate=record.over_2_5_rate,
        btts_rate=record.btts_rate,
        goal_environment=(
            record.goal_environment
        ),
        home_advantage_multiplier=(
            record.home_advantage_multiplier
        ),
        elo_home_advantage=(
            record.elo_home_advantage
        ),
    )


class LeagueStatisticsService:
    async def rebuild_competition(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
    ) -> LeagueStatisticsBuildResult:
        normalized_code = competition_code.upper()

        statement = (
            select(MatchRecord)
            .where(
                MatchRecord.competition_code
                == normalized_code,
                MatchRecord.status
                == "FINISHED",
                MatchRecord.home_score.is_not(None),
                MatchRecord.away_score.is_not(None),
            )
            .order_by(
                MatchRecord.kickoff_utc.asc()
            )
        )

        result = await session.execute(statement)
        matches = list(result.scalars().all())

        if not matches:
            return LeagueStatisticsBuildResult(
                competition_code=normalized_code,
                matches_processed=0,
                statistics_created=False,
            )

        total_goals = 0
        home_goals = 0
        away_goals = 0

        home_wins = 0
        draws = 0
        away_wins = 0

        over_2_5 = 0
        btts = 0

        for match in matches:
            home_score = match.home_score
            away_score = match.away_score

            if (
                home_score is None
                or away_score is None
            ):
                continue

            home_goals += home_score
            away_goals += away_score
            total_goals += home_score + away_score

            if home_score > away_score:
                home_wins += 1
            elif home_score < away_score:
                away_wins += 1
            else:
                draws += 1

            if home_score + away_score > 2.5:
                over_2_5 += 1

            if home_score > 0 and away_score > 0:
                btts += 1

        matches_played = len(matches)

        average_goals = (
            total_goals / matches_played
        )

        average_home_goals = (
            home_goals / matches_played
        )

        average_away_goals = (
            away_goals / matches_played
        )

        home_win_rate = safe_rate(
            home_wins,
            matches_played,
        )

        draw_rate = safe_rate(
            draws,
            matches_played,
        )

        away_win_rate = safe_rate(
            away_wins,
            matches_played,
        )

        goal_environment = clamp(
            average_goals
            / REFERENCE_GOALS_PER_MATCH,
            0.85,
            1.15,
        )

        goal_difference_ratio = (
            (
                average_home_goals
                - average_away_goals
            )
            / max(average_goals, 0.1)
        )

        home_advantage_multiplier = clamp(
            1 + goal_difference_ratio * 0.60,
            1.0,
            1.15,
        )

        elo_home_advantage = clamp(
            40
            + (
                home_win_rate
                - away_win_rate
            )
            * 100,
            20,
            90,
        )

        existing_statement = (
            select(LeagueStatisticsRecord)
            .where(
                LeagueStatisticsRecord
                .competition_code
                == normalized_code
            )
        )

        existing_result = await session.execute(
            existing_statement
        )

        record = (
            existing_result.scalar_one_or_none()
        )

        created = record is None

        if record is None:
            record = LeagueStatisticsRecord(
                competition_code=normalized_code,
                competition_name=(
                    matches[0].competition_name
                ),
            )

            session.add(record)

        record.competition_name = (
            matches[0].competition_name
        )

        record.matches_played = matches_played
        record.total_goals = total_goals
        record.home_goals = home_goals
        record.away_goals = away_goals

        record.average_goals = round(
            average_goals,
            3,
        )

        record.average_home_goals = round(
            average_home_goals,
            3,
        )

        record.average_away_goals = round(
            average_away_goals,
            3,
        )

        record.home_win_rate = home_win_rate
        record.draw_rate = draw_rate
        record.away_win_rate = away_win_rate

        record.over_2_5_rate = safe_rate(
            over_2_5,
            matches_played,
        )

        record.btts_rate = safe_rate(
            btts,
            matches_played,
        )

        record.goal_environment = round(
            goal_environment,
            4,
        )

        record.home_advantage_multiplier = round(
            home_advantage_multiplier,
            4,
        )

        record.elo_home_advantage = round(
            elo_home_advantage,
            2,
        )

        await session.commit()

        return LeagueStatisticsBuildResult(
            competition_code=normalized_code,
            matches_processed=matches_played,
            statistics_created=created,
        )

    async def get_competition_statistics(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
    ) -> LeagueStatisticsResponse | None:
        statement = (
            select(LeagueStatisticsRecord)
            .where(
                LeagueStatisticsRecord
                .competition_code
                == competition_code.upper()
            )
        )

        result = await session.execute(statement)
        record = result.scalar_one_or_none()

        if record is None:
            return None

        return record_to_response(record)


def get_league_statistics_service(
) -> LeagueStatisticsService:
    return LeagueStatisticsService()