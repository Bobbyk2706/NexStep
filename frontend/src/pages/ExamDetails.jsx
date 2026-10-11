import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, ExternalLink, CheckCircle2, Info } from "lucide-react";
import Card from "../components/ui/Card";
import EligibilityPill from "../components/ui/EligibilityPill";
import * as examsApi from "../api/exams";
import { formatDate } from "../utils/date";

// "Age 21 to 32" / "Minimum age 21" / "Maximum age 32", or null.
function ageText(info) {
  const { minimum_age: min, maximum_age: max } = info || {};

  if (min != null && max != null) return `${min} to ${max} years`;
  if (min != null) return `At least ${min} years`;
  if (max != null) return `Up to ${max} years`;

  return null;
}

function EligibilityDetails({ info, officialUrl }) {
  if (!info) return null;

  const rows = [
    ["Age", ageText(info)],
    ["Qualification", info.educational_qualification],
    ["Nationality", info.nationality],
    ["Work experience", info.work_experience],
  ].filter(([, value]) => value);

  const other = info.other_requirements || [];

  if (info.not_available && rows.length === 0 && other.length === 0) {
    return (
      <Card className="flex items-start gap-3">
        <Info size={18} className="mt-0.5 shrink-0 text-slate-400" />
        <div>
          <p className="font-medium text-ink">Eligibility is not stated in the notification</p>
          <p className="mt-1 text-sm text-slate-500">
            Please read the official notification before applying.
            {officialUrl && (
              <>
                {" "}
                <a href={officialUrl} target="_blank" rel="noreferrer" className="font-medium text-gold hover:underline">
                  Open official notification
                </a>
              </>
            )}
          </p>
        </div>
      </Card>
    );
  }

  if (rows.length === 0 && other.length === 0) return null;

  return (
    <Card>
      <h2 className="font-display text-base font-semibold text-ink">Eligibility from the official notification</h2>

      {rows.length > 0 && (
        <dl className="mt-3 grid gap-3 sm:grid-cols-2">
          {rows.map(([label, value]) => (
            <div key={label}>
              <dt className="text-xs uppercase tracking-wide text-slate-400">{label}</dt>
              <dd className="mt-0.5 text-sm text-ink">{value}</dd>
            </div>
          ))}
        </dl>
      )}

      {other.length > 0 && (
        <ul className="mt-4 flex list-disc flex-col gap-1.5 pl-5 text-sm text-slate-600">
          {other.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}

      <p className="mt-4 text-xs text-slate-400">
        Always confirm against the official notification before you apply.
      </p>
    </Card>
  );
}

function firstExamDate(notification) {
  const dates = notification?.exam_dates || [];
  if (dates.length === 0) return null;

  return [...dates].sort(
    (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
  )[0]?.start_date || null;
}

export default function ExamDetails() {
  const { id } = useParams();
  const [exam, setExam] = useState(undefined);
  const [eligibility, setEligibility] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setExam(undefined);
    setEligibility(null);
    setError("");

    Promise.allSettled([
      examsApi.getExamById(id),
      examsApi.evaluateEligibility(id),
    ]).then(([examResult, eligibilityResult]) => {
      if (!active) return;

      if (examResult.status === "fulfilled") {
        setExam(examResult.value);
      } else {
        setExam(null);
        setError(examResult.reason?.message || "Could not load this exam.");
      }

      if (eligibilityResult.status === "fulfilled") {
        setEligibility(eligibilityResult.value);
      }
    });

    return () => {
      active = false;
    };
  }, [id]);

  if (exam === undefined) {
    return <p className="text-sm text-slate-400">Loading exam details...</p>;
  }

  if (exam === null) {
    return (
      <Card>
        <p className="text-sm text-slate-500">We couldn't find that exam.</p>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
        <Link to="/eligibility" className="mt-3 inline-block text-sm font-medium text-gold hover:underline">
          Back to eligibility results
        </Link>
      </Card>
    );
  }

  const notification = exam.latest_approved_notification;
  const eligible = eligibility?.eligibility_status === "ELIGIBLE";
  const unknown = eligibility?.eligibility_status === "UNKNOWN";
  const reason = eligibility?.reason || "No eligibility result is available.";
  const examDate = firstExamDate(notification);

  return (
    <div className="flex flex-col gap-6">
      <Link to="/eligibility" className="flex w-fit items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-ink">
        <ArrowLeft size={15} /> Back to eligibility results
      </Link>

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">{exam.name}</h1>
          <p className="mt-1 text-slate-500">{exam.conducting_body?.name || "—"} · {exam.type || "Exam"}</p>
        </div>
        <EligibilityPill
          eligible={eligible}
          unknown={unknown}
          deadline={notification?.application_end_date}
        />
      </div>

      <Card className="flex items-start gap-3">
        {unknown ? (
          <Info size={18} className="mt-0.5 shrink-0 text-slate-400" />
        ) : (
          <CheckCircle2 size={18} className={`mt-0.5 shrink-0 ${eligible ? "text-signal-500" : "text-slate-400"}`} />
        )}
        <div>
          <p className="font-medium text-ink">
            {unknown ? "Check the official notification" : eligible ? "You're eligible" : "You're not eligible — yet"}
          </p>
          <p className="mt-1 whitespace-pre-line text-sm text-slate-500">{reason}</p>
        </div>
      </Card>

      <EligibilityDetails info={exam.eligibility_info} officialUrl={notification?.official_url} />

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <p className="text-xs uppercase tracking-wide text-slate-400">Application opens</p>
          <p className="mt-1.5 font-mono text-sm text-ink">{formatDate(notification?.application_start_date)}</p>
        </Card>
        <Card>
          <p className="text-xs uppercase tracking-wide text-slate-400">Application deadline</p>
          <p className="mt-1.5 font-mono text-sm text-ink">{formatDate(notification?.application_end_date)}</p>
        </Card>
        <Card>
          <p className="text-xs uppercase tracking-wide text-slate-400">Exam date</p>
          <p className="mt-1.5 font-mono text-sm text-ink">{formatDate(examDate)}</p>
        </Card>
      </div>

      {exam.description && (
        <Card>
          <h2 className="font-display text-base font-semibold text-ink">About this exam</h2>
          <p className="mt-3 text-sm leading-6 text-slate-600">{exam.description}</p>
        </Card>
      )}

      {notification?.ai_summary && (
        <Card>
          <h2 className="font-display text-base font-semibold text-ink">Latest official notification</h2>
          <p className="mt-1 text-sm font-medium text-ink">{notification.title}</p>
          <p className="mt-3 text-sm leading-6 text-slate-600">{notification.ai_summary}</p>
        </Card>
      )}

      {notification?.exam_dates?.length > 0 && (
        <Card>
          <h2 className="font-display text-base font-semibold text-ink">All examination dates</h2>
          <ul className="mt-3 flex flex-col gap-2">
            {notification.exam_dates.map((dateRange) => (
              <li key={`${dateRange.exam_date_id}-${dateRange.start_date}`} className="text-sm text-slate-600">
                {formatDate(dateRange.start_date)}
                {dateRange.end_date && dateRange.end_date !== dateRange.start_date
                  ? ` – ${formatDate(dateRange.end_date)}`
                  : ""}
              </li>
            ))}
          </ul>
        </Card>
      )}

      {(notification?.official_url || exam.off_exam_page) && (
        <a
          href={notification?.official_url || exam.off_exam_page}
          target="_blank"
          rel="noreferrer"
          className="flex w-fit items-center gap-2 rounded-xl bg-indigo-700 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-600"
        >
          Visit official website <ExternalLink size={15} />
        </a>
      )}
    </div>
  );
}

