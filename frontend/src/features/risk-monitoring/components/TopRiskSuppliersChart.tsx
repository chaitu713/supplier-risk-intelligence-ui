import type { RiskSupplierItem } from "../../../api/risk";

interface TopRiskSuppliersChartProps {
  items: RiskSupplierItem[];
  isLoading: boolean;
}

export function TopRiskSuppliersChart({
  items,
  isLoading,
}: TopRiskSuppliersChartProps) {
  const maxValue = Math.max(...items.map((item) => item.riskScore), 1);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">Top 10 High-Risk Suppliers</h3>
        <p className="mt-1 text-sm text-slate-500">
          Highest-risk suppliers ranked by risk score.
        </p>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {Array.from({ length: 10 }).map((_, index) => (
            <div key={index} className="h-12 animate-pulse rounded-2xl bg-slate-100" />
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div key={item.supplierId}>
              <div className="mb-2 flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-medium text-slate-900">{item.supplierName}</p>
                  <p className="text-xs text-slate-500">
                    {[item.country, item.category].filter(Boolean).join(" • ")}
                  </p>
                </div>
                <span className="text-sm font-semibold text-slate-700">
                  {item.riskScore.toFixed(2)}
                </span>
              </div>
              <div className="h-3 rounded-full bg-slate-100">
                <div
                  className="h-3 rounded-full bg-blue-700"
                  style={{ width: `${(item.riskScore / maxValue) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
