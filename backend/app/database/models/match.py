from datetime import datetime

from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class MatchRecord(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    provider_match_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
        index=True,
    )

    competition_id: Mapped[int] = mapped_column(
        Integer,
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

    matchday: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    kickoff_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
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

    home_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    away_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_matches_competition_kickoff",
            "competition_code",
            "kickoff_utc",
        ),
        Index(
            "ix_matches_home_away",
            "home_team_id",
            "away_team_id",
        ),
    )