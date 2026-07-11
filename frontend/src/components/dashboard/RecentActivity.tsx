import {
  Activity,
  ArrowDown,
  Brain,
  CircleAlert,
  Sparkles,
} from "lucide-react";

const activities = [
  {
    id: 1,
    title: "18 new value bets found",
    description: "The model completed its latest market scan.",
    time: "2 minutes ago",
    icon: Sparkles,
    iconStyle: "bg-cyan-500/10 text-cyan-400",
  },
  {
    id: 2,
    title: "Pinnacle odds shortened",
    description: "Liverpool vs Arsenal O2.5 moved from 2.12 to 2.05.",
    time: "8 minutes ago",
    icon: ArrowDown,
    iconStyle: "bg-yellow-500/10 text-yellow-400",
  },
  {
    id: 3,
    title: "Confidence score increased",
    description: "Barcelona -1 Asian Handicap increased to 89%.",
    time: "14 minutes ago",
    icon: Brain,
    iconStyle: "bg-purple-500/10 text-purple-400",
  },
  {
    id: 4,
    title: "Live match statistics updated",
    description: "Liverpool vs Arsenal match data refreshed.",
    time: "21 minutes ago",
    icon: Activity,
    iconStyle: "bg-green-500/10 text-green-400",
  },
  {
    id: 5,
    title: "Team news detected",
    description: "A starting defender is listed as unavailable.",
    time: "35 minutes ago",
    icon: CircleAlert,
    iconStyle: "bg-red-500/10 text-red-400",
  },
];

export default function RecentActivity() {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <div>
        <h2 className="text-xl font-semibold text-white">
          Recent Activity
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Latest model and market updates
        </p>
      </div>

      <div className="mt-6 space-y-5">
        {activities.map((activity) => {
          const Icon = activity.icon;

          return (
            <div
              key={activity.id}
              className="flex gap-4 border-b border-slate-700/70 pb-5 last:border-b-0 last:pb-0"
            >
              <div
                className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${activity.iconStyle}`}
              >
                <Icon size={19} />
              </div>

              <div className="min-w-0 flex-1">
                <p className="font-medium text-white">
                  {activity.title}
                </p>

                <p className="mt-1 text-sm leading-5 text-slate-400">
                  {activity.description}
                </p>

                <p className="mt-2 text-xs text-slate-500">
                  {activity.time}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}