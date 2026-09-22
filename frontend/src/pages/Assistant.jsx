import { useState } from "react";
import { useProfile } from "../context/ProfileContext";
import EmptyState from "../components/chat/EmptyState";
import MessageBubble from "../components/chat/MessageBubble";
import MessageInput from "../components/chat/MessageInput";
import { suggestedQuestions, findAnswer } from "../data/assistantKnowledge";

let msgCounter = 0;
const nextId = () => `m${++msgCounter}`;

const DEV_STATES = [
  { key: "normal", label: "Normal" },
  { key: "no-info", label: "No info" },
  { key: "backend-unavailable", label: "Backend down" },
  { key: "network-error", label: "Network error" },
];

export default function Assistant() {
  const { profile, exams } = useProfile();
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);
  const [devState, setDevState] = useState("normal");

  async function resolveAnswer(query, thinkingId, baseMessages) {
    await new Promise((r) => setTimeout(r, 1000));

    let resolved;
    if (devState !== "normal") {
      resolved = { id: thinkingId, role: "assistant", status: devState };
    } else {
      const match = findAnswer(query, { profile, exams });
      resolved = match
        ? { id: thinkingId, role: "assistant", status: "done", content: match.content, sources: match.sources }
        : { id: thinkingId, role: "assistant", status: "no-info" };
    }

    setMessages(baseMessages.map((m) => (m.id === thinkingId ? resolved : m)));
    setSending(false);
  }

  function handleSend(text) {
    setSending(true);
    const userMsg = { id: nextId(), role: "user", content: text };
    const thinkingId = nextId();
    const withThinking = [...messages, userMsg, { id: thinkingId, role: "assistant", status: "thinking" }];
    setMessages(withThinking);
    resolveAnswer(text, thinkingId, withThinking);
  }

  function handleRetry() {
    const lastUser = [...messages].reverse().find((m) => m.role === "user");
    if (!lastUser) return;
    setSending(true);
    const thinkingId = nextId();
    const withThinking = messages.map((m, i, arr) =>
      i === arr.length - 1 && m.role === "assistant" ? { id: thinkingId, role: "assistant", status: "thinking" } : m
    );
    setMessages(withThinking);
    resolveAnswer(lastUser.content, thinkingId, withThinking);
  }

  function handleRegenerate(messageId) {
    const idx = messages.findIndex((m) => m.id === messageId);
    const lastUser = [...messages.slice(0, idx)].reverse().find((m) => m.role === "user");
    if (!lastUser) return;
    setSending(true);
    const thinkingId = nextId();
    const withThinking = messages.map((m) => (m.id === messageId ? { id: thinkingId, role: "assistant", status: "thinking" } : m));
    setMessages(withThinking);
    resolveAnswer(lastUser.content, thinkingId, withThinking);
  }

  return (
    <div className="flex min-h-[calc(100vh-140px)] flex-col md:min-h-[calc(100vh-100px)]">
      {messages.length === 0 ? (
        <EmptyState questions={suggestedQuestions} onSelect={handleSend} />
      ) : (
        <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-6 py-6">
          {messages.map((m) => (
            <MessageBubble key={m.id} message={m} onRetry={handleRetry} onRegenerate={handleRegenerate} />
          ))}
        </div>
      )}

      <div className="sticky bottom-0 mx-auto w-full max-w-2xl bg-paper/95 pb-2 pt-4 backdrop-blur-sm">
        <MessageInput onSend={handleSend} disabled={sending} />
        <div className="mt-2 flex items-center gap-2 justify-end">
          <span className="font-mono text-[10px] uppercase tracking-wide text-slate-400">Preview:</span>
          {DEV_STATES.map((s) => (
            <button
              key={s.key}
              onClick={() => setDevState(s.key)}
              className={`font-mono text-[10px] uppercase tracking-wide transition ${
                devState === s.key ? "text-gold" : "text-slate-400 hover:text-slate-600"
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
