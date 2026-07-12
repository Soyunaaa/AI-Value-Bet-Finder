from datetime import UTC, datetime

from sqlalchemy import (
    Float,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class TeamStatisticsRecord(Base):
    __tablename__ = "team_statistics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    team_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
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

    matches_played: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    wins: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    draws: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    losses: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    goals_scored: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    goals_conceded: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_matches: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_wins: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_draws: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_losses: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_goals_scored: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_goals_conceded: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_matches: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_wins: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_draws: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_losses: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_goals_scored: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_goals_conceded: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    points_per_game: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    average_goals_scored: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    average_goals_conceded: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    home_average_scored: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    home_average_conceded: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    away_average_scored: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    away_average_conceded: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    last_five_form: Mapped[str] = mapped_column(
        String(5),
        default="",
        nullable=False,
    )

    last_ten_form: Mapped[str] = mapped_column(
        String(10),
        default="",
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "competition_code",
            name=(
                "uq_team_statistics_team_competition"
            ),
        ),
        Index(
            "ix_team_statistics_competition_team",
            "competition_code",
            "team_id",
        ),
    )