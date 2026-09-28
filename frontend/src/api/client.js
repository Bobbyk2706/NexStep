// Central API client.
//
// createClient() builds a fetch wrapper with 401 handling, so the student
// app and the admin app can share the same logic while keeping separate
// tokens (an admin session must never double as a student session).
//
// When a request that carried a token comes back 401, the session is no
// longer valid. The client (optionally) tries a token refresh once, retries,
// and if it is still 401 calls onUnauthorized() so the owning auth context
// can clear its state — RequireAuth / RequireAdminAuth then redirect to
// /login. A 401 on a request that sent no token (e.g. a wrong password on
// login) is just a failed attempt and does NOT count as an expired session.

export const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const TOKEN_KEY = "nexstep_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export function createClient({ getToken, refresh, onUnauthorized }) {
  async function send(path, { method, body, headers }) {
    const token = getToken();
    const res = await fetch(`${BASE_URL}${path}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...headers,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    return { res, sentToken: Boolean(token) };
  }

  // `auth: false` opts a call out of session-expiry handling (login, logout).
  return async function request(path, { method = "GET", body, headers = {}, auth = true } = {}) {
    const opts = { method, body, headers };
    let { res, sentToken } = await send(path, opts);

    if (res.status === 401 && auth && sentToken) {
      if (refresh && (await refresh())) {
        ({ res } = await send(path, opts));
      }
      if (res.status === 401) onUnauthorized?.();
    }

    if (!res.ok) {
      let message = `Request failed (${res.status})`;
      try {
        const data = await res.json();
        message = data.message || data.error || message;
      } catch {
        // response wasn't JSON — keep the generic message
      }
      throw new ApiError(message, res.status);
    }

    if (res.status === 204) return null;
    return res.json();
  };
}

// Student session: subscribe to be told when the token stops being valid.
const expiredListeners = new Set();
export function onSessionExpired(fn) {
  expiredListeners.add(fn);
  return () => expiredListeners.delete(fn);
}

export const request = createClient({
  getToken,
  onUnauthorized() {
    setToken(null);
    expiredListeners.forEach((fn) => fn());
  },
});

// Small helper so mock modules can simulate network latency without
// every file re-implementing a sleep function.
export const mockDelay = (ms = 350) => new Promise((resolve) => setTimeout(resolve, ms));