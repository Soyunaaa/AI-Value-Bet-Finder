from app.models.fixture_analysis import (
    AnalysisDataSources,
    FixtureAnalysisResult,
    LeagueCalibrationSummary,
    TeamFormSummary,
)
from app.models.football import FootballFixture
from app.models.prediction import (
    MatchPredictionRequest,
)

from app.services.fixture_data_service import (
    FixtureDataService,
)
from app.services.persistent_elo_lookup_service import (
    get_persistent_fixture_elo,
)
from app.services.prediction.confidence import (
    calculate_confidence,
)
from app.services.prediction.elo import (
    build_fixture_elo,
)
from app.services.prediction.expected_goals import (
    estimate_expected_goals,
)
from app.services.prediction.league_calibration import (
    get_league_calibration,
)
from app.services.prediction.reasons import (
    build_reasons,
)
from app.services.prediction_service import (
    predict_match,
)
from app.services.team_statistics_service import (
    get_team_statistics_record,
    record_to_team_strength,
)
from app.services.team_strength_service import (
    build_team_strength,
)


RECENT_MATCH_LIMIT = 10


def summarize_team_form(
    *,
    team_id: int,
    team_name: str,
    matches: list[FootballFixture],
) -> TeamFormSummary:
    wins = 0
    draws = 0
    losses = 0

    goals_scored = 0
    goals_conceded = 0
    matches_used = 0

    for match in matches:
        home_score = match.full_time.home
        away_score = match.full_time.away

        if (
            home_score is None
            or away_score is None
        ):
            continue

        team_is_home = (
            match.home_team.id == team_id
        )

        team_is_away = (
            match.away_team.id == team_id
        )

        if (
            not team_is_home
            and not team_is_away
        ):
            continue

        if team_is_home:
            scored = home_score
            conceded = away_score
        else:
            scored = away_score
            conceded = home_score

        goals_scored += scored
        goals_conceded += conceded
        matches_used += 1

        if scored > conceded:
            wins += 1
        elif scored == conceded:
            draws += 1
        else:
            losses += 1

    if matches_used == 0:
        return TeamFormSummary(
            team_id=team_id,
            team_name=team_name,
            matches_used=0,
            wins=0,
            draws=0,
            losses=0,
            goals_scored=0,
            goals_conceded=0,
            average_goals_scored=1.0,
            average_goals_conceded=1.0,
            points_per_game=0.0,
        )

    points = wins * 3 + draws

    return TeamFormSummary(
        team_id=team_id,
        team_name=team_name,
        matches_used=matches_used,
        wins=wins,
        draws=draws,
        losses=losses,
        goals_scored=goals_scored,
        goals_conceded=goals_conceded,
        average_goals_scored=round(
            goals_scored / matches_used,
            3,
        ),
        average_goals_conceded=round(
            goals_conceded / matches_used,
            3,
        ),
        points_per_game=round(
            points / matches_used,
            3,
        ),
    )


class FixtureAnalysisService:
    def __init__(self) -> None:
        self.fixture_data = FixtureDataService()

    async def analyse_fixture(
        self,
        fixture_id: int,
    ) -> FixtureAnalysisResult:
        fixture_result = (
            await self.fixture_data
            .get_fixture_with_source(
                fixture_id
            )
        )

        fixture = fixture_result.fixture

        home_history_result = (
            await self.fixture_data
            .get_team_history_with_source(
                team_id=fixture.home_team.id,
                before_fixture=fixture,
                limit=RECENT_MATCH_LIMIT,
            )
        )

        away_history_result = (
            await self.fixture_data
            .get_team_history_with_source(
                team_id=fixture.away_team.id,
                before_fixture=fixture,
                limit=RECENT_MATCH_LIMIT,
            )
        )

        home_matches = (
            home_history_result.matches
        )

        away_matches = (
            away_history_result.matches
        )

        home_form = summarize_team_form(
            team_id=fixture.home_team.id,
            team_name=fixture.home_team.name,
            matches=home_matches,
        )

        away_form = summarize_team_form(
            team_id=fixture.away_team.id,
            team_name=fixture.away_team.name,
            matches=away_matches,
        )

        competition_code = (
            fixture.competition.code
        )

        home_statistics_record = (
            await get_team_statistics_record(
                team_id=fixture.home_team.id,
                competition_code=competition_code,
            )
        )

        away_statistics_record = (
            await get_team_statistics_record(
                team_id=fixture.away_team.id,
                competition_code=competition_code,
            )
        )

        if home_statistics_record is not None:
            home_strength = (
                record_to_team_strength(
                    home_statistics_record
                )
            )

            home_statistics_source = (
                "database"
            )
        else:
            home_strength = build_team_strength(
                team_id=fixture.home_team.id,
                team_name=fixture.home_team.name,
                matches=home_matches,
            )

            home_statistics_source = (
                "calculated"
            )

        if away_statistics_record is not None:
            away_strength = (
                record_to_team_strength(
                    away_statistics_record
                )
            )

            away_statistics_source = (
                "database"
            )
        else:
            away_strength = build_team_strength(
                team_id=fixture.away_team.id,
                team_name=fixture.away_team.name,
                matches=away_matches,
            )

            away_statistics_source = (
                "calculated"
            )

        league_calibration = (
            get_league_calibration(
                competition_code
            )
        )

        persistent_elo = (
            await get_persistent_fixture_elo(
                home_team_id=(
                    fixture.home_team.id
                ),
                home_team_name=(
                    fixture.home_team.name
                ),
                away_team_id=(
                    fixture.away_team.id
                ),
                away_team_name=(
                    fixture.away_team.name
                ),
                competition_code=(
                    competition_code
                ),
                kickoff_utc=fixture.utc_date,
            )
        )

        if persistent_elo is not None:
            elo = persistent_elo
            elo_source = "database"
        else:
            elo = build_fixture_elo(
                home_team_id=(
                    fixture.home_team.id
                ),
                home_team_name=(
                    fixture.home_team.name
                ),
                away_team_id=(
                    fixture.away_team.id
                ),
                away_team_name=(
                    fixture.away_team.name
                ),
                matches=[
                    *home_matches,
                    *away_matches,
                ],
                as_of=fixture.utc_date,
                competition_code=(
                    competition_code
                ),
            )

            elo_source = "calculated"

        home_expected_goals = (
            estimate_expected_goals(
                attacking_team=home_strength,
                defending_team=away_strength,
                venue_attack_average=(
                    home_strength
                    .home_average_scored
                ),
                opponent_venue_conceding_average=(
                    away_strength
                    .away_average_conceded
                ),
                home_advantage=True,
                elo_difference=(
                    elo.rating_difference
                ),
                competition_code=(
                    competition_code
                ),
            )
        )

        away_expected_goals = (
            estimate_expected_goals(
                attacking_team=away_strength,
                defending_team=home_strength,
                venue_attack_average=(
                    away_strength
                    .away_average_scored
                ),
                opponent_venue_conceding_average=(
                    home_strength
                    .home_average_conceded
                ),
                home_advantage=False,
                elo_difference=(
                    -elo.rating_difference
                ),
                competition_code=(
                    competition_code
                ),
            )
        )

        prediction = predict_match(
            MatchPredictionRequest(
                home_team=(
                    fixture.home_team.name
                ),
                away_team=(
                    fixture.away_team.name
                ),
                home_expected_goals=(
                    home_expected_goals
                ),
                away_expected_goals=(
                    away_expected_goals
                ),
            )
        )

        strongest_probability = max(
            prediction.home_win.probability,
            prediction.draw.probability,
            prediction.away_win.probability,
            prediction.over_2_5.probability,
            prediction.under_2_5.probability,
        )

        confidence = calculate_confidence(
            home_matches=(
                home_form.matches_used
            ),
            away_matches=(
                away_form.matches_used
            ),
            probability_strength=(
                strongest_probability
            ),
        )

        reasons = build_reasons(
            home_form=home_form,
            away_form=away_form,
            home_strength=home_strength,
            away_strength=away_strength,
            elo=elo,
            home_expected_goals=(
                home_expected_goals
            ),
            away_expected_goals=(
                away_expected_goals
            ),
        )

        return FixtureAnalysisResult(
            fixture=fixture,
            home_form=home_form,
            away_form=away_form,
            home_strength=home_strength,
            away_strength=away_strength,
            elo=elo,
            league_calibration=(
                LeagueCalibrationSummary(
                    competition_code=(
                        league_calibration
                        .competition_code
                    ),
                    goal_environment=(
                        league_calibration
                        .goal_environment
                    ),
                    home_advantage_multiplier=(
                        league_calibration
                        .home_advantage_multiplier
                    ),
                    elo_home_advantage=(
                        league_calibration
                        .elo_home_advantage
                    ),
                )
            ),
            data_sources=AnalysisDataSources(
                fixture=fixture_result.source,
                home_history=(
                    home_history_result.source
                ),
                away_history=(
                    away_history_result.source
                ),
                home_statistics=(
                    home_statistics_source
                ),
                away_statistics=(
                    away_statistics_source
                ),
                elo=elo_source,
            ),
            home_expected_goals=(
                home_expected_goals
            ),
            away_expected_goals=(
                away_expected_goals
            ),
            prediction=prediction,
            confidence=confidence,
            reasons=reasons,
        )


def get_fixture_analysis_service(
) -> FixtureAnalysisService:
    return FixtureAnalysisService()