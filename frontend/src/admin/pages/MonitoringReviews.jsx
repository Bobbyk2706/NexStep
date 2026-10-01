import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import { getMonitoringReviews } from "../api/adminMonitoring";

function StatusPill({ status }) {
  const styles = {
    PENDING: "bg-amber-50 text-amber-700",
    APPROVED: "bg-green-50 text-green-700",
    REJECTED: "bg-red-50 text-red-700",
  };

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
        styles[status] || "bg-slate-100 text-slate-600"
      }`}
    >
      {status}
    </span>
  );
}

function formatDate(value) {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  return date.toLocaleString();
}

export default function MonitoringReviews() {
  const [reviews, setReviews] = useState([]);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadReviews() {
    try {
      setLoading(true);
      setError("");

      const data = await getMonitoringReviews(
        filter || undefined
      );

      setReviews(
        Array.isArray(data)
          ? data
          : []
      );
    } catch (err) {
      setError(
        err.message ||
          "Could not load monitoring reviews."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReviews();
  }, [filter]);

  return (
    <div className="flex flex-col gap-6">
      {/* Page Header */}
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          Monitoring Reviews
        </h1>

        <p className="mt-1.5 text-slate-600">
          Review changes detected in official exam
          notifications before they are published.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {[
          ["", "All"],
          ["PENDING", "Pending"],
          ["APPROVED", "Approved"],
          ["REJECTED", "Rejected"],
        ].map(([value, label]) => (
          <button
            key={value || "all"}
            type="button"
            onClick={() => setFilter(value)}
            className={`rounded-xl px-4 py-2 text-sm font-medium transition ${
              filter === value
                ? "bg-ink text-white"
                : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Loading */}
      {loading ? (
        <Card>
          <p className="text-sm text-slate-500">
            Loading monitoring reviews...
          </p>
        </Card>
      ) : reviews.length === 0 ? (
        /* Empty State */
        <Card>
          <div className="py-8 text-center">
            <h2 className="font-display text-lg font-semibold text-ink">
              No monitoring reviews
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              No document changes have been queued
              for review.
            </p>
          </div>
        </Card>
      ) : (
        /* Review List */
        <div className="flex flex-col gap-4">
          {reviews.map((review) => (
            <Card key={review.review_id}>
              <div className="flex flex-col gap-5">
                {/* Review Header */}
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <div className="flex flex-wrap items-center gap-3">
                      <h2 className="font-display text-lg font-semibold text-ink">
                        {review.exam_name}
                      </h2>

                      <StatusPill
                        status={review.review_status}
                      />
                    </div>

                    <p className="mt-1 text-sm text-slate-500">
                      Notification #{review.notification_id}

                      {review.notification_title
                        ? ` • ${review.notification_title}`
                        : ""}
                    </p>
                  </div>

                  {/* FIXED VIEW CHANGES LINK */}
                  <Link
                    to={`/admin/monitoring/reviews/${review.review_id}`}
                    className="rounded-xl bg-ink px-4 py-2 text-center text-sm font-medium text-white hover:bg-slate-800"
                  >
                    View Changes
                  </Link>
                </div>

                {/* Review Metadata */}
                <div className="grid gap-4 border-t border-slate-100 pt-4 md:grid-cols-4">
                  {/* Changes */}
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      Changes
                    </p>

                    <p className="mt-1 text-sm font-semibold text-ink">
                      {review.change_count ?? "—"}
                    </p>
                  </div>

                  {/* Human Review */}
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      Human Review
                    </p>

                    <p className="mt-1 text-sm font-semibold text-ink">
                      {review.requires_human_review === true
                        ? "Required"
                        : review.requires_human_review === false
                        ? "Not required"
                        : "—"}
                    </p>
                  </div>

                  {/* Eligibility */}
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      Eligibility
                    </p>

                    <p className="mt-1 text-sm font-semibold text-ink">
                      {review.requires_eligibility_re_evaluation ===
                      true
                        ? "Re-evaluation required"
                        : review.requires_eligibility_re_evaluation ===
                          false
                        ? "No re-evaluation"
                        : "—"}
                    </p>
                  </div>

                  {/* Detection Date */}
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      Detected
                    </p>

                    <p className="mt-1 text-sm text-slate-600">
                      {formatDate(review.created_at)}
                    </p>
                  </div>
                </div>

                {/* AI Summary */}
                {review.semantic_summary && (
                  <div className="rounded-xl bg-slate-50 px-4 py-3">
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      AI Summary
                    </p>

                    <p className="mt-1 text-sm leading-6 text-slate-700">
                      {review.semantic_summary}
                    </p>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}