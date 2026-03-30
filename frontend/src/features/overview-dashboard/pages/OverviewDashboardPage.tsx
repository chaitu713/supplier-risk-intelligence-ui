import { ApiError } from "../../../api/client";
import { CountryBarChart } from "../components/CountryBarChart";
import { EsgDistributionChart } from "../components/EsgDistributionChart";
import { KpiCard } from "../components/KpiCard";
import {
  useCountryDistribution,
  useEsgDistribution,
  useOverviewMetrics,
} from "../hooks/useOverviewDashboard";

export function OverviewDashboardPage() {
  const metricsQuery = useOverviewMetrics();
  const countriesQuery = useCountryDistribution();
  const esgQuery = useEsgDistribution();

  const errorMessage = getErrorMessage(
    metricsQuery.error ?? countriesQuery.error ?? esgQuery.error,
  );

  const metrics = metricsQuery.data;

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-6 py-10 lg:px-8">
        <header className="rounded-[2rem] border border-slate-200 bg-white px-8 py-8 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-indigo-700">
            Overview Dashboard
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
            High-level supplier metrics and distribution insights
          </h1>
          <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-600 sm:text-base">
            This page mirrors the Streamlit overview dashboard with backend-powered KPI
            cards and chart sections for supplier geography and ESG score spread.
          </p>
        </header>

        {errorMessage ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <KpiCard
            label="Total Suppliers"
            value={metrics ? metrics.totalSuppliers.toLocaleString() : "-"}
            subtitle="Active in network"
            accentClassName="bg-blue-700"
          />
          <KpiCard
            label="Avg ESG Score"
            value={metrics ? metrics.avgEsgScore.toFixed(1) : "-"}
            subtitle="Environmental and social"
            accentClassName="bg-emerald-600"
          />
          <KpiCard
            label="Avg Delay"
            value={metrics ? `${metrics.avgDelayDays.toFixed(1)}d` : "-"}
            subtitle="Delivery performance"
            accentClassName="bg-amber-500"
          />
          <KpiCard
            label="Avg Defect Rate"
            value={metrics ? `${metrics.avgDefectRatePct.toFixed(2)}%` : "-"}
            subtitle="Quality metric"
            accentClassName="bg-cyan-600"
          />
          <KpiCard
            label="High Risk"
            value={metrics ? metrics.highRiskCount.toLocaleString() : "-"}
            subtitle="Require attention"
            accentClassName="bg-rose-600"
          />
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <CountryBarChart
            items={countriesQuery.data ?? []}
            isLoading={countriesQuery.isLoading}
          />
          <EsgDistributionChart bins={esgQuery.data ?? []} isLoading={esgQuery.isLoading} />
        </section>
      </div>
    </div>
  );
}

function getErrorMessage(error: unknown): string | null {
  if (!error) {
    return null;
  }

  if (error instanceof ApiError) {
    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong while loading overview analytics.";
}
