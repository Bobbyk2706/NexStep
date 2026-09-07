import { Link } from "react-router-dom";
import { ListChecks, Search, ArrowRight, CalendarClock } from "lucide-react";
import Card from "../components/ui/Card";
import EligibilityPill from "../components/ui/EligibilityPill";
import { useAuth } from "../context/AuthContext";
import { useProfile } from "../context/ProfileContext";
import { useNotifications } from "../context/NotificationsContext";
import { formatDate, daysUntil } from "../utils/date";

function StatCard({ label, value, accent }) {
  return (
    <Card className="flex flex-col gap-1">
      <p className="text-sm text-slate-500">{label}</p>
      <p className={`font-display text-3xl font-semibold ${accent || "text-ink"}`}>{value}</p>
    </Card>
  );
}

export default function Dashboard() {
  const { user } = useAuth();
  const { exams, eligibleExams, loading } = useProfile();
  const { notifications } = useNotifications();

  const upcoming = eligibleExams
    .filter((e) => daysUntil(e.applicationDeadline) !== null)
    .sort((a, b) => new Date(a.applicationDeadline) - new Date(b.applicationDeadline))
    .slice(0, 4);

  const recentNotifications = notifications.slice(0, 4);

  return (
    <div className="flex flex-col gap-8">
      <div>
        <p className="text-sm text-slate-500">Welcome back</p>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          {user?.name?.split(" ")[0] || "Student"}
        </h1>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Total exams tracked" value={loading ? "—" : exams.length} />
        <StatCard label="You're eligible for" value={loading ? "—" : eligibleExams.length} accent="text-signal-600" />
        <StatCard
          label="Closing within 14 days"
          value={loading ? "—" : eligibleExams.filter((e) => { const d = daysUntil(e.applicationDeadline); return d !== null && d >= 0 && d <= 14; }).length}
          accent="text-amber-600"
        />
        <StatCard label="Unread notifications" value={notifications.filter((n) => !n.read).length} />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-base font-semibold text-ink">Upcoming deadlines & exam dates</h2>
            <Link to="/upcoming" className="flex items-center gap-1 text-sm font-medium text-indigo-700 hover:underline">
              View all <ArrowRight size={14} />
            </Link>
          </div>
          <div className="flex flex-col divide-y divide-slate-100">
            {upcoming.length === 0 && !loading && (
              <p className="py-4 text-sm text-slate-400">No upcoming deadlines among your eligible exams yet.</p>
            )}
            {upcoming.map((exam) => (
              <Link
                key={exam.id}
                to={`/exams/${exam.id}`}
                className="flex items-center justify-between gap-4 py-3.5 first:pt-0 last:pb-0 hover:opacity-80"
              >
                <div className="min-w-0">
                  <p className="truncate font-medium text-ink">{exam.name}</p>
                  <p className="truncate text-xs text-slate-500">
                    Applications close {formatDate(exam.applicationDeadline)} · Exam on {formatDate(exam.examDate)}
                  </p>
                </div>
                <EligibilityPill eligible={exam.eligible} deadline={exam.applicationDeadline} size="sm" />
              </Link>
            ))}
          </div>
        </Card>

        <Card>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-display text-base font-semibold text-ink">Recent notifications</h2>
            <Link to="/notifications" className="flex items-center gap-1 text-sm font-medium text-indigo-700 hover:underline">
              View all <ArrowRight size={14} />
            </Link>
          </div>
          <div className="flex flex-col divide-y divide-slate-100">
            {recentNotifications.length === 0 && <p className="py-4 text-sm text-slate-400">You're all caught up.</p>}
            {recentNotifications.map((n) => (
              <div key={n.id} className="flex items-start gap-2.5 py-3 first:pt-0 last:pb-0">
                <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${n.read ? "bg-slate-200" : "bg-indigo-600"}`} />
                <div className="min-w-0">
                  <p className="truncate text-sm font-medium text-ink">{n.title}</p>
                  <p className="truncate text-xs text-slate-500">{n.message}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Link to="/eligibility" className="group flex items-center gap-4 rounded-2xl border border-slate-200/70 bg-white p-5 shadow-card transition hover:border-indigo-200">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-700 text-white">
            <ListChecks size={18} />
          </div>
          <div>
            <p className="font-display font-semibold text-ink">See your eligibility results</p>
            <p className="text-sm text-slate-500">Every exam, checked against your profile.</p>
          </div>
          <ArrowRight size={16} className="ml-auto shrink-0 text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-indigo-600" />
        </Link>
        <Link to="/search" className="group flex items-center gap-4 rounded-2xl border border-slate-200/70 bg-white p-5 shadow-card transition hover:border-indigo-200">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-700 text-white">
            <Search size={18} />
          </div>
          <div>
            <p className="font-display font-semibold text-ink">Browse all exams</p>
            <p className="text-sm text-slate-500">Search by name, organization, or category.</p>
          </div>
          <ArrowRight size={16} className="ml-auto shrink-0 text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-indigo-600" />
        </Link>
      </div>

      {eligibleExams.length === 0 && !loading && (
        <Card className="flex items-center gap-4 bg-indigo-50/50">
          <CalendarClock size={20} className="shrink-0 text-indigo-700" />
          <p className="text-sm text-slate-700">
            Nothing's matched yet — that updates automatically as exams are added or your profile changes.
          </p>
        </Card>
      )}
    </div>
  );
}
