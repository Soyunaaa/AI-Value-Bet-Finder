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


BestPriceMap = dict[
    tuple[str, str],
    tuple[str, float],
]


def save_best_price(
    *,
    prices: BestPriceMap,
    market: str,
    selection: str,
    bookmaker: str,
    price: float,
) -> None:
    key = (market, selection)
    existing = prices.get(key)

    if existing is None or price > existing[1]:
        prices[key] = (
            bookmaker,
            price,
        )


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


def extract_best_market_prices(
    event: OddsEvent,
) -> BestPriceMap:
    best_prices: BestPriceMap = {}

    for bookmaker in event.bookmakers:
        for market in bookmaker.markets:
            if market.key == "h2h":
                for outcome in market.outcomes:
                    selection = classify_h2h_outcome(
                        outcome_name=outcome.name,
                        event=event,
                    )

                    if selection is None:
                        continue

                    save_best_price(
                        prices=best_prices,
                        market="1X2",
                        selection=selection,
                        bookmaker=bookmaker.title,
                        price=outcome.price,
                    )

            elif market.key == "totals":
                for outcome in market.outcomes:
                    if outcome.point != 2.5:
                        continue

                    normalized_name = (
                        outcome.name.strip().lower()
                    )

                    if normalized_name == "over":
                        selection = "Over 2.5"
                    elif normalized_name == "under":
                        selection = "Under 2.5"
                    else:
                        continue

                    save_best_price(
                        prices=best_prices,
                        market="Goals",
                        selection=selection,
                        bookmaker=bookmaker.title,
                        price=outcome.price,
                    )

            elif market.key == "btts":
                for outcome in market.outcomes:
                    normalized_name = (
                        outcome.name.strip().lower()
                    )

                    if normalized_name == "yes":
                        selection = "Yes"
                    elif normalized_name == "no":
                        selection = "No"
                    else:
                        continue

                    save_best_price(
                        prices=best_prices,
                        market="BTTS",
                        selection=selection,
                        bookmaker=bookmaker.title,
                        price=outcome.price,
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

        # First request: obtain events for fixture matching.
        event_list_response = (
            await self.odds_service.get_odds(
                sport_key=sport_key,
                regions=[region],
                markets=["h2h"],
            )
        )

        match = find_best_odds_event(
            fixture=analysis.fixture,
            events=event_list_response.events,
        )

        if match is None:
            raise FixtureOddsMatchError(
                "No sufficiently similar odds event "
                "could be matched to this fixture."
            )

        matched_event, match_score = match

        # Second request: fetch all supported markets for
        # the single matched event.
        event_odds_response = (
            await self.odds_service.get_event_odds(
                sport_key=sport_key,
                event_id=matched_event.id,
                regions=[region],
                markets=[
                    "h2h",
                    "totals",
                    "btts",
                ],
            )
        )

        odds_event = event_odds_response.event

        best_prices = extract_best_market_prices(
            odds_event
        )

        if not best_prices:
            raise NoUsableOddsError(
                "The matched event did not contain usable "
                "1X2, Over/Under 2.5 or BTTS prices."
            )

        selections: list[
            MarketSelectionInput
        ] = []

        selection_order = [
            ("1X2", "Home Win"),
            ("1X2", "Draw"),
            ("1X2", "Away Win"),
            ("Goals", "Over 2.5"),
            ("Goals", "Under 2.5"),
            ("BTTS", "Yes"),
            ("BTTS", "No"),
        ]

        for market, selection in selection_order:
            price_data = best_prices.get(
                (market, selection)
            )

            # Markets that are unavailable are skipped rather
            # than causing the entire scan to fail.
            if price_data is None:
                continue

            bookmaker, bookmaker_odds = (
                price_data
            )

            model_probability = (
                probability_for_selection(
                    prediction=analysis.prediction,
                    market=market,
                    selection=selection,
                )
            )

            selections.append(
                MarketSelectionInput(
                    market=market,
                    selection=selection,
                    bookmaker=bookmaker,
                    bookmaker_odds=bookmaker_odds,
                    model_probability=model_probability,
                )
            )

        if not selections:
            raise NoUsableOddsError(
                "No bookmaker prices could be mapped "
                "to model probabilities."
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
                event_odds_response
                .quota
                .requests_remaining
            ),
        )


def get_automatic_fixture_value_service(
) -> AutomaticFixtureValueService:
    return AutomaticFixtureValueService()