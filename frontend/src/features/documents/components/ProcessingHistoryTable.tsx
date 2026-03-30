import type { DocumentHistoryItem } from "../../../api/documents";

interface ProcessingHistoryTableProps {
  items: DocumentHistoryItem[];
  isLoading: boolean;
}

export function ProcessingHistoryTable({
  items,
  isLoading,
}: ProcessingHistoryTableProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-slate-900">Processing History</h3>
        <p className="mt-1 text-sm text-slate-500">
          Recent document ingestion activity from the backend.
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left">
          <thead>
            <tr className="text-xs uppercase tracking-wide text-slate-500">
              <th className="px-4 py-3 font-medium">Document</th>
              <th className="px-4 py-3 font-medium">Type</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Records</th>
              <th className="px-4 py-3 font-medium">Processed At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {isLoading ? (
              Array.from({ length: 5 }).map((_, index) => (
                <tr key={index}>
                  <td className="px-4 py-4" colSpan={5}>
                    <div className="h-6 animate-pulse rounded bg-slate-100" />
                  </td>
                </tr>
              ))
            ) : items.length > 0 ? (
              items.map((item) => (
                <tr key={`${item.documentName}-${item.timestamp}`} className="hover:bg-slate-50">
                  <td className="px-4 py-4 text-sm font-medium text-slate-900">
                    {item.documentName}
                  </td>
                  <td className="px-4 py-4 text-sm capitalize text-slate-600">
                    {item.documentType}
                  </td>
                  <td className="px-4 py-4 text-sm text-slate-600">{item.status}</td>
                  <td className="px-4 py-4 text-sm text-slate-600">{item.recordsAdded}</td>
                  <td className="px-4 py-4 text-sm text-slate-600">{item.timestamp}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td className="px-4 py-10 text-center text-sm text-slate-500" colSpan={5}>
                  No ingestion history available yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
