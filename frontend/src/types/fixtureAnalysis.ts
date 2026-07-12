import type { FootballFixture } from "./football";

export interface MarketProbability {
  probability: number;
  fair_odds: number | null;
}

export interface ScoreProbability {
  home_goals: number;
  away_goals: number;
  probability: number;
}

export interface MatchPrediction {
  home_team: string;
  away_team: string;

  home_expected_goals: number;
  away_expected_goals: number;
  total_expected_goals: number;

  home_win: MarketProbability;
  draw: MarketProbability;
  away_win: MarketProbability;

  over_2_5: MarketProbability;
  under_2_5: MarketProbability;

  both_teams_to_score_yes: MarketProbability;
  both_teams_to_score_no: MarketProbability;

  most_likely_score: ScoreProbability;
  score_probabilities: ScoreProbability[];
}

export interface TeamFormSummary {
  team_id: number;
  team_name: string;
  matches_used: number;

  wins: number;
  draws: number;
  losses: number;

  goals_scored: number;
  goals_conceded: number;

  average_goals_scored: number;
  average_goals_conceded: number;
  points_per_game: number;
}

export interface TeamStrengthRating {
  team_id: number;
  team_name: string;
  matches_used: number;

  attack_rating: number;
  defence_rating: number;
  form_rating: number;
  overall_rating: number;

  average_goals_scored: number;
  average_goals_conceded: number;
  points_per_game: number;

  home_average_scored: number;
  home_average_conceded: number;

  away_average_scored: number;
  away_average_conceded: number;
}

export interface FixtureAnalysis {
  fixture: FootballFixture;

  home_form: TeamFormSummary;
  away_form: TeamFormSummary;

  home_strength: TeamStrengthRating;
  away_strength: TeamStrengthRating;

  elo: FixtureEloSummary;
  league_calibration: LeagueCalibrationSummary;

  data_sources: AnalysisDataSources;

  home_expected_goals: number;
  away_expected_goals: number;

  prediction: MatchPrediction;

  confidence: number;
  reasons: string[];
}
export interface TeamEloRating {
  team_id: number;
  team_name: string;
  rating: number;
  matches_processed: number;
}

export interface FixtureEloSummary {
  home: TeamEloRating;
  away: TeamEloRating;

  rating_difference: number;
  expected_home_score: number;
  expected_away_score: number;
}
export interface LeagueCalibrationSummary {
  competition_code: string;
  goal_environment: number;
  home_advantage_multiplier: number;
  elo_home_advantage: number;
}
export type AnalysisDataSource =
  | "database"
  | "external_api"
  | "merged"
  | "calculated";

export interface AnalysisDataSources {
  fixture: AnalysisDataSource;
  home_history: AnalysisDataSource;
  away_history: AnalysisDataSource;
  home_statistics: AnalysisDataSource;
  away_statistics: AnalysisDataSource;
}