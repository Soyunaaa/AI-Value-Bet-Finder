import { Activity, CircleDot } from "lucide-react";

const stats = [
  { label: "Possession", home: "57%", away: "43%" },
  { label: "Shots", home: "12", away: "7" },
  { label: "Shots on target", home: "6", away: "3" },
  { label: "Corners", home: "7", away: "4" },
];

export default function LiveMatchCard() {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Activity size={20} className="text-red-400" />

            <h2 className="text-xl font-semibold text-white">
              Live Match
            </h2>
          </div>

          <p className="mt-1 text-sm text-slate-400">
            Premier League
          </p>
        </div>

        <span className="flex items-center gap-2 rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-400">
          <CircleDot size={14} />
          LIVE · 73'
        </span>
      </div>

      <div className="my-8 grid grid-cols-[1fr_auto_1fr] items-center gap-4">
        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-red-500/10 text-xl font-bold text-red-400">
            LIV
          </div>

          <p className="mt-3 font-semibold text-white">Liverpool</p>
        </div>

        <div className="text-center">
          <p className="text-4xl font-bold text-white">2 - 1</p>
          <p className="mt-1 text-xs uppercase tracking-widest text-slate-500">
            Score
          </p>
        </div>

        <div className="text-center">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-cyan-500/10 text-xl font-bold text-cyan-400">
            ARS
          </div>

          <p className="mt-3 font-semibold text-white">Arsenal</p>
        </div>
      </div>

      <div className="space-y-4">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="grid grid-cols-[50px_1fr_50px] items-center gap-3"
          >
            <span className="text-right font-semibold text-white">
              {stat.home}
            </span>

            <div className="text-center">
              <p className="text-xs text-slate-500">{stat.label}</p>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-700">
                <div className="h-full w-[57%] rounded-full bg-cyan-400" />
              </div>
            </div>

            <span className="font-semibold text-white">{stat.away}</span>
          </div>
        ))}
      </div>
    </section>
  );
}