import { useMemo, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";

import { ApiError } from "../../../api/client";
import type { DocumentKind } from "../../../api/documents";
import { ProcessingHistoryTable } from "../components/ProcessingHistoryTable";
import { ProcessingSummaryCard } from "../components/ProcessingSummaryCard";
import { ProcessingTimeline } from "../components/ProcessingTimeline";
import { UploadCard } from "../components/UploadCard";
import { UploadDropzone } from "../components/UploadDropzone";
import {
  useDocumentHistory,
  useIngestionJob,
  useStartDocumentIngestion,
} from "../hooks/useDocumentIngestion";

type FileState = Record<DocumentKind, File | null>;

const initialFiles: FileState = {
  supplier: null,
  esg: null,
  transaction: null,
};

const uploadDefinitions: Array<{
  kind: DocumentKind;
  title: string;
  description: string;
  icon: string;
  tintClassName: string;
  emptyLabel: string;
}> = [
  {
    kind: "supplier",
    title: "Supplier Document",
    description: "Company and supplier master data",
    icon: "🏭",
    tintClassName: "bg-blue-50 text-blue-700",
    emptyLabel: "Upload supplier PDF",
  },
  {
    kind: "esg",
    title: "ESG Document",
    description: "Environmental and social metrics",
    icon: "🌿",
    tintClassName: "bg-emerald-50 text-emerald-700",
    emptyLabel: "Upload ESG PDF",
  },
  {
    kind: "transaction",
    title: "Transaction Document",
    description: "Order and transaction records",
    icon: "💳",
    tintClassName: "bg-amber-50 text-amber-700",
    emptyLabel: "Upload transaction PDF",
  },
];

export function DocumentIngestionPage() {
  const queryClient = useQueryClient();
  const [files, setFiles] = useState<FileState>(initialFiles);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);

  const historyQuery = useDocumentHistory();
  const startIngestionMutation = useStartDocumentIngestion();
  const ingestionJobQuery = useIngestionJob(activeJobId);

  const isReadyToProcess = useMemo(
    () => Boolean(files.supplier && files.esg && files.transaction),
    [files],
  );

  const currentJob = ingestionJobQuery.data ?? startIngestionMutation.data;

  const handleFileChange = (kind: DocumentKind, file: File | null) => {
    setFiles((current) => ({
      ...current,
      [kind]: file,
    }));
  };

  const handleProcessDocuments = async () => {
    if (!files.supplier || !files.esg || !files.transaction) {
      return;
    }

    const job = await startIngestionMutation.mutateAsync({
      supplierFile: files.supplier,
      esgFile: files.esg,
      transactionFile: files.transaction,
    });

    setActiveJobId(job.jobId);
    void queryClient.invalidateQueries({ queryKey: ["documents", "history"] });
  };

  const errorMessage = getErrorMessage(
    startIngestionMutation.error ?? ingestionJobQuery.error ?? historyQuery.error,
  );

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-6 py-10 lg:px-8">
        <header className="rounded-[2rem] border border-slate-200 bg-white px-8 py-8 shadow-sm">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="text-sm font-semibold uppercase tracking-[0.18em] text-blue-700">
                Document Ingestion
              </p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
                Upload and process supplier, ESG, and transaction PDFs
              </h1>
              <p className="mt-4 text-sm leading-6 text-slate-600 sm:text-base">
                This React flow replaces the Streamlit ingestion page with a cleaner
                production-ready UI. It registers uploads, sends files to object storage,
                triggers ingestion, and tracks processing history through backend APIs.
              </p>
            </div>

            <button
              type="button"
              onClick={() => void handleProcessDocuments()}
              disabled={!isReadyToProcess || startIngestionMutation.isPending}
              className="inline-flex items-center justify-center rounded-2xl bg-blue-700 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              {startIngestionMutation.isPending ? "Processing..." : "Process Documents"}
            </button>
          </div>
        </header>

        <section className="grid gap-4 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm md:grid-cols-5">
          {[
            { title: "Upload", subtitle: "Select PDF files" },
            { title: "Store", subtitle: "Upload to blob storage" },
            { title: "Extract", subtitle: "Run document intelligence" },
            { title: "Process", subtitle: "Parse structured records" },
            { title: "History", subtitle: "Log ingestion results" },
          ].map((step, index) => (
            <div key={step.title} className="flex items-center gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-blue-50 text-sm font-semibold text-blue-700">
                {index + 1}
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-900">{step.title}</p>
                <p className="text-xs text-slate-500">{step.subtitle}</p>
              </div>
            </div>
          ))}
        </section>

        {errorMessage ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}

        <section className="grid gap-6 xl:grid-cols-3">
          {uploadDefinitions.map((definition) => (
            <UploadCard
              key={definition.kind}
              icon={definition.icon}
              title={definition.title}
              description={definition.description}
              tintClassName={definition.tintClassName}
            >
              <UploadDropzone
                label={definition.emptyLabel}
                file={files[definition.kind]}
                onFileSelect={(file) => handleFileChange(definition.kind, file)}
              />
            </UploadCard>
          ))}
        </section>

        <div className="grid gap-6 xl:grid-cols-[1.25fr_0.9fr]">
          <ProcessingTimeline
            job={currentJob}
            isLoading={startIngestionMutation.isPending && !currentJob}
          />

          {currentJob?.status === "completed" ? (
            <ProcessingSummaryCard job={currentJob} />
          ) : (
            <aside className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Ready State</h3>
              <p className="mt-1 text-sm text-slate-500">
                All three documents must be selected before the pipeline can start.
              </p>

              <div className="mt-5 space-y-3">
                {uploadDefinitions.map((definition) => {
                  const selected = Boolean(files[definition.kind]);

                  return (
                    <div
                      key={definition.kind}
                      className="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-3"
                    >
                      <span className="text-sm font-medium text-slate-700">
                        {definition.title}
                      </span>
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-medium ${
                          selected
                            ? "bg-emerald-50 text-emerald-700"
                            : "bg-slate-100 text-slate-500"
                        }`}
                      >
                        {selected ? "Selected" : "Pending"}
                      </span>
                    </div>
                  );
                })}
              </div>
            </aside>
          )}
        </div>

        <ProcessingHistoryTable
          items={historyQuery.data ?? []}
          isLoading={historyQuery.isLoading}
        />
      </div>
    </div>
  );
}

function getErrorMessage(error: unknown): string | null {
  if (!error) {
    return null;
  }

  if (error instanceof ApiError) {
    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Something went wrong while processing documents.";
}
