const suggestions = [
  "Which suppliers have the highest risk scores?",
  "Which countries have the most high-risk suppliers?",
  "Recommend low-risk suppliers for sourcing",
];

interface PromptSuggestionsProps {
  onSelect: (prompt: string) => void;
}

export function PromptSuggestions({ onSelect }: PromptSuggestionsProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {suggestions.map((prompt) => (
        <button
          key={prompt}
          type="button"
          onClick={() => onSelect(prompt)}
          className="rounded-full border border-slate-200 bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700"
        >
          {prompt}
        </button>
      ))}
    </div>
  );
}
