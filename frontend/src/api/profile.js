import { mockDelay } from "./client";
import { mockProfile } from "./mockData";

let currentProfile = null; // null until the student saves their profile once

export async function getProfile() {
  await mockDelay(200);
  return currentProfile;
  // Real version:
  // return request("/student/profile");
}

export async function saveProfile(profile) {
  await mockDelay();
  currentProfile = { ...profile };
  return currentProfile;
  // Real version:
  // return request("/student/profile", { method: "PUT", body: profile });
}

// Convenience for demos — seeds a filled profile without going through the form.
export async function seedDemoProfile() {
  await mockDelay(150);
  currentProfile = { ...mockProfile };
  return currentProfile;
}
