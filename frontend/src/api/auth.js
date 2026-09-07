import { mockDelay, setToken } from "./client";

// Mocked auth. Replace the bodies below with:
//   return request("/auth/login", { method: "POST", body: { email, password } });
//   return request("/auth/signup", { method: "POST", body: { name, email, password } });
// Vivek's API is expected to return { token, user, hasProfile } — this mock
// mirrors that shape so nothing downstream (AuthContext, routes) needs to
// change when the real endpoint is wired in.

export async function login({ email, password }) {
  await mockDelay();
  if (!email || !password) {
    throw new Error("Enter your email and password.");
  }
  if (password.length < 6) {
    throw new Error("That email/password combination doesn't match our records.");
  }
  const token = `mock.${btoa(email)}.token`;
  setToken(token);
  return {
    token,
    user: { name: email.split("@")[0], email },
    hasProfile: true,
  };
}

export async function signup({ name, email, password }) {
  await mockDelay();
  if (!name || !email || !password) {
    throw new Error("Fill in your name, email, and password.");
  }
  if (password.length < 6) {
    throw new Error("Password must be at least 6 characters.");
  }
  const token = `mock.${btoa(email)}.token`;
  setToken(token);
  return {
    token,
    user: { name, email },
    hasProfile: false,
  };
}

export function logout() {
  setToken(null);
}
