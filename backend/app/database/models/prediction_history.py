from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


class PredictionSnapshotRecord(Base):
    __tablename__ = "prediction_snapshots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    provider_match_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    model_version: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="v1",
    )

    competition_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    competition_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    kickoff_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    home_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    home_team_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    away_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    away_team_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    home_expected_goals: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    away_expected_goals: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    home_win_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    draw_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    away_win_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    over_2_5_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    under_2_5_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    btts_yes_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    btts_no_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    most_likely_home_goals: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    most_likely_away_goals: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    home_elo: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    away_elo: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    goal_environment: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    home_advantage_multiplier: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    elo_home_advantage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    result: Mapped[
        "PredictionResultRecord | None"
    ] = relationship(
        back_populates="snapshot",
        cascade="all, delete-orphan",
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "provider_match_id",
            "model_version",
            name=(
                "uq_prediction_snapshot_match_version"
            ),
        ),
        Index(
            "ix_prediction_snapshot_competition_kickoff",
            "competition_code",
            "kickoff_utc",
        ),
    )


class PredictionResultRecord(Base):
    __tablename__ = "prediction_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey(
            "prediction_snapshots.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    home_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    away_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    actual_outcome: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    predicted_outcome: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    correct_outcome: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    over_2_5_result: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    btts_result: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    most_likely_score_correct: Mapped[bool] = (
        mapped_column(
            Boolean,
            nullable=False,
        )
    )

    brier_score_1x2: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    log_loss_1x2: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    graded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    snapshot: Mapped[
        PredictionSnapshotRecord
    ] = relationship(
        back_populates="result",
    )