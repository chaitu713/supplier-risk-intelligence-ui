import type { AdvisorMessage } from "../../../api/advisor";

interface ChatMessageProps {
  message: AdvisorMessage;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-3xl rounded-3xl px-5 py-4 text-sm leading-6 shadow-sm ${
          isUser
            ? "bg-blue-700 text-white"
            : "border border-slate-200 bg-white text-slate-700"
        }`}
      >
        {!isUser ? (
          <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-500">
            AI-generated insights based on supplier performance data
          </p>
        ) : null}
        <div className="whitespace-pre-wrap">{message.content}</div>
      </div>
    </div>
  );
}
