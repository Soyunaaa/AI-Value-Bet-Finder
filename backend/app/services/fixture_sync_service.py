from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.match import MatchRecord
from app.models.database import FixtureSyncResult
from app.models.football import FootballFixture
from app.services.football_service import FootballService
from app.services.league_statistics_service import (
    LeagueStatisticsService,
)
from app.services.persistent_elo_service import (
    PersistentEloService,
)
from app.services.team_statistics_builder import (
    TeamStatisticsBuilder,
)
from app.services.prediction_grading_service import (
    PredictionGradingService,
)

def fixture_has_changed(
    *,
    record: MatchRecord,
    fixture: FootballFixture,
) -> bool:
    return any(
        [
            record.competition_id
            != fixture.competition.id,
            record.competition_code
            != fixture.competition.code,
            record.competition_name
            != fixture.competition.name,
            record.matchday
            != fixture.matchday,
            record.kickoff_utc
            != fixture.utc_date,
            record.status
            != fixture.status.value,
            record.home_team_id
            != fixture.home_team.id,
            record.home_team_name
            != fixture.home_team.name,
            record.away_team_id
            != fixture.away_team.id,
            record.away_team_name
            != fixture.away_team.name,
            record.home_score
            != fixture.full_time.home,
            record.away_score
            != fixture.full_time.away,
        ]
    )


def update_match_record(
    *,
    record: MatchRecord,
    fixture: FootballFixture,
) -> None:
    record.competition_id = (
        fixture.competition.id
    )
    record.competition_code = (
        fixture.competition.code
    )
    record.competition_name = (
        fixture.competition.name
    )

    record.matchday = fixture.matchday
    record.kickoff_utc = fixture.utc_date
    record.status = fixture.status.value

    record.home_team_id = fixture.home_team.id
    record.home_team_name = (
        fixture.home_team.name
    )

    record.away_team_id = fixture.away_team.id
    record.away_team_name = (
        fixture.away_team.name
    )

    record.home_score = fixture.full_time.home
    record.away_score = fixture.full_time.away


def create_match_record(
    fixture: FootballFixture,
) -> MatchRecord:
    return MatchRecord(
        provider_match_id=fixture.id,
        competition_id=fixture.competition.id,
        competition_code=(
            fixture.competition.code
        ),
        competition_name=(
            fixture.competition.name
        ),
        matchday=fixture.matchday,
        kickoff_utc=fixture.utc_date,
        status=fixture.status.value,
        home_team_id=fixture.home_team.id,
        home_team_name=fixture.home_team.name,
        away_team_id=fixture.away_team.id,
        away_team_name=fixture.away_team.name,
        home_score=fixture.full_time.home,
        away_score=fixture.full_time.away,
    )


class FixtureSyncService:
    def __init__(self) -> None:
        self.football_service = FootballService()

        self.statistics_builder = (
            TeamStatisticsBuilder()
        )

        self.elo_service = PersistentEloService()

        self.league_statistics_service = (
            LeagueStatisticsService()
        )

    async def sync_competition(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> FixtureSyncResult:
        normalized_code = (
            competition_code.upper()
        )

        fixtures = (
            await self.football_service.get_matches(
                competition_code=normalized_code,
                date_from=date_from,
                date_to=date_to,
            )
        )

        inserted = 0
        updated = 0
        unchanged = 0

        fixture_ids = [
            fixture.id
            for fixture in fixtures
        ]

        existing_records: dict[
            int,
            MatchRecord,
        ] = {}

        if fixture_ids:
            statement = (
                select(MatchRecord)
                .where(
                    MatchRecord.provider_match_id.in_(
                        fixture_ids
                    )
                )
            )

            result = await session.execute(
                statement
            )

            existing_records = {
                record.provider_match_id: record
                for record in (
                    result.scalars().all()
                )
            }

        for fixture in fixtures:
            existing_record = (
                existing_records.get(
                    fixture.id
                )
            )

            if existing_record is None:
                session.add(
                    create_match_record(fixture)
                )
                inserted += 1
                continue

            if fixture_has_changed(
                record=existing_record,
                fixture=fixture,
            ):
                update_match_record(
                    record=existing_record,
                    fixture=fixture,
                )
                updated += 1
            else:
                unchanged += 1

        await session.flush()

        statistics_result = (
            await self.statistics_builder
            .rebuild_competition(
                session=session,
                competition_code=normalized_code,
            )
        )

        elo_result = (
            await self.elo_service
            .rebuild_competition(
                session=session,
                competition_code=normalized_code,
            )
        )

        league_statistics_result = (
            await self.league_statistics_service
            .rebuild_competition(
                session=session,
                competition_code=normalized_code,
            )
        )

        await self.prediction_grading_service\
            .grade_pending_predictions(
                session=session,
                competition_code=normalized_code,
    )
        count_statement = select(
            func.count(MatchRecord.id)
        )

        count_result = await session.execute(
            count_statement
        )

        total_matches_stored = (
            count_result.scalar_one()
        )

        return FixtureSyncResult(
            competition_code=normalized_code,
            fixtures_received=len(fixtures),
            fixtures_inserted=inserted,
            fixtures_updated=updated,
            fixtures_unchanged=unchanged,
            total_matches_stored=(
                total_matches_stored
            ),
            statistics_rebuilt=True,
            statistics=statistics_result,
            elo_rebuilt=True,
            elo=elo_result,
            league_statistics_rebuilt=True,
            league_statistics=(
                league_statistics_result
            ),
        )


def get_fixture_sync_service(
) -> FixtureSyncService:
    return FixtureSyncService()