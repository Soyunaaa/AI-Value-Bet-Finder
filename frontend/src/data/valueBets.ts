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
  fairOdds: number;
  ev: number;
  confidence: number;

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

export const valueBets: ValueBet[] = [
  {
    id: 1,
    match: "Liverpool vs Arsenal",
    league: "Premier League",
    homeTeam: "Liverpool",
    awayTeam: "Arsenal",
    kickoff: "18:30",

    market: "Over 2.5 Goals",
    bookmaker: "Pinnacle",
    odds: 2.05,
    fairOdds: 1.74,
    ev: 17.9,
    confidence: 93,

    attackRating: 92,
    defenceRating: 78,
    goalsRating: 94,
    cornersRating: 86,
    cardsRating: 61,

    homeXg: 2.12,
    awayXg: 1.34,
    expectedCorners: 10.8,
    expectedCards: 4.6,

    weather: "Clear, 14°C",
    teamNews: "Arsenal may be missing one starting defender.",

    reasons: [
      "Liverpool average more than two goals per home match.",
      "The teams have a combined expected-goals total of 3.46.",
      "Arsenal have conceded regularly in recent away fixtures.",
      "Both teams have strong attacking ratings.",
      "The available bookmaker price is above the model's fair price.",
    ],

    bookmakerOdds: [
      { name: "Pinnacle", odds: 2.05 },
      { name: "Bet365", odds: 2.02 },
      { name: "Unibet", odds: 1.98 },
      { name: "Betfair", odds: 2.0 },
    ],
  },
  {
    id: 2,
    match: "Barcelona vs Sevilla",
    league: "La Liga",
    homeTeam: "Barcelona",
    awayTeam: "Sevilla",
    kickoff: "20:00",

    market: "Barcelona -1 Asian Handicap",
    bookmaker: "Bet365",
    odds: 1.98,
    fairOdds: 1.72,
    ev: 15.1,
    confidence: 89,

    attackRating: 91,
    defenceRating: 82,
    goalsRating: 88,
    cornersRating: 79,
    cardsRating: 58,

    homeXg: 2.31,
    awayXg: 0.86,
    expectedCorners: 9.7,
    expectedCards: 4.2,

    weather: "Dry, 18°C",
    teamNews: "Barcelona expected to field a strong starting eleven.",

    reasons: [
      "Barcelona have a strong home attacking record.",
      "Sevilla's away defensive rating is below the league average.",
      "The model projects Barcelona to create more than two expected goals.",
      "Barcelona's recent home form is strong.",
      "The Asian Handicap price is above the estimated fair price.",
    ],

    bookmakerOdds: [
      { name: "Bet365", odds: 1.98 },
      { name: "Pinnacle", odds: 1.95 },
      { name: "Unibet", odds: 1.92 },
      { name: "Betfair", odds: 1.94 },
    ],
  },
  {
    id: 3,
    match: "Inter vs Atalanta",
    league: "Serie A",
    homeTeam: "Inter",
    awayTeam: "Atalanta",
    kickoff: "19:45",

    market: "Both Teams To Score",
    bookmaker: "Unibet",
    odds: 2.1,
    fairOdds: 1.86,
    ev: 12.9,
    confidence: 85,

    attackRating: 87,
    defenceRating: 74,
    goalsRating: 84,
    cornersRating: 76,
    cardsRating: 68,

    homeXg: 1.84,
    awayXg: 1.29,
    expectedCorners: 9.4,
    expectedCards: 5.1,

    weather: "Cloudy, 12°C",
    teamNews: "No major attacking absences reported.",

    reasons: [
      "Both teams generate consistent expected-goals figures.",
      "Atalanta have scored in most recent away fixtures.",
      "Inter's attack has performed strongly at home.",
      "The combined projected xG exceeds three goals.",
      "The market price offers a positive expected return.",
    ],

    bookmakerOdds: [
      { name: "Unibet", odds: 2.1 },
      { name: "Pinnacle", odds: 2.06 },
      { name: "Bet365", odds: 2.02 },
      { name: "Betfair", odds: 2.04 },
    ],
  },
  {
    id: 4,
    match: "Dortmund vs Leipzig",
    league: "Bundesliga",
    homeTeam: "Dortmund",
    awayTeam: "Leipzig",
    kickoff: "20:30",

    market: "Over 9.5 Corners",
    bookmaker: "Betfair",
    odds: 2.2,
    fairOdds: 1.97,
    ev: 11.7,
    confidence: 82,

    attackRating: 83,
    defenceRating: 70,
    goalsRating: 81,
    cornersRating: 92,
    cardsRating: 64,

    homeXg: 1.72,
    awayXg: 1.58,
    expectedCorners: 11.3,
    expectedCards: 4.8,

    weather: "Light wind, 10°C",
    teamNews: "Both teams expected to use attacking formations.",

    reasons: [
      "Both teams rank highly for corners won.",
      "The model projects more than eleven total corners.",
      "Dortmund create frequent wide attacks at home.",
      "Leipzig concede a high number of away corners.",
      "The bookmaker line is below the model projection.",
    ],

    bookmakerOdds: [
      { name: "Betfair", odds: 2.2 },
      { name: "Pinnacle", odds: 2.14 },
      { name: "Bet365", odds: 2.1 },
      { name: "Unibet", odds: 2.08 },
    ],
  },
];