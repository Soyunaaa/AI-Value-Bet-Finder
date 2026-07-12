from sqlalchemy import select

from app.database.models.prediction_history import (
    PredictionSnapshotRecord,
)
from app.database.session import (
    AsyncSessionFactory,
)
from app.models.fixture_analysis import (
    FixtureAnalysisResult,
)
from app.models.prediction_history import (
    PredictionSnapshotSaveResult,
)


MODEL_VERSION = "v1"


def create_snapshot_record(
    *,
    analysis: FixtureAnalysisResult,
    model_version: str = MODEL_VERSION,
) -> PredictionSnapshotRecord:
    prediction = analysis.prediction
    fixture = analysis.fixture

    return PredictionSnapshotRecord(
        provider_match_id=fixture.id,
        model_version=model_version,
        competition_code=(
            fixture.competition.code
        ),
        competition_name=(
            fixture.competition.name
        ),
        kickoff_utc=fixture.utc_date,
        home_team_id=fixture.home_team.id,
        home_team_name=(
            fixture.home_team.name
        ),
        away_team_id=fixture.away_team.id,
        away_team_name=(
            fixture.away_team.name
        ),
        home_expected_goals=(
            analysis.home_expected_goals
        ),
        away_expected_goals=(
            analysis.away_expected_goals
        ),
        home_win_probability=(
            prediction.home_win.probability
        ),
        draw_probability=(
            prediction.draw.probability
        ),
        away_win_probability=(
            prediction.away_win.probability
        ),
        over_2_5_probability=(
            prediction.over_2_5.probability
        ),
        under_2_5_probability=(
            prediction.under_2_5.probability
        ),
        btts_yes_probability=(
            prediction
            .both_teams_to_score_yes
            .probability
        ),
        btts_no_probability=(
            prediction
            .both_teams_to_score_no
            .probability
        ),
        most_likely_home_goals=(
            prediction
            .most_likely_score
            .home_goals
        ),
        most_likely_away_goals=(
            prediction
            .most_likely_score
            .away_goals
        ),
        confidence=analysis.confidence,
        home_elo=analysis.elo.home.rating,
        away_elo=analysis.elo.away.rating,
        goal_environment=(
            analysis
            .league_calibration
            .goal_environment
        ),
        home_advantage_multiplier=(
            analysis
            .league_calibration
            .home_advantage_multiplier
        ),
        elo_home_advantage=(
            analysis
            .league_calibration
            .elo_home_advantage
        ),
    )


async def save_prediction_snapshot(
    *,
    analysis: FixtureAnalysisResult,
    model_version: str = MODEL_VERSION,
) -> PredictionSnapshotSaveResult:
    async with AsyncSessionFactory() as session:
        statement = (
            select(PredictionSnapshotRecord)
            .where(
                PredictionSnapshotRecord
                .provider_match_id
                == analysis.fixture.id,
                PredictionSnapshotRecord
                .model_version
                == model_version,
            )
        )

        result = await session.execute(
            statement
        )

        existing = result.scalar_one_or_none()

        if existing is not None:
            return PredictionSnapshotSaveResult(
                snapshot_id=existing.id,
                provider_match_id=(
                    existing.provider_match_id
                ),
                model_version=(
                    existing.model_version
                ),
                created=False,
                captured_at=(
                    existing.captured_at
                ),
            )

        record = create_snapshot_record(
            analysis=analysis,
            model_version=model_version,
        )

        session.add(record)
        await session.commit()
        await session.refresh(record)

        return PredictionSnapshotSaveResult(
            snapshot_id=record.id,
            provider_match_id=(
                record.provider_match_id
            ),
            model_version=(
                record.model_version
            ),
            created=True,
            captured_at=record.captured_at,
        )