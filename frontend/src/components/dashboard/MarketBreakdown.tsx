const markets = [
  {
    name: "Goals O/U",
    bets: 42,
    hitRate: 68,
    profit: 8.4,
  },
  {
    name: "1X2",
    bets: 28,
    hitRate: 61,
    profit: 4.7,
  },
  {
    name: "Asian Handicap",
    bets: 21,
    hitRate: 64,
    profit: 3.9,
  },
  {
    name: "Corners O/U",
    bets: 19,
    hitRate: 58,
    profit: 2.1,
  },
];

export default function MarketBreakdown() {
  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <div>
        <h2 className="text-xl font-semibold text-white">
          Market Performance
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Results by betting market
        </p>
      </div>

      <div className="mt-6 space-y-5">
        {markets.map((market) => (
          <div key={market.name}>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-white">{market.name}</p>
                <p className="text-xs text-slate-500">
                  {market.bets} tracked bets
                </p>
              </div>

              <div className="text-right">
                <p className="font-semibold text-green-400">
                  +{market.profit.toFixed(1)}u
                </p>
                <p className="text-xs text-slate-500">
                  {market.hitRate}% hit rate
                </p>
              </div>
            </div>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-700">
              <div
                className="h-full rounded-full bg-cyan-400"
                style={{ width: `${market.hitRate}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}