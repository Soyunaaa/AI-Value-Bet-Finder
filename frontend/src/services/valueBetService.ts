import type { ValueBet } from "../data/valueBets";
import type { ApiValueBet } from "../types/api";

import { apiRequest } from "./api";

function mapApiValueBet(
  bet: ApiValueBet
): ValueBet {
  return {
    id: bet.id,
    match: bet.match,
    league: bet.league,
    homeTeam: bet.home_team,
    awayTeam: bet.away_team,
    kickoff: bet.kickoff,

    market: bet.market,
    bookmaker: bet.bookmaker,

    odds: bet.odds,
    modelProbability: bet.model_probability,
    impliedProbability: bet.implied_probability,
    probabilityEdge: bet.probability_edge,
    fairOdds: bet.fair_odds,

    // Backend decimal converted into a displayed percentage.
    ev: bet.expected_value * 100,

    confidence: bet.confidence,

    fullKellyFraction: bet.full_kelly_fraction,
    recommendedKellyFraction:
      bet.recommended_kelly_fraction,
    recommendedStake: bet.recommended_stake,

    attackRating: bet.attack_rating,
    defenceRating: bet.defence_rating,
    goalsRating: bet.goals_rating,
    cornersRating: bet.corners_rating,
    cardsRating: bet.cards_rating,

    homeXg: bet.home_xg,
    awayXg: bet.away_xg,
    expectedCorners: bet.expected_corners,
    expectedCards: bet.expected_cards,

    weather: bet.weather,
    teamNews: bet.team_news,

    reasons: bet.reasons,

    bookmakerOdds: bet.bookmaker_odds.map(
      (bookmaker) => ({
        name: bookmaker.name,
        odds: bookmaker.odds,
      })
    ),
  };
}

export async function getValueBets(): Promise<
  ValueBet[]
> {
  const response = await apiRequest<ApiValueBet[]>(
    "/value-bets"
  );

  return response.map(mapApiValueBet);
}

export async function getValueBet(
  betId: number
): Promise<ValueBet> {
  const response = await apiRequest<ApiValueBet>(
    `/value-bets/${betId}`
  );

  return mapApiValueBet(response);
}