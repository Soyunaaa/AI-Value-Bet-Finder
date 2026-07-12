export interface ValueBet {
  id: number;
  match: string;
  league: string;
  homeTeam: string;
  awayTeam: string;
  kickoff: string;

  market: string;
  bookmaker: string;

  odds: number;
  modelProbability: number;
  impliedProbability: number;
  probabilityEdge: number;
  fairOdds: number;
  ev: number;
  confidence: number;

  fullKellyFraction: number;
  recommendedKellyFraction: number;
  recommendedStake: number;

  attackRating: number;
  defenceRating: number;
  goalsRating: number;
  cornersRating: number;
  cardsRating: number;

  homeXg: number;
  awayXg: number;
  expectedCorners: number;
  expectedCards: number;

  weather: string;
  teamNews: string;

  reasons: string[];

  bookmakerOdds: {
    name: string;
    odds: number;
  }[];
}