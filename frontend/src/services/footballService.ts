import type { FootballFixture } from "../types/football";

import { apiRequest } from "./api";

interface GetFixturesOptions {
  competition?: string;
  dateFrom?: string;
  dateTo?: string;
}

export async function getFixtures(
  options: GetFixturesOptions = {}
): Promise<FootballFixture[]> {
  const params = new URLSearchParams();

  if (options.competition) {
    params.set("competition", options.competition);
  }

  if (options.dateFrom) {
    params.set("date_from", options.dateFrom);
  }

  if (options.dateTo) {
    params.set("date_to", options.dateTo);
  }

  const query = params.toString();

  return apiRequest<FootballFixture[]>(
    `/football/matches${query ? `?${query}` : ""}`
  );
}