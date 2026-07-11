import { ArrowUpRight, Sparkles } from "lucide-react";
import { valueBets } from "../../data/valueBets";

function getConfidenceStyle(confidence: number) {
  if (confidence >= 90) {
    return "bg-green-500/10 text-green-400";
  }

  if (confidence >= 85) {
    return "bg-cyan-500/10 text-cyan-400";
  }

  return "bg-yellow-500/10 text-yellow-400";
}

export default function ValueBetTable() {
  return (
    <section className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800">
      <div className="flex items-center justify-between border-b border-slate-700 px-6 py-5">
        <div>
          <div className="flex items-center gap-2">
            <Sparkles size={20} className="text-cyan-400" />

            <h2 className="text-xl font-semibold text-white">
              Top Value Bets
            </h2>
          </div>

          <p className="mt-1 text-sm text-slate-400">
            Highest-rated opportunities found by the model
          </p>
        </div>

        <button
          type="button"
          className="flex items-center gap-2 rounded-lg bg-cyan-500/10 px-3 py-2 text-sm font-medium text-cyan-400 transition hover:bg-cyan-500/20"
        >
          View all
          <ArrowUpRight size={16} />
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[800px]">
          <thead>
            <tr className="border-b border-slate-700 text-left text-xs uppercase tracking-wider text-slate-500">
              <th className="px-6 py-4 font-medium">Match</th>
              <th className="px-4 py-4 font-medium">Market</th>
              <th className="px-4 py-4 font-medium">Bookmaker</th>
              <th className="px-4 py-4 font-medium">Odds</th>
              <th className="px-4 py-4 font-medium">Fair odds</th>
              <th className="px-4 py-4 font-medium">EV</th>
              <th className="px-6 py-4 font-medium">Confidence</th>
            </tr>
          </thead>

          <tbody>
            {valueBets.map((bet) => (
              <tr
                key={bet.id}
                className="border-b border-slate-700/70 transition last:border-b-0 hover:bg-slate-700/30"
              >
                <td className="px-6 py-4">
                  <p className="font-medium text-white">{bet.match}</p>
                  <p className="mt-1 text-xs text-slate-500">
                    {bet.league}
                  </p>
                </td>

                <td className="px-4 py-4 text-sm text-slate-300">
                  {bet.market}
                </td>

                <td className="px-4 py-4 text-sm text-slate-300">
                  {bet.bookmaker}
                </td>

                <td className="px-4 py-4 font-semibold text-white">
                  {bet.odds.toFixed(2)}
                </td>

                <td className="px-4 py-4 text-sm text-slate-400">
                  {bet.fairOdds.toFixed(2)}
                </td>

                <td className="px-4 py-4 font-semibold text-green-400">
                  +{bet.ev.toFixed(1)}%
                </td>

                <td className="px-6 py-4">
                  <span
                    className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${getConfidenceStyle(
                      bet.confidence
                    )}`}
                  >
                    {bet.confidence}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}