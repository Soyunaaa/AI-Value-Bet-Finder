export interface FootballTeam {
  id: number;
  name: string;
  short_name: string | null;
  tla: string | null;
  crest: string | null;
}

export interface FootballCompetition {
  id: number;
  code: string;
  name: string;
  emblem: string | null;
}

export interface FootballScore {
  home: number | null;
  away: number | null;
}

export type MatchStatus =
  | "SCHEDULED"
  | "TIMED"
  | "IN_PLAY"
  | "PAUSED"
  | "FINISHED"
  | "POSTPONED"
  | "SUSPENDED"
  | "CANCELLED"
  | "UNKNOWN";

export interface FootballFixture {
  id: number;
  utc_date: string;
  status: MatchStatus;
  matchday: number | null;

  competition: FootballCompetition;
  home_team: FootballTeam;
  away_team: FootballTeam;

  full_time: FootballScore;
  half_time: FootballScore;
}