import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import StatusBadge from "../components/StatusBadge";
import { getDashboardStats } from "../api/adminExtractions";
import { formatDate } from "../../utils/date";

function StatCard({ label, value, accent }) {
  return (
    <Card className="flex flex-col gap-1">
      <p className="text-sm text-slate-500">{label}</p>
      <p className={`font-display text-3xl font-semibold ${accent || "text-ink"}`}>{value}</p>
    </Card>
  );
}

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getDashboardStats().then(setStats);
  }, []);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Admin Dashboard</h1>
        <p className="mt-1.5 text-slate-600">Overview of the exam ingestion and extraction review pipeline.</p>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Pending Reviews" value={stats?.pendingReviews ?? "—"} accent="text-amber-600" />
        <StatCard label="Approved Exams" value={stats?.approvedExams ?? "—"} accent="text-signal-600" />
        <StatCard label="Rejected Extractions" value={stats?.rejectedExtractions ?? "—"} accent="text-red-600" />
        <StatCard label="Failed Extractions" value={stats?.failedExtractions ?? "—"} accent="text-red-700" />
      </div>

      <Card>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-display text-base font-semibold text-ink">Recent activity</h2>
          <Link to="/admin/extractions" className="text-sm font-medium text-gold hover:underline">
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
              {stats?.recent.map((row) => (
                <tr key={row.id} className="border-b border-slate-50 last:border-none">
                  <td className="py-3 font-medium text-ink">{row.examName}</td>
                  <td className="py-3 text-slate-500">{row.version}</td>
                  <td className="py-3"><StatusBadge status={row.status} size="sm" /></td>
                  <td className="py-3 text-slate-500">{formatDate(row.createdDate)}</td>
                  <td className="py-3 text-right">
                    <Link to={`/admin/extractions/${row.id}`} className="font-medium text-gold hover:underline">
                      {row.status === "PENDING_REVIEW" ? "Review" : "View"}
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
