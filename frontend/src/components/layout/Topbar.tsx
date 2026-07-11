import { Bell, Search, UserCircle } from "lucide-react";

export default function Topbar() {
  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-700 bg-slate-900 px-8">
      <div>
        <h2 className="text-2xl font-bold text-white">Dashboard</h2>
        <p className="text-sm text-slate-400">
          AI Football Value Betting Analytics
        </p>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center rounded-xl bg-slate-800 px-4 py-2">
          <Search size={18} className="text-slate-400" />

          <input
            type="text"
            placeholder="Search teams..."
            className="ml-2 w-48 bg-transparent text-white outline-none placeholder:text-slate-500"
          />
        </div>

        <button
          type="button"
          className="rounded-xl bg-slate-800 p-3 transition hover:bg-slate-700"
          aria-label="Notifications"
        >
          <Bell size={20} />
        </button>

        <button
          type="button"
          className="rounded-xl bg-slate-800 p-2 transition hover:bg-slate-700"
          aria-label="User profile"
        >
          <UserCircle size={32} />
        </button>
      </div>
    </header>
  );
}