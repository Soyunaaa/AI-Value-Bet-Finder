export interface ValueBet {
  id: number;
  match: string;
  league: string;
  market: string;
  bookmaker: string;
  odds: number;
  fairOdds: number;
  ev: number;
  confidence: number;
}

export const valueBets: ValueBet[] = [
  {
    id: 1,
    match: "Liverpool vs Arsenal",
    league: "Premier League",
    market: "Over 2.5 Goals",
    bookmaker: "Pinnacle",
    odds: 2.05,
    fairOdds: 1.74,
    ev: 17.9,
    confidence: 93,
  },
  {
    id: 2,
    match: "Barcelona vs Sevilla",
    league: "La Liga",
    market: "Barcelona -1 Asian Handicap",
    bookmaker: "Bet365",
    odds: 1.98,
    fairOdds: 1.72,
    ev: 15.1,
    confidence: 89,
  },
  {
    id: 3,
    match: "Inter vs Atalanta",
    league: "Serie A",
    market: "Both Teams To Score",
    bookmaker: "Unibet",
    odds: 2.1,
    fairOdds: 1.86,
    ev: 12.9,
    confidence: 85,
  },
  {
    id: 4,
    match: "Dortmund vs Leipzig",
    league: "Bundesliga",
    market: "Over 9.5 Corners",
    bookmaker: "Betfair",
    odds: 2.2,
    fairOdds: 1.97,
    ev: 11.7,
    confidence: 82,
  },
];