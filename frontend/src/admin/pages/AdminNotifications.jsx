import { useCallback, useEffect, useState } from "react";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import { formatDate } from "../../utils/date";
import {
  getNotificationLog,
  getNotificationSummary,
  retryNotificationEmail,
  runDeadlineReminders,
} from "../api/adminNotifications";

const FILTERS = [
  ["", "All"],
  ["SENT", "Sent"],
  ["FAILED", "Failed"],
  ["SKIPPED", "Skipped"],
  ["PENDING", "Pending"],
];

const TYPE_LABEL = {
  NEW_ELIGIBLE_EXAM: "New eligible exam",
  EXAM_UPDATED: "Exam updated",
  DEADLINE_REMINDER: "Deadline reminder",
  ELIGIBILITY_CHANGED: "Eligibility changed",
};

const STATUS_STYLE = {
  SENT: "text-signal-600 bg-signal-50",
  FAILED: "text-red-600 bg-red-50",
  SKIPPED: "text-amber-600 bg-amber-50",
  PENDING: "text-slate-500 bg-slate-100",
};

function StatCard({ label, value, accent = "text-ink" }) {
  return (
    <Card>
      <p className="text-xs uppercase tracking-wide text-slate-400">{label}</p>
      <p className={`mt-1 font-display text-2xl font-semibold ${accent}`}>{value ?? "—"}</p>
    </Card>
  );
}

export default function AdminNotifications() {
  const [rows, setRows] = useState([]);
  const [summary, setSummary] = useState(null);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busyId, setBusyId] = useState(null);
  const [running, setRunning] = useState(false);

  const load = useCallback(async (emailStatus) => {
    setLoading(true);
    setError("");

    try {
      const [log, stats] = await Promise.all([
        getNotificationLog({ emailStatus }),
        getNotificationSummary(),
      ]);
      setRows(log);
      setSummary(stats);
    } catch (err) {
      setError(err?.message || "Could not load notifications.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load(filter);
  }, [filter, load]);

  async function handleRetry(id) {
    setBusyId(id);
    setError("");
    setNotice("");

    try {
      const result = await retryNotificationEmail(id);
      setNotice(`Email status is now ${result?.email_status || "updated"}.`);
      await load(filter);
    } catch (err) {
      setError(err?.message || "Could not retry the email.");
    } finally {
      setBusyId(null);
    }
  }

  async function handleRunReminders() {
    setRunning(true);
    setError("");
    setNotice("");

    try {
      const result = await runDeadlineReminders();
      setNotice(`Deadline reminders ran: ${result?.created ?? 0} new notification(s) created.`);
      await load(filter);
    } catch (err) {
      setError(err?.message || "Could not run deadline reminders.");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
            Notifications
          </h1>
          <p className="mt-1.5 max-w-xl text-slate-600">
            Every notification sent to students, with its email delivery status. Retry any email
            that failed or was skipped.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" className="text-sm" onClick={() => load(filter)}>
            Refresh
          </Button>
          <Button
            variant="secondary"
            className="text-sm"
            loading={running}
            onClick={handleRunReminders}
          >
            Run deadline reminders now
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Total" value={summary?.total} />
        <StatCard label="Emails sent" value={summary?.sent} accent="text-signal-600" />
        <StatCard label="Failed" value={summary?.failed} accent="text-red-600" />
        <StatCard label="Skipped" value={summary?.skipped} accent="text-amber-600" />
      </div>

      {error && (
        <p className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
          {error}
        </p>
      )}
      {notice && (
        <p className="rounded-xl bg-signal-50 px-3.5 py-2.5 text-sm text-signal-600 ring-1 ring-inset ring-slate-200">
          {notice}
        </p>
      )}

      <Card>
        <div className="mb-4 flex flex-wrap gap-2">
          {FILTERS.map(([value, label]) => (
            <button
              key={value || "all"}
              onClick={() => setFilter(value)}
              className={`rounded-full px-3 py-1 text-xs font-medium ${
                filter === value
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
                <th className="pb-2 font-medium">Student</th>
                <th className="pb-2 font-medium">Notification</th>
                <th className="pb-2 font-medium">Email</th>
                <th className="pb-2 font-medium">Date</th>
                <th className="pb-2 font-medium" />
              </tr>
            </thead>
            <tbody>
              {!loading && rows.length === 0 && (
                <tr>
                  <td colSpan={5} className="py-6 text-center text-sm text-slate-400">
                    No notifications match this view.
                  </td>
                </tr>
              )}
              {rows.map((row) => (
                <tr key={row.id} className="border-b border-slate-50 align-top last:border-none">
                  <td className="py-3 pr-3">
                    <p className="font-medium text-ink">{row.studentName}</p>
                    <p className="text-xs text-slate-400">{row.studentEmail}</p>
                  </td>
                  <td className="max-w-md py-3 pr-3">
                    <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                      {TYPE_LABEL[row.type] || row.type}
                    </p>
                    <p className="font-medium text-ink">{row.title}</p>
                    <p className="mt-0.5 text-slate-500">{row.message}</p>
                  </td>
                  <td className="py-3 pr-3">
                    {row.emailStatus ? (
                      <span
                        className={`rounded-full px-2.5 py-1 font-mono text-[11px] uppercase tracking-wide ${
                          STATUS_STYLE[row.emailStatus] || STATUS_STYLE.PENDING
                        }`}
                      >
                        {row.emailStatus}
                      </span>
                    ) : (
                      <span className="text-xs text-slate-400">In-app only</span>
                    )}
                    {row.emailError && (
                      <p className="mt-1 max-w-[14rem] text-xs text-slate-400">{row.emailError}</p>
                    )}
                  </td>
                  <td className="py-3 pr-3 text-slate-500">
                    {row.createdAt ? formatDate(row.createdAt) : "—"}
                  </td>
                  <td className="py-3 text-right">
                    {(row.emailStatus === "FAILED" || row.emailStatus === "SKIPPED") && (
                      <button
                        disabled={busyId === row.id}
                        onClick={() => handleRetry(row.id)}
                        className="text-sm font-medium text-gold hover:underline disabled:opacity-50"
                      >
                        {busyId === row.id ? "Retrying…" : "Retry email"}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}