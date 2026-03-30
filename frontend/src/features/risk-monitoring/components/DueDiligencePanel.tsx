import { useState } from "react";

import type { DueDiligenceResponse, RiskSupplierItem } from "../../../api/risk";

interface DueDiligencePanelProps {
  suppliers: RiskSupplierItem[];
  result: DueDiligenceResponse | undefined;
  isLoading: boolean;
  onRun: (supplierId: number) => void;
}

export function DueDiligencePanel({
  suppliers,
  result,
  isLoading,
  onRun,
}: DueDiligencePanelProps) {
  const [selectedSupplierId, setSelectedSupplierId] = useState<number | "">("");

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">Supplier Due Diligence Agent</h3>
        <p className="mt-1 text-sm text-slate-500">
          Run AI-assisted evaluation for one of the current high-risk suppliers.
        </p>
      </div>

      <div className="flex flex-col gap-4 md:flex-row">
        <select
          value={selectedSupplierId}
          onChange={(event) =>
            setSelectedSupplierId(event.target.value ? Number(event.target.value) : "")
          }
          className="min-h-12 flex-1 rounded-2xl border border-slate-300 bg-white px-4 text-sm text-slate-700 outline-none ring-0 transition focus:border-blue-600"
        >
          <option value="">Select a supplier</option>
          {suppliers.map((supplier) => (
            <option key={supplier.supplierId} value={supplier.supplierId}>
              {supplier.supplierName}
            </option>
          ))}
        </select>

        <button
          type="button"
          disabled={selectedSupplierId === "" || isLoading}
          onClick={() => selectedSupplierId !== "" && onRun(selectedSupplierId)}
          className="inline-flex min-h-12 items-center justify-center rounded-2xl bg-blue-700 px-5 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isLoading ? "Running..." : "Run Due Diligence"}
        </button>
      </div>

      {result ? (
        <div className="mt-6 space-y-5">
          <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
            <h4 className="text-lg font-semibold text-slate-900">{result.supplier}</h4>
            <div className="mt-4 grid gap-3 md:grid-cols-3">
              <Metric label="Operational Risk" value={result.opRisk} />
              <Metric label="ESG Risk" value={result.esgRisk} />
              <Metric label="Overall Risk" value={result.overall} />
            </div>
          </div>

          <div>
            <h5 className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">
              Key Issues
            </h5>
            <ul className="mt-3 space-y-2">
              {result.issues.map((issue) => (
                <li
                  key={issue}
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700"
                >
                  {issue}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h5 className="text-sm font-semibold uppercase tracking-[0.16em] text-slate-500">
              Recommendation
            </h5>
            <div className="mt-3 rounded-2xl border border-slate-200 bg-white px-4 py-4 text-sm leading-6 text-slate-700">
              {result.aiSummary}
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white px-4 py-4">
      <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-500">
        {label}
      </p>
      <p className="mt-2 text-base font-semibold text-slate-900">{value}</p>
    </div>
  );
}
