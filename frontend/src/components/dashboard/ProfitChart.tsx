import {
  Line,
} from "react-chartjs-2";

import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const data = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  datasets: [
    {
      label: "Profit",
      data: [0, 2.4, 1.8, 5.2, 7.1, 10.4, 13.8],
      borderColor: "#06b6d4",
      backgroundColor: "rgba(6, 182, 212, 0.12)",
      fill: true,
      tension: 0.4,
      pointRadius: 3,
      pointHoverRadius: 5,
    },
  ],
};

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      backgroundColor: "#0f172a",
      borderColor: "#334155",
      borderWidth: 1,
      titleColor: "#ffffff",
      bodyColor: "#cbd5e1",
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
      ticks: {
        color: "#94a3b8",
      },
    },
    y: {
      grid: {
        color: "rgba(148, 163, 184, 0.1)",
      },
      ticks: {
        color: "#94a3b8",
        callback: (value: string | number) => `${value}u`,
      },
    },
  },
};

export default function ProfitChart() {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-xl font-semibold text-white">
            Weekly Performance
          </h2>

          <p className="mt-1 text-sm text-slate-400">
            Simulated profit using flat one-unit stakes
          </p>
        </div>

        <div className="text-right">
          <p className="text-sm text-slate-400">Net profit</p>
          <p className="text-2xl font-bold text-green-400">+13.8u</p>
        </div>
      </div>

      <div className="mt-6 h-72">
        <Line data={data} options={options} />
      </div>
    </section>
  );
}