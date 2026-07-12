import { Check, ChevronDown, Trophy } from "lucide-react";
import { useState } from "react";

export interface LeagueOption {
  code: string;
  name: string;
  country: string;
}

interface LeagueSelectorProps {
  leagues: LeagueOption[];
  selectedLeague: LeagueOption;
  onLeagueChange: (league: LeagueOption) => void;
}

export default function LeagueSelector({
  leagues,
  selectedLeague,
  onLeagueChange,
}: LeagueSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  function selectLeague(league: LeagueOption) {
    onLeagueChange(league);
    setIsOpen(false);
  }

  return (
    <section className="relative rounded-2xl border border-slate-700 bg-slate-800 p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-cyan-500/10 p-3 text-cyan-400">
            <Trophy size={22} />
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              Selected competition
            </p>

            <h2 className="mt-1 text-lg font-semibold text-white">
              {selectedLeague.name}
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              {selectedLeague.country}
            </p>
          </div>
        </div>

        <div className="relative">
          <button
            type="button"
            onClick={() => setIsOpen((current) => !current)}
            className="flex w-full min-w-52 items-center justify-between gap-3 rounded-xl border border-slate-700 bg-slate-900/60 px-4 py-3 text-sm font-medium text-slate-200 transition hover:border-cyan-500 sm:w-auto"
          >
            Change competition

            <ChevronDown
              size={18}
              className={`transition ${
                isOpen ? "rotate-180" : ""
              }`}
            />
          </button>

          {isOpen && (
            <div className="absolute right-0 z-30 mt-2 w-72 overflow-hidden rounded-xl border border-slate-700 bg-slate-900 shadow-2xl">
              {leagues.map((league) => {
                const isSelected =
                  league.code === selectedLeague.code;

                return (
                  <button
                    key={league.code}
                    type="button"
                    onClick={() => selectLeague(league)}
                    className="flex w-full items-center justify-between gap-4 border-b border-slate-800 px-4 py-3 text-left transition last:border-b-0 hover:bg-slate-800"
                  >
                    <div>
                      <p
                        className={`font-medium ${
                          isSelected
                            ? "text-cyan-400"
                            : "text-white"
                        }`}
                      >
                        {league.name}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {league.country} · {league.code}
                      </p>
                    </div>

                    {isSelected && (
                      <Check
                        size={18}
                        className="shrink-0 text-cyan-400"
                      />
                    )}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}