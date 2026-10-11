import { request, ApiError } from "./client";

// Backend: POST /api/assistant/chat
// (app/routers/chatbot_router.py -> app/services/chatbot_service.py).
//
// `history` is the running conversation as [{role, content}], oldest
// first, matching what the chat UI already keeps in state.
export async function askAssistant(message, history = []) {
  try {
    const data = await request("/assistant/chat", {
      method: "POST",
      body: {
        message,
        history: history
          .filter((m) => m.role === "user" || m.role === "assistant")
          .filter((m) => typeof m.content === "string" && m.content)
          .slice(-6),
      },
    });

    return { kind: "ok", data };
  } catch (err) {
    if (err instanceof ApiError && err.status === 429) {
      return { kind: "rate-limited", message: err.message };
    }
    if (err instanceof ApiError) {
      // 5xx, or a 4xx such as an expired login: the chat UI has no
      // dedicated "log in again" state, so show the unavailable state.
      return { kind: "backend-unavailable" };
    }
    // fetch() itself threw: no response at all (offline, DNS, CORS).
    return { kind: "network-error" };
  }
}

export function toChatMessage(thinkingId, result) {
  if (result.kind === "backend-unavailable") {
    return { id: thinkingId, role: "assistant", status: "backend-unavailable" };
  }
  if (result.kind === "network-error") {
    return { id: thinkingId, role: "assistant", status: "network-error" };
  }
  if (result.kind === "rate-limited") {
    return {
      id: thinkingId,
      role: "assistant",
      status: "done",
      content:
        result.message ||
        "You have asked a lot of questions. Please wait a few minutes and try again.",
      sources: [],
    };
  }

  const { answer, sources, unavailable } = result.data;

  // No AI model could be reached on the server.
  if (unavailable) {
    return { id: thinkingId, role: "assistant", status: "backend-unavailable" };
  }

  // Show every real answer, including greetings and "how does NexStep
  // work" replies that match no specific exam.
  if (!answer || !answer.trim()) {
    return { id: thinkingId, role: "assistant", status: "no-info" };
  }

  return {
    id: thinkingId,
    role: "assistant",
    status: "done",
    content: answer,
    sources: (sources || []).map((s) => ({
      id: s.exam_id,
      title: s.exam_name,
      category: s.notification_title || "Official notification",
    })),
  };
}