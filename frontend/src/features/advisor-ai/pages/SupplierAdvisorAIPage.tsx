import { useEffect, useMemo, useState } from "react";

import { ApiError } from "../../../api/client";
import { ChatComposer } from "../components/ChatComposer";
import { ChatMessage } from "../components/ChatMessage";
import { PromptSuggestions } from "../components/PromptSuggestions";
import {
  useAdvisorSession,
  useCreateAdvisorSession,
  useSendAdvisorMessage,
} from "../hooks/useAdvisorAI";

export function SupplierAdvisorAIPage() {
  const [sessionId, setSessionId] = useState<string | null>(null);

  const createSessionMutation = useCreateAdvisorSession();
  const sessionQuery = useAdvisorSession(sessionId);
  const sendMessageMutation = useSendAdvisorMessage(sessionId);

  useEffect(() => {
    if (!sessionId && !createSessionMutation.isPending && !createSessionMutation.data) {
      createSessionMutation.mutate(undefined, {
        onSuccess: (session) => setSessionId(session.sessionId),
      });
    }
  }, [createSessionMutation, sessionId]);

  const messages = useMemo(() => sessionQuery.data?.messages ?? [], [sessionQuery.data]);

  const handleSend = async (message: string) => {
    if (!sessionId) {
      return;
    }

    await sendMessageMutation.mutateAsync(message);
  };

  const errorMessage = getErrorMessage(
    createSessionMutation.error ?? sessionQuery.error ?? sendMessageMutation.error,
  );

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-6 py-10 lg:px-8">
        <header className="rounded-[2rem] border border-slate-200 bg-white px-8 py-8 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-violet-700">
            Supplier Advisor AI
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
            AI-powered guidance across supplier risk, ESG, and performance
          </h1>
          <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-600 sm:text-base">
            This page mirrors the Streamlit advisor chat with example prompts,
            session-based message history, and backend-powered supplier analysis.
          </p>

          <div className="mt-6">
            <PromptSuggestions onSelect={(prompt) => void handleSend(prompt)} />
          </div>
        </header>

        {errorMessage ? (
          <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
            {errorMessage}
          </div>
        ) : null}

        <section className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm">
          {messages.length === 0 ? (
            <div className="rounded-3xl border border-dashed border-slate-200 bg-slate-50 px-6 py-14 text-center">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-to-br from-blue-700 to-violet-700 text-2xl text-white shadow-lg">
                AI
              </div>
              <h2 className="mt-5 text-xl font-semibold text-slate-900">
                Supplier Advisor AI Ready
              </h2>
              <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-slate-500">
                Ask anything about supplier risk, ESG performance, or operational insights.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <ChatMessage
                  key={`${message.role}-${message.createdAt}-${index}`}
                  message={message}
                />
              ))}
            </div>
          )}
        </section>

        <ChatComposer
          isLoading={
            createSessionMutation.isPending ||
            sessionQuery.isLoading ||
            sendMessageMutation.isPending
          }
          onSubmit={handleSend}
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

  return "Something went wrong while loading the advisor experience.";
}
