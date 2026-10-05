import { request, setToken, getToken } from "./client";

// Requires a real dotted domain with a 2+ letter ending, so
// "example@nexstep" is rejected but "name@college.ac.in" passes.
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@.]{2,}$/;

export function isValidEmail(value) {
  return EMAIL_PATTERN.test((value || "").trim());
}

const EMAIL_ERROR = "Enter a valid email address, like name@example.com.";

/**
 * Student login.
 *
 * Backend: POST /auth/login
 * Response: { token, user: { name, email }, hasProfile }
 */
export async function login({ email, password }) {
  if (!email || !password) {
    throw new Error("Enter your email and password.");
  }

  const cleanEmail = email.trim();

  if (!isValidEmail(cleanEmail)) {
    throw new Error(EMAIL_ERROR);
  }

  const data = await request("/auth/login", {
    method: "POST",
    body: { email: cleanEmail, password },
    auth: false,
  });

  if (!data?.token) {
    throw new Error("Login succeeded but no authentication token was returned.");
  }

  setToken(data.token);

  return data;
}

/**
 * Signup step 1: email a verification code. No account is created yet.
 *
 * Backend: POST /auth/register/start
 * Response: { email, expiresInSeconds, resendAfterSeconds }
 */
export async function startSignup({ name, email, password }) {
  if (!name || !email || !password) {
    throw new Error("Fill in your name, email, and password.");
  }

  const cleanEmail = email.trim();

  if (!isValidEmail(cleanEmail)) {
    throw new Error(EMAIL_ERROR);
  }

  if (password.length < 6) {
    throw new Error("Password must be at least 6 characters.");
  }

  return request("/auth/register/start", {
    method: "POST",
    body: { name: name.trim(), email: cleanEmail, password },
    auth: false,
  });
}

/**
 * Signup step 2: confirm the code. The account is created only now.
 *
 * Backend: POST /auth/register/verify
 * Response: { token, user: { name, email }, hasProfile: false }
 */
export async function verifySignup({ email, code }) {
  if (!/^\d{6}$/.test((code || "").trim())) {
    throw new Error("Enter the 6-digit code from your email.");
  }

  const data = await request("/auth/register/verify", {
    method: "POST",
    body: { email: email.trim(), code: code.trim() },
    auth: false,
  });

  if (!data?.token) {
    throw new Error("Verification succeeded but no authentication token was returned.");
  }

  setToken(data.token);

  return data;
}

/**
 * Send a fresh code.
 *
 * Backend: POST /auth/register/resend
 */
export async function resendSignupCode(email) {
  return request("/auth/register/resend", {
    method: "POST",
    body: { email: email.trim() },
    auth: false,
  });
}

/**
 * Get the currently authenticated user.
 *
 * Backend: GET /auth/me
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
 * Backend: POST /auth/logout
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