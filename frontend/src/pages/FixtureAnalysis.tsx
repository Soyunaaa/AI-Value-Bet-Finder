import type { ReactNode } from "react";

import {
  AlertCircle,
  ArrowLeft,
  BarChart3,
  CheckCircle2,
  Clock3,
  Goal,
  LoaderCircle,
  RefreshCw,
  Shield,
  Sparkles,
  Target,
  Trophy,
} from "lucide-react";

import {
  Link,
  Navigate,
  useParams,
} from "react-router-dom";

import DashboardLayout from "../components/layout/DashboardLayout";

import { useFixtureAnalysis } from "../hooks/useFixtureAnalysis";

import type {
  MarketProbability,
  TeamFormSummary,
} from "../types/fixtureAnalysis";

function formatKickoff(utcDate: string) {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(utcDate));
}

function formatPercentage(probability: number) {
  return `${(probability * 100).toFixed(1)}%`;
}

function getFormResultString(
  form: TeamFormSummary
) {
  return [
    ...Array(form.wins).fill("W"),
    ...Array(form.draws).fill("D"),
    ...Array(form.losses).fill("L"),
  ]
    .slice(0, form.matches_used)
    .join("");
}

export default function FixtureAnalysis() {
  const { fixtureId } = useParams();

  const parsedFixtureId = Number(fixtureId);

  const {
    analysis,
    loading,
    refreshing,
    error,
    refresh,
    retry,
  } = useFixtureAnalysis(parsedFixtureId);

  if (
    !Number.isInteger(parsedFixtureId) ||
    parsedFixtureId <= 0
  ) {
    return <Navigate to="/" replace />;
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="rounded-2xl border border-slate-700 bg-slate-800 p-16 text-center">
          <LoaderCircle
            size={42}
            className="mx-auto animate-spin text-cyan-400"
          />

          <h1 className="mt-5 text-xl font-semibold text-white">
            Generating fixture analysis
          </h1>

          <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">
            Loading the fixture, recent team results and
            calculated market probabilities.
          </p>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !analysis) {
    return (
      <DashboardLayout>
        <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-12 text-center">
          <AlertCircle
            size={42}
            className="mx-auto text-red-400"
          />

          <h1 className="mt-5 text-xl font-semibold text-white">
            Unable to generate analysis
          </h1>

          <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">
            {error ??
              "The backend returned no fixture-analysis data."}
          </p>

          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <button
              type="button"
              onClick={retry}
              className="rounded-xl bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
            >
              Try again
            </button>

            <Link
              to="/"
              className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm font-semibold text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400"
            >
              Return to dashboard
            </Link>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const {
    fixture,
    home_form: homeForm,
    away_form: awayForm,
    prediction,
  } = analysis;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <section className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-sm font-medium text-slate-400 transition hover:text-cyan-400"
          >
            <ArrowLeft size={17} />
            Back to dashboard
          </Link>

          <button
            type="button"
            disabled={refreshing}
            onClick={refresh}
            className="flex items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm font-medium text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <RefreshCw
              size={17}
              className={
                refreshing ? "animate-spin" : ""
              }
            />

            {refreshing
              ? "Recalculating..."
              : "Recalculate"}
          </button>
        </section>

        <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
          <div className="flex flex-col gap-6 xl:flex-row xl:items-center xl:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wider text-cyan-400">
                {fixture.competition.name}
              </p>

              <h1 className="mt-2 text-3xl font-bold text-white">
                {fixture.home_team.name} vs{" "}
                {fixture.away_team.name}
              </h1>

              <div className="mt-3 flex flex-wrap items-center gap-4 text-sm text-slate-400">
                <span className="flex items-center gap-2">
                  <Clock3 size={16} />
                  {formatKickoff(fixture.utc_date)}
                </span>

                {fixture.matchday !== null && (
                  <span>
                    Matchday {fixture.matchday}
                  </span>
                )}
              </div>
            </div>

            <div className="rounded-xl border border-yellow-500/20 bg-yellow-500/5 px-5 py-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-yellow-400">
                Model confidence
              </p>

              <p className="mt-1 text-3xl font-bold text-yellow-400">
                {analysis.confidence.toFixed(1)}%
              </p>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
          <SummaryCard
            title="Expected Goals"
            value={`${analysis.home_expected_goals.toFixed(
              2
            )} - ${analysis.away_expected_goals.toFixed(
              2
            )}`}
            icon={<Goal size={24} />}
            color="text-cyan-400"
          />

          <SummaryCard
            title="Most Likely Score"
            value={`${prediction.most_likely_score.home_goals} - ${prediction.most_likely_score.away_goals}`}
            icon={<Target size={24} />}
            color="text-green-400"
          />

          <SummaryCard
            title="Total Expected Goals"
            value={prediction.total_expected_goals.toFixed(
              2
            )}
            icon={<BarChart3 size={24} />}
            color="text-purple-400"
          />

          <SummaryCard
            title="Recent Matches Used"
            value={`${homeForm.matches_used + awayForm.matches_used}`}
            icon={<Trophy size={24} />}
            color="text-yellow-400"
          />
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(340px,1fr)]">
          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <div className="flex items-center gap-2">
              <Sparkles
                size={21}
                className="text-cyan-400"
              />

              <h2 className="text-xl font-semibold text-white">
                1X2 Prediction
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              Probabilities calculated from the expected-goals
              distribution
            </p>

            <div className="mt-6 space-y-6">
              <ProbabilityBar
                label={`${fixture.home_team.name} win`}
                market={prediction.home_win}
                color="bg-cyan-400"
              />

              <ProbabilityBar
                label="Draw"
                market={prediction.draw}
                color="bg-yellow-400"
              />

              <ProbabilityBar
                label={`${fixture.away_team.name} win`}
                market={prediction.away_win}
                color="bg-purple-400"
              />
            </div>
          </div>

          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <div className="flex items-center gap-2">
              <Target
                size={21}
                className="text-green-400"
              />

              <h2 className="text-xl font-semibold text-white">
                Goals Markets
              </h2>
            </div>

            <div className="mt-6 space-y-5">
              <CompactMarket
                label="Over 2.5 Goals"
                market={prediction.over_2_5}
              />

              <CompactMarket
                label="Under 2.5 Goals"
                market={prediction.under_2_5}
              />

              <CompactMarket
                label="BTTS — Yes"
                market={
                  prediction.both_teams_to_score_yes
                }
              />

              <CompactMarket
                label="BTTS — No"
                market={
                  prediction.both_teams_to_score_no
                }
              />
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          <TeamFormCard
            form={homeForm}
            heading="Home Team Form"
            accent="text-cyan-400"
          />

          <TeamFormCard
            form={awayForm}
            heading="Away Team Form"
            accent="text-purple-400"
          />
        </section>

        <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <div className="flex items-center gap-2">
              <Shield
                size={21}
                className="text-green-400"
              />

              <h2 className="text-xl font-semibold text-white">
                Model Explanation
              </h2>
            </div>

            <p className="mt-1 text-sm text-slate-400">
              Factors currently used by the baseline model
            </p>

            <div className="mt-6 space-y-4">
              {analysis.reasons.map((reason) => (
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

          <div className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
            <h2 className="text-xl font-semibold text-white">
              Likely Scores
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Highest-probability scorelines
            </p>

            <div className="mt-6 space-y-3">
              {prediction.score_probabilities
                .slice(0, 5)
                .map((score, index) => (
                  <div
                    key={`${score.home_goals}-${score.away_goals}`}
                    className="flex items-center justify-between rounded-xl bg-slate-900/60 p-4"
                  >
                    <div className="flex items-center gap-3">
                      <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-cyan-500/10 text-xs font-bold text-cyan-400">
                        {index + 1}
                      </span>

                      <span className="font-semibold text-white">
                        {score.home_goals} -{" "}
                        {score.away_goals}
                      </span>
                    </div>

                    <span className="font-semibold text-slate-300">
                      {formatPercentage(
                        score.probability
                      )}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-yellow-500/20 bg-yellow-500/5 p-5">
          <p className="font-medium text-yellow-400">
            Baseline statistical analysis
          </p>

          <p className="mt-2 text-sm leading-6 text-slate-400">
            This analysis uses recent finished-match averages and
            a Poisson score model. It does not yet account for
            injuries, expected lineups, advanced xG, corners,
            referee data, weather or live bookmaker odds.
          </p>
        </section>
      </div>
    </DashboardLayout>
  );
}

interface SummaryCardProps {
  title: string;
  value: string;
  icon: ReactNode;
  color: string;
}

function SummaryCard({
  title,
  value,
  icon,
  color,
}: SummaryCardProps) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800 p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">
            {title}
          </p>

          <p className={`mt-2 text-2xl font-bold ${color}`}>
            {value}
          </p>
        </div>

        <div
          className={`rounded-xl bg-slate-900/60 p-3 ${color}`}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}

interface ProbabilityBarProps {
  label: string;
  market: MarketProbability;
  color: string;
}

function ProbabilityBar({
  label,
  market,
  color,
}: ProbabilityBarProps) {
  const percentage = market.probability * 100;

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="font-medium text-slate-300">
          {label}
        </p>

        <div className="text-right">
          <p className="font-bold text-white">
            {percentage.toFixed(1)}%
          </p>

          <p className="text-xs text-slate-500">
            Fair odds{" "}
            {market.fair_odds?.toFixed(2) ?? "—"}
          </p>
        </div>
      </div>

      <div className="mt-3 h-2.5 overflow-hidden rounded-full bg-slate-700">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

interface CompactMarketProps {
  label: string;
  market: MarketProbability;
}

function CompactMarket({
  label,
  market,
}: CompactMarketProps) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-xl bg-slate-900/60 p-4">
      <div>
        <p className="font-medium text-white">
          {label}
        </p>

        <p className="mt-1 text-xs text-slate-500">
          Fair odds{" "}
          {market.fair_odds?.toFixed(2) ?? "—"}
        </p>
      </div>

      <p className="text-xl font-bold text-cyan-400">
        {formatPercentage(market.probability)}
      </p>
    </div>
  );
}

interface TeamFormCardProps {
  form: TeamFormSummary;
  heading: string;
  accent: string;
}

function TeamFormCard({
  form,
  heading,
  accent,
}: TeamFormCardProps) {
  const resultString = getFormResultString(form);

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-800 p-6">
      <p className={`text-sm font-semibold ${accent}`}>
        {heading}
      </p>

      <h2 className="mt-2 text-xl font-bold text-white">
        {form.team_name}
      </h2>

      <p className="mt-1 text-sm text-slate-400">
        Based on {form.matches_used} finished matches
      </p>

      <div className="mt-5 flex flex-wrap gap-2">
        {resultString.length > 0 ? (
          resultString.split("").map((result, index) => (
            <span
              key={`${result}-${index}`}
              className={`flex h-8 w-8 items-center justify-center rounded-lg text-xs font-bold ${
                result === "W"
                  ? "bg-green-500/10 text-green-400"
                  : result === "D"
                    ? "bg-yellow-500/10 text-yellow-400"
                    : "bg-red-500/10 text-red-400"
              }`}
            >
              {result}
            </span>
          ))
        ) : (
          <p className="text-sm text-slate-500">
            No completed matches found.
          </p>
        )}
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <FormMetric
          label="PPG"
          value={form.points_per_game.toFixed(2)}
        />

        <FormMetric
          label="Goals For"
          value={form.average_goals_scored.toFixed(2)}
        />

        <FormMetric
          label="Goals Against"
          value={form.average_goals_conceded.toFixed(
            2
          )}
        />

        <FormMetric
          label="Record"
          value={`${form.wins}-${form.draws}-${form.losses}`}
        />
      </div>
    </section>
  );
}

interface FormMetricProps {
  label: string;
  value: string;
}

function FormMetric({
  label,
  value,
}: FormMetricProps) {
  return (
    <div className="rounded-xl bg-slate-900/60 p-3">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-2 font-bold text-white">
        {value}
      </p>
    </div>
  );
}