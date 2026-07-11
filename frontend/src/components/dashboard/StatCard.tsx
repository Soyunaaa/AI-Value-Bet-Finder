import type { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  color?: string;
}

export default function StatCard({
  title,
  value,
  icon,
  color = "text-cyan-400",
}: StatCardProps) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6 transition hover:scale-[1.02] hover:border-cyan-500">

      <div className="flex items-center justify-between">

        <div>
          <p className="text-sm text-slate-400">
            {title}
          </p>

          <h3 className={`mt-2 text-3xl font-bold ${color}`}>
            {value}
          </h3>
        </div>

        <div className="text-cyan-400">
          {icon}
        </div>

      </div>

    </div>
  );
}