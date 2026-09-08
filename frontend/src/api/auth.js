import { request, setToken } from "./client";

export async function login({ email, password }) {
  const res = await request("/auth/login", {
    method: "POST",
    body: { email, password },
  });
  setToken(res.token);
  return res;
}

export async function signup({ name, email, password }) {
  const res = await request("/auth/signup", {
    method: "POST",
    body: { name, email, password },
  });
  setToken(res.token);
  return res;
}

export function logout() {
  setToken(null);
}