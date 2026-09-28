import { BASE_URL, createClient } from "../../api/client";

const ADMIN_TOKEN_KEY = "nexstep_admin_token";
const ADMIN_REFRESH_KEY = "nexstep_admin_refresh_token";

export function getAdminToken() {
  return localStorage.getItem(ADMIN_TOKEN_KEY);
}

export function setAdminSession({ access, refresh }) {
  localStorage.setItem(ADMIN_TOKEN_KEY, access);
  if (refresh) localStorage.setItem(ADMIN_REFRESH_KEY, refresh);
}

export function clearAdminSession() {
  localStorage.removeItem(ADMIN_TOKEN_KEY);
  localStorage.removeItem(ADMIN_REFRESH_KEY);
}

// Access tokens are short-lived (15 min by default). Refresh tokens ROTATE:
// each one works exactly once. So several requests failing at the same
// moment must share ONE refresh call — a second parallel call would present
// an already-rotated token and get rejected, logging the admin out for no
// reason.
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
        // Another tab may have rotated the token a moment ago. If the stored
        // refresh token changed since we read it, the session is fine.
        return localStorage.getItem(ADMIN_REFRESH_KEY) !== sent;
      }
      const data = await res.json();
      setAdminSession({ access: data.access_token, refresh: data.refresh_token });
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

export const adminRequest = createClient({
  getToken: getAdminToken,
  refresh: refreshAdminSession,
  onUnauthorized() {
    clearAdminSession();
    expiredListeners.forEach((fn) => fn());
  },
});