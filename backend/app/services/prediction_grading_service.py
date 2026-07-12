import math

from sqlalchemy import (
    Integer,
    and_,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.match import MatchRecord
from app.database.models.prediction_history import (
    PredictionResultRecord,
    PredictionSnapshotRecord,
)
from app.models.prediction_history import (
    PredictionGradingResult,
    PredictionPerformanceSummary,
)

LOG_LOSS_EPSILON = 1e-15


def actual_outcome(
    *,
    home_score: int,
    away_score: int,
) -> str:
    if home_score > away_score:
        return "HOME"

    if home_score < away_score:
        return "AWAY"

    return "DRAW"


def predicted_outcome(
    *,
    home_probability: float,
    draw_probability: float,
    away_probability: float,
) -> str:
    probabilities = {
        "HOME": home_probability,
        "DRAW": draw_probability,
        "AWAY": away_probability,
    }

    return max(
        probabilities,
        key=probabilities.get,
    )


def brier_score_1x2(
    *,
    home_probability: float,
    draw_probability: float,
    away_probability: float,
    outcome: str,
) -> float:
    targets = {
        "HOME": 1.0 if outcome == "HOME" else 0.0,
        "DRAW": 1.0 if outcome == "DRAW" else 0.0,
        "AWAY": 1.0 if outcome == "AWAY" else 0.0,
    }

    score = (
        (
            home_probability
            - targets["HOME"]
        )
        ** 2
        + (
            draw_probability
            - targets["DRAW"]
        )
        ** 2
        + (
            away_probability
            - targets["AWAY"]
        )
        ** 2
    )

    return round(score, 6)


def log_loss_1x2(
    *,
    home_probability: float,
    draw_probability: float,
    away_probability: float,
    outcome: str,
) -> float:
    probabilities = {
        "HOME": home_probability,
        "DRAW": draw_probability,
        "AWAY": away_probability,
    }

    actual_probability = probabilities[outcome]

    safe_probability = min(
        max(
            actual_probability,
            LOG_LOSS_EPSILON,
        ),
        1 - LOG_LOSS_EPSILON,
    )

    return round(
        -math.log(safe_probability),
        6,
    )


def build_prediction_result(
    *,
    snapshot: PredictionSnapshotRecord,
    match: MatchRecord,
) -> PredictionResultRecord:
    if (
        match.home_score is None
        or match.away_score is None
    ):
        raise ValueError(
            "A finished score is required to grade a prediction."
        )

    outcome = actual_outcome(
        home_score=match.home_score,
        away_score=match.away_score,
    )

    predicted = predicted_outcome(
        home_probability=(
            snapshot.home_win_probability
        ),
        draw_probability=(
            snapshot.draw_probability
        ),
        away_probability=(
            snapshot.away_win_probability
        ),
    )

    total_goals = (
        match.home_score
        + match.away_score
    )

    return PredictionResultRecord(
        snapshot_id=snapshot.id,
        home_score=match.home_score,
        away_score=match.away_score,
        actual_outcome=outcome,
        predicted_outcome=predicted,
        correct_outcome=(
            predicted == outcome
        ),
        over_2_5_result=(
            total_goals > 2.5
        ),
        btts_result=(
            match.home_score > 0
            and match.away_score > 0
        ),
        most_likely_score_correct=(
            snapshot.most_likely_home_goals
            == match.home_score
            and snapshot.most_likely_away_goals
            == match.away_score
        ),
        brier_score_1x2=brier_score_1x2(
            home_probability=(
                snapshot.home_win_probability
            ),
            draw_probability=(
                snapshot.draw_probability
            ),
            away_probability=(
                snapshot.away_win_probability
            ),
            outcome=outcome,
        ),
        log_loss_1x2=log_loss_1x2(
            home_probability=(
                snapshot.home_win_probability
            ),
            draw_probability=(
                snapshot.draw_probability
            ),
            away_probability=(
                snapshot.away_win_probability
            ),
            outcome=outcome,
        ),
    )


class PredictionGradingService:
    async def grade_pending_predictions(
        self,
        *,
        session: AsyncSession,
        competition_code: str | None = None,
    ) -> PredictionGradingResult:
        normalized_code = (
            competition_code.upper()
            if competition_code
            else None
        )

        snapshot_statement = (
            select(
                PredictionSnapshotRecord,
                MatchRecord,
                PredictionResultRecord.id,
            )
            .join(
                MatchRecord,
                MatchRecord.provider_match_id
                == PredictionSnapshotRecord.provider_match_id,
            )
            .outerjoin(
                PredictionResultRecord,
                PredictionResultRecord.snapshot_id
                == PredictionSnapshotRecord.id,
            )
        )

        if normalized_code is not None:
            snapshot_statement = (
                snapshot_statement.where(
                    PredictionSnapshotRecord
                    .competition_code
                    == normalized_code
                )
            )

        result = await session.execute(
            snapshot_statement
        )

        rows = result.all()

        graded = 0
        already_graded = 0
        waiting = 0

        for (
            snapshot,
            match,
            existing_result_id,
        ) in rows:
            if existing_result_id is not None:
                already_graded += 1
                continue

            if (
                match.status != "FINISHED"
                or match.home_score is None
                or match.away_score is None
            ):
                waiting += 1
                continue

            session.add(
                build_prediction_result(
                    snapshot=snapshot,
                    match=match,
                )
            )

            graded += 1

        await session.commit()

        return PredictionGradingResult(
            competition_code=normalized_code,
            snapshots_checked=len(rows),
            predictions_graded=graded,
            predictions_already_graded=(
                already_graded
            ),
            predictions_waiting_for_result=waiting,
        )

    async def get_performance_summary(
        self,
        *,
        session: AsyncSession,
        competition_code: str | None = None,
        model_version: str | None = None,
    ) -> PredictionPerformanceSummary:
        normalized_code = (
            competition_code.upper()
            if competition_code
            else None
        )

        filters = []

        if normalized_code is not None:
            filters.append(
                PredictionSnapshotRecord
                .competition_code
                == normalized_code
            )

        if model_version is not None:
            filters.append(
                PredictionSnapshotRecord
                .model_version
                == model_version
            )

        statement = (
            select(
                func.count(
                    PredictionResultRecord.id
                ),
                func.sum(
                    func.cast(
                        PredictionResultRecord
                        .correct_outcome,
                        Integer,
                    )
                ),
                func.sum(
                    func.cast(
                        PredictionResultRecord
                        .most_likely_score_correct,
                        Integer,
                    )
                ),
                func.avg(
                    PredictionResultRecord
                    .brier_score_1x2
                ),
                func.avg(
                    PredictionResultRecord
                    .log_loss_1x2
                ),
                func.sum(
                    func.cast(
                        PredictionResultRecord
                        .over_2_5_result,
                        Integer,
                    )
                ),
                func.sum(
                    func.cast(
                        PredictionResultRecord
                        .btts_result,
                        Integer,
                    )
                ),
            )
            .join(
                PredictionSnapshotRecord,
                PredictionSnapshotRecord.id
                == PredictionResultRecord.snapshot_id,
            )
        )

        if filters:
            statement = statement.where(
                and_(*filters)
            )

        result = await session.execute(
            statement
        )

        (
            graded,
            correct,
            exact_scores,
            average_brier,
            average_log_loss,
            over_results,
            btts_results,
        ) = result.one()

        graded = int(graded or 0)
        correct = int(correct or 0)
        exact_scores = int(exact_scores or 0)

        return PredictionPerformanceSummary(
            competition_code=normalized_code,
            model_version=model_version,
            predictions_graded=graded,
            correct_outcomes=correct,
            outcome_accuracy=(
                round(correct / graded, 4)
                if graded
                else 0.0
            ),
            exact_scores=exact_scores,
            exact_score_rate=(
                round(exact_scores / graded, 4)
                if graded
                else 0.0
            ),
            average_brier_score=round(
                float(average_brier or 0),
                6,
            ),
            average_log_loss=round(
                float(average_log_loss or 0),
                6,
            ),
            over_2_5_results=int(
                over_results or 0
            ),
            btts_results=int(
                btts_results or 0
            ),
        )


def get_prediction_grading_service(
) -> PredictionGradingService:
    return PredictionGradingService()