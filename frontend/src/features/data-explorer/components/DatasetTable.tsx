import type { DatasetRecord } from "../../../api/datasets";

interface DatasetTableProps {
  records: DatasetRecord[];
  isLoading: boolean;
}

export function DatasetTable({ records, isLoading }: DatasetTableProps) {
  const columns = records[0] ? Object.keys(records[0]) : [];

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-slate-900">Dataset Preview</h3>
        <p className="mt-1 text-sm text-slate-500">
          Showing the first 100 rows from the selected dataset, matching the current
          Streamlit behavior.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left">
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column}
                  className="whitespace-nowrap px-4 py-3 text-xs font-semibold uppercase tracking-[0.14em] text-slate-500"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading ? (
              Array.from({ length: 8 }).map((_, index) => (
                <tr key={index}>
                  <td className="px-4 py-4" colSpan={Math.max(columns.length, 1)}>
                    <div className="h-6 animate-pulse rounded bg-slate-100" />
                  </td>
                </tr>
              ))
            ) : records.length > 0 ? (
              records.map((record, rowIndex) => (
                <tr key={rowIndex} className="hover:bg-slate-50">
                  {Object.entries(record).map(([column, value]) => (
                    <td
                      key={`${rowIndex}-${column}`}
                      className="whitespace-nowrap px-4 py-3 text-sm text-slate-700"
                    >
                      {formatCellValue(value)}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td
                  className="px-4 py-10 text-center text-sm text-slate-500"
                  colSpan={Math.max(columns.length, 1)}
                >
                  No records found for the selected dataset.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "—";
  }

  if (typeof value === "number") {
    return Number.isInteger(value) ? value.toString() : value.toFixed(2);
  }

  return String(value);
}
