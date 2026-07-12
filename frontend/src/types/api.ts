export interface ApiBookmakerOdds {
  name: string;
  odds: number;
}

export interface ApiValueBet {
  id: number;
  match: string;
  league: string;
  home_team: string;
  away_team: string;
  kickoff: string;

  market: string;
  bookmaker: string;

  odds: number;
  fair_odds: number;
  expected_value: number;
  confidence: number;

  attack_rating: number;
  defence_rating: number;
  goals_rating: number;
  corners_rating: number;
  cards_rating: number;

  home_xg: number;
  away_xg: number;
  expected_corners: number;
  expected_cards: number;

  weather: string;
  team_news: string;

  reasons: string[];
  bookmaker_odds: ApiBookmakerOdds[];
}