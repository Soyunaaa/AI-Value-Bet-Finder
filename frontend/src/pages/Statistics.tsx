import type { ReactNode } from "react";

import {
  BarChart3,
  CircleDollarSign,
  Percent,
  Target,
  Trophy,
  TrendingUp,
} from "lucide-react";

import DashboardLayout from "../components/layout/DashboardLayout";
import MonthlyProfitChart from "../components/dashboard/MonthlyProfitChart";

import {
  bookmakerStatistics,
  leagueStatistics,
  marketStatistics,
} from "../data/statistics";

export default function Statistics() {
  const totalBets = marketStatistics.reduce(
    (total, market) => total + market.bets,
    0
  );

  const totalWins = marketStatistics.reduce(
    (total, market) => total + market.wins,
    0
  );

  const totalProfit = marketStatistics.reduce(
    (total, market) => total + market.profit,
    0
  );

  const winRate = (totalWins / totalBets) * 100;
  const roi = (totalProfit / totalBets) * 100;

  const bestMarket = [...marketStatistics].sort(
    (first, second) => second.roi - first.roi
  )[0];

  const worstMarket = [...marketStatistics].sort(
    (first, second) => first.roi - second.roi
  )[0];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <section className="flex items-center gap-3">
          <div className="rounded-xl bg-cyan-500/10 p-3 text-cyan-400">
            <BarChart3 size={27} />
          </div>

          <div>
            <h1 className="text-3xl font-bold text-white">
              Statistics
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              Track model performance across markets, leagues and bookmakers
            </p>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            title="Tracked Bets"
            value={totalBets.toString()}
            icon={<Target size={25} />}
            color="text-cyan-400"
          />

          <SummaryCard
            title="Win Rate"
            value={`${winRate.toFixed(1)}%`}
            icon={<Trophy size={25} />}
            color="text-yellow-400"
          />

          <SummaryCard
            title="Net Profit"
            value={`+${totalProfit.toFixed(1)}u`}
            icon={<CircleDollarSign size={25} />}
            color="text-green-400"
          />

          <SummaryCard
            title="ROI"
            value={`${roi.toFixed(1)}%`}
            icon={<TrendingUp size={25} />}
            color="text-purple-400"
          />
        </section>

        <section className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-5">
          <p className="font-medium text-cyan-400">
            Demonstration performance data
          </p>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            These statistics are generated from placeholder results.
            Real bet history and model performance will later come from
            the backend database.
          </p>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
          <MonthlyProfitChart />

          <div className="space-y-6">
            <PerformanceHighlight
              label="Best-performing market"
              market={bestMarket.market}
              value={`${bestMarket.roi.toFixed(1)}% ROI`}
              description={`+${bestMarket.profit.toFixed(1)} units from ${bestMarket.bets} bets`}
              positive
            />

            <PerformanceHighlight
              label="Lowest-performing market"
              market={worstMarket.market}
              value={`${worstMarket.roi.toFixed(1)}% ROI`}
              description={`+${worstMarket.profit.toFixed(1)} units from ${worstMarket.bets} bets`}
            />
          </div>
        </section>

        <section className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800">
          <div className="border-b border-slate-700 px-6 py-5">
            <h2 className="text-xl font-semibold text-white">
              Market Performance
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Results grouped by betting market
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px]">
              <thead>
                <tr className="border-b border-slate-700 text-left text-xs uppercase tracking-wider text-slate-500">
                  <th className="px-6 py-4 font-medium">Market</th>
                  <th className="px-4 py-4 font-medium">Bets</th>
                  <th className="px-4 py-4 font-medium">Wins</th>
                  <th className="px-4 py-4 font-medium">Win rate</th>
                  <th className="px-4 py-4 font-medium">Profit</th>
                  <th className="px-6 py-4 font-medium">ROI</th>
                </tr>
              </thead>

              <tbody>
                {marketStatistics.map((market) => (
                  <tr
                    key={market.market}
                    className="border-b border-slate-700/70 transition last:border-b-0 hover:bg-slate-700/30"
                  >
                    <td className="px-6 py-4 font-semibold text-white">
                      {market.market}
                    </td>

                    <td className="px-4 py-4 text-slate-300">
                      {market.bets}
                    </td>

                    <td className="px-4 py-4 text-slate-300">
                      {market.wins}
                    </td>

                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <span className="w-12 text-sm font-semibold text-white">
                          {market.winRate.toFixed(1)}%
                        </span>

                        <div className="h-2 w-24 overflow-hidden rounded-full bg-slate-700">
                          <div
                            className="h-full rounded-full bg-cyan-400"
                            style={{
                              width: `${market.winRate}%`,
                            }}
                          />
                        </div>
                      </div>
                    </td>

                    <td className="px-4 py-4 font-semibold text-green-400">
                      +{market.profit.toFixed(1)}u
                    </td>

                    <td className="px-6 py-4 font-semibold text-cyan-400">
                      {market.roi.toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <PerformanceList
            title="League Performance"
            subtitle="Results grouped by competition"
            items={leagueStatistics.map((league) => ({
              name: league.league,
              details: `${league.bets} bets`,
              profit: league.profit,
              roi: league.roi,
            }))}
          />

          <PerformanceList
            title="Bookmaker Performance"
            subtitle="Results grouped by selected bookmaker"
            items={bookmakerStatistics.map((bookmaker) => ({
              name: bookmaker.bookmaker,
              details: `${bookmaker.bets} bets · Avg odds ${bookmaker.averageOdds.toFixed(
                2
              )}`,
              profit: bookmaker.profit,
              roi: bookmaker.roi,
            }))}
          />
        </section>
      </div>
    </DashboardLayout>
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
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-5 transition hover:-translate-y-1 hover:border-cyan-500/60">
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

interface PerformanceHighlightProps {
  label: string;
  market: string;
  value: string;
  description: string;
  positive?: boolean;
}

function PerformanceHighlight({
  label,
  market,
  value,
  description,
  positive = false,
}: PerformanceHighlightProps) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <h2 className="mt-3 text-xl font-bold text-white">
        {market}
      </h2>

      <p
        className={`mt-3 text-3xl font-bold ${
          positive ? "text-green-400" : "text-cyan-400"
        }`}
      >
        {value}
      </p>

      <p className="mt-2 text-sm text-slate-400">
        {description}
      </p>
    </div>
  );
}

interface PerformanceItem {
  name: string;
  details: string;
  profit: number;
  roi: number;
}

interface PerformanceListProps {
  title: string;
  subtitle: string;
  items: PerformanceItem[];
}

function PerformanceList({
  title,
  subtitle,
  items,
}: PerformanceListProps) {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <div>
        <h2 className="text-xl font-semibold text-white">
          {title}
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          {subtitle}
        </p>
      </div>

      <div className="mt-6 space-y-5">
        {items.map((item) => (
          <div key={item.name}>
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-white">
                  {item.name}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  {item.details}
                </p>
              </div>

              <div className="text-right">
                <p className="font-semibold text-green-400">
                  +{item.profit.toFixed(1)}u
                </p>

                <p className="mt-1 text-xs text-cyan-400">
                  {item.roi.toFixed(1)}% ROI
                </p>
              </div>
            </div>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-700">
              <div
                className="h-full rounded-full bg-cyan-400"
                style={{
                  width: `${Math.min(item.roi * 4, 100)}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}