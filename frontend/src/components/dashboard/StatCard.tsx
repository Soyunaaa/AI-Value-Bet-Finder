import type { ReactNode } from "react";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  color?: string;
  trend?: number;
  description?: string;
}

export default function StatCard({
  title,
  value,
  icon,
  color = "text-cyan-400",
  trend,
  description,
}: StatCardProps) {
  const trendIsPositive = trend !== undefined && trend >= 0;

  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6 transition duration-200 hover:-translate-y-1 hover:border-cyan-500/70">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-400">{title}</p>

          <h3 className={`mt-2 text-3xl font-bold ${color}`}>
            {value}
          </h3>
        </div>

        <div className="rounded-xl bg-cyan-500/10 p-3 text-cyan-400">
          {icon}
        </div>
      </div>

      <div className="mt-5 flex items-center gap-2">
        {trend !== undefined && (
          <span
            className={`flex items-center gap-1 rounded-full px-2 py-1 text-xs font-semibold ${
              trendIsPositive
                ? "bg-green-500/10 text-green-400"
                : "bg-red-500/10 text-red-400"
            }`}
          >
            {trendIsPositive ? (
              <ArrowUpRight size={14} />
            ) : (
              <ArrowDownRight size={14} />
            )}

            {Math.abs(trend)}%
          </span>
        )}

        {description && (
          <span className="text-xs text-slate-500">
            {description}
          </span>
        )}
      </div>
    </div>
  );
}