
import { request, setToken, getToken } from "./client";

/**
 * Student login.
 *
 * Backend:
 * POST /auth/login
 *
 * Response:
 * {
 *   token: "...",
 *   user: {
 *     name: "...",
 *     email: "..."
 *   },
 *   hasProfile: true | false
 * }
 */
export async function login({ email, password }) {
  if (!email || !password) {
    throw new Error("Enter your email and password.");
  }

  const data = await request("/auth/login", {
    method: "POST",
    body: {
      email,
      password,
    },
    auth: false,
  });

  if (!data?.token) {
    throw new Error("Login succeeded but no authentication token was returned.");
  }

  setToken(data.token);

  return data;
}

/**
 * Student signup.
 *
 * Backend:
 * POST /auth/signup
 *
 * Response:
 * {
 *   token: "...",
 *   user: {
 *     name: "...",
 *     email: "..."
 *   },
 *   hasProfile: false
 * }
 */
export async function signup({ name, email, password }) {
  if (!name || !email || !password) {
    throw new Error("Fill in your name, email, and password.");
  }

  if (password.length < 6) {
    throw new Error("Password must be at least 6 characters.");
  }

  const data = await request("/auth/signup", {
    method: "POST",
    body: {
      name,
      email,
      password,
    },
    auth: false,
  });

  if (!data?.token) {
    throw new Error("Signup succeeded but no authentication token was returned.");
  }

  setToken(data.token);

  return data;
}

/**
 * Get the currently authenticated user.
 *
 * Backend:
 * GET /auth/me
 */
export async function getCurrentUser() {
  if (!getToken()) {
    return null;
  }

  return request("/auth/me");
}

/**
 * Logout.
 *
 * Backend:
 * POST /auth/logout
 *
 * The backend invalidates the user's token version.
 */
export async function logout() {
  try {
    if (getToken()) {
      await request("/auth/logout", {
        method: "POST",
      });
    }
  } finally {
    setToken(null);
  }
}

