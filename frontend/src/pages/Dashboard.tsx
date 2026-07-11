import {
  Brain,
  CalendarDays,
  Gem,
  Percent,
} from "lucide-react";

import DashboardLayout from "../components/layout/DashboardLayout";
import LiveMatchCard from "../components/dashboard/LiveMatchCard";
import MarketBreakdown from "../components/dashboard/MarketBreakdown";
import ProfitChart from "../components/dashboard/ProfitChart";
import RecentActivity from "../components/dashboard/RecentActivity";
import StatCard from "../components/dashboard/StatCard";
import ValueBetTable from "../components/dashboard/ValueBetTable";

export default function Dashboard() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Today's Matches"
            value="127"
            icon={<CalendarDays size={30} />}
            trend={6.7}
            description="since yesterday"
          />

          <StatCard
            title="Value Bets"
            value="18"
            icon={<Gem size={30} />}
            color="text-green-400"
            trend={12.5}
            description="latest scan"
          />

          <StatCard
            title="Average EV"
            value="12.8%"
            icon={<Percent size={30} />}
            trend={2.3}
            description="this week"
          />

          <StatCard
            title="AI Confidence"
            value="91%"
            icon={<Brain size={30} />}
            color="text-yellow-400"
            trend={-1.2}
            description="since last scan"
          />
        </section>

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
              Current development status
            </p>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-xl bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">
                  Markets Tracked
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  4
                </p>
              </div>

              <div className="rounded-xl bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">
                  Bookmakers
                </p>

                <p className="mt-2 text-2xl font-bold text-white">
                  4
                </p>
              </div>

              <div className="rounded-xl bg-slate-900/60 p-5">
                <p className="text-sm text-slate-400">
                  Model Status
                </p>

                <p className="mt-2 text-2xl font-bold text-green-400">
                  Demo
                </p>
              </div>
            </div>

            <div className="mt-6 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-5">
              <p className="font-medium text-cyan-400">
                Development mode
              </p>

              <p className="mt-2 text-sm leading-6 text-slate-400">
                The dashboard currently uses demonstration data.
                Live statistics, odds and model predictions will be
                connected during the backend and API phases.
              </p>
            </div>
          </div>

          <RecentActivity />
        </section>
      </div>
    </DashboardLayout>
  );
}