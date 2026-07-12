import {
  AlertCircle,
  CalendarClock,
  ChevronRight,
  CircleDot,
  Clock3,
  LoaderCircle,
  RefreshCw,
} from "lucide-react";

import type { FootballFixture } from "../../types/football";

interface UpcomingFixturesProps {
  fixtures: FootballFixture[];
  loading: boolean;
  refreshing: boolean;
  error: string | null;
  onRefresh: () => void;
  onRetry: () => void;
}

function formatKickoff(utcDate: string) {
  return new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(utcDate));
}

function formatDate(utcDate: string) {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
  }).format(new Date(utcDate));
}

function getStatusLabel(status: FootballFixture["status"]) {
  const labels: Record<FootballFixture["status"], string> = {
    SCHEDULED: "Scheduled",
    TIMED: "Upcoming",
    IN_PLAY: "Live",
    PAUSED: "Paused",
    FINISHED: "Finished",
    POSTPONED: "Postponed",
    SUSPENDED: "Suspended",
    CANCELLED: "Cancelled",
    UNKNOWN: "Unknown",
  };

  return labels[status];
}

export default function UpcomingFixtures({
  fixtures = [],
  loading,
  refreshing,
  error,
  onRefresh,
  onRetry,
}: UpcomingFixturesProps) {
  return (
    <section className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800">
      <div className="border-b border-slate-700 px-6 py-5">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <CalendarClock
                size={21}
                className="text-cyan-400"
              />

              <h2 className="text-xl font-semibold text-white">
                Upcoming Fixtures
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              Real match data from the football provider
            </p>
          </div>

          <button
            type="button"
            onClick={onRefresh}
            disabled={refreshing}
            className="flex items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <RefreshCw
              size={16}
              className={refreshing ? "animate-spin" : ""}
            />

            {refreshing ? "Refreshing..." : "Refresh"}
          </button>
        </div>
      </div>

      {loading ? (
        <div className="px-6 py-14 text-center">
          <LoaderCircle
            size={36}
            className="mx-auto animate-spin text-cyan-400"
          />

          <p className="mt-4 font-medium text-white">
            Loading fixtures
          </p>

          <p className="mt-2 text-sm text-slate-400">
            Requesting match data from FastAPI.
          </p>
        </div>
      ) : error ? (
        <div className="px-6 py-14 text-center">
          <AlertCircle
            size={36}
            className="mx-auto text-red-400"
          />

          <p className="mt-4 font-medium text-white">
            Unable to load fixtures
          </p>

          <p className="mt-2 text-sm text-slate-400">
            {error}
          </p>

          <button
            type="button"
            onClick={onRetry}
            className="mt-5 rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
          >
            Try again
          </button>
        </div>
      ) : fixtures.length === 0 ? (
        <div className="px-6 py-14 text-center">
          <CalendarClock
            size={36}
            className="mx-auto text-slate-600"
          />

          <p className="mt-4 font-medium text-white">
            No fixtures found
          </p>

          <p className="mt-2 text-sm text-slate-400">
            The provider returned no matches for this selection.
          </p>
        </div>
      ) : (
        <div className="divide-y divide-slate-700/70">
          {fixtures.slice(0, 8).map((fixture) => (
            <button
              key={fixture.id}
              type="button"
              className="grid w-full grid-cols-[80px_1fr_auto] items-center gap-4 px-6 py-5 text-left transition hover:bg-slate-700/30"
            >
              <div>
                <div className="flex items-center gap-2 text-white">
                  <Clock3
                    size={15}
                    className="text-slate-500"
                  />

                  <span className="font-semibold">
                    {formatKickoff(fixture.utc_date)}
                  </span>
                </div>

                <span className="mt-1 block text-xs text-slate-500">
                  {formatDate(fixture.utc_date)}
                </span>
              </div>

              <div className="min-w-0">
                <p className="text-xs font-medium uppercase tracking-wider text-cyan-400">
                  {fixture.competition.name}
                </p>

                <div className="mt-2 flex flex-wrap items-center gap-2">
                  <span className="font-semibold text-white">
                    {fixture.home_team.name}
                  </span>

                  <span className="text-xs text-slate-500">
                    vs
                  </span>

                  <span className="font-semibold text-white">
                    {fixture.away_team.name}
                  </span>
                </div>

                <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                  <CircleDot
                    size={13}
                    className={
                      fixture.status === "IN_PLAY"
                        ? "text-red-400"
                        : "text-green-400"
                    }
                  />

                  <span>{getStatusLabel(fixture.status)}</span>

                  {fixture.matchday !== null && (
                    <>
                      <span>•</span>
                      <span>Matchday {fixture.matchday}</span>
                    </>
                  )}
                </div>
              </div>

              <ChevronRight
                size={20}
                className="text-slate-500"
              />
            </button>
          ))}
        </div>
      )}
    </section>
  );
}