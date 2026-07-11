import {
  ChartNoAxesColumnIncreasing,
  ChevronRight,
  CircleDot,
  Flag,
  Goal,
  RectangleHorizontal,
} from "lucide-react";

import type { LiveMatch } from "../../data/liveMatches";

interface LiveMatchListCardProps {
  match: LiveMatch;
}

export default function LiveMatchListCard({
  match,
}: LiveMatchListCardProps) {
  return (
    <article className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800 transition hover:-translate-y-1 hover:border-cyan-500/60">
      <div className="flex items-center justify-between border-b border-slate-700 px-5 py-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
            {match.league}
          </p>

          <div className="mt-1 flex items-center gap-2 text-xs font-semibold text-red-400">
            <CircleDot size={13} />
            Live · {match.minute}'
          </div>
        </div>

        <button
          type="button"
          className="rounded-lg bg-slate-900/60 p-2 text-slate-400 transition hover:bg-slate-700 hover:text-white"
          aria-label="Open match analysis"
        >
          <ChevronRight size={19} />
        </button>
      </div>

      <div className="px-5 py-6">
        <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-4">
          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-cyan-500/10 text-sm font-bold text-cyan-400">
              {match.homeTeam.slice(0, 3).toUpperCase()}
            </div>

            <p className="mt-3 font-semibold text-white">
              {match.homeTeam}
            </p>
          </div>

          <div className="text-center">
            <p className="text-3xl font-bold text-white">
              {match.homeScore} - {match.awayScore}
            </p>

            <p className="mt-1 text-xs uppercase tracking-wider text-slate-500">
              Score
            </p>
          </div>

          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-500/10 text-sm font-bold text-purple-400">
              {match.awayTeam.slice(0, 3).toUpperCase()}
            </div>

            <p className="mt-3 font-semibold text-white">
              {match.awayTeam}
            </p>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-2 gap-3">
          <Stat
            icon={<ChartNoAxesColumnIncreasing size={15} />}
            label="Possession"
            value={`${match.homePossession}% - ${match.awayPossession}%`}
          />

          <Stat
            icon={<Goal size={15} />}
            label="Shots"
            value={`${match.homeShots} - ${match.awayShots}`}
          />

          <Stat
            icon={<Flag size={15} />}
            label="Corners"
            value={`${match.homeCorners} - ${match.awayCorners}`}
          />

          <Stat
            icon={<RectangleHorizontal size={15} />}
            label="Cards"
            value={`${match.homeCards} - ${match.awayCards}`}
          />
        </div>

        {match.valueMarket && (
          <div className="mt-5 rounded-xl border border-green-500/20 bg-green-500/5 p-4">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-medium uppercase tracking-wider text-green-400">
                  Live value detected
                </p>

                <p className="mt-1 font-semibold text-white">
                  {match.valueMarket}
                </p>
              </div>

              <div className="text-right">
                <p className="font-bold text-white">
                  {match.valueOdds?.toFixed(2)}
                </p>

                <p className="text-xs font-semibold text-green-400">
                  +{match.valueEv?.toFixed(1)}% EV
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </article>
  );
}

interface StatProps {
  icon: React.ReactNode;
  label: string;
  value: string;
}

function Stat({ icon, label, value }: StatProps) {
  return (
    <div className="rounded-xl bg-slate-900/60 p-3">
      <div className="flex items-center gap-2 text-xs text-slate-500">
        {icon}
        {label}
      </div>

      <p className="mt-2 font-semibold text-white">{value}</p>
    </div>
  );
}