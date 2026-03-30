import type { RiskSegmentationItem } from "../../../api/risk";

interface RiskSegmentationChartProps {
  items: RiskSegmentationItem[];
  isLoading: boolean;
}

const colors: Record<string, string> = {
  High: "bg-rose-600",
  Medium: "bg-amber-500",
  Low: "bg-emerald-600",
};

export function RiskSegmentationChart({
  items,
  isLoading,
}: RiskSegmentationChartProps) {
  const total = items.reduce((sum, item) => sum + item.supplierCount, 0);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">Risk Segmentation</h3>
        <p className="mt-1 text-sm text-slate-500">
          Supplier mix by high, medium, and low operational risk.
        </p>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          <div className="h-6 animate-pulse rounded-full bg-slate-100" />
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, index) => (
              <div key={index} className="h-14 animate-pulse rounded-2xl bg-slate-100" />
            ))}
          </div>
        </div>
      ) : (
        <>
          <div className="flex h-5 overflow-hidden rounded-full bg-slate-100">
            {items.map((item) => (
              <div
                key={item.riskLevel}
                className={colors[item.riskLevel]}
                style={{ width: `${total === 0 ? 0 : (item.supplierCount / total) * 100}%` }}
                title={`${item.riskLevel}: ${item.supplierCount}`}
              />
            ))}
          </div>

          <div className="mt-6 space-y-3">
            {items.map((item) => (
              <div
                key={item.riskLevel}
                className="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-4"
              >
                <div className="flex items-center gap-3">
                  <span className={`h-3 w-3 rounded-full ${colors[item.riskLevel]}`} />
                  <span className="text-sm font-medium text-slate-700">{item.riskLevel}</span>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-slate-900">{item.supplierCount}</p>
                  <p className="text-xs text-slate-500">
                    {total === 0 ? 0 : ((item.supplierCount / total) * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </section>
  );
}
