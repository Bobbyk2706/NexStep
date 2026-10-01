import { request } from "./client";

function normalizeType(value) {
  const type = String(value || "").toUpperCase();

  if (type.includes("DEADLINE")) return "deadline";
  if (type.includes("ELIGIBLE")) return "new-eligible";
  if (type.includes("EXAM")) return "exam";
  return "update";
}

function normalizeNotification(notification) {
  return {
    ...notification,
    id: notification.notification_id,
    type: normalizeType(notification.notification_type),
    read: Boolean(notification.is_read),
    timestamp: notification.created_at,
    examId: notification.exam_id,
  };
}

export async function getNotifications() {
  const data = await request("/notifications");
  return (data || []).map(normalizeNotification);
}

export async function markAsRead(id) {
  if (id === undefined || id === null || id === "") {
    throw new Error("Notification ID is required.");
  }

  await request(`/notifications/${encodeURIComponent(id)}/read`, {
    method: "POST",
  });

  return getNotifications();
}

export async function markAllAsRead() {
  await request("/notifications/read-all", {
    method: "POST",
  });

  return getNotifications();
}
