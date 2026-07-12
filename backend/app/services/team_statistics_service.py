from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.team_statistics import (
    TeamStatisticsRecord,
)
from app.database.session import (
    AsyncSessionFactory,
)
from app.models.database import (
    TeamStatisticsResponse,
)
from app.models.team_strength import (
    TeamStrengthRating,
)


DEFAULT_GOALS_AVERAGE = 1.35
MAX_RATING_GOALS = 3.0


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    return max(
        minimum,
        min(value, maximum),
    )


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


def record_to_team_strength(
    record: TeamStatisticsRecord,
) -> TeamStrengthRating:
    average_scored = (
        record.average_goals_scored
        or DEFAULT_GOALS_AVERAGE
    )

    average_conceded = (
        record.average_goals_conceded
        or DEFAULT_GOALS_AVERAGE
    )

    attack_rating = normalize_goal_rating(
        average_scored
    )

    defence_rating = clamp(
        100
        - normalize_goal_rating(
            average_conceded
        ),
        0,
        100,
    )

    form_rating = calculate_form_rating(
        record.points_per_game
    )

    overall_rating = (
        attack_rating * 0.40
        + defence_rating * 0.35
        + form_rating * 0.25
    )

    return TeamStrengthRating(
        team_id=record.team_id,
        team_name=record.team_name,
        matches_used=record.matches_played,
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
            average_scored,
            3,
        ),
        average_goals_conceded=round(
            average_conceded,
            3,
        ),
        points_per_game=round(
            record.points_per_game,
            3,
        ),
        home_average_scored=round(
            (
                record.home_average_scored
                or average_scored
            ),
            3,
        ),
        home_average_conceded=round(
            (
                record.home_average_conceded
                or average_conceded
            ),
            3,
        ),
        away_average_scored=round(
            (
                record.away_average_scored
                or average_scored
            ),
            3,
        ),
        away_average_conceded=round(
            (
                record.away_average_conceded
                or average_conceded
            ),
            3,
        ),
    )


async def get_team_statistics_record(
    *,
    team_id: int,
    competition_code: str,
) -> TeamStatisticsRecord | None:
    async with AsyncSessionFactory() as session:
        statement = (
            select(TeamStatisticsRecord)
            .where(
                TeamStatisticsRecord.team_id
                == team_id,
                TeamStatisticsRecord.competition_code
                == competition_code.upper(),
            )
        )

        result = await session.execute(
            statement
        )

        return result.scalar_one_or_none()


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