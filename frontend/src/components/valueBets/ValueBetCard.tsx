import {
  Building2,
  ChartNoAxesCombined,
  Sparkles,
  Star,
} from "lucide-react";

import { Link } from "react-router-dom";

import type { ValueBet } from "../../data/valueBets";

interface ValueBetCardProps {
  bet: ValueBet;
}

function getStars(confidence: number) {
  if (confidence >= 92) return 5;
  if (confidence >= 88) return 4;
  if (confidence >= 84) return 3;
  if (confidence >= 80) return 2;

  return 1;
}

export default function ValueBetCard({
  bet,
}: ValueBetCardProps) {
  const stars = getStars(bet.confidence);

  const modelProbability = Math.round(
    (1 / bet.fairOdds) * 100
  );

  const bookmakerProbability = Math.round(
    (1 / bet.odds) * 100
  );

  return (
    <article className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800 transition duration-200 hover:-translate-y-1 hover:border-cyan-500/60">
      <div className="border-b border-slate-700 px-5 py-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
              {bet.league}
            </p>

            <h2 className="mt-2 text-lg font-bold text-white">
              {bet.match}
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Kickoff {bet.kickoff}
            </p>
          </div>

          <div className="flex">
            {Array.from({ length: 5 }).map((_, index) => (
              <Star
                key={index}
                size={15}
                className={
                  index < stars
                    ? "fill-yellow-400 text-yellow-400"
                    : "text-slate-600"
                }
              />
            ))}
          </div>
        </div>
      </div>

      <div className="p-5">
        <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-cyan-400">
            <Sparkles size={15} />
            Model selection
          </div>

          <p className="mt-2 text-lg font-bold text-white">
            {bet.market}
          </p>
        </div>

        <div className="mt-5 grid grid-cols-3 gap-3">
          <Metric
            label="Best odds"
            value={bet.odds.toFixed(2)}
            color="text-white"
          />

          <Metric
            label="Fair odds"
            value={bet.fairOdds.toFixed(2)}
            color="text-cyan-400"
          />

          <Metric
            label="Expected value"
            value={`+${bet.ev.toFixed(1)}%`}
            color="text-green-400"
          />
        </div>

        <div className="mt-5 rounded-xl bg-slate-900/60 p-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-slate-400">
              Model confidence
            </span>

            <span className="font-bold text-white">
              {bet.confidence}%
            </span>
          </div>

          <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-700">
            <div
              className="h-full rounded-full bg-cyan-400"
              style={{ width: `${bet.confidence}%` }}
            />
          </div>
        </div>

        <div className="mt-5 grid grid-cols-2 gap-3">
          <div className="rounded-xl bg-slate-900/60 p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <ChartNoAxesCombined size={14} />
              Model probability
            </div>

            <p className="mt-2 text-lg font-bold text-white">
              {modelProbability}%
            </p>
          </div>

          <div className="rounded-xl bg-slate-900/60 p-4">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Building2 size={14} />
              Market probability
            </div>

            <p className="mt-2 text-lg font-bold text-white">
              {bookmakerProbability}%
            </p>
          </div>
        </div>

        <div className="mt-5 flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500">
              Bookmaker
            </p>

            <p className="mt-1 font-semibold text-white">
              {bet.bookmaker}
            </p>
          </div>

          <Link
            to={`/analysis/${bet.id}`}
            className="rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
          >
            Analyse
          </Link>
        </div>
      </div>
    </article>
  );
}

interface MetricProps {
  label: string;
  value: string;
  color: string;
}

function Metric({
  label,
  value,
  color,
}: MetricProps) {
  return (
    <div className="rounded-xl bg-slate-900/60 p-3">
      <p className="text-xs text-slate-500">{label}</p>

      <p className={`mt-2 text-lg font-bold ${color}`}>
        {value}
      </p>
    </div>
  );
}