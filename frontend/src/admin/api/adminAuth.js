import { mockDelay } from "../../api/client";

const ADMIN_TOKEN_KEY = "nexstep_admin_token";

export function getAdminToken() {
  return localStorage.getItem(ADMIN_TOKEN_KEY);
}

function setAdminToken(token) {
  if (token) localStorage.setItem(ADMIN_TOKEN_KEY, token);
  else localStorage.removeItem(ADMIN_TOKEN_KEY);
}

// Mocked. Replace with:
//   return request("/admin/auth/login", { method: "POST", body: { email, password } });
// using a request() helper pointed at the admin API base — keep this on a
// separate base URL / auth scheme from the student app if your backend
// splits them, since admin sessions should never double as student sessions.
export async function adminLogin({ email, password }) {
  await mockDelay(300);
  if (!email || !password) {
    throw new Error("Enter your email and password.");
  }
  if (password.length < 6) {
    throw new Error("Invalid credentials.");
  }
  const token = `mock.admin.${btoa(email)}.token`;
  setAdminToken(token);
  return { token, admin: { name: email.split("@")[0], email } };
}

export function adminLogout() {
  setAdminToken(null);
}
