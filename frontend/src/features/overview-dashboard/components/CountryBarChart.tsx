import type { CountryDistributionItem } from "../../../api/analytics";

interface CountryBarChartProps {
  items: CountryDistributionItem[];
  isLoading: boolean;
}

export function CountryBarChart({ items, isLoading }: CountryBarChartProps) {
  const maxValue = Math.max(...items.map((item) => item.supplierCount), 1);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">Suppliers by Country</h3>
        <p className="mt-1 text-sm text-slate-500">
          Top supplier geographies from the current network.
        </p>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {Array.from({ length: 7 }).map((_, index) => (
            <div key={index} className="h-10 animate-pulse rounded-2xl bg-slate-100" />
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div key={item.country}>
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium text-slate-700">{item.country}</span>
                <span className="text-slate-500">{item.supplierCount}</span>
              </div>
              <div className="h-3 rounded-full bg-slate-100">
                <div
                  className="h-3 rounded-full bg-blue-700"
                  style={{ width: `${(item.supplierCount / maxValue) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
