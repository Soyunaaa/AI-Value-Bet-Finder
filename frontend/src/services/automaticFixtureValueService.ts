import type { AutomaticFixtureValue } from "../types/automaticFixtureValue";

import { apiRequest } from "./api";

interface GetAutomaticFixtureValueOptions {
  sportKey: string;
  region?: string;
  bankroll?: number;
  kellyFraction?: number;
  minimumExpectedValue?: number;
}

export async function getAutomaticFixtureValue(
  fixtureId: number,
  options: GetAutomaticFixtureValueOptions
): Promise<AutomaticFixtureValue> {
  const params = new URLSearchParams({
    sport_key: options.sportKey,
    region: options.region ?? "eu",
    bankroll: String(options.bankroll ?? 1000),
    kelly_fraction: String(
      options.kellyFraction ?? 0.25
    ),
    minimum_expected_value: String(
      options.minimumExpectedValue ?? 0.05
    ),
  });

  return apiRequest<AutomaticFixtureValue>(
    `/automatic-fixture-value/${fixtureId}?${params.toString()}`
  );
}