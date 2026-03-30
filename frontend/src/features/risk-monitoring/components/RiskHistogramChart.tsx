import type { RiskHistogramBin } from "../../../api/risk";

interface RiskHistogramChartProps {
  bins: RiskHistogramBin[];
  isLoading: boolean;
}

export function RiskHistogramChart({ bins, isLoading }: RiskHistogramChartProps) {
  const maxValue = Math.max(...bins.map((bin) => bin.count), 1);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">Risk Score Distribution</h3>
        <p className="mt-1 text-sm text-slate-500">
          Histogram view of supplier risk scores across the fleet.
        </p>
      </div>

      {isLoading ? (
        <div className="flex h-72 items-end gap-2">
          {Array.from({ length: 7 }).map((_, index) => (
            <div
              key={index}
              className="w-full animate-pulse rounded-t-2xl bg-slate-100"
              style={{ height: `${30 + ((index % 4) + 1) * 12}%` }}
            />
          ))}
        </div>
      ) : (
        <>
          <div className="flex h-72 items-end gap-3">
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
          <div className="mt-4 grid grid-cols-4 gap-2 text-[11px] text-slate-500 sm:grid-cols-7">
            {bins.map((bin) => (
              <span key={bin.label} className="truncate">
                {bin.start.toFixed(1)}
              </span>
            ))}
          </div>
        </>
      )}
    </section>
  );
}
