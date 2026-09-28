import {
  adminRequest,
  getAdminToken,
  setAdminSession,
  clearAdminSession,
} from "./adminClient";

export { getAdminToken };

// Backend: POST /auth/admin/login -> { access_token, refresh_token }, then
// GET /auth/me for the admin's name/email. Adapted here (rather than adding
// a new backend route) so the rest of the admin UI keeps getting the
// { token, admin } shape it already expects.
export async function adminLogin({ email, password }) {
  const tokens = await adminRequest("/auth/admin/login", {
    method: "POST",
    body: { email, password },
    auth: false,
  });
  setAdminSession({ access: tokens.access_token, refresh: tokens.refresh_token });
  const admin = await fetchAdminSession();
  return { token: tokens.access_token, admin };
}

// Validates the stored token against the backend. Used on page load so a
// stale/expired token can't keep the admin UI open.
export async function fetchAdminSession() {
  const me = await adminRequest("/auth/me");
  return { name: me.name, email: me.email };
}

export function adminLogout() {
  const token = getAdminToken();
  clearAdminSession();
  if (token) {
    // Best effort: tells the backend to revoke this admin's refresh tokens.
    adminRequest("/auth/logout", {
      method: "POST",
      auth: false,
      headers: { Authorization: `Bearer ${token}` },
    }).catch(() => {});
  }
}