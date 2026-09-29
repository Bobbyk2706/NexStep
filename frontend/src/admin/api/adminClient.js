import { BASE_URL, createClient } from "../../api/client";

const ROOT_API_URL = BASE_URL.replace(/\/api\/?$/, "");
const ADMIN_TOKEN_KEY = "nexstep_admin_token";
const ADMIN_REFRESH_KEY = "nexstep_admin_refresh_token";

export function getAdminToken() {
  return localStorage.getItem(ADMIN_TOKEN_KEY);
}

export function setAdminSession({ access, refresh }) {
  localStorage.setItem(ADMIN_TOKEN_KEY, access);
  if (refresh) {
    localStorage.setItem(ADMIN_REFRESH_KEY, refresh);
  }
}

export function clearAdminSession() {
  localStorage.removeItem(ADMIN_TOKEN_KEY);
  localStorage.removeItem(ADMIN_REFRESH_KEY);
}

let inFlight = null;

function refreshAdminSession() {
  if (!inFlight) {
    inFlight = (async () => {
      const sent = localStorage.getItem(ADMIN_REFRESH_KEY);
      if (!sent) return false;

      const res = await fetch(`${BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: sent }),
      });

      if (!res.ok) {
        return localStorage.getItem(ADMIN_REFRESH_KEY) !== sent;
      }

      const data = await res.json();
      setAdminSession({
        access: data.access_token,
        refresh: data.refresh_token,
      });
      return true;
    })().finally(() => {
      inFlight = null;
    });
  }

  return inFlight;
}

const expiredListeners = new Set();

export function onAdminSessionExpired(fn) {
  expiredListeners.add(fn);
  return () => expiredListeners.delete(fn);
}

// Admin authentication lives under /api, while the admin discovery/review
// routes are mounted at /admin in the backend. Keeping this client rooted at
// the server origin lets one request helper handle both route groups.
export const adminRequest = createClient({
  getToken: getAdminToken,
  refresh: refreshAdminSession,
  baseUrl: ROOT_API_URL,
  onUnauthorized() {
    clearAdminSession();
    expiredListeners.forEach((fn) => fn());
  },
});
