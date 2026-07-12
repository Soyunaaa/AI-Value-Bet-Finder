export interface MarketStatistic {
  market: string;
  bets: number;
  wins: number;
  winRate: number;
  profit: number;
  roi: number;
}

export interface LeagueStatistic {
  league: string;
  bets: number;
  profit: number;
  roi: number;
}

export interface BookmakerStatistic {
  bookmaker: string;
  bets: number;
  averageOdds: number;
  profit: number;
  roi: number;
}

export const monthlyPerformance = [
  { month: "Jan", profit: 4.2 },
  { month: "Feb", profit: 7.8 },
  { month: "Mar", profit: 5.1 },
  { month: "Apr", profit: 10.4 },
  { month: "May", profit: 13.7 },
  { month: "Jun", profit: 16.3 },
  { month: "Jul", profit: 19.8 },
  { month: "Aug", profit: 22.5 },
];

export const marketStatistics: MarketStatistic[] = [
  {
    market: "Goals O/U",
    bets: 84,
    wins: 57,
    winRate: 67.9,
    profit: 18.4,
    roi: 21.9,
  },
  {
    market: "Asian Handicap",
    bets: 53,
    wins: 34,
    winRate: 64.2,
    profit: 10.8,
    roi: 20.4,
  },
  {
    market: "1X2",
    bets: 61,
    wins: 37,
    winRate: 60.7,
    profit: 8.2,
    roi: 13.4,
  },
  {
    market: "Corners O/U",
    bets: 48,
    wins: 29,
    winRate: 60.4,
    profit: 6.9,
    roi: 14.4,
  },
  {
    market: "BTTS",
    bets: 39,
    wins: 22,
    winRate: 56.4,
    profit: 3.6,
    roi: 9.2,
  },
];

export const leagueStatistics: LeagueStatistic[] = [
  {
    league: "Premier League",
    bets: 73,
    profit: 14.8,
    roi: 20.3,
  },
  {
    league: "La Liga",
    bets: 58,
    profit: 10.5,
    roi: 18.1,
  },
  {
    league: "Serie A",
    bets: 49,
    profit: 8.1,
    roi: 16.5,
  },
  {
    league: "Bundesliga",
    bets: 45,
    profit: 6.7,
    roi: 14.9,
  },
  {
    league: "Ligue 1",
    bets: 31,
    profit: 3.8,
    roi: 12.3,
  },
];

export const bookmakerStatistics: BookmakerStatistic[] = [
  {
    bookmaker: "Pinnacle",
    bets: 86,
    averageOdds: 2.06,
    profit: 16.9,
    roi: 19.7,
  },
  {
    bookmaker: "Betfair",
    bets: 67,
    averageOdds: 2.12,
    profit: 11.8,
    roi: 17.6,
  },
  {
    bookmaker: "Bet365",
    bets: 74,
    averageOdds: 1.98,
    profit: 9.7,
    roi: 13.1,
  },
  {
    bookmaker: "Unibet",
    bets: 58,
    averageOdds: 2.01,
    profit: 7.4,
    roi: 12.8,
  },
];