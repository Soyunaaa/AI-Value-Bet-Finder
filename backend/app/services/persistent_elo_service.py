from collections import defaultdict
from dataclasses import dataclass

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.database.models.elo import (
    EloHistoryRecord,
    TeamEloRecord,
)
from app.database.models.match import (
    MatchRecord,
)
from app.models.database import (
    EloBuildResult,
    EloHistoryResponse,
    TeamEloResponse,
)
from app.services.prediction.elo import (
    INITIAL_ELO,
    K_FACTOR,
    expected_score,
    goal_difference_multiplier,
)
from app.services.prediction.league_calibration import (
    get_league_calibration,
)


@dataclass(frozen=True)
class EloChanges:
    expected_home: float
    expected_away: float

    home_change: float
    away_change: float

    home_result: str
    away_result: str


def result_labels(
    *,
    home_goals: int,
    away_goals: int,
) -> tuple[str, str]:
    if home_goals > away_goals:
        return "W", "L"

    if home_goals < away_goals:
        return "L", "W"

    return "D", "D"


def result_scores(
    *,
    home_goals: int,
    away_goals: int,
) -> tuple[float, float]:
    if home_goals > away_goals:
        return 1.0, 0.0

    if home_goals < away_goals:
        return 0.0, 1.0

    return 0.5, 0.5


def calculate_elo_changes(
    *,
    home_rating: float,
    away_rating: float,
    home_goals: int,
    away_goals: int,
    home_advantage_elo: float,
) -> EloChanges:
    expected_home = expected_score(
        rating=(
            home_rating
            + home_advantage_elo
        ),
        opponent_rating=away_rating,
    )

    expected_away = 1 - expected_home

    actual_home, actual_away = result_scores(
        home_goals=home_goals,
        away_goals=away_goals,
    )

    home_result, away_result = result_labels(
        home_goals=home_goals,
        away_goals=away_goals,
    )

    margin_multiplier = (
        goal_difference_multiplier(
            home_goals - away_goals
        )
    )

    effective_k = (
        K_FACTOR
        * margin_multiplier
    )

    home_change = (
        effective_k
        * (
            actual_home
            - expected_home
        )
    )

    away_change = (
        effective_k
        * (
            actual_away
            - expected_away
        )
    )

    return EloChanges(
        expected_home=expected_home,
        expected_away=expected_away,
        home_change=home_change,
        away_change=away_change,
        home_result=home_result,
        away_result=away_result,
    )


class PersistentEloService:
    async def rebuild_competition(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
    ) -> EloBuildResult:
        normalized_code = (
            competition_code.upper()
        )

        calibration = get_league_calibration(
            normalized_code
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

        await session.execute(
            delete(EloHistoryRecord).where(
                EloHistoryRecord.competition_code
                == normalized_code
            )
        )

        await session.execute(
            delete(TeamEloRecord).where(
                TeamEloRecord.competition_code
                == normalized_code
            )
        )

        ratings: defaultdict[int, float] = defaultdict(
            lambda: INITIAL_ELO
        )

        match_counts: defaultdict[int, int] = defaultdict(
            int
        )

        team_names: dict[int, str] = {}

        history_rows = 0

        for match in matches:
            home_goals = match.home_score
            away_goals = match.away_score

            if (
                home_goals is None
                or away_goals is None
            ):
                continue

            home_id = match.home_team_id
            away_id = match.away_team_id

            team_names[home_id] = (
                match.home_team_name
            )

            team_names[away_id] = (
                match.away_team_name
            )

            home_before = ratings[home_id]
            away_before = ratings[away_id]

            changes = calculate_elo_changes(
                home_rating=home_before,
                away_rating=away_before,
                home_goals=home_goals,
                away_goals=away_goals,
                home_advantage_elo=(
                    calibration.elo_home_advantage
                ),
            )

            home_after = (
                home_before
                + changes.home_change
            )

            away_after = (
                away_before
                + changes.away_change
            )

            ratings[home_id] = home_after
            ratings[away_id] = away_after

            match_counts[home_id] += 1
            match_counts[away_id] += 1

            session.add(
                EloHistoryRecord(
                    provider_match_id=(
                        match.provider_match_id
                    ),
                    competition_code=(
                        normalized_code
                    ),
                    kickoff_utc=(
                        match.kickoff_utc
                    ),
                    team_id=home_id,
                    team_name=(
                        match.home_team_name
                    ),
                    opponent_team_id=away_id,
                    opponent_team_name=(
                        match.away_team_name
                    ),
                    venue="HOME",
                    result=changes.home_result,
                    rating_before=round(
                        home_before,
                        3,
                    ),
                    rating_after=round(
                        home_after,
                        3,
                    ),
                    rating_change=round(
                        changes.home_change,
                        3,
                    ),
                )
            )

            session.add(
                EloHistoryRecord(
                    provider_match_id=(
                        match.provider_match_id
                    ),
                    competition_code=(
                        normalized_code
                    ),
                    kickoff_utc=(
                        match.kickoff_utc
                    ),
                    team_id=away_id,
                    team_name=(
                        match.away_team_name
                    ),
                    opponent_team_id=home_id,
                    opponent_team_name=(
                        match.home_team_name
                    ),
                    venue="AWAY",
                    result=changes.away_result,
                    rating_before=round(
                        away_before,
                        3,
                    ),
                    rating_after=round(
                        away_after,
                        3,
                    ),
                    rating_change=round(
                        changes.away_change,
                        3,
                    ),
                )
            )

            history_rows += 2

        for team_id, rating in ratings.items():
            session.add(
                TeamEloRecord(
                    team_id=team_id,
                    team_name=team_names[team_id],
                    competition_code=(
                        normalized_code
                    ),
                    rating=round(
                        rating,
                        3,
                    ),
                    matches_processed=(
                        match_counts[team_id]
                    ),
                )
            )

        await session.commit()

        return EloBuildResult(
            competition_code=normalized_code,
            matches_processed=len(matches),
            teams_rated=len(ratings),
            history_rows_created=history_rows,
        )

    async def get_competition_ratings(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
    ) -> list[TeamEloResponse]:
        statement = (
            select(TeamEloRecord)
            .where(
                TeamEloRecord.competition_code
                == competition_code.upper()
            )
            .order_by(
                TeamEloRecord.rating.desc()
            )
        )

        result = await session.execute(
            statement
        )

        return [
            TeamEloResponse(
                team_id=record.team_id,
                team_name=record.team_name,
                competition_code=(
                    record.competition_code
                ),
                rating=record.rating,
                matches_processed=(
                    record.matches_processed
                ),
                updated_at=record.updated_at,
            )
            for record in result.scalars().all()
        ]

    async def get_team_history(
        self,
        *,
        session: AsyncSession,
        competition_code: str,
        team_id: int,
    ) -> list[EloHistoryResponse]:
        statement = (
            select(EloHistoryRecord)
            .where(
                EloHistoryRecord.competition_code
                == competition_code.upper(),
                EloHistoryRecord.team_id
                == team_id,
            )
            .order_by(
                EloHistoryRecord.kickoff_utc.asc()
            )
        )

        result = await session.execute(
            statement
        )

        return [
            EloHistoryResponse(
                provider_match_id=(
                    record.provider_match_id
                ),
                competition_code=(
                    record.competition_code
                ),
                kickoff_utc=(
                    record.kickoff_utc
                ),
                team_id=record.team_id,
                team_name=record.team_name,
                opponent_team_id=(
                    record.opponent_team_id
                ),
                opponent_team_name=(
                    record.opponent_team_name
                ),
                venue=record.venue,
                result=record.result,
                rating_before=(
                    record.rating_before
                ),
                rating_after=(
                    record.rating_after
                ),
                rating_change=(
                    record.rating_change
                ),
            )
            for record in result.scalars().all()
        ]


def get_persistent_elo_service(
) -> PersistentEloService:
    return PersistentEloService()