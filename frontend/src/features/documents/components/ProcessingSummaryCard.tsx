import type { IngestionJob } from "../../../api/documents";

interface ProcessingSummaryCardProps {
  job: IngestionJob | undefined;
}

export function ProcessingSummaryCard({ job }: ProcessingSummaryCardProps) {
  const summary = job?.summary;

  return (
    <section className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-xl shadow-sm">
          ✓
        </div>
        <div>
          <h3 className="text-lg font-semibold text-emerald-900">
            Processing Summary
          </h3>
          <p className="text-sm text-emerald-800/80">
            Final record counts from the ingestion pipeline.
          </p>
        </div>
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-3">
        <SummaryMetric
          label="Supplier records"
          value={summary?.supplierRecordsAdded ?? 0}
        />
        <SummaryMetric label="ESG records" value={summary?.esgRecordsAdded ?? 0} />
        <SummaryMetric
          label="Transaction records"
          value={summary?.transactionRecordsAdded ?? 0}
        />
      </div>
    </section>
  );
}

function SummaryMetric({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="rounded-2xl border border-emerald-100 bg-white px-4 py-5">
      <p className="text-xs font-medium uppercase tracking-wide text-emerald-700">
        {label}
      </p>
      <p className="mt-2 text-2xl font-semibold text-slate-900">{value}</p>
    </div>
  );
}
