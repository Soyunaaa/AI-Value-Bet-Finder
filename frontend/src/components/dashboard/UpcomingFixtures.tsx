import {
  CalendarClock,
  ChevronRight,
  CircleDot,
  Clock3,
} from "lucide-react";

const fixtures = [
  {
    id: 1,
    time: "18:30",
    league: "Premier League",
    homeTeam: "Liverpool",
    awayTeam: "Arsenal",
    markets: 14,
    status: "Upcoming",
  },
  {
    id: 2,
    time: "19:45",
    league: "Serie A",
    homeTeam: "Inter",
    awayTeam: "Atalanta",
    markets: 11,
    status: "Upcoming",
  },
  {
    id: 3,
    time: "20:00",
    league: "La Liga",
    homeTeam: "Barcelona",
    awayTeam: "Sevilla",
    markets: 16,
    status: "Upcoming",
  },
  {
    id: 4,
    time: "20:30",
    league: "Bundesliga",
    homeTeam: "Dortmund",
    awayTeam: "Leipzig",
    markets: 9,
    status: "Upcoming",
  },
];

const leagueFilters = [
  "All",
  "Premier League",
  "La Liga",
  "Serie A",
  "Bundesliga",
];

export default function UpcomingFixtures() {
  return (
    <section className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800">
      <div className="border-b border-slate-700 px-6 py-5">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div className="flex items-center gap-2">
              <CalendarClock size={21} className="text-cyan-400" />

              <h2 className="text-xl font-semibold text-white">
                Upcoming Fixtures
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              Matches currently being monitored by the model
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            {leagueFilters.map((league, index) => (
              <button
                key={league}
                type="button"
                className={`rounded-lg px-3 py-2 text-xs font-medium transition ${
                  index === 0
                    ? "bg-cyan-500 text-slate-950"
                    : "bg-slate-900/70 text-slate-400 hover:bg-slate-700 hover:text-white"
                }`}
              >
                {league}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="divide-y divide-slate-700/70">
        {fixtures.map((fixture) => (
          <button
            key={fixture.id}
            type="button"
            className="grid w-full grid-cols-[70px_1fr_auto] items-center gap-4 px-6 py-5 text-left transition hover:bg-slate-700/30"
          >
            <div>
              <div className="flex items-center gap-2 text-white">
                <Clock3 size={15} className="text-slate-500" />

                <span className="font-semibold">
                  {fixture.time}
                </span>
              </div>

              <span className="mt-1 block text-xs text-slate-500">
                Today
              </span>
            </div>

            <div className="min-w-0">
              <p className="text-xs font-medium uppercase tracking-wider text-cyan-400">
                {fixture.league}
              </p>

              <div className="mt-2 flex flex-wrap items-center gap-2">
                <span className="font-semibold text-white">
                  {fixture.homeTeam}
                </span>

                <span className="text-xs text-slate-500">
                  vs
                </span>

                <span className="font-semibold text-white">
                  {fixture.awayTeam}
                </span>
              </div>

              <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                <CircleDot size={13} className="text-green-400" />

                <span>{fixture.status}</span>

                <span>•</span>

                <span>{fixture.markets} tracked markets</span>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="hidden rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-400 sm:inline-flex">
                Analyse
              </span>

              <ChevronRight size={20} className="text-slate-500" />
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}