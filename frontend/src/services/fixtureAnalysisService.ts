import type { FixtureAnalysis } from "../types/fixtureAnalysis";

import { apiRequest } from "./api";

export async function getFixtureAnalysis(
  fixtureId: number
): Promise<FixtureAnalysis> {
  return apiRequest<FixtureAnalysis>(
    `/fixture-analysis/${fixtureId}`
  );
}