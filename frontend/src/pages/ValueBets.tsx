import type { ReactNode } from "react";

import {
  AlertCircle,
  Gem,
  LoaderCircle,
  Percent,
  RefreshCw,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import {
  useEffect,
  useMemo,
  useState,
} from "react";

import DashboardLayout from "../components/layout/DashboardLayout";
import ValueBetCard from "../components/valueBets/ValueBetCard";
import ValueBetFilters from "../components/valueBets/ValueBetFilters";

import type { ValueBet } from "../data/valueBets";

import { getValueBets } from "../services/valueBetService";

function getMarketGroup(market: string) {
  const lowerMarket = market.toLowerCase();

  if (lowerMarket.includes("corner")) {
    return "Corners";
  }

  if (lowerMarket.includes("asian handicap")) {
    return "Asian Handicap";
  }

  if (lowerMarket.includes("both teams")) {
    return "BTTS";
  }

  if (
    lowerMarket.includes("over") ||
    lowerMarket.includes("under")
  ) {
    return "Goals";
  }

  return "1X2";
}

export default function ValueBets() {
  const [valueBets, setValueBets] = useState<ValueBet[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [league, setLeague] = useState("All");
  const [market, setMarket] = useState("All");
  const [sortBy, setSortBy] = useState("ev");

  async function loadValueBets(showRefreshState = false) {
    if (showRefreshState) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    setError(null);

    try {
      const bets = await getValueBets();
      setValueBets(bets);
    } catch (requestError) {
      const message =
        requestError instanceof Error
          ? requestError.message
          : "Unable to load value bets.";

      setError(message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    void loadValueBets();
  }, []);

  const filteredBets = useMemo(() => {
    const result = valueBets.filter((bet) => {
      const matchesSearch = bet.match
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesLeague =
        league === "All" || bet.league === league;

      const matchesMarket =
        market === "All" ||
        getMarketGroup(bet.market) === market;

      return matchesSearch && matchesLeague && matchesMarket;
    });

    return [...result].sort((firstBet, secondBet) => {
      if (sortBy === "confidence") {
        return secondBet.confidence - firstBet.confidence;
      }

      if (sortBy === "odds") {
        return secondBet.odds - firstBet.odds;
      }

      return secondBet.ev - firstBet.ev;
    });
  }, [
    valueBets,
    search,
    league,
    market,
    sortBy,
  ]);

  const averageEv =
    valueBets.length > 0
      ? valueBets.reduce(
          (total, bet) => total + bet.ev,
          0
        ) / valueBets.length
      : 0;

  const averageConfidence =
    valueBets.length > 0
      ? valueBets.reduce(
          (total, bet) => total + bet.confidence,
          0
        ) / valueBets.length
      : 0;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <section className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-cyan-500/10 p-3 text-cyan-400">
              <Gem size={26} />
            </div>

            <div>
              <h1 className="text-3xl font-bold text-white">
                Value Bets
              </h1>

              <p className="mt-1 text-sm text-slate-400">
                Compare model probabilities with bookmaker prices
              </p>
            </div>
          </div>

          <button
            type="button"
            disabled={refreshing}
            onClick={() => void loadValueBets(true)}
            className="flex items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm font-medium text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <RefreshCw
              size={17}
              className={refreshing ? "animate-spin" : ""}
            />

            {refreshing ? "Refreshing..." : "Refresh data"}
          </button>
        </section>

        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState
            message={error}
            onRetry={() => void loadValueBets()}
          />
        ) : (
          <>
            <section className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <SummaryCard
                title="Opportunities found"
                value={valueBets.length.toString()}
                icon={<Sparkles size={23} />}
                color="text-cyan-400"
              />

              <SummaryCard
                title="Average EV"
                value={`${averageEv.toFixed(1)}%`}
                icon={<Percent size={23} />}
                color="text-green-400"
              />

              <SummaryCard
                title="Average confidence"
                value={`${averageConfidence.toFixed(0)}%`}
                icon={<ShieldCheck size={23} />}
                color="text-yellow-400"
              />
            </section>

            <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-5">
              <p className="font-medium text-cyan-400">
                Connected to FastAPI
              </p>

              <p className="mt-1 text-sm leading-6 text-slate-400">
                These value bets are now loaded from the Python
                backend. The backend still contains demonstration
                data, but the frontend no longer imports it directly.
              </p>
            </section>

            <ValueBetFilters
              search={search}
              league={league}
              market={market}
              sortBy={sortBy}
              onSearchChange={setSearch}
              onLeagueChange={setLeague}
              onMarketChange={setMarket}
              onSortChange={setSortBy}
            />

            <section>
              <div className="mb-4 flex items-center justify-between">
                <p className="text-sm text-slate-400">
                  Showing {filteredBets.length} of{" "}
                  {valueBets.length} bets
                </p>
              </div>

              {filteredBets.length > 0 ? (
                <div className="grid grid-cols-1 gap-6 xl:grid-cols-2 2xl:grid-cols-3">
                  {filteredBets.map((bet) => (
                    <ValueBetCard
                      key={bet.id}
                      bet={bet}
                    />
                  ))}
                </div>
              ) : (
                <div className="rounded-2xl border border-slate-700 bg-slate-800 p-12 text-center">
                  <Gem
                    size={36}
                    className="mx-auto text-slate-600"
                  />

                  <h2 className="mt-4 text-lg font-semibold text-white">
                    No value bets found
                  </h2>

                  <p className="mt-2 text-sm text-slate-400">
                    Try changing the filters or search term.
                  </p>
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}

function LoadingState() {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-16 text-center">
      <LoaderCircle
        size={38}
        className="mx-auto animate-spin text-cyan-400"
      />

      <h2 className="mt-5 text-lg font-semibold text-white">
        Loading value bets
      </h2>

      <p className="mt-2 text-sm text-slate-400">
        Requesting data from the FastAPI backend.
      </p>
    </div>
  );
}

interface ErrorStateProps {
  message: string;
  onRetry: () => void;
}

function ErrorState({
  message,
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-10 text-center">
      <AlertCircle
        size={38}
        className="mx-auto text-red-400"
      />

      <h2 className="mt-5 text-lg font-semibold text-white">
        Unable to load value bets
      </h2>

      <p className="mx-auto mt-2 max-w-xl text-sm text-slate-400">
        {message}
      </p>

      <p className="mx-auto mt-2 max-w-xl text-sm text-slate-500">
        Make sure FastAPI is running on port 8000.
      </p>

      <button
        type="button"
        onClick={onRetry}
        className="mt-6 rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
      >
        Try again
      </button>
    </div>
  );
}

interface SummaryCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  color: string;
}

function SummaryCard({
  title,
  value,
  icon,
  color,
}: SummaryCardProps) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">
            {title}
          </p>

          <p className={`mt-2 text-3xl font-bold ${color}`}>
            {value}
          </p>
        </div>

        <div
          className={`rounded-xl bg-slate-900/60 p-3 ${color}`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}