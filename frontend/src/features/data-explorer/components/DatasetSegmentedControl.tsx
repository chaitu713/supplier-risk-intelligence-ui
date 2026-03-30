import type { DatasetKey } from "../../../api/datasets";

interface DatasetSegmentedControlProps {
  value: DatasetKey;
  onChange: (value: DatasetKey) => void;
}

const options: Array<{ value: DatasetKey; label: string }> = [
  { value: "suppliers", label: "Suppliers" },
  { value: "esg", label: "ESG" },
  { value: "transactions", label: "Transactions" },
];

export function DatasetSegmentedControl({
  value,
  onChange,
}: DatasetSegmentedControlProps) {
  return (
    <div className="inline-flex rounded-2xl border border-slate-200 bg-slate-100 p-1">
      {options.map((option) => {
        const active = option.value === value;

        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={`rounded-xl px-4 py-2 text-sm font-medium transition ${
              active
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-500 hover:text-slate-700"
            }`}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
