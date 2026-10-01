// Central API client used by the student and admin apps.
//
// `baseUrl` is configurable so the student API (/api) and the admin
// extraction routes (mounted at /admin) can share the same request logic.

export const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const TOKEN_KEY = "nexstep_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export class ApiError extends Error {
  constructor(message, status, extra = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = extra.code ?? null;
    this.officialUrl = extra.officialUrl ?? null;
    this.pagesChecked = extra.pagesChecked ?? null;
  }
}

export function createClient({
  getToken: readToken,
  refresh,
  onUnauthorized,
  baseUrl = BASE_URL,
}) {
  async function send(path, { method, body, headers }) {
    const token = readToken();

    const res = await fetch(`${baseUrl}${path}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...(token
          ? {
              Authorization: `Bearer ${token}`,
            }
          : {}),
        ...headers,
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });

    return {
      res,
      sentToken: Boolean(token),
    };
  }

  return async function request(
    path,
    {
      method = "GET",
      body,
      headers = {},
      auth = true,
    } = {}
  ) {
    const options = {
      method,
      body,
      headers,
    };

    let { res, sentToken } = await send(path, options);

    if (res.status === 401 && auth && sentToken) {
      let refreshed = false;

      if (refresh) {
        try {
          refreshed = await refresh();
        } catch {
          refreshed = false;
        }
      }

      if (refreshed) {
        ({ res } = await send(path, options));
      }

      if (res.status === 401) {
        onUnauthorized?.();
      }
    }

        if (!res.ok) {
      let message = `Request failed (${res.status})`;
      let extra = {};

      try {
        const data = await res.json();
        const d = data?.detail;

        if (typeof d === "string") {
          message = d;
        } else if (Array.isArray(d)) {
          // FastAPI validation errors: [{ loc, msg, type }, ...]
          message = d.map((item) => item?.msg).filter(Boolean).join("; ") || message;
        } else if (d && typeof d === "object") {
          message = d.message || message;
          extra = {
            code: d.code,
            officialUrl: d.official_url,
            pagesChecked: d.pages_checked,
          };
        } else {
          message = data?.message || data?.error || message;
        }
      } catch {
        // Keep the generic message for non-JSON responses.
      }

      throw new ApiError(message, res.status, extra);
    }

    if (res.status === 204) {
      return null;
    }

    const contentType = res.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
      return null;
    }

    return res.json();
  };
}

const expiredListeners = new Set();

export function onSessionExpired(fn) {
  expiredListeners.add(fn);
  return () => expiredListeners.delete(fn);
}

export const request = createClient({
  getToken,
  onUnauthorized() {
    setToken(null);

    expiredListeners.forEach((listener) => {
      try {
        listener();
      } catch {
        // One listener must not prevent the others from running.
      }
    });
  },
});
