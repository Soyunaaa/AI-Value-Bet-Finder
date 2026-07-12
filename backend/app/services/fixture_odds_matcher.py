import re
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher

from app.models.football import FootballFixture
from app.models.odds import OddsEvent


TEAM_ALIASES = {
    "manchester united fc": "manchester united",
    "manchester city fc": "manchester city",
    "tottenham hotspur fc": "tottenham",
    "wolverhampton wanderers fc": "wolves",
    "brighton hove albion fc": "brighton",
    "newcastle united fc": "newcastle",
    "nottingham forest fc": "nottingham forest",
    "west ham united fc": "west ham",
    "paris saint germain fc": "psg",
    "fc internazionale milano": "inter milan",
}


def normalize_team_name(name: str) -> str:
    normalized = unicodedata.normalize(
        "NFKD",
        name,
    )

    normalized = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

    normalized = normalized.lower()

    normalized = re.sub(
        r"[^a-z0-9 ]+",
        " ",
        normalized,
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    ).strip()

    ignored_words = {
    "fc",
    "afc",
    "cf",
    "f",
    "c",
    "calcio",
    "club",
}

    parts = [
        part
        for part in normalized.split()
        if part not in ignored_words
    ]

    normalized = " ".join(parts)

    return TEAM_ALIASES.get(
        normalized,
        normalized,
    )


def team_similarity(
    first_name: str,
    second_name: str,
) -> float:
    first = normalize_team_name(first_name)
    second = normalize_team_name(second_name)

    if first == second:
        return 1.0

    if first in second or second in first:
        return 0.92

    return SequenceMatcher(
        None,
        first,
        second,
    ).ratio()


def kickoff_similarity(
    fixture_time: datetime,
    odds_time: datetime,
) -> float:
    difference_seconds = abs(
        (
            fixture_time
            - odds_time
        ).total_seconds()
    )

    difference_hours = (
        difference_seconds / 3600
    )

    if difference_hours <= 1:
        return 1.0

    if difference_hours <= 3:
        return 0.9

    if difference_hours <= 12:
        return 0.65

    if difference_hours <= 24:
        return 0.35

    return 0.0


def event_match_score(
    *,
    fixture: FootballFixture,
    odds_event: OddsEvent,
) -> float:
    direct_home_score = team_similarity(
        fixture.home_team.name,
        odds_event.home_team,
    )

    direct_away_score = team_similarity(
        fixture.away_team.name,
        odds_event.away_team,
    )

    direct_score = (
        direct_home_score
        + direct_away_score
    ) / 2

    reversed_home_score = team_similarity(
        fixture.home_team.name,
        odds_event.away_team,
    )

    reversed_away_score = team_similarity(
        fixture.away_team.name,
        odds_event.home_team,
    )

    reversed_score = (
        reversed_home_score
        + reversed_away_score
    ) / 2

    # We normally require the same home/away ordering.
    name_score = max(
        direct_score,
        reversed_score * 0.75,
    )

    time_score = kickoff_similarity(
        fixture.utc_date,
        odds_event.commence_time,
    )

    return round(
        name_score * 0.8
        + time_score * 0.2,
        4,
    )


def find_best_odds_event(
    *,
    fixture: FootballFixture,
    events: list[OddsEvent],
    minimum_score: float = 0.72,
) -> tuple[OddsEvent, float] | None:
    candidates = [
        (
            event,
            event_match_score(
                fixture=fixture,
                odds_event=event,
            ),
        )
        for event in events
    ]

    if not candidates:
        return None

    best_event, best_score = max(
        candidates,
        key=lambda candidate: candidate[1],
    )

    if best_score < minimum_score:
        return None

    return best_event, best_score