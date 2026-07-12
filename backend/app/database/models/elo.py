from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
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


class TeamEloRecord(Base):
    __tablename__ = "team_elo"

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

    rating: Mapped[float] = mapped_column(
        Float,
        default=1500.0,
        nullable=False,
    )

    matches_processed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "competition_code",
            name="uq_team_elo_team_competition",
        ),
        Index(
            "ix_team_elo_competition_rating",
            "competition_code",
            "rating",
        ),
    )


class EloHistoryRecord(Base):
    __tablename__ = "elo_history"

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

    competition_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    kickoff_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
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

    opponent_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    opponent_team_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    venue: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
    )

    rating_before: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    rating_after: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    rating_change: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "provider_match_id",
            "team_id",
            name="uq_elo_history_match_team",
        ),
        Index(
            "ix_elo_history_team_date",
            "team_id",
            "kickoff_utc",
        ),
    )