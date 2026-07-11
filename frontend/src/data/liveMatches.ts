export interface LiveMatch {
  id: number;
  league: string;
  minute: number;
  homeTeam: string;
  awayTeam: string;
  homeScore: number;
  awayScore: number;
  homePossession: number;
  awayPossession: number;
  homeShots: number;
  awayShots: number;
  homeShotsOnTarget: number;
  awayShotsOnTarget: number;
  homeCorners: number;
  awayCorners: number;
  homeCards: number;
  awayCards: number;
  valueMarket?: string;
  valueOdds?: number;
  valueEv?: number;
}

export const liveMatches: LiveMatch[] = [
  {
    id: 1,
    league: "Premier League",
    minute: 73,
    homeTeam: "Liverpool",
    awayTeam: "Arsenal",
    homeScore: 2,
    awayScore: 1,
    homePossession: 57,
    awayPossession: 43,
    homeShots: 12,
    awayShots: 7,
    homeShotsOnTarget: 6,
    awayShotsOnTarget: 3,
    homeCorners: 7,
    awayCorners: 4,
    homeCards: 2,
    awayCards: 1,
    valueMarket: "Over 3.5 Goals",
    valueOdds: 2.2,
    valueEv: 13.4,
  },
  {
    id: 2,
    league: "La Liga",
    minute: 61,
    homeTeam: "Barcelona",
    awayTeam: "Sevilla",
    homeScore: 1,
    awayScore: 0,
    homePossession: 64,
    awayPossession: 36,
    homeShots: 14,
    awayShots: 5,
    homeShotsOnTarget: 7,
    awayShotsOnTarget: 2,
    homeCorners: 6,
    awayCorners: 2,
    homeCards: 1,
    awayCards: 3,
    valueMarket: "Barcelona -1.5",
    valueOdds: 2.05,
    valueEv: 10.8,
  },
  {
    id: 3,
    league: "Serie A",
    minute: 38,
    homeTeam: "Inter",
    awayTeam: "Atalanta",
    homeScore: 0,
    awayScore: 0,
    homePossession: 52,
    awayPossession: 48,
    homeShots: 8,
    awayShots: 6,
    homeShotsOnTarget: 3,
    awayShotsOnTarget: 2,
    homeCorners: 4,
    awayCorners: 3,
    homeCards: 0,
    awayCards: 1,
    valueMarket: "Over 9.5 Corners",
    valueOdds: 1.95,
    valueEv: 8.7,
  },
  {
    id: 4,
    league: "Bundesliga",
    minute: 82,
    homeTeam: "Dortmund",
    awayTeam: "Leipzig",
    homeScore: 2,
    awayScore: 2,
    homePossession: 49,
    awayPossession: 51,
    homeShots: 15,
    awayShots: 13,
    homeShotsOnTarget: 7,
    awayShotsOnTarget: 6,
    homeCorners: 5,
    awayCorners: 8,
    homeCards: 3,
    awayCards: 2,
  },
];