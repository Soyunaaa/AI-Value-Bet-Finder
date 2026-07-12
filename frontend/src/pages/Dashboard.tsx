import {
  Brain,
  CalendarDays,
  Gem,
  Percent,
} from "lucide-react";

import { useState } from "react";

import DashboardLayout from "../components/layout/DashboardLayout";
import LeagueSelector from "../components/dashboard/LeagueSelector";
import LiveMatchCard from "../components/dashboard/LiveMatchCard";
import MarketBreakdown from "../components/dashboard/MarketBreakdown";
import ProfitChart from "../components/dashboard/ProfitChart";
import RecentActivity from "../components/dashboard/RecentActivity";
import StatCard from "../components/dashboard/StatCard";
import UpcomingFixtures from "../components/dashboard/UpcomingFixtures";
import ValueBetTable from "../components/dashboard/ValueBetTable";

import type { LeagueOption } from "../components/dashboard/LeagueSelector";

import { useFixtures } from "../hooks/useFixtures";

const leagues: LeagueOption[] = [
  {
    code: "PL",
    name: "Premier League",
    country: "England",
  },
  {
    code: "PD",
    name: "La Liga",
    country: "Spain",
  },
  {
    code: "BL1",
    name: "Bundesliga",
    country: "Germany",
  },
  {
    code: "SA",
    name: "Serie A",
    country: "Italy",
  },
  {
    code: "FL1",
    name: "Ligue 1",
    country: "France",
  },
  {
    code: "CL",
    name: "Champions League",
    country: "Europe",
  },
];

export default function Dashboard() {
  const [selectedLeague, setSelectedLeague] =
    useState<LeagueOption>(leagues[0]);

  const {
    fixtures,
    loading,
    refreshing,
    error,
    refresh,
    retry,
  } = useFixtures({
    competition: selectedLeague.code,
  });

  const liveMatches = fixtures.filter(
    (fixture) => fixture.status === "IN_PLAY"
  ).length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <LeagueSelector
          leagues={leagues}
          selectedLeague={selectedLeague}
          onLeagueChange={setSelectedLeague}
        />

        <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Loaded Fixtures"
            value={loading ? "..." : fixtures.length.toString()}
            icon={<CalendarDays size={30} />}
            trend={6.7}
            description={selectedLeague.name}
          />

          <StatCard
            title="Live Matches"
            value={loading ? "..." : liveMatches.toString()}
            icon={<Gem size={30} />}
            color="text-green-400"
            trend={12.5}
            description="currently active"
          />

          <StatCard
            title="Average EV"
            value="18.1%"
            icon={<Percent size={30} />}
            trend={2.3}
            description="backend demo"
          />

          <StatCard
            title="AI Confidence"
            value="91%"
            icon={<Brain size={30} />}
            color="text-yellow-400"
            trend={-1.2}
            description="backend demo"
          />
        </section>

        <UpcomingFixtures
          fixtures={fixtures}
          loading={loading}
          refreshing={refreshing}
          error={error}
          onRefresh={refresh}
          onRetry={retry}
        />

        <section className="grid grid-cols-1 gap-6 2xl:grid-cols-[minmax(0,2fr)_minmax(340px,1fr)]">
          <ValueBetTable />
          <LiveMatchCard />
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
          <ProfitChart />
          <MarketBreakdown />
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <h2 className="text-xl font-semibold text-white">
              Dashboard Summary
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Current data connection status
            </p>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">
                  Fixtures Source
                </p>

                <p className="mt-2 text-lg font-bold text-white">
                  FastAPI
                </p>
              </div>

              <div className="rounded-xl bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">
                  Competition
                </p>

                <p className="mt-2 text-lg font-bold text-white">
                  {selectedLeague.name}
                </p>
              </div>

              <div className="rounded-xl bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">
                  Provider Status
                </p>

                <p
                  className={`mt-2 text-lg font-bold ${
                    error ? "text-red-400" : "text-green-400"
                  }`}
                >
                  {error ? "Unavailable" : "Connected"}
                </p>
              </div>
            </div>

            <div className="mt-6 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-5">
              <p className="font-medium text-cyan-400">
                Live fixture integration
              </p>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                The dashboard now reloads fixtures whenever you
                select another competition. Match availability
                depends on your football-data.org plan.
              </p>
            </div>
          </div>

          <RecentActivity />
        </section>
      </div>
    </DashboardLayout>
  );
}