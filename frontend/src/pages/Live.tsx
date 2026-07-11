import {
  Activity,
  CircleDot,
  Radio,
  RefreshCw,
} from "lucide-react";

import DashboardLayout from "../components/layout/DashboardLayout";
import LiveMatchListCard from "../components/dashboard/LiveMatchListCard";
import { liveMatches } from "../data/liveMatches";

export default function Live() {
  const matchesWithValue = liveMatches.filter(
    (match) => match.valueMarket
  ).length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <section className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <div className="rounded-xl bg-red-500/10 p-3 text-red-400">
                <Radio size={25} />
              </div>

              <div>
                <h1 className="text-3xl font-bold text-white">
                  Live Matches
                </h1>

                <p className="mt-1 text-sm text-slate-400">
                  Live scores, statistics and in-play value opportunities
                </p>
              </div>
            </div>
          </div>

          <button
            type="button"
            className="flex items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm font-medium text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400"
          >
            <RefreshCw size={17} />
            Refresh matches
          </button>
        </section>

        <section className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <SummaryCard
            title="Live now"
            value={liveMatches.length.toString()}
            icon={<CircleDot size={23} />}
            color="text-red-400"
          />

          <SummaryCard
            title="Live value bets"
            value={matchesWithValue.toString()}
            icon={<Activity size={23} />}
            color="text-green-400"
          />

          <SummaryCard
            title="Tracked leagues"
            value="4"
            icon={<Radio size={23} />}
            color="text-cyan-400"
          />
        </section>

        <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 px-5 py-4">
          <p className="font-medium text-cyan-400">
            Demonstration live data
          </p>

          <p className="mt-1 text-sm text-slate-400">
            These fixtures are currently mock data. Live scores and
            statistics will later be loaded from the backend.
          </p>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-2 2xl:grid-cols-3">
          {liveMatches.map((match) => (
            <LiveMatchListCard key={match.id} match={match} />
          ))}
        </section>
      </div>
    </DashboardLayout>
  );
}

interface SummaryCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
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
          <p className="text-sm text-slate-400">{title}</p>
          <p className={`mt-2 text-3xl font-bold ${color}`}>
            {value}
          </p>
        </div>

        <div className={`rounded-xl bg-slate-900/60 p-3 ${color}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}