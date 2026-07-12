from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select

from app.database.models.elo import (
    EloHistoryRecord,
    TeamEloRecord,
)
from app.database.session import (
    AsyncSessionFactory,
)
from app.models.elo import (
    FixtureEloSummary,
    TeamEloRating,
)
from app.services.prediction.elo import (
    expected_score,
)
from app.services.prediction.league_calibration import (
    get_league_calibration,
)


@dataclass(frozen=True)
class StoredTeamElo:
    team_id: int
    team_name: str
    rating: float
    matches_processed: int


async def get_latest_rating_before(
    *,
    team_id: int,
    competition_code: str,
    before: datetime,
) -> StoredTeamElo | None:
    normalized_code = competition_code.upper()

    async with AsyncSessionFactory() as session:
        history_statement = (
            select(EloHistoryRecord)
            .where(
                EloHistoryRecord.team_id
                == team_id,
                EloHistoryRecord.competition_code
                == normalized_code,
                EloHistoryRecord.kickoff_utc
                < before,
            )
            .order_by(
                EloHistoryRecord.kickoff_utc.desc()
            )
            .limit(1)
        )

        history_result = await session.execute(
            history_statement
        )

        history_record = (
            history_result.scalar_one_or_none()
        )

        if history_record is not None:
            count_statement = (
                select(EloHistoryRecord.id)
                .where(
                    EloHistoryRecord.team_id
                    == team_id,
                    EloHistoryRecord.competition_code
                    == normalized_code,
                    EloHistoryRecord.kickoff_utc
                    < before,
                )
            )

            count_result = await session.execute(
                count_statement
            )

            matches_processed = len(
                count_result.scalars().all()
            )

            return StoredTeamElo(
                team_id=history_record.team_id,
                team_name=history_record.team_name,
                rating=history_record.rating_after,
                matches_processed=matches_processed,
            )

        # This fallback is useful for upcoming fixtures after
        # the latest finished match stored in Elo history.
        current_statement = (
            select(TeamEloRecord)
            .where(
                TeamEloRecord.team_id
                == team_id,
                TeamEloRecord.competition_code
                == normalized_code,
            )
        )

        current_result = await session.execute(
            current_statement
        )

        current_record = (
            current_result.scalar_one_or_none()
        )

        if current_record is None:
            return None

        return StoredTeamElo(
            team_id=current_record.team_id,
            team_name=current_record.team_name,
            rating=current_record.rating,
            matches_processed=(
                current_record.matches_processed
            ),
        )


async def get_persistent_fixture_elo(
    *,
    home_team_id: int,
    home_team_name: str,
    away_team_id: int,
    away_team_name: str,
    competition_code: str,
    kickoff_utc: datetime,
) -> FixtureEloSummary | None:
    home_rating = await get_latest_rating_before(
        team_id=home_team_id,
        competition_code=competition_code,
        before=kickoff_utc,
    )

    away_rating = await get_latest_rating_before(
        team_id=away_team_id,
        competition_code=competition_code,
        before=kickoff_utc,
    )

    if (
        home_rating is None
        or away_rating is None
    ):
        return None

    calibration = get_league_calibration(
        competition_code
    )

    expected_home = expected_score(
        rating=(
            home_rating.rating
            + calibration.elo_home_advantage
        ),
        opponent_rating=away_rating.rating,
    )

    expected_away = 1 - expected_home

    return FixtureEloSummary(
        home=TeamEloRating(
            team_id=home_team_id,
            team_name=home_team_name,
            rating=round(
                home_rating.rating,
                1,
            ),
            matches_processed=(
                home_rating.matches_processed
            ),
        ),
        away=TeamEloRating(
            team_id=away_team_id,
            team_name=away_team_name,
            rating=round(
                away_rating.rating,
                1,
            ),
            matches_processed=(
                away_rating.matches_processed
            ),
        ),
        rating_difference=round(
            home_rating.rating
            - away_rating.rating,
            1,
        ),
        expected_home_score=round(
            expected_home,
            4,
        ),
        expected_away_score=round(
            expected_away,
            4,
        ),
    )