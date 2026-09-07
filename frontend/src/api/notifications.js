import { mockDelay } from "./client";
import { mockNotifications } from "./mockData";

let notifications = [...mockNotifications];

export async function getNotifications() {
  await mockDelay(200);
  return [...notifications].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  // Real version:
  // return request("/notifications");
}

export async function markAsRead(id) {
  await mockDelay(100);
  notifications = notifications.map((n) => (n.id === id ? { ...n, read: true } : n));
  return notifications;
  // Real version:
  // return request(`/notifications/${id}/read`, { method: "POST" });
}

export async function markAllAsRead() {
  await mockDelay(150);
  notifications = notifications.map((n) => ({ ...n, read: true }));
  return notifications;
}
