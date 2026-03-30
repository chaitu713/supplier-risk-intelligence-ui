import type { HistogramBin } from "../../../api/analytics";

interface EsgDistributionChartProps {
  bins: HistogramBin[];
  isLoading: boolean;
}

export function EsgDistributionChart({
  bins,
  isLoading,
}: EsgDistributionChartProps) {
  const maxValue = Math.max(...bins.map((bin) => bin.count), 1);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">ESG Score Distribution</h3>
        <p className="mt-1 text-sm text-slate-500">
          Histogram of supplier ESG scores across the portfolio.
        </p>
      </div>

      {isLoading ? (
        <div className="flex h-72 items-end gap-2">
          {Array.from({ length: 20 }).map((_, index) => (
            <div
              key={index}
              className="w-full animate-pulse rounded-t-2xl bg-slate-100"
              style={{ height: `${25 + ((index % 5) + 1) * 8}%` }}
            />
          ))}
        </div>
      ) : (
        <>
          <div className="flex h-72 items-end gap-2">
            {bins.map((bin) => (
              <div key={bin.label} className="group flex w-full flex-col items-center justify-end">
                <div
                  className="w-full rounded-t-2xl bg-blue-700/85 transition group-hover:bg-blue-800"
                  style={{ height: `${(bin.count / maxValue) * 100}%` }}
                  title={`${bin.label}: ${bin.count}`}
                />
              </div>
            ))}
          </div>
          <div className="mt-4 grid grid-cols-4 gap-2 text-[11px] text-slate-500 sm:grid-cols-5">
            {bins.filter((_, index) => index % Math.ceil(bins.length / 5 || 1) === 0).map((bin) => (
              <span key={bin.label}>{bin.start.toFixed(0)}</span>
            ))}
          </div>
        </>
      )}
    </section>
  );
}
