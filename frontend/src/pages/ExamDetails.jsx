import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, ExternalLink, CheckCircle2 } from "lucide-react";
import Card from "../components/ui/Card";
import EligibilityPill from "../components/ui/EligibilityPill";
import { useProfile } from "../context/ProfileContext";
import * as examsApi from "../api/exams";
import { formatDate } from "../utils/date";

export default function ExamDetails() {
  const { id } = useParams();
  const { profile } = useProfile();
  const [exam, setExam] = useState(undefined); // undefined = loading, null = not found

  useEffect(() => {
    let active = true;
    setExam(undefined);
    examsApi.getExamById(id, profile).then((data) => {
      if (active) setExam(data);
    });
    return () => {
      active = false;
    };
  }, [id, profile]);

  if (exam === undefined) {
    return <p className="text-sm text-slate-400">Loading exam details...</p>;
  }

  if (exam === null) {
    return (
      <Card>
        <p className="text-sm text-slate-500">We couldn't find that exam.</p>
        <Link to="/eligibility" className="mt-3 inline-block text-sm font-medium text-indigo-700 hover:underline">
          Back to eligibility results
        </Link>
      </Card>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <Link to="/eligibility" className="flex w-fit items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-ink">
        <ArrowLeft size={15} /> Back to eligibility results
      </Link>

      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">{exam.name}</h1>
          <p className="mt-1 text-slate-500">{exam.organization} · {exam.category}</p>
        </div>
        <EligibilityPill eligible={exam.eligible} deadline={exam.applicationDeadline} />
      </div>

      <Card className="flex items-start gap-3">
        <CheckCircle2 size={18} className={`mt-0.5 shrink-0 ${exam.eligible ? "text-signal-500" : "text-slate-400"}`} />
        <div>
          <p className="font-medium text-ink">{exam.eligible ? "You're eligible" : "You're not eligible — yet"}</p>
          <p className="mt-1 text-sm text-slate-500">{exam.reason}</p>
          <p className="mt-2 text-xs text-slate-400">Eligibility rule: {exam.eligibilityRule}</p>
        </div>
      </Card>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <p className="text-xs uppercase tracking-wide text-slate-400">Application opens</p>
          <p className="mt-1.5 font-mono text-sm text-ink">{formatDate(exam.applicationStart)}</p>
        </Card>
        <Card>
          <p className="text-xs uppercase tracking-wide text-slate-400">Application deadline</p>
          <p className="mt-1.5 font-mono text-sm text-ink">{formatDate(exam.applicationDeadline)}</p>
        </Card>
        <Card>
          <p className="text-xs uppercase tracking-wide text-slate-400">Exam date</p>
          <p className="mt-1.5 font-mono text-sm text-ink">{formatDate(exam.examDate)}</p>
        </Card>
      </div>

      <Card>
        <h2 className="font-display text-base font-semibold text-ink">Syllabus</h2>
        <ul className="mt-3 flex flex-col gap-2">
          {exam.syllabus.map((item) => (
            <li key={item} className="flex items-start gap-2.5 text-sm text-slate-600">
              <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-indigo-400" />
              {item}
            </li>
          ))}
        </ul>
      </Card>

      <Card>
        <h2 className="font-display text-base font-semibold text-ink">Important information</h2>
        <ul className="mt-3 flex flex-col gap-2">
          {exam.importantInfo.map((item) => (
            <li key={item} className="flex items-start gap-2.5 text-sm text-slate-600">
              <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-amber-400" />
              {item}
            </li>
          ))}
        </ul>
      </Card>

      <a
        href={exam.officialLink}
        target="_blank"
        rel="noreferrer"
        className="flex w-fit items-center gap-2 rounded-xl bg-indigo-700 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-600"
      >
        Visit official website <ExternalLink size={15} />
      </a>
    </div>
  );
}
