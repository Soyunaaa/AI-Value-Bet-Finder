import { useMemo, useState } from "react";
import { Gem, Percent, ShieldCheck, Sparkles } from "lucide-react";

import DashboardLayout from "../components/layout/DashboardLayout";
import ValueBetCard from "../components/valueBets/ValueBetCard";
import ValueBetFilters from "../components/valueBets/ValueBetFilters";
import { valueBets } from "../data/valueBets";

function getMarketGroup(market: string) {
  const lowerMarket = market.toLowerCase();

  if (lowerMarket.includes("corner")) return "Corners";
  if (lowerMarket.includes("asian handicap")) return "Asian Handicap";
  if (lowerMarket.includes("both teams")) return "BTTS";
  if (lowerMarket.includes("over") || lowerMarket.includes("under")) {
    return "Goals";
  }

  return "1X2";
}

export default function ValueBets() {
  const [search, setSearch] = useState("");
  const [league, setLeague] = useState("All");
  const [market, setMarket] = useState("All");
  const [sortBy, setSortBy] = useState("ev");

  const filteredBets = useMemo(() => {
    const result = valueBets.filter((bet) => {
      const matchesSearch = bet.match
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesLeague =
        league === "All" || bet.league === league;

      const matchesMarket =
        market === "All" || getMarketGroup(bet.market) === market;

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
  }, [search, league, market, sortBy]);

  const averageEv =
    valueBets.reduce((total, bet) => total + bet.ev, 0) /
    valueBets.length;

  const averageConfidence =
    valueBets.reduce((total, bet) => total + bet.confidence, 0) /
    valueBets.length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <section className="flex items-center gap-3">
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
        </section>

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
            Demonstration recommendations
          </p>

          <p className="mt-1 text-sm leading-6 text-slate-400">
            The current probabilities and bookmaker odds are mock data.
            They are not betting advice and should not be treated as live
            market information.
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
              Showing {filteredBets.length} of {valueBets.length} bets
            </p>
          </div>

          {filteredBets.length > 0 ? (
            <div className="grid grid-cols-1 gap-6 xl:grid-cols-2 2xl:grid-cols-3">
              {filteredBets.map((bet) => (
                <ValueBetCard key={bet.id} bet={bet} />
              ))}
            </div>
          ) : (
            <div className="rounded-2xl border border-slate-700 bg-slate-800 p-12 text-center">
              <Gem size={36} className="mx-auto text-slate-600" />

              <h2 className="mt-4 text-lg font-semibold text-white">
                No value bets found
              </h2>

              <p className="mt-2 text-sm text-slate-400">
                Try changing the filters or search term.
              </p>
            </div>
          )}
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