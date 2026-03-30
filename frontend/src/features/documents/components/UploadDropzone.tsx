import { useId } from "react";

interface UploadDropzoneProps {
  label: string;
  file: File | null;
  accept?: string;
  onFileSelect: (file: File | null) => void;
}

export function UploadDropzone({
  label,
  file,
  accept = ".pdf,application/pdf",
  onFileSelect,
}: UploadDropzoneProps) {
  const inputId = useId();

  return (
    <div className="space-y-3">
      <label
        htmlFor={inputId}
        className="flex min-h-40 cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-center transition hover:border-blue-500 hover:bg-blue-50"
      >
        <span className="text-sm font-medium text-slate-800">
          {file ? file.name : label}
        </span>
        <span className="mt-2 text-xs text-slate-500">
          Drag and drop a PDF here, or click to browse
        </span>
        {file ? (
          <span className="mt-3 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
            {(file.size / 1024 / 1024).toFixed(2)} MB
          </span>
        ) : null}
      </label>

      <input
        id={inputId}
        type="file"
        accept={accept}
        className="hidden"
        onChange={(event) => onFileSelect(event.target.files?.[0] ?? null)}
      />

      {file ? (
        <button
          type="button"
          onClick={() => onFileSelect(null)}
          className="text-xs font-medium text-rose-600 transition hover:text-rose-700"
        >
          Remove file
        </button>
      ) : null}
    </div>
  );
}
