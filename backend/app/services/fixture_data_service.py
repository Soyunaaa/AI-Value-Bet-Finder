from dataclasses import dataclass

from app.models.football import FootballFixture

from app.providers.football_data import (
    FootballDataOrgProvider,
)

from app.services.match_history_service import (
    MatchHistoryService,
)


MINIMUM_LOCAL_HISTORY = 5


@dataclass(frozen=True)
class SourcedFixture:
    fixture: FootballFixture
    source: str


@dataclass(frozen=True)
class SourcedHistory:
    matches: list[FootballFixture]
    source: str


class FixtureDataService:
    def __init__(self) -> None:
        self.local_history = MatchHistoryService()

        self.external_provider = (
            FootballDataOrgProvider()
        )

    async def get_fixture_with_source(
        self,
        fixture_id: int,
    ) -> SourcedFixture:
        local_fixture = (
            await self.local_history.get_fixture(
                fixture_id
            )
        )

        if local_fixture is not None:
            return SourcedFixture(
                fixture=local_fixture,
                source="database",
            )

        external_fixture = (
            await self.external_provider.get_match(
                fixture_id
            )
        )

        return SourcedFixture(
            fixture=external_fixture,
            source="external_api",
        )

    async def get_fixture(
        self,
        fixture_id: int,
    ) -> FootballFixture:
        result = await self.get_fixture_with_source(
            fixture_id
        )

        return result.fixture

    async def get_team_history_with_source(
        self,
        *,
        team_id: int,
        before_fixture: FootballFixture,
        limit: int,
    ) -> SourcedHistory:
        local_matches = (
            await self.local_history
            .get_team_finished_matches(
                team_id=team_id,
                before=before_fixture.utc_date,
                limit=limit,
            )
        )

        if (
            len(local_matches)
            >= MINIMUM_LOCAL_HISTORY
        ):
            return SourcedHistory(
                matches=local_matches,
                source="database",
            )

        external_matches = (
            await self.external_provider
            .get_team_matches(
                team_id,
                status="FINISHED",
                limit=limit,
            )
        )

        eligible_external_matches = [
            match
            for match in external_matches
            if (
                match.utc_date
                < before_fixture.utc_date
            )
        ]

        if not local_matches:
            return SourcedHistory(
                matches=(
                    eligible_external_matches[
                        :limit
                    ]
                ),
                source="external_api",
            )

        merged_matches = {
            match.id: match
            for match in [
                *local_matches,
                *eligible_external_matches,
            ]
        }

        matches = sorted(
            merged_matches.values(),
            key=lambda match: match.utc_date,
            reverse=True,
        )[:limit]

        return SourcedHistory(
            matches=matches,
            source="merged",
        )

    async def get_team_history(
        self,
        *,
        team_id: int,
        before_fixture: FootballFixture,
        limit: int,
    ) -> list[FootballFixture]:
        result = (
            await self.get_team_history_with_source(
                team_id=team_id,
                before_fixture=before_fixture,
                limit=limit,
            )
        )

        return result.matches