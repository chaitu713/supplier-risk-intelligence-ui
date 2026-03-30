import { useState } from "react";

interface ChatComposerProps {
  isLoading: boolean;
  initialValue?: string;
  onSubmit: (message: string) => Promise<void> | void;
}

export function ChatComposer({
  isLoading,
  initialValue = "",
  onSubmit,
}: ChatComposerProps) {
  const [value, setValue] = useState(initialValue);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) {
      return;
    }

    await onSubmit(trimmed);
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 rounded-3xl border border-slate-200 bg-white p-4 shadow-sm">
      <textarea
        value={value}
        onChange={(event) => setValue(event.target.value)}
        rows={3}
        placeholder="Ask about your supplier network..."
        className="resize-none rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-blue-600"
      />
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading || !value.trim()}
          className="inline-flex min-h-11 items-center justify-center rounded-2xl bg-blue-700 px-5 text-sm font-semibold text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isLoading ? "Analyzing..." : "Send"}
        </button>
      </div>
    </form>
  );
}
