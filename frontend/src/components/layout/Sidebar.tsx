import {
  LayoutDashboard,
  Activity,
  Trophy,
  Brain,
  BarChart3,
  Settings,
} from "lucide-react";

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard" },
  { icon: Activity, label: "Live Matches" },
  { icon: Trophy, label: "Value Bets" },
  { icon: BarChart3, label: "Statistics" },
  { icon: Brain, label: "AI Predictions" },
  { icon: Settings, label: "Settings" },
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-slate-800 border-r border-slate-700 flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-2xl font-bold text-cyan-400">
          AI Value Bet
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Football Analytics
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-slate-300 transition hover:bg-slate-700 hover:text-cyan-400"
            >
              <Icon size={20} />
              {item.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}