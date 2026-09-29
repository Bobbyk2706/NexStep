
import { request } from "./client";

/**
 * Get the currently authenticated student's profile.
 *
 * Backend:
 * GET /student/profile
 */
export async function getProfile() {
  return request("/student/profile");
}

/**
 * Create/update the currently authenticated student's profile.
 *
 * Backend:
 * PUT /student/profile
 */
export async function saveProfile(profile) {
  return request("/student/profile", {
    method: "PUT",
    body: profile,
  });
}

