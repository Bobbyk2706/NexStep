import { adminRequest } from "./adminClient";

export async function runMonitoring() {
  return adminRequest("/api/admin/monitoring/run", {
    method: "POST",
  });
}

export async function getMonitoringReviews(status) {
  const query = status
    ? `?status_filter=${encodeURIComponent(status)}`
    : "";

  return adminRequest(
    `/api/admin/monitoring/reviews${query}`
  );
}

export async function getMonitoringReview(reviewId) {
  return adminRequest(
    `/api/admin/monitoring/reviews/${reviewId}`
  );
}

export async function approveMonitoringReview(
  reviewId
) {
  return adminRequest(
    `/api/admin/monitoring/reviews/${reviewId}/approve`,
    {
      method: "POST",
    }
  );
}

export async function rejectMonitoringReview(
  reviewId,
  reason
) {
  return adminRequest(
    `/api/admin/monitoring/reviews/${reviewId}/reject`,
    {
      method: "POST",
      body: {
        reason,
      },
    }
  );
}

export async function applyMonitoringReview(
  reviewId
) {
  return adminRequest(
    `/api/admin/monitoring/reviews/${reviewId}/apply`,
    {
      method: "POST",
    }
  );
}