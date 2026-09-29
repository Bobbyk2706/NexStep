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
    if (err instanceof ApiError && err.status >= 500) {
      return { kind: "backend-unavailable" };
    }
    if (err instanceof ApiError) {
      // 4xx (e.g. auth expired) — surface as backend-unavailable too;
      // the chat UI has no dedicated "please log in again" state yet.
      return { kind: "backend-unavailable" };
    }
    // fetch() itself threw — no response at all (offline, DNS, CORS).
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

  const { answer, sources, grounded } = result.data;

  if (!grounded && (!sources || sources.length === 0)) {
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
