import {
  useCallback,
  useEffect,
  useState,
} from "react";

import type { FootballFixture } from "../types/football";

import { getFixtures } from "../services/footballService";

interface UseFixturesOptions {
  competition?: string;
  dateFrom?: string;
  dateTo?: string;
}

export function useFixtures(
  options: UseFixturesOptions = {}
) {
  const [fixtures, setFixtures] = useState<FootballFixture[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadFixtures = useCallback(
    async (showRefreshState = false) => {
      if (showRefreshState) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError(null);

      try {
        const result = await getFixtures(options);
        setFixtures(result);
      } catch (requestError) {
        const message =
          requestError instanceof Error
            ? requestError.message
            : "Unable to load fixtures.";

        setError(message);
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [
      options.competition,
      options.dateFrom,
      options.dateTo,
    ]
  );

  useEffect(() => {
    void loadFixtures();
  }, [loadFixtures]);

  return {
    fixtures,
    loading,
    refreshing,
    error,
    refresh: () => loadFixtures(true),
    retry: () => loadFixtures(false),
  };
}