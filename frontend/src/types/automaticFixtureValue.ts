export interface PositiveValueSelection {
  fixture_id: number | null;

  market: string;
  selection: string;
  bookmaker: string;

  bookmaker_odds: number;
  model_probability: number;
  implied_probability: number;
  probability_edge: number;

  fair_odds: number;
  expected_value: number;

  full_kelly_fraction: number;
  recommended_kelly_fraction: number;
  recommended_stake: number;
}

export interface MarketEvaluationResult {
  fixture_id: number | null;

  selections_evaluated: number;
  positive_value_count: number;

  minimum_expected_value: number;

  positive_value_selections: PositiveValueSelection[];
}

export interface MatchedOddsEvent {
  odds_event_id: string;
  sport_key: string;

  home_team: string;
  away_team: string;

  match_score: number;
}

export interface AutomaticFixtureValue {
  fixture_id: number;

  home_team: string;
  away_team: string;
  competition: string;

  matched_event: MatchedOddsEvent;

  model_confidence: number;

  home_expected_goals: number;
  away_expected_goals: number;

  evaluation: MarketEvaluationResult;

  odds_requests_remaining: number | null;
}