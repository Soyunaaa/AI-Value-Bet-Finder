from app.models.fixture_value import (
    FixtureValueRequest,
    FixtureValueResult,
)

from app.models.market_evaluation import (
    MarketEvaluationRequest,
    MarketSelectionInput,
)

from app.models.prediction import (
    MatchPredictionResult,
)

from app.services.fixture_analysis_service import (
    FixtureAnalysisService,
)

from app.services.market_evaluation_service import (
    evaluate_markets,
)


class UnsupportedMarketSelectionError(ValueError):
    pass


def normalize_text(value: str) -> str:
    return " ".join(
        value.lower()
        .replace("—", "-")
        .replace("_", " ")
        .split()
    )


def probability_for_selection(
    *,
    prediction: MatchPredictionResult,
    market: str,
    selection: str,
) -> float:
    normalized_market = normalize_text(market)
    normalized_selection = normalize_text(selection)

    if normalized_market in {
        "1x2",
        "match result",
        "full time result",
    }:
        if normalized_selection in {
            "home",
            "home win",
            "1",
        }:
            return prediction.home_win.probability

        if normalized_selection in {
            "draw",
            "x",
        }:
            return prediction.draw.probability

        if normalized_selection in {
            "away",
            "away win",
            "2",
        }:
            return prediction.away_win.probability

    if normalized_market in {
        "goals",
        "goals over under",
        "over under 2.5",
        "o/u 2.5",
    }:
        if normalized_selection in {
            "over 2.5",
            "over 2.5 goals",
            "o2.5",
        }:
            return prediction.over_2_5.probability

        if normalized_selection in {
            "under 2.5",
            "under 2.5 goals",
            "u2.5",
        }:
            return prediction.under_2_5.probability

    if normalized_market in {
        "btts",
        "both teams to score",
    }:
        if normalized_selection in {
            "yes",
            "btts yes",
        }:
            return (
                prediction
                .both_teams_to_score_yes
                .probability
            )

        if normalized_selection in {
            "no",
            "btts no",
        }:
            return (
                prediction
                .both_teams_to_score_no
                .probability
            )

    raise UnsupportedMarketSelectionError(
        "Unsupported market or selection: "
        f"{market} / {selection}. "
        "Supported markets are 1X2, Goals O/U 2.5 "
        "and BTTS."
    )


class FixtureValueService:
    def __init__(self) -> None:
        self.analysis_service = FixtureAnalysisService()

    async def evaluate_fixture(
        self,
        *,
        fixture_id: int,
        request: FixtureValueRequest,
    ) -> FixtureValueResult:
        analysis = (
            await self.analysis_service.analyse_fixture(
                fixture_id
            )
        )

        selections: list[MarketSelectionInput] = []

        for offered_price in request.odds:
            model_probability = probability_for_selection(
                prediction=analysis.prediction,
                market=offered_price.market,
                selection=offered_price.selection,
            )

            selections.append(
                MarketSelectionInput(
                    market=offered_price.market,
                    selection=offered_price.selection,
                    bookmaker=offered_price.bookmaker,
                    bookmaker_odds=(
                        offered_price.bookmaker_odds
                    ),
                    model_probability=model_probability,
                )
            )

        evaluation = evaluate_markets(
            MarketEvaluationRequest(
                fixture_id=fixture_id,
                bankroll=request.bankroll,
                kelly_fraction=request.kelly_fraction,
                minimum_expected_value=(
                    request.minimum_expected_value
                ),
                selections=selections,
            )
        )

        return FixtureValueResult(
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
            model_confidence=analysis.confidence,
            home_expected_goals=(
                analysis.home_expected_goals
            ),
            away_expected_goals=(
                analysis.away_expected_goals
            ),
            evaluation=evaluation,
        )


def get_fixture_value_service() -> FixtureValueService:
    return FixtureValueService()