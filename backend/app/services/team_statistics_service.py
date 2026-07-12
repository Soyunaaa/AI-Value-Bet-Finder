from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.team_statistics import (
    TeamStatisticsRecord,
)
from app.models.database import (
    TeamStatisticsResponse,
)


def record_to_response(
    record: TeamStatisticsRecord,
) -> TeamStatisticsResponse:
    return TeamStatisticsResponse(
        team_id=record.team_id,
        team_name=record.team_name,
        competition_code=(
            record.competition_code
        ),
        competition_name=(
            record.competition_name
        ),
        matches_played=(
            record.matches_played
        ),
        wins=record.wins,
        draws=record.draws,
        losses=record.losses,
        goals_scored=record.goals_scored,
        goals_conceded=(
            record.goals_conceded
        ),
        points_per_game=(
            record.points_per_game
        ),
        average_goals_scored=(
            record.average_goals_scored
        ),
        average_goals_conceded=(
            record.average_goals_conceded
        ),
        home_average_scored=(
            record.home_average_scored
        ),
        home_average_conceded=(
            record.home_average_conceded
        ),
        away_average_scored=(
            record.away_average_scored
        ),
        away_average_conceded=(
            record.away_average_conceded
        ),
        last_five_form=(
            record.last_five_form
        ),
        last_ten_form=(
            record.last_ten_form
        ),
    )


async def get_competition_team_statistics(
    *,
    session: AsyncSession,
    competition_code: str,
) -> list[TeamStatisticsResponse]:
    statement = (
        select(TeamStatisticsRecord)
        .where(
            TeamStatisticsRecord.competition_code
            == competition_code.upper()
        )
        .order_by(
            TeamStatisticsRecord.points_per_game
            .desc()
        )
    )

    result = await session.execute(
        statement
    )

    return [
        record_to_response(record)
        for record in result.scalars().all()
    ]