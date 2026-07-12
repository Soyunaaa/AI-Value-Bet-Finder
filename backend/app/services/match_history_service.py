from datetime import datetime

from sqlalchemy import (
    or_,
    select,
)

from app.database.models.match import (
    MatchRecord,
)
from app.database.session import (
    AsyncSessionFactory,
)
from app.models.football import (
    FootballCompetition,
    FootballFixture,
    FootballScore,
    FootballTeam,
    MatchStatus,
)


def match_record_to_fixture(
    record: MatchRecord,
) -> FootballFixture:
    try:
        status = MatchStatus(record.status)
    except ValueError:
        status = MatchStatus.unknown

    return FootballFixture(
        id=record.provider_match_id,
        utc_date=record.kickoff_utc,
        status=status,
        matchday=record.matchday,
        competition=FootballCompetition(
            id=record.competition_id,
            code=record.competition_code,
            name=record.competition_name,
            emblem=None,
        ),
        home_team=FootballTeam(
            id=record.home_team_id,
            name=record.home_team_name,
            short_name=None,
            tla=None,
            crest=None,
        ),
        away_team=FootballTeam(
            id=record.away_team_id,
            name=record.away_team_name,
            short_name=None,
            tla=None,
            crest=None,
        ),
        full_time=FootballScore(
            home=record.home_score,
            away=record.away_score,
        ),
        half_time=FootballScore(
            home=None,
            away=None,
        ),
    )


class MatchHistoryService:
    async def get_fixture(
        self,
        provider_match_id: int,
    ) -> FootballFixture | None:
        async with AsyncSessionFactory() as session:
            statement = (
                select(MatchRecord)
                .where(
                    MatchRecord.provider_match_id
                    == provider_match_id
                )
            )

            result = await session.execute(
                statement
            )

            record = result.scalar_one_or_none()

            if record is None:
                return None

            return match_record_to_fixture(
                record
            )

    async def get_team_finished_matches(
        self,
        *,
        team_id: int,
        before: datetime,
        limit: int = 10,
    ) -> list[FootballFixture]:
        async with AsyncSessionFactory() as session:
            statement = (
                select(MatchRecord)
                .where(
                    or_(
                        MatchRecord.home_team_id
                        == team_id,
                        MatchRecord.away_team_id
                        == team_id,
                    ),
                    MatchRecord.status
                    == MatchStatus.finished.value,
                    MatchRecord.kickoff_utc
                    < before,
                    MatchRecord.home_score.is_not(
                        None
                    ),
                    MatchRecord.away_score.is_not(
                        None
                    ),
                )
                .order_by(
                    MatchRecord.kickoff_utc.desc()
                )
                .limit(limit)
            )

            result = await session.execute(
                statement
            )

            records = result.scalars().all()

            return [
                match_record_to_fixture(record)
                for record in records
            ]


def get_match_history_service(
) -> MatchHistoryService:
    return MatchHistoryService()