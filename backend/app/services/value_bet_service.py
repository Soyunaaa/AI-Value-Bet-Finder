from app.models.calculation import ValueCalculationRequest
from app.models.value_bet import BookmakerOdds, ValueBet

from app.services.calculation_service import calculate_value


DEFAULT_BANKROLL = 1000.0
DEFAULT_KELLY_FRACTION = 0.25


def build_value_bet(
    *,
    id: int,
    match: str,
    league: str,
    home_team: str,
    away_team: str,
    kickoff: str,
    market: str,
    bookmaker: str,
    odds: float,
    model_probability: float,
    confidence: float,
    attack_rating: float,
    defence_rating: float,
    goals_rating: float,
    corners_rating: float,
    cards_rating: float,
    home_xg: float,
    away_xg: float,
    expected_corners: float,
    expected_cards: float,
    weather: str,
    team_news: str,
    reasons: list[str],
    bookmaker_odds: list[BookmakerOdds],
) -> ValueBet:
    calculation = calculate_value(
        ValueCalculationRequest(
            bookmaker_odds=odds,
            model_probability=model_probability,
            bankroll=DEFAULT_BANKROLL,
            kelly_fraction=DEFAULT_KELLY_FRACTION,
        )
    )

    return ValueBet(
        id=id,
        match=match,
        league=league,
        home_team=home_team,
        away_team=away_team,
        kickoff=kickoff,
        market=market,
        bookmaker=bookmaker,
        odds=odds,
        model_probability=calculation.model_probability,
        implied_probability=calculation.implied_probability,
        probability_edge=calculation.probability_edge,
        fair_odds=calculation.fair_odds,
        expected_value=calculation.expected_value,
        confidence=confidence,
        full_kelly_fraction=calculation.full_kelly_fraction,
        recommended_kelly_fraction=(
            calculation.recommended_kelly_fraction
        ),
        recommended_stake=calculation.recommended_stake,
        attack_rating=attack_rating,
        defence_rating=defence_rating,
        goals_rating=goals_rating,
        corners_rating=corners_rating,
        cards_rating=cards_rating,
        home_xg=home_xg,
        away_xg=away_xg,
        expected_corners=expected_corners,
        expected_cards=expected_cards,
        weather=weather,
        team_news=team_news,
        reasons=reasons,
        bookmaker_odds=bookmaker_odds,
    )


_VALUE_BETS: list[ValueBet] = [
    build_value_bet(
        id=1,
        match="Liverpool vs Arsenal",
        league="Premier League",
        home_team="Liverpool",
        away_team="Arsenal",
        kickoff="18:30",
        market="Over 2.5 Goals",
        bookmaker="Pinnacle",
        odds=2.05,
        model_probability=0.58,
        confidence=93,
        attack_rating=92,
        defence_rating=78,
        goals_rating=94,
        corners_rating=86,
        cards_rating=61,
        home_xg=2.12,
        away_xg=1.34,
        expected_corners=10.8,
        expected_cards=4.6,
        weather="Clear, 14°C",
        team_news=(
            "Arsenal may be missing one starting defender."
        ),
        reasons=[
            "Liverpool average more than two goals per home match.",
            "The combined expected-goals projection is 3.46.",
            "Arsenal have conceded regularly in recent away fixtures.",
            "Both teams have strong attacking ratings.",
            "The available price is above the model's fair price.",
        ],
        bookmaker_odds=[
            BookmakerOdds(name="Pinnacle", odds=2.05),
            BookmakerOdds(name="Bet365", odds=2.02),
            BookmakerOdds(name="Betfair", odds=2.00),
            BookmakerOdds(name="Unibet", odds=1.98),
        ],
    ),
    build_value_bet(
        id=2,
        match="Barcelona vs Sevilla",
        league="La Liga",
        home_team="Barcelona",
        away_team="Sevilla",
        kickoff="20:00",
        market="Barcelona -1 Asian Handicap",
        bookmaker="Bet365",
        odds=1.98,
        model_probability=0.59,
        confidence=89,
        attack_rating=91,
        defence_rating=82,
        goals_rating=88,
        corners_rating=79,
        cards_rating=58,
        home_xg=2.31,
        away_xg=0.86,
        expected_corners=9.7,
        expected_cards=4.2,
        weather="Dry, 18°C",
        team_news=(
            "Barcelona are expected to field a strong starting eleven."
        ),
        reasons=[
            "Barcelona have a strong home attacking record.",
            "Sevilla's away defence rates below the league average.",
            "The model projects Barcelona above two expected goals.",
            "Barcelona's recent home form is strong.",
            "The handicap price is above the estimated fair price.",
        ],
        bookmaker_odds=[
            BookmakerOdds(name="Bet365", odds=1.98),
            BookmakerOdds(name="Pinnacle", odds=1.95),
            BookmakerOdds(name="Betfair", odds=1.94),
            BookmakerOdds(name="Unibet", odds=1.92),
        ],
    ),
]


def list_value_bets() -> list[ValueBet]:
    return _VALUE_BETS


def get_value_bet_by_id(
    bet_id: int,
) -> ValueBet | None:
    return next(
        (
            bet
            for bet in _VALUE_BETS
            if bet.id == bet_id
        ),
        None,
    )