import { useState } from "react";
import EmptyState from "../components/chat/EmptyState";
import MessageBubble from "../components/chat/MessageBubble";
import MessageInput from "../components/chat/MessageInput";
import { askAssistant, toChatMessage } from "../api/assistant";

const SUGGESTED_QUESTIONS = [
  "Am I eligible for GATE 2027?",
  "When does the CAT 2026 application close?",
  "How does NexStep decide what I'm eligible for?",
  "What happens if my CGPA changes?",
  "Am I eligible for UPSC Civil Services?",
  "How will I know about new deadlines?",
];

let msgCounter = 0;
const nextId = () => `m${++msgCounter}`;

export default function Assistant() {
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);

  async function resolveAnswer(query, thinkingId, baseMessages) {
    const history = baseMessages.filter((m) => m.id !== thinkingId);
    const result = await askAssistant(query, history);
    const resolved = toChatMessage(thinkingId, result);

    setMessages((current) =>
      current.map((message) =>
        message.id === thinkingId ? resolved : message
      )
    );
    setSending(false);
  }

  function handleSend(text) {
    if (!text?.trim() || sending) return;

    setSending(true);

    const userMsg = { id: nextId(), role: "user", content: text.trim() };
    const thinkingId = nextId();
    const withThinking = [
      ...messages,
      userMsg,
      { id: thinkingId, role: "assistant", status: "thinking" },
    ];

    setMessages(withThinking);
    resolveAnswer(text.trim(), thinkingId, withThinking);
  }

  function handleRetry() {
    const lastUser = [...messages].reverse().find((m) => m.role === "user");
    if (!lastUser || sending) return;

    setSending(true);
    const thinkingId = nextId();
    const withThinking = [
      ...messages,
      { id: thinkingId, role: "assistant", status: "thinking" },
    ];

    setMessages(withThinking);
    resolveAnswer(lastUser.content, thinkingId, withThinking);
  }

  function handleRegenerate(messageId) {
    const idx = messages.findIndex((m) => m.id === messageId);
    const lastUser = [...messages.slice(0, idx)]
      .reverse()
      .find((m) => m.role === "user");

    if (!lastUser || sending) return;

    setSending(true);
    const thinkingId = nextId();
    const withThinking = messages.map((message) =>
      message.id === messageId
        ? { id: thinkingId, role: "assistant", status: "thinking" }
        : message
    );

    setMessages(withThinking);
    resolveAnswer(lastUser.content, thinkingId, withThinking);
  }

  return (
    <div className="flex min-h-[calc(100vh-140px)] flex-col md:min-h-[calc(100vh-100px)]">
      {messages.length === 0 ? (
        <EmptyState questions={SUGGESTED_QUESTIONS} onSelect={handleSend} />
      ) : (
        <div className="mx-auto flex w-full max-w-2xl flex-1 flex-col gap-6 py-6">
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              onRetry={handleRetry}
              onRegenerate={handleRegenerate}
            />
          ))}
        </div>
      )}

      <div className="sticky bottom-0 mx-auto w-full max-w-2xl bg-paper/95 pb-2 pt-4 backdrop-blur-sm">
        <MessageInput onSend={handleSend} disabled={sending} />
      </div>
    </div>
  );
}
