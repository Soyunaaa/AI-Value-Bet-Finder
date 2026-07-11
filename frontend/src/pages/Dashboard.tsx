import {
  Brain,
  CalendarDays,
  Gem,
  Percent,
} from "lucide-react";

import DashboardLayout from "../components/layout/DashboardLayout";
import LiveMatchCard from "../components/dashboard/LiveMatchCard";
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
            icon={<CalendarDays size={34} />}
          />

          <StatCard
            title="Value Bets"
            value="18"
            icon={<Gem size={34} />}
            color="text-green-400"
          />

          <StatCard
            title="Average EV"
            value="12.8%"
            icon={<Percent size={34} />}
          />

          <StatCard
            title="AI Confidence"
            value="91%"
            icon={<Brain size={34} />}
            color="text-yellow-400"
          />
        </section>

        <section className="grid grid-cols-1 gap-6 2xl:grid-cols-[minmax(0,2fr)_minmax(340px,1fr)]">
          <ValueBetTable />
          <LiveMatchCard />
        </section>
      </div>
    </DashboardLayout>
  );
}