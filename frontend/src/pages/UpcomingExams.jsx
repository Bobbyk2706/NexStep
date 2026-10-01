import { Link } from "react-router-dom";
import { useProfile } from "../context/ProfileContext";
import EligibilityPill from "../components/ui/EligibilityPill";
import Card from "../components/ui/Card";
import { formatDate, daysUntil } from "../utils/date";

function getLatestNotification(exam) {
  return exam.latest_approved_notification || null;
}

function getApplicationDeadline(exam) {
  return getLatestNotification(exam)?.application_end_date || null;
}

function getExamDate(exam) {
  const dates = getLatestNotification(exam)?.exam_dates || [];

  if (dates.length === 0) {
    return null;
  }

  return [...dates]
    .sort(
      (a, b) =>
        new Date(a.start_date).getTime() -
        new Date(b.start_date).getTime()
    )[0]?.start_date || null;
}

export default function UpcomingExams() {
  const { eligibleExams, loading } = useProfile();

  const timeline = eligibleExams
    .flatMap((exam) => [
      {
        exam,
        label: "Application deadline",
        date: getApplicationDeadline(exam),
      },
      {
        exam,
        label: "Exam date",
        date: getExamDate(exam),
      },
    ])
    .filter((item) => {
      if (!item.date) return false;

      const days = daysUntil(item.date);
      return days === null || days >= -1;
    })
    .sort(
      (a, b) =>
        new Date(a.date).getTime() - new Date(b.date).getTime()
    );

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          Upcoming deadlines & exams
        </h1>

        <p className="mt-1.5 text-slate-600">
          Everything you're eligible for, in the order it happens.
        </p>
      </div>

      {loading && (
        <p className="text-sm text-slate-400">
          Loading your timeline...
        </p>
      )}

      {!loading && timeline.length === 0 && (
        <Card>
          <p className="text-sm text-slate-500">
            Nothing eligible on your timeline right now. Check{" "}
            <Link
              to="/eligibility"
              className="font-medium text-gold hover:underline"
            >
              eligibility results
            </Link>{" "}
            as your profile updates.
          </p>
        </Card>
      )}

      <div className="relative flex flex-col">
        {timeline.length > 0 && (
          <div className="absolute bottom-2 left-[7px] top-2 w-px step-line" />
        )}

        {timeline.map((item, index) => {
          const deadline = getApplicationDeadline(item.exam);

          return (
            <div
              key={`${item.exam.exam_id}-${item.label}-${index}`}
              className="relative flex gap-4 pb-6 last:pb-0"
            >
              <span className="relative z-10 mt-1.5 h-3.5 w-3.5 shrink-0 rounded-full border-2 border-white bg-indigo-600 ring-4 ring-paper" />

              <Card className="flex-1">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-400">
                      {item.label}
                    </p>

                    <p className="mt-0.5 font-mono text-sm font-medium text-ink">
                      {formatDate(item.date)}
                    </p>
                  </div>

                  <EligibilityPill
                    eligible={item.exam.eligible}
                    deadline={deadline}
                    size="sm"
                  />
                </div>

                <Link
                  to={`/exams/${item.exam.exam_id}`}
                  className="mt-3 block font-display font-semibold text-ink hover:text-gold"
                >
                  {item.exam.name}
                </Link>

                <p className="text-sm text-slate-500">
                  {item.exam.conducting_body?.name || "—"}
                </p>
              </Card>
            </div>
          );
        })}
      </div>
    </div>
  );
}