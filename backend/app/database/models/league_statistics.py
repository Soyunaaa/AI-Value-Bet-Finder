from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class LeagueStatisticsRecord(Base):
    __tablename__ = "league_statistics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    competition_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
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

    total_goals: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    home_goals: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    away_goals: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    average_goals: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    average_home_goals: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    average_away_goals: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    home_win_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    draw_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    away_win_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    over_2_5_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    btts_rate: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )

    goal_environment: Mapped[float] = mapped_column(
        Float,
        default=1,
        nullable=False,
    )

    home_advantage_multiplier: Mapped[
        float
    ] = mapped_column(
        Float,
        default=1.08,
        nullable=False,
    )

    elo_home_advantage: Mapped[float] = mapped_column(
        Float,
        default=65,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )