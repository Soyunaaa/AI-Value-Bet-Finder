import {
  Bar,
} from "react-chartjs-2";

import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Title,
  Tooltip,
} from "chart.js";

import { monthlyPerformance } from "../../data/statistics";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const data = {
  labels: monthlyPerformance.map((item) => item.month),
  datasets: [
    {
      label: "Profit",
      data: monthlyPerformance.map((item) => item.profit),
      backgroundColor: "rgba(6, 182, 212, 0.7)",
      borderColor: "#06b6d4",
      borderWidth: 1,
      borderRadius: 8,
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
      callbacks: {
        label: (context: { raw: unknown }) =>
          ` ${Number(context.raw).toFixed(1)} units`,
      },
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
      beginAtZero: true,
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

export default function MonthlyProfitChart() {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <div>
        <h2 className="text-xl font-semibold text-white">
          Monthly Profit
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Simulated net profit using one-unit stakes
        </p>
      </div>

      <div className="mt-6 h-80">
        <Bar data={data} options={options} />
      </div>
    </section>
  );
}