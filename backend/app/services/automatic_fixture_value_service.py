from app.models.automatic_fixture_value import (
    AutomaticFixtureValueResult,
    MatchedOddsEvent,
)

from app.models.market_evaluation import (
    MarketEvaluationRequest,
    MarketSelectionInput,
)

from app.models.odds import OddsEvent

from app.services.fixture_analysis_service import (
    FixtureAnalysisService,
)

from app.services.fixture_odds_matcher import (
    find_best_odds_event,
    normalize_team_name,
)

from app.services.fixture_value_service import (
    probability_for_selection,
)

from app.services.market_evaluation_service import (
    evaluate_markets,
)

from app.services.odds_service import OddsService


class FixtureOddsMatchError(RuntimeError):
    pass


class NoUsableOddsError(RuntimeError):
    pass


def classify_h2h_outcome(
    *,
    outcome_name: str,
    event: OddsEvent,
) -> str | None:
    normalized_outcome = normalize_team_name(
        outcome_name
    )

    normalized_home = normalize_team_name(
        event.home_team
    )

    normalized_away = normalize_team_name(
        event.away_team
    )

    if normalized_outcome == "draw":
        return "Draw"

    if (
        normalized_outcome == normalized_home
        or normalized_outcome in normalized_home
        or normalized_home in normalized_outcome
    ):
        return "Home Win"

    if (
        normalized_outcome == normalized_away
        or normalized_outcome in normalized_away
        or normalized_away in normalized_outcome
    ):
        return "Away Win"

    return None


def extract_best_h2h_prices(
    event: OddsEvent,
) -> dict[str, tuple[str, float]]:
    best_prices: dict[
        str,
        tuple[str, float],
    ] = {}

    for bookmaker in event.bookmakers:
        for market in bookmaker.markets:
            if market.key != "h2h":
                continue

            for outcome in market.outcomes:
                selection = classify_h2h_outcome(
                    outcome_name=outcome.name,
                    event=event,
                )

                if selection is None:
                    continue

                existing = best_prices.get(
                    selection
                )

                if (
                    existing is None
                    or outcome.price > existing[1]
                ):
                    best_prices[selection] = (
                        bookmaker.title,
                        outcome.price,
                    )

    return best_prices


class AutomaticFixtureValueService:
    def __init__(self) -> None:
        self.analysis_service = (
            FixtureAnalysisService()
        )

        self.odds_service = OddsService()

    async def evaluate_fixture(
        self,
        *,
        fixture_id: int,
        sport_key: str,
        region: str,
        bankroll: float,
        kelly_fraction: float,
        minimum_expected_value: float,
    ) -> AutomaticFixtureValueResult:
        analysis = (
            await self.analysis_service
            .analyse_fixture(fixture_id)
        )

        odds_response = (
            await self.odds_service.get_odds(
                sport_key=sport_key,
                regions=[region],
                markets=["h2h"],
            )
        )

        match = find_best_odds_event(
            fixture=analysis.fixture,
            events=odds_response.events,
        )

        if match is None:
            raise FixtureOddsMatchError(
                "No sufficiently similar odds event "
                "could be matched to this fixture."
            )

        odds_event, match_score = match

        best_prices = extract_best_h2h_prices(
            odds_event
        )

        required_selections = {
            "Home Win",
            "Draw",
            "Away Win",
        }

        missing_selections = (
            required_selections
            - set(best_prices)
        )

        if missing_selections:
            raise NoUsableOddsError(
                "The matched event did not contain "
                "complete 1X2 prices. Missing: "
                + ", ".join(
                    sorted(missing_selections)
                )
            )

        selections: list[
            MarketSelectionInput
        ] = []

        for selection_name in [
            "Home Win",
            "Draw",
            "Away Win",
        ]:
            bookmaker, bookmaker_odds = (
                best_prices[selection_name]
            )

            model_probability = (
                probability_for_selection(
                    prediction=analysis.prediction,
                    market="1X2",
                    selection=selection_name,
                )
            )

            selections.append(
                MarketSelectionInput(
                    market="1X2",
                    selection=selection_name,
                    bookmaker=bookmaker,
                    bookmaker_odds=bookmaker_odds,
                    model_probability=(
                        model_probability
                    ),
                )
            )

        evaluation = evaluate_markets(
            MarketEvaluationRequest(
                fixture_id=fixture_id,
                bankroll=bankroll,
                kelly_fraction=kelly_fraction,
                minimum_expected_value=(
                    minimum_expected_value
                ),
                selections=selections,
            )
        )

        return AutomaticFixtureValueResult(
            fixture_id=fixture_id,
            home_team=(
                analysis.fixture.home_team.name
            ),
            away_team=(
                analysis.fixture.away_team.name
            ),
            competition=(
                analysis.fixture.competition.name
            ),
            matched_event=MatchedOddsEvent(
                odds_event_id=odds_event.id,
                sport_key=odds_event.sport_key,
                home_team=odds_event.home_team,
                away_team=odds_event.away_team,
                match_score=match_score,
            ),
            model_confidence=(
                analysis.confidence
            ),
            home_expected_goals=(
                analysis.home_expected_goals
            ),
            away_expected_goals=(
                analysis.away_expected_goals
            ),
            evaluation=evaluation,
            odds_requests_remaining=(
                odds_response
                .quota
                .requests_remaining
            ),
        )


def get_automatic_fixture_value_service(
) -> AutomaticFixtureValueService:
    return AutomaticFixtureValueService()