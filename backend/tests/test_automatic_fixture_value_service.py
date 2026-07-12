from datetime import UTC, datetime

from app.models.odds import (
    OddsBookmaker,
    OddsEvent,
    OddsMarket,
    OddsOutcome,
)

from app.services.automatic_fixture_value_service import (
    extract_best_market_prices,
)


NOW = datetime(
    2026,
    8,
    15,
    12,
    0,
    tzinfo=UTC,
)


def create_event() -> OddsEvent:
    return OddsEvent(
        id="event-1",
        sport_key="soccer_epl",
        sport_title="EPL",
        commence_time=NOW,
        home_team="Arsenal",
        away_team="Chelsea",
        bookmakers=[
            OddsBookmaker(
                key="first",
                title="First Bookmaker",
                last_update=NOW,
                markets=[
                    OddsMarket(
                        key="h2h",
                        last_update=NOW,
                        outcomes=[
                            OddsOutcome(
                                name="Arsenal",
                                price=2.10,
                            ),
                            OddsOutcome(
                                name="Draw",
                                price=3.40,
                            ),
                            OddsOutcome(
                                name="Chelsea",
                                price=3.60,
                            ),
                        ],
                    ),
                    OddsMarket(
                        key="totals",
                        last_update=NOW,
                        outcomes=[
                            OddsOutcome(
                                name="Over",
                                price=1.90,
                                point=2.5,
                            ),
                            OddsOutcome(
                                name="Under",
                                price=1.95,
                                point=2.5,
                            ),
                        ],
                    ),
                    OddsMarket(
                        key="btts",
                        last_update=NOW,
                        outcomes=[
                            OddsOutcome(
                                name="Yes",
                                price=1.80,
                            ),
                            OddsOutcome(
                                name="No",
                                price=2.00,
                            ),
                        ],
                    ),
                ],
            ),
            OddsBookmaker(
                key="second",
                title="Second Bookmaker",
                last_update=NOW,
                markets=[
                    OddsMarket(
                        key="h2h",
                        last_update=NOW,
                        outcomes=[
                            OddsOutcome(
                                name="Arsenal",
                                price=2.20,
                            ),
                            OddsOutcome(
                                name="Draw",
                                price=3.30,
                            ),
                            OddsOutcome(
                                name="Chelsea",
                                price=3.50,
                            ),
                        ],
                    ),
                    OddsMarket(
                        key="totals",
                        last_update=NOW,
                        outcomes=[
                            OddsOutcome(
                                name="Over",
                                price=2.05,
                                point=2.5,
                            ),
                            OddsOutcome(
                                name="Under",
                                price=1.85,
                                point=2.5,
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def test_extracts_best_prices_for_all_markets() -> None:
    prices = extract_best_market_prices(
        create_event()
    )

    assert prices[
        ("1X2", "Home Win")
    ] == (
        "Second Bookmaker",
        2.20,
    )

    assert prices[
        ("1X2", "Draw")
    ] == (
        "First Bookmaker",
        3.40,
    )

    assert prices[
        ("Goals", "Over 2.5")
    ] == (
        "Second Bookmaker",
        2.05,
    )

    assert prices[
        ("Goals", "Under 2.5")
    ] == (
        "First Bookmaker",
        1.95,
    )

    assert prices[
        ("BTTS", "Yes")
    ] == (
        "First Bookmaker",
        1.80,
    )

    assert prices[
        ("BTTS", "No")
    ] == (
        "First Bookmaker",
        2.00,
    )


def test_ignores_non_two_point_five_totals() -> None:
    event = create_event()

    event.bookmakers[0].markets.append(
        OddsMarket(
            key="totals",
            last_update=NOW,
            outcomes=[
                OddsOutcome(
                    name="Over",
                    price=3.00,
                    point=3.5,
                ),
            ],
        )
    )

    prices = extract_best_market_prices(event)

    assert prices[
        ("Goals", "Over 2.5")
    ][1] == 2.05