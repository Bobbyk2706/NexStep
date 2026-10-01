import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import StatusBadge from "../components/StatusBadge";
import { getDashboardStats } from "../api/adminExtractions";
import { runMonitoring } from "../api/adminMonitoring";
import { formatDate } from "../../utils/date";

function StatCard({ label, value, accent }) {
  return (
    <Card className="flex flex-col gap-1">
      <p className="text-sm text-slate-500">{label}</p>
      <p className={`font-display text-3xl font-semibold ${accent || "text-ink"}`}>
        {value}
      </p>
    </Card>
  );
}

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  const [monitoringRunning, setMonitoringRunning] = useState(false);
  const [monitoringResult, setMonitoringResult] = useState(null);
  const [monitoringError, setMonitoringError] = useState("");

  useEffect(() => {
    getDashboardStats()
      .then(setStats)
      .catch((err) =>
        setError(err.message || "Could not load dashboard data.")
      );
  }, []);

  async function handleRunMonitoring() {
    setMonitoringRunning(true);
    setMonitoringError("");
    setMonitoringResult(null);

    try {
      const response = await runMonitoring();

      setMonitoringResult(response?.result || response);
    } catch (err) {
      setMonitoringError(
        err.message || "Could not run the monitoring cycle."
      );
    } finally {
      setMonitoringRunning(false);
    }
  }

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          Admin Dashboard
        </h1>
        <p className="mt-1.5 text-slate-600">
          Overview of the exam ingestion and extraction review pipeline.
        </p>
      </div>

      {error && (
        <p className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard
          label="Pending Reviews"
          value={stats?.pendingReviews ?? "—"}
          accent="text-amber-600"
        />
        <StatCard
          label="Approved Extractions"
          value={stats?.approvedExams ?? "—"}
          accent="text-signal-600"
        />
        <StatCard
          label="Rejected Extractions"
          value={stats?.rejectedExtractions ?? "—"}
          accent="text-red-600"
        />
        <StatCard
          label="Failed Extractions"
          value={stats?.failedExtractions ?? "—"}
          accent="text-red-700"
        />
      </div>

      {/* Monitoring */}
      <Card>
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="font-display text-base font-semibold text-ink">
              Official Notification Monitoring
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Check approved exam notifications for changes in their official
              documents.
            </p>
          </div>

          <button
            type="button"
            onClick={handleRunMonitoring}
            disabled={monitoringRunning}
            className="rounded-xl bg-ink px-4 py-2.5 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {monitoringRunning ? "Running Monitoring..." : "Run Monitoring"}
          </button>
        </div>

        {monitoringError && (
          <div className="mt-4 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">
            {monitoringError}
          </div>
        )}

        {monitoringResult && (
          <div className="mt-5 rounded-xl border border-slate-100 bg-slate-50 p-4">
            <p className="mb-3 text-sm font-semibold text-ink">
              Monitoring completed
            </p>

            <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
              <div>
                <p className="text-xs text-slate-500">
                  Notifications Found
                </p>
                <p className="mt-1 text-lg font-semibold text-ink">
                  {monitoringResult.notifications_found ?? 0}
                </p>
              </div>

              <div>
                <p className="text-xs text-slate-500">
                  Notifications Processed
                </p>
                <p className="mt-1 text-lg font-semibold text-ink">
                  {monitoringResult.notifications_processed ?? 0}
                </p>
              </div>

              <div>
                <p className="text-xs text-slate-500">Successful</p>
                <p className="mt-1 text-lg font-semibold text-signal-600">
                  {monitoringResult.successful ?? 0}
                </p>
              </div>

              <div>
                <p className="text-xs text-slate-500">Failed</p>
                <p className="mt-1 text-lg font-semibold text-red-600">
                  {monitoringResult.failed ?? 0}
                </p>
              </div>
            </div>

            {Array.isArray(monitoringResult.results) &&
              monitoringResult.results.length > 0 && (
                <div className="mt-5">
                  <p className="mb-2 text-sm font-medium text-ink">
                    Notification Results
                  </p>

                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                      <thead>
                        <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400">
                          <th className="pb-2 font-medium">
                            Notification ID
                          </th>
                          <th className="pb-2 font-medium">
                            Monitoring Status
                          </th>
                          <th className="pb-2 font-medium">
                            Result
                          </th>
                        </tr>
                      </thead>

                      <tbody>
                        {monitoringResult.results.map((item) => (
                          <tr
                            key={item.notification_id}
                            className="border-b border-slate-100 last:border-none"
                          >
                            <td className="py-3 font-medium text-ink">
                              {item.notification_id}
                            </td>

                            <td className="py-3">
                              <span
                                className={
                                  item.status === "SUCCESS"
                                    ? "rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700"
                                    : "rounded-full bg-red-50 px-2.5 py-1 text-xs font-medium text-red-700"
                                }
                              >
                                {item.status}
                              </span>
                            </td>

                            <td className="py-3 text-slate-500">
                              {item.result?.status ||
                                item.error ||
                                "Completed"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
          </div>
        )}
      </Card>

      <Card>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-display text-base font-semibold text-ink">
            Recent activity
          </h2>

          <Link
            to="/admin/extractions"
            className="text-sm font-medium text-gold hover:underline"
          >
            View all
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
                <th className="pb-2 font-medium">Exam</th>
                <th className="pb-2 font-medium">Version</th>
                <th className="pb-2 font-medium">Status</th>
                <th className="pb-2 font-medium">Date</th>
                <th className="pb-2 font-medium text-right">Action</th>
              </tr>
            </thead>

            <tbody>
              {stats?.recent?.map((row) => (
                <tr
                  key={row.id}
                  className="border-b border-slate-50 last:border-none"
                >
                  <td className="py-3 font-medium text-ink">
                    {row.examName}
                  </td>

                  <td className="py-3 text-slate-500">
                    {row.version}
                  </td>

                  <td className="py-3">
                    <StatusBadge status={row.status} size="sm" />
                  </td>

                  <td className="py-3 text-slate-500">
                    {formatDate(row.createdDate)}
                  </td>

                  <td className="py-3 text-right">
                    <Link
                      to={`/admin/extractions/${row.id}`}
                      className="font-medium text-gold hover:underline"
                    >
                      {row.status === "PENDING_REVIEW"
                        ? "Review"
                        : "View"}
                    </Link>
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