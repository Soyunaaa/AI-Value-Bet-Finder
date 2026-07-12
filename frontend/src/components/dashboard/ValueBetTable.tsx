import { ArrowUpRight, Sparkles } from "lucide-react";

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
            Live backend data will be connected here next
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

      <div className="px-6 py-10 text-center text-slate-400">
        Value bets are now loaded on the dedicated Value Bets page.
      </div>
    </section>
  );
}