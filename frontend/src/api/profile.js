import { request } from "./client";

export async function getProfile() {
  return request("/student/profile");
}

export async function saveProfile(profile) {
  return request("/student/profile", { method: "PUT", body: profile });
}

// seedDemoProfile() removed — it only made sense against the in-memory
// mock. There's no backend equivalent (and shouldn't be, since it
// silently wrote fake data). If any page still imports this, replace
// that usage with the real login/signup + PUT /student/profile flow.