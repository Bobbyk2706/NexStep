import { Link } from "react-router-dom";
import { CalendarClock, BellRing, Sparkles, Info } from "lucide-react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import { useNotifications } from "../context/NotificationsContext";
import { timeAgo } from "../utils/date";

const TYPE_META = {
  deadline: { icon: CalendarClock, color: "text-amber-600 bg-amber-50" },
  exam: { icon: BellRing, color: "text-indigo-700 bg-indigo-50" },
  "new-eligible": { icon: Sparkles, color: "text-signal-600 bg-signal-50" },
  update: { icon: Info, color: "text-slate-500 bg-slate-50" },
};

export default function Notifications() {
  const { notifications, markRead, markAllRead } = useNotifications();

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Notifications</h1>
          <p className="mt-1.5 text-slate-600">Deadlines, new matches, and updates to exams you're tracking.</p>
        </div>
        {notifications.some((n) => !n.read) && (
          <Button variant="secondary" className="text-sm" onClick={markAllRead}>
            Mark all as read
          </Button>
        )}
      </div>

      <div className="flex flex-col gap-3">
        {notifications.length === 0 && (
          <Card>
            <p className="text-sm text-slate-500">You're all caught up — nothing here yet.</p>
          </Card>
        )}
        {notifications.map((n) => {
          const meta = TYPE_META[n.type] || TYPE_META.update;
          const Icon = meta.icon;
          return (
            <Card
              key={n.id}
              className={`flex items-start gap-4 ${!n.read ? "ring-1 ring-inset ring-indigo-100" : ""}`}
            >
              <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${meta.color}`}>
                <Icon size={16} />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-start justify-between gap-3">
                  <p className="font-medium text-ink">{n.title}</p>
                  <span className="shrink-0 text-xs text-slate-400">{timeAgo(n.timestamp)}</span>
                </div>
                <p className="mt-1 text-sm text-slate-500">{n.message}</p>
                <div className="mt-2.5 flex items-center gap-4">
                  {n.examId && (
                    <Link to={`/exams/${n.examId}`} className="text-sm font-medium text-indigo-700 hover:underline">
                      View exam
                    </Link>
                  )}
                  {!n.read && (
                    <button onClick={() => markRead(n.id)} className="text-sm font-medium text-slate-400 hover:text-ink">
                      Mark as read
                    </button>
                  )}
                </div>
              </div>
              {!n.read && <span className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-indigo-600" />}
            </Card>
          );
        })}
      </div>
    </div>
  );
}
