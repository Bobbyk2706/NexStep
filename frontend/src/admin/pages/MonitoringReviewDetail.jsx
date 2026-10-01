import { useEffect, useState } from "react";
import {
  Link,
  useNavigate,
  useParams,
} from "react-router-dom";

import Card from "../../components/ui/Card";

import {
  getMonitoringReview,
  approveMonitoringReview,
  rejectMonitoringReview,
  applyMonitoringReview,
} from "../api/adminMonitoring";

function StatusPill({ status }) {
  const styles = {
    PENDING: "bg-amber-50 text-amber-700",
    APPROVED: "bg-green-50 text-green-700",
    REJECTED: "bg-red-50 text-red-700",
  };

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
        styles[status] ||
        "bg-slate-100 text-slate-600"
      }`}
    >
      {status}
    </span>
  );
}

function SectionTitle({ children }) {
  return (
    <h2 className="font-display text-lg font-semibold text-ink">
      {children}
    </h2>
  );
}

function HashBlock({ label, value }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 break-all rounded-lg bg-slate-50 px-3 py-2 font-mono text-xs text-slate-700">
        {value || "—"}
      </p>
    </div>
  );
}

function JsonValue({ value }) {
  if (
    value === null ||
    value === undefined
  ) {
    return (
      <span className="text-slate-400">
        —
      </span>
    );
  }

  if (
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean"
  ) {
    return (
      <span className="whitespace-pre-wrap text-sm text-slate-700">
        {String(value)}
      </span>
    );
  }

  return (
    <pre className="overflow-x-auto whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-xs leading-5 text-slate-700">
      {JSON.stringify(value, null, 2)}
    </pre>
  );
}

export default function MonitoringReviewDetail() {
  const { reviewId } = useParams();
  const navigate = useNavigate();

  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [rejectionReason, setRejectionReason] =
    useState("");

  async function loadReview() {
    try {
      setLoading(true);
      setError("");

      const data =
        await getMonitoringReview(reviewId);

      setReview(data);
    } catch (err) {
      setError(
        err.message ||
          "Could not load monitoring review."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReview();
  }, [reviewId]);

  async function handleApprove() {
    if (
      !window.confirm(
        "Approve this monitoring change?"
      )
    ) {
      return;
    }

    try {
      setBusy(true);
      setError("");

      await approveMonitoringReview(reviewId);

      await loadReview();
    } catch (err) {
      setError(
        err.message ||
          "Could not approve monitoring review."
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleReject() {
    const reason =
      rejectionReason.trim();

    if (!reason) {
      setError(
        "Please enter a rejection reason."
      );
      return;
    }

    try {
      setBusy(true);
      setError("");

      await rejectMonitoringReview(
        reviewId,
        reason
      );

      setRejectionReason("");

      await loadReview();
    } catch (err) {
      setError(
        err.message ||
          "Could not reject monitoring review."
      );
    } finally {
      setBusy(false);
    }
  }

  async function handleApply() {
    if (
      !window.confirm(
        "Publish this approved monitoring change into the authoritative exam data?"
      )
    ) {
      return;
    }

    try {
      setBusy(true);
      setError("");

      await applyMonitoringReview(reviewId);

      await loadReview();
    } catch (err) {
      setError(
        err.message ||
          "Could not apply monitoring review."
      );
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return (
      <Card>
        <p className="text-sm text-slate-500">
          Loading monitoring review...
        </p>
      </Card>
    );
  }

  if (!review) {
    return (
      <Card>
        <p className="text-sm text-red-600">
          {error ||
            "Monitoring review not found."}
        </p>
      </Card>
    );
  }

  const structuralChanges =
    review.structural_changes;

  const semanticAnalysis =
    review.semantic_analysis;

  const impactAnalysis =
    review.impact_analysis;

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div>
        <Link
          to="/admin/monitoring"
          className="text-sm font-medium text-gold hover:underline"
        >
          ← Back to Monitoring Reviews
        </Link>

        <div className="mt-4 flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
          <div>
            <div className="flex flex-wrap items-center gap-3">
              <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
                {review.exam_name}
              </h1>

              <StatusPill
                status={
                  review.review_status
                }
              />
            </div>

            <p className="mt-1.5 text-slate-600">
              Notification #
              {review.notification_id}

              {review.notification_title
                ? ` • ${review.notification_title}`
                : ""}
            </p>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Document Change */}
      <Card>
        <SectionTitle>
          Document Change
        </SectionTitle>

        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <HashBlock
            label="Previous document hash"
            value={
              review.old_document_hash
            }
          />

          <HashBlock
            label="New document hash"
            value={
              review.new_document_hash
            }
          />
        </div>

        {review.document_url && (
          <div className="mt-4">
            <p className="text-xs uppercase tracking-wide text-slate-400">
              Official document URL
            </p>

            <a
              href={review.document_url}
              target="_blank"
              rel="noreferrer"
              className="mt-1 block break-all text-sm text-gold hover:underline"
            >
              {review.document_url}
            </a>
          </div>
        )}
      </Card>

      {/* Structural Changes */}
      <Card>
        <SectionTitle>
          Structural Changes
        </SectionTitle>

        <div className="mt-4">
          {structuralChanges?.changes?.length ? (
            <div className="flex flex-col gap-4">
              {structuralChanges.changes.map(
                (change, index) => (
                  <div
                    key={
                      change.change_index ??
                      index
                    }
                    className="rounded-xl border border-slate-200 p-4"
                  >
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                        Change #
                        {change.change_index ??
                          index}
                      </span>

                      <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700">
                        {change.change_type}
                      </span>
                    </div>

                    <p className="mt-3 text-xs font-medium uppercase tracking-wide text-slate-400">
                      Path
                    </p>

                    <p className="mt-1 break-all font-mono text-xs text-slate-700">
                      {change.path}
                    </p>

                    <div className="mt-4 grid gap-4 md:grid-cols-2">
                      <div>
                        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                          Previous value
                        </p>

                        <JsonValue
                          value={
                            change.old_value
                          }
                        />
                      </div>

                      <div>
                        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                          New value
                        </p>

                        <JsonValue
                          value={
                            change.new_value
                          }
                        />
                      </div>
                    </div>
                  </div>
                )
              )}
            </div>
          ) : (
            <JsonValue
              value={structuralChanges}
            />
          )}
        </div>
      </Card>

      {/* AI Semantic Analysis */}
      <Card>
        <SectionTitle>
          AI Semantic Analysis
        </SectionTitle>

        {semanticAnalysis?.overall_summary && (
          <div className="mt-4 rounded-xl bg-slate-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
              Overall Summary
            </p>

            <p className="mt-1 text-sm leading-6 text-slate-700">
              {
                semanticAnalysis.overall_summary
              }
            </p>
          </div>
        )}

        <div className="mt-4 flex flex-col gap-4">
          {semanticAnalysis?.changes?.map(
            (change) => (
              <div
                key={
                  change.change_index
                }
                className="rounded-xl border border-slate-200 p-4"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
                    Change #
                    {change.change_index}
                  </span>

                  <span className="rounded-full bg-indigo-50 px-2.5 py-1 text-xs font-semibold text-indigo-700">
                    {change.confidence}
                  </span>

                  {change.requires_human_review && (
                    <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700">
                      Human review
                    </span>
                  )}
                </div>

                <h3 className="mt-3 font-semibold text-ink">
                  {change.summary}
                </h3>

                <p className="mt-2 text-sm text-slate-600">
                  <strong>
                    Affected requirement:
                  </strong>{" "}
                  {
                    change.affected_requirement
                  }
                </p>

                <p className="mt-2 text-sm text-slate-600">
                  <strong>
                    Potential impact:
                  </strong>{" "}
                  {change.impact}
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-700">
                  {change.explanation}
                </p>
              </div>
            )
          )}
        </div>
      </Card>

      {/* Impact Analysis */}
      <Card>
        <SectionTitle>
          Impact Analysis
        </SectionTitle>

        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <div className="rounded-xl bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-400">
              Human review
            </p>

            <p className="mt-1 font-semibold text-ink">
              {impactAnalysis?.overall_requires_human_review
                ? "Required"
                : "Not required"}
            </p>
          </div>

          <div className="rounded-xl bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-400">
              Eligibility re-evaluation
            </p>

            <p className="mt-1 font-semibold text-ink">
              {impactAnalysis?.overall_requires_eligibility_re_evaluation
                ? "Required"
                : "Not required"}
            </p>
          </div>
        </div>

        <div className="mt-4">
          <JsonValue
            value={impactAnalysis}
          />
        </div>
      </Card>

      {/* Pending Decision */}
      {review.review_status ===
        "PENDING" && (
        <Card>
          <SectionTitle>
            Administrator Decision
          </SectionTitle>

          <div className="mt-4 flex flex-col gap-4">
            {/* Approve */}
            <button
              type="button"
              disabled={busy}
              onClick={handleApprove}
              className="rounded-xl bg-green-700 px-4 py-3 text-sm font-semibold text-white hover:bg-green-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {busy
                ? "Processing..."
                : "Approve Change"}
            </button>

            {/* Reject */}
            <div className="border-t border-slate-100 pt-4">
              <label className="text-sm font-medium text-ink">
                Rejection reason
              </label>

              <textarea
                value={rejectionReason}
                onChange={(event) =>
                  setRejectionReason(
                    event.target.value
                  )
                }
                rows={4}
                placeholder="Explain why this detected change should be rejected..."
                className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-slate-400"
              />

              <button
                type="button"
                disabled={busy}
                onClick={handleReject}
                className="mt-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700 hover:bg-red-100 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {busy
                  ? "Processing..."
                  : "Reject Change"}
              </button>
            </div>
          </div>
        </Card>
      )}

      {/* Approved */}
      {review.review_status ===
        "APPROVED" && (
        <Card>
          <SectionTitle>
            Publish Approved Change
          </SectionTitle>

          <p className="mt-2 text-sm leading-6 text-slate-600">
            The administrator has approved this
            monitoring review. Publishing will update
            the authoritative exam notification and
            persist the newly extracted information.
          </p>

          <button
            type="button"
            disabled={busy}
            onClick={handleApply}
            className="mt-4 rounded-xl bg-ink px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {busy
              ? "Publishing..."
              : "Apply & Publish Change"}
          </button>
        </Card>
      )}

      {/* Rejected */}
      {review.review_status ===
        "REJECTED" &&
        review.rejection_reason && (
          <Card>
            <SectionTitle>
              Rejection Reason
            </SectionTitle>

            <p className="mt-3 rounded-xl bg-red-50 p-4 text-sm leading-6 text-red-700">
              {review.rejection_reason}
            </p>
          </Card>
        )}
    </div>
  );
}