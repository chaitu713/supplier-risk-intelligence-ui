interface DatasetSummaryCardsProps {
  totalRows: number;
  totalColumns: number;
}

export function DatasetSummaryCards({
  totalRows,
  totalColumns,
}: DatasetSummaryCardsProps) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <SummaryCard label="Total Rows" value={totalRows.toLocaleString()} />
      <SummaryCard label="Columns" value={String(totalColumns)} />
    </div>
  );
}

function SummaryCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
        {label}
      </p>
      <p className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
        {value}
      </p>
    </div>
  );
}
