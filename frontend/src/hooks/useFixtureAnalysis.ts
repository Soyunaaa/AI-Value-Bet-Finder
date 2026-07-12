import {
  useCallback,
  useEffect,
  useState,
} from "react";

import type { FixtureAnalysis } from "../types/fixtureAnalysis";

import { getFixtureAnalysis } from "../services/fixtureAnalysisService";

export function useFixtureAnalysis(
  fixtureId: number
) {
  const [analysis, setAnalysis] =
    useState<FixtureAnalysis | null>(null);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadAnalysis = useCallback(
    async (showRefreshState = false) => {
      if (
        !Number.isInteger(fixtureId) ||
        fixtureId <= 0
      ) {
        setError("Invalid fixture ID.");
        setLoading(false);
        return;
      }

      if (showRefreshState) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError(null);

      try {
        const result =
          await getFixtureAnalysis(fixtureId);

        setAnalysis(result);
      } catch (requestError) {
        const message =
          requestError instanceof Error
            ? requestError.message
            : "Unable to load fixture analysis.";

        setError(message);
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [fixtureId]
  );

  useEffect(() => {
    void loadAnalysis();
  }, [loadAnalysis]);

  return {
    analysis,
    loading,
    refreshing,
    error,
    refresh: () => loadAnalysis(true),
    retry: () => loadAnalysis(false),
  };
}