import { adminRequest } from "./adminClient";

/**
 * Notifications sent to students, newest first.
 * Backend: GET /admin/notifications
 */
export async function getNotificationLog({ emailStatus = "", limit = 100 } = {}) {
  const params = new URLSearchParams();

  if (emailStatus) params.set("email_status", emailStatus);
  params.set("limit", String(limit));

  const data = await adminRequest(`/admin/notifications?${params.toString()}`);

  return (data || []).map((row) => ({
    id: row.notification_id,
    studentId: row.student_id,
    studentName: row.student_name,
    studentEmail: row.student_email,
    examId: row.exam_id,
    examName: row.exam_name,
    type: row.notification_type,
    title: row.title,
    message: row.message,
    isRead: Boolean(row.is_read),
    createdAt: row.created_at,
    emailStatus: row.email_status,
    emailSentAt: row.email_sent_at,
    emailError: row.email_error,
  }));
}

/**
 * Counts by email status.
 * Backend: GET /admin/notifications/summary
 */
export async function getNotificationSummary() {
  return adminRequest("/admin/notifications/summary");
}

/**
 * Retry a failed or skipped email.
 * Backend: POST /admin/notifications/{id}/retry-email
 */
export async function retryNotificationEmail(id) {
  return adminRequest(
    `/admin/notifications/${encodeURIComponent(id)}/retry-email`,
    { method: "POST" }
  );
}

/**
 * Run the deadline-reminder job now.
 * Backend: POST /admin/notifications/run-deadline-reminders
 */
export async function runDeadlineReminders() {
  return adminRequest("/admin/notifications/run-deadline-reminders", {
    method: "POST",
  });
}