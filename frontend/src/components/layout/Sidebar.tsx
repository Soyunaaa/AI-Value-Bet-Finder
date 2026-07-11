import {
  Activity,
  BarChart3,
  Brain,
  LayoutDashboard,
  Settings,
  Trophy,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menuItems = [
  {
    icon: LayoutDashboard,
    label: "Dashboard",
    path: "/",
  },
  {
    icon: Activity,
    label: "Live Matches",
    path: "/live",
    badge: "4",
  },
  {
    icon: Trophy,
    label: "Value Bets",
    path: "/value-bets",
  },
  {
    icon: BarChart3,
    label: "Statistics",
    path: "/statistics",
  },
  {
    icon: Brain,
    label: "AI Predictions",
    path: "/predictions",
  },
  {
    icon: Settings,
    label: "Settings",
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside className="flex min-h-screen w-72 shrink-0 flex-col border-r border-slate-700 bg-slate-800">
      <div className="border-b border-slate-700 p-6">
        <h1 className="text-2xl font-bold text-cyan-400">
          AI Value Bet
        </h1>

        <p className="mt-1 text-sm text-slate-400">
          Football Analytics
        </p>
      </div>

      <nav className="flex-1 space-y-2 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.label}
              to={item.path}
              className={({ isActive }) =>
                `flex w-full items-center gap-3 rounded-xl px-4 py-3 transition ${
                  isActive
                    ? "bg-cyan-500/10 text-cyan-400"
                    : "text-slate-300 hover:bg-slate-700 hover:text-cyan-400"
                }`
              }
            >
              <Icon size={20} />

              <span className="flex-1 text-left">
                {item.label}
              </span>

              {item.badge && (
                <span className="rounded-full bg-red-500/10 px-2 py-1 text-xs font-semibold text-red-400">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}