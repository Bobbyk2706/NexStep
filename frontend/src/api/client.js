// Central API client.
//
// Right now every function in src/api/*.js reads from the mock data in
// mockData.js so the whole app runs with no backend. When Vivek's API is
// ready, point BASE_URL at it and each api/*.js file can swap its mock
// body for a call to `request(...)` below — the rest of the app (pages,
// components) never touches fetch directly, so nothing else changes.

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const TOKEN_KEY = "nexstep_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export async function request(path, { method = "GET", body, headers = {} } = {}) {
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
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

// Small helper so mock modules can simulate network latency without
// every file re-implementing a sleep function.
export const mockDelay = (ms = 350) => new Promise((resolve) => setTimeout(resolve, ms));
