import { Filter, Search } from "lucide-react";

interface ValueBetFiltersProps {
  search: string;
  league: string;
  market: string;
  sortBy: string;
  onSearchChange: (value: string) => void;
  onLeagueChange: (value: string) => void;
  onMarketChange: (value: string) => void;
  onSortChange: (value: string) => void;
}

export default function ValueBetFilters({
  search,
  league,
  market,
  sortBy,
  onSearchChange,
  onLeagueChange,
  onMarketChange,
  onSortChange,
}: ValueBetFiltersProps) {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-5">
      <div className="flex items-center gap-2">
        <Filter size={20} className="text-cyan-400" />

        <div>
          <h2 className="font-semibold text-white">Filters</h2>
          <p className="text-sm text-slate-400">
            Narrow down available value bets
          </p>
        </div>
      </div>

      <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <label className="block">
          <span className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-500">
            Search
          </span>

          <div className="flex items-center rounded-xl border border-slate-700 bg-slate-900/60 px-3">
            <Search size={17} className="text-slate-500" />

            <input
              type="text"
              value={search}
              onChange={(event) => onSearchChange(event.target.value)}
              placeholder="Search teams..."
              className="w-full bg-transparent px-3 py-3 text-sm text-white outline-none placeholder:text-slate-600"
            />
          </div>
        </label>

        <label className="block">
          <span className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-500">
            League
          </span>

          <select
            value={league}
            onChange={(event) => onLeagueChange(event.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-900/60 px-3 py-3 text-sm text-white outline-none focus:border-cyan-500"
          >
            <option value="All">All leagues</option>
            <option value="Premier League">Premier League</option>
            <option value="La Liga">La Liga</option>
            <option value="Serie A">Serie A</option>
            <option value="Bundesliga">Bundesliga</option>
          </select>
        </label>

        <label className="block">
          <span className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-500">
            Market
          </span>

          <select
            value={market}
            onChange={(event) => onMarketChange(event.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-900/60 px-3 py-3 text-sm text-white outline-none focus:border-cyan-500"
          >
            <option value="All">All markets</option>
            <option value="Goals">Goals</option>
            <option value="1X2">1X2</option>
            <option value="Asian Handicap">Asian Handicap</option>
            <option value="Corners">Corners</option>
            <option value="BTTS">BTTS</option>
          </select>
        </label>

        <label className="block">
          <span className="mb-2 block text-xs font-medium uppercase tracking-wider text-slate-500">
            Sort by
          </span>

          <select
            value={sortBy}
            onChange={(event) => onSortChange(event.target.value)}
            className="w-full rounded-xl border border-slate-700 bg-slate-900/60 px-3 py-3 text-sm text-white outline-none focus:border-cyan-500"
          >
            <option value="ev">Highest EV</option>
            <option value="confidence">Highest confidence</option>
            <option value="odds">Highest odds</option>
          </select>
        </label>
      </div>
    </section>
  );
}