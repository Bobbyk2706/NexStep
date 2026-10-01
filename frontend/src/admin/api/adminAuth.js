import {
  adminRequest,
  getAdminToken,
  setAdminSession,
  clearAdminSession,
} from "./adminClient";

export { getAdminToken };

export async function adminLogin({ email, password }) {
  const tokens = await adminRequest("/api/auth/admin/login", {
    method: "POST",
    body: { email, password },
    auth: false,
  });

  if (!tokens?.access_token || !tokens?.refresh_token) {
    throw new Error("Admin login succeeded but authentication tokens were not returned.");
  }

  setAdminSession({
    access: tokens.access_token,
    refresh: tokens.refresh_token,
  });

  const admin = await fetchAdminSession();
  return { token: tokens.access_token, admin };
}

export async function fetchAdminSession() {
  const me = await adminRequest("/api/auth/me");
  return { name: me.name, email: me.email };
}

export function adminLogout() {
  const token = getAdminToken();
  clearAdminSession();

  if (token) {
    adminRequest("/api/auth/logout", {
      method: "POST",
      auth: false,
      headers: { Authorization: `Bearer ${token}` },
    }).catch(() => {});
  }
}
