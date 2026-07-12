import type { ReactNode } from "react";

import {
  AlertCircle,
  ArrowLeft,
  Brain,
  CheckCircle2,
  CloudSun,
  Goal,
  LoaderCircle,
  ShieldCheck,
  Sparkles,
  Target,
  Users,
} from "lucide-react";

import {
  Link,
  Navigate,
  useParams,
} from "react-router-dom";

import {
  useEffect,
  useState,
} from "react";

import DashboardLayout from "../components/layout/DashboardLayout";

import type { ValueBet } from "../data/valueBets";

import { getValueBet } from "../services/valueBetService";

export default function Analysis() {
  const { id } = useParams();

  const betId = Number(id);

  const [bet, setBet] = useState<ValueBet | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!Number.isInteger(betId) || betId <= 0) {
      setNotFound(true);
      setLoading(false);
      return;
    }

    async function loadBet() {
      try {
        const result = await getValueBet(betId);
        setBet(result);
      } catch (requestError) {
        const message =
          requestError instanceof Error
            ? requestError.message
            : "Unable to load analysis.";

        if (message === "Value bet not found") {
          setNotFound(true);
        } else {
          setError(message);
        }
      } finally {
        setLoading(false);
      }
    }

    void loadBet();
  }, [betId]);

  if (notFound) {
    return <Navigate to="/value-bets" replace />;
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-16 text-center">
          <LoaderCircle
            size={40}
            className="mx-auto animate-spin text-cyan-400"
          />

          <h1 className="mt-5 text-xl font-semibold text-white">
            Loading analysis
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            Requesting model data from FastAPI.
          </p>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !bet) {
    return (
      <DashboardLayout>
        <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-12 text-center">
          <AlertCircle
            size={40}
            className="mx-auto text-red-400"
          />

          <h1 className="mt-5 text-xl font-semibold text-white">
            Unable to load analysis
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            {error ?? "No analysis data was returned."}
          </p>

          <Link
            to="/value-bets"
            className="mt-6 inline-flex rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
          >
            Return to value bets
          </Link>
        </div>
      </DashboardLayout>
    );
  }

  const modelProbability = (1 / bet.fairOdds) * 100;
  const marketProbability = (1 / bet.odds) * 100;

  const probabilityEdge =
    modelProbability - marketProbability;

  const sortedBookmakers = [...bet.bookmakerOdds].sort(
    (first, second) => second.odds - first.odds
  );

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <Link
          to="/value-bets"
          className="inline-flex items-center gap-2 text-sm font-medium text-slate-400 transition hover:text-cyan-400"
        >
          <ArrowLeft size={17} />
          Back to value bets
        </Link>

        <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="flex flex-col gap-6 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-cyan-400">
                {bet.league}
              </p>

              <h1 className="mt-2 text-3xl font-bold text-white">
                {bet.homeTeam} vs {bet.awayTeam}
              </h1>

              <p className="mt-2 text-sm text-slate-400">
                Kickoff {bet.kickoff}
              </p>
            </div>

            <div className="rounded-xl border border-green-500/20 bg-green-500/5 px-5 py-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-green-400">
                Positive expected value
              </p>

              <p className="mt-1 text-3xl font-bold text-green-400">
                +{bet.ev.toFixed(1)}%
              </p>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
          <div className="rounded-2xl border border-cyan-500/30 bg-slate-800 p-6">
            <div className="flex items-center gap-2 text-cyan-400">
              <Sparkles size={21} />

              <p className="text-sm font-semibold uppercase tracking-wider">
                Model recommendation
              </p>
            </div>

            <h2 className="mt-4 text-3xl font-bold text-white">
              {bet.market}
            </h2>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
              The model estimates that the available price is
              greater than the calculated fair price.
            </p>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
              <MainMetric
                label="Best odds"
                value={bet.odds.toFixed(2)}
                color="text-white"
              />

              <MainMetric
                label="Fair odds"
                value={bet.fairOdds.toFixed(2)}
                color="text-cyan-400"
              />

              <MainMetric
                label="Confidence"
                value={`${bet.confidence}%`}
                color="text-yellow-400"
              />
            </div>
          </div>

          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <div className="flex items-center gap-2">
              <Brain size={21} className="text-purple-400" />

              <h2 className="text-xl font-semibold text-white">
                Probability Edge
              </h2>
            </div>

            <div className="mt-6 space-y-5">
              <ProbabilityRow
                label="Model probability"
                value={modelProbability}
                color="bg-cyan-400"
              />

              <ProbabilityRow
                label="Market probability"
                value={marketProbability}
                color="bg-slate-500"
              />
            </div>

            <div className="mt-6 rounded-xl bg-green-500/10 p-4">
              <p className="text-sm text-slate-400">
                Probability difference
              </p>

              <p className="mt-1 text-2xl font-bold text-green-400">
                +{probabilityEdge.toFixed(1)}%
              </p>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <div className="flex items-center gap-2">
              <Target size={21} className="text-cyan-400" />

              <h2 className="text-xl font-semibold text-white">
                Model Ratings
              </h2>
            </div>

            <div className="mt-6 space-y-5">
              <RatingBar
                label="Attack strength"
                value={bet.attackRating}
              />

              <RatingBar
                label="Defensive strength"
                value={bet.defenceRating}
              />

              <RatingBar
                label="Goals model"
                value={bet.goalsRating}
              />

              <RatingBar
                label="Corners model"
                value={bet.cornersRating}
              />

              <RatingBar
                label="Cards model"
                value={bet.cardsRating}
              />
            </div>
          </div>

          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <div className="flex items-center gap-2">
              <ShieldCheck
                size={21}
                className="text-green-400"
              />

              <h2 className="text-xl font-semibold text-white">
                Why the model likes it
              </h2>
            </div>

            <div className="mt-6 space-y-4">
              {bet.reasons.map((reason) => (
                <div
                  key={reason}
                  className="flex items-start gap-3"
                >
                  <CheckCircle2
                    size={18}
                    className="mt-0.5 shrink-0 text-green-400"
                  />

                  <p className="text-sm leading-6 text-slate-300">
                    {reason}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 lg:grid-cols-4">
          <InfoCard
            icon={<Goal size={20} />}
            title="Expected Goals"
            value={`${bet.homeXg.toFixed(2)} - ${bet.awayXg.toFixed(2)}`}
          />

          <InfoCard
            icon={<Target size={20} />}
            title="Expected Corners"
            value={bet.expectedCorners.toFixed(1)}
          />

          <InfoCard
            icon={<Users size={20} />}
            title="Expected Cards"
            value={bet.expectedCards.toFixed(1)}
          />

          <InfoCard
            icon={<CloudSun size={20} />}
            title="Weather"
            value={bet.weather}
          />
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(300px,1fr)]">
          <div className="overflow-hidden rounded-2xl border border-slate-700 bg-slate-800">
            <div className="border-b border-slate-700 px-6 py-5">
              <h2 className="text-xl font-semibold text-white">
                Bookmaker Comparison
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Odds returned by the backend
              </p>
            </div>

            <div className="divide-y divide-slate-700/70">
              {sortedBookmakers.map((bookmaker, index) => (
                <div
                  key={bookmaker.name}
                  className="flex items-center justify-between px-6 py-4"
                >
                  <div>
                    <p className="font-semibold text-white">
                      {bookmaker.name}
                    </p>

                    {index === 0 && (
                      <p className="mt-1 text-xs font-medium text-green-400">
                        Best available price
                      </p>
                    )}
                  </div>

                  <p className="text-xl font-bold text-white">
                    {bookmaker.odds.toFixed(2)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <h2 className="text-xl font-semibold text-white">
              Match Information
            </h2>

            <div className="mt-6 space-y-5">
              <DetailRow
                label="Team news"
                value={bet.teamNews}
              />

              <DetailRow
                label="Selected bookmaker"
                value={bet.bookmaker}
              />

              <DetailRow
                label="Market"
                value={bet.market}
              />

              <DetailRow
                label="Data source"
                value="FastAPI backend"
              />
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-5">
          <p className="font-medium text-yellow-400">
            Demonstration analysis
          </p>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            The frontend now loads this analysis from FastAPI, but
            the backend values are still placeholders. They are not
            live betting information or betting advice.
          </p>
        </section>
      </div>
    </DashboardLayout>
  );
}

interface MainMetricProps {
  label: string;
  value: string;
  color: string;
}

function MainMetric({
  label,
  value,
  color,
}: MainMetricProps) {
  return (
    <div className="rounded-xl bg-slate-900/60 p-4">
      <p className="text-sm text-slate-400">
        {label}
      </p>

      <p className={`mt-2 text-2xl font-bold ${color}`}>
        {value}
      </p>
    </div>
  );
}

interface ProbabilityRowProps {
  label: string;
  value: number;
  color: string;
}

function ProbabilityRow({
  label,
  value,
  color,
}: ProbabilityRowProps) {
  return (
    <div>
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-400">
          {label}
        </p>

        <p className="font-bold text-white">
          {value.toFixed(1)}%
        </p>
      </div>

      <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-700">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

interface RatingBarProps {
  label: string;
  value: number;
}

function RatingBar({
  label,
  value,
}: RatingBarProps) {
  return (
    <div>
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-300">
          {label}
        </p>

        <p className="font-semibold text-white">
          {value}%
        </p>
      </div>

      <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-700">
        <div
          className="h-full rounded-full bg-cyan-400"
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}

interface InfoCardProps {
  icon: ReactNode;
  title: string;
  value: string;
}

function InfoCard({
  icon,
  title,
  value,
}: InfoCardProps) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-5">
      <div className="text-cyan-400">{icon}</div>

      <p className="mt-4 text-sm text-slate-400">
        {title}
      </p>

      <p className="mt-2 text-xl font-bold text-white">
        {value}
      </p>
    </div>
  );
}

interface DetailRowProps {
  label: string;
  value: string;
}

function DetailRow({
  label,
  value,
}: DetailRowProps) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-sm leading-6 text-white">
        {value}
      </p>
    </div>
  );
}