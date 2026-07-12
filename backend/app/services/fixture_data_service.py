from app.models.football import (
    FootballFixture,
)

from app.providers.football_data import (
    FootballDataOrgProvider,
)

from app.services.match_history_service import (
    MatchHistoryService,
)


MINIMUM_LOCAL_HISTORY = 5


class FixtureDataService:
    def __init__(self) -> None:
        self.local_history = (
            MatchHistoryService()
        )

        self.external_provider = (
            FootballDataOrgProvider()
        )

    async def get_fixture(
        self,
        fixture_id: int,
    ) -> FootballFixture:
        local_fixture = (
            await self.local_history.get_fixture(
                fixture_id
            )
        )

        if local_fixture is not None:
            return local_fixture

        return await self.external_provider.get_match(
            fixture_id
        )

    async def get_team_history(
        self,
        *,
        team_id: int,
        before_fixture: FootballFixture,
        limit: int,
    ) -> list[FootballFixture]:
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
            return local_matches

        external_matches = (
            await self.external_provider
            .get_team_matches(
                team_id,
                status="FINISHED",
                limit=limit,
            )
        )

        # Prevent a completed fixture occurring after the
        # fixture being analysed from leaking into the model.
        eligible_external_matches = [
            match
            for match in external_matches
            if (
                match.utc_date
                < before_fixture.utc_date
            )
        ]

        if len(local_matches) == 0:
            return eligible_external_matches[
                :limit
            ]

        # Merge both sources and remove duplicate provider IDs.
        merged_matches = {
            match.id: match
            for match in [
                *local_matches,
                *eligible_external_matches,
            ]
        }

        return sorted(
            merged_matches.values(),
            key=lambda match: match.utc_date,
            reverse=True,
        )[:limit]
        