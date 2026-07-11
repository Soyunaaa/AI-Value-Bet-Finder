export default function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-white flex">
      
      {/* Sidebar */}
      <aside className="w-64 bg-slate-800 border-r border-slate-700 p-6">
        <h1 className="text-2xl font-bold text-cyan-400 mb-8">
          AI Value Bet
        </h1>

        <nav className="space-y-4">
          <div className="cursor-pointer hover:text-cyan-400">
            Dashboard
          </div>

          <div className="cursor-pointer hover:text-cyan-400">
            Value Bets
          </div>

          <div className="cursor-pointer hover:text-cyan-400">
            Live Matches
          </div>

          <div className="cursor-pointer hover:text-cyan-400">
            Statistics
          </div>

          <div className="cursor-pointer hover:text-cyan-400">
            AI Predictions
          </div>

          <div className="cursor-pointer hover:text-cyan-400">
            Settings
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">

        <h2 className="text-4xl font-bold mb-8">
          Dashboard
        </h2>

        {/* Top Cards */}
        <div className="grid grid-cols-4 gap-6 mb-8">

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-slate-400">Today's Matches</h3>
            <p className="text-3xl font-bold mt-2">127</p>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-slate-400">Value Bets</h3>
            <p className="text-3xl font-bold mt-2 text-green-400">18</p>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-slate-400">Average EV</h3>
            <p className="text-3xl font-bold mt-2 text-cyan-400">
              12.8%
            </p>
          </div>

          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="text-slate-400">Confidence</h3>
            <p className="text-3xl font-bold mt-2 text-yellow-400">
              91%
            </p>
          </div>

        </div>

        {/* Value Bets Table */}
        <div className="bg-slate-800 rounded-2xl p-6">

          <h3 className="text-2xl font-bold mb-6">
            Top Value Bets
          </h3>

          <table className="w-full">

            <thead>
              <tr className="text-slate-400 text-left border-b border-slate-700">
                <th className="pb-3">Match</th>
                <th className="pb-3">Market</th>
                <th className="pb-3">Odds</th>
                <th className="pb-3">EV</th>
                <th className="pb-3">Confidence</th>
              </tr>
            </thead>

            <tbody>

              <tr className="border-b border-slate-700">
                <td className="py-4">Liverpool vs Arsenal</td>
                <td>Over 2.5 Goals</td>
                <td>2.05</td>
                <td className="text-green-400">+17.2%</td>
                <td>93%</td>
              </tr>

              <tr className="border-b border-slate-700">
                <td className="py-4">Barcelona vs Sevilla</td>
                <td>Home Win</td>
                <td>1.95</td>
                <td className="text-green-400">+14.4%</td>
                <td>89%</td>
              </tr>

            </tbody>

          </table>

        </div>

      </main>

    </div>
  );
}