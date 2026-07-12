import { useCallback, useState } from "react";

import type { AutomaticFixtureValue } from "../types/automaticFixtureValue";

import { getAutomaticFixtureValue } from "../services/automaticFixtureValueService";

interface ScanOptions {
  sportKey: string;
  region?: string;
  bankroll?: number;
  kellyFraction?: number;
  minimumExpectedValue?: number;
}

export function useAutomaticFixtureValue(
  fixtureId: number
) {
  const [result, setResult] =
    useState<AutomaticFixtureValue | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] =
    useState<string | null>(null);

  const scan = useCallback(
    async (options: ScanOptions) => {
      if (
        !Number.isInteger(fixtureId) ||
        fixtureId <= 0
      ) {
        setError("Invalid fixture ID.");
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const response =
          await getAutomaticFixtureValue(
            fixtureId,
            options
          );

        setResult(response);
      } catch (requestError) {
        const message =
          requestError instanceof Error
            ? requestError.message
            : "Unable to scan bookmaker odds.";

        setError(message);
      } finally {
        setLoading(false);
      }
    },
    [fixtureId]
  );

  return {
    result,
    loading,
    error,
    scan,
    clearError: () => setError(null),
  };
}