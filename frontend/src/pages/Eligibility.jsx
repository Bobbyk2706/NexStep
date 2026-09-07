import { useState } from "react";
import { Link } from "react-router-dom";
import Card from "../components/ui/Card";
import EligibilityPill from "../components/ui/EligibilityPill";
import { useProfile } from "../context/ProfileContext";
import { formatDate } from "../utils/date";

const FILTERS = ["All", "Eligible", "Not eligible"];

export default function Eligibility() {
  const { exams, loading } = useProfile();
  const [filter, setFilter] = useState("Eligible");

  const filtered = exams.filter((e) => {
    if (filter === "Eligible") return e.eligible;
    if (filter === "Not eligible") return !e.eligible;
    return true;
  });

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          Your eligibility results
        </h1>
        <p className="mt-1.5 text-slate-600">
          Checked automatically against your profile — no need to pick an exam first.
        </p>
      </div>

      <div className="flex gap-2">
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`rounded-xl px-3.5 py-1.5 text-sm font-medium transition ${
              filter === f ? "bg-indigo-700 text-white" : "bg-white text-slate-600 ring-1 ring-inset ring-slate-200 hover:bg-slate-50"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {loading && <p className="text-sm text-slate-400">Checking your profile against every exam...</p>}

      <div className="flex flex-col gap-3">
        {!loading && filtered.length === 0 && (
          <Card>
            <p className="text-sm text-slate-500">No exams in this view yet.</p>
          </Card>
        )}
        {filtered.map((exam) => (
          <Card key={exam.id} className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0">
              <div className="flex items-center gap-2.5">
                <h3 className="font-display font-semibold text-ink">{exam.name}</h3>
                <EligibilityPill eligible={exam.eligible} deadline={exam.applicationDeadline} size="sm" />
              </div>
              <p className="mt-1 text-sm text-slate-500">{exam.organization}</p>
              <p className="mt-1.5 text-xs text-slate-400">{exam.reason}</p>
              <p className="mt-2 font-mono text-xs text-slate-500">
                Apply by {formatDate(exam.applicationDeadline)} · Exam on {formatDate(exam.examDate)}
              </p>
            </div>
            <Link
              to={`/exams/${exam.id}`}
              className="shrink-0 rounded-xl px-4 py-2 text-center text-sm font-medium text-indigo-700 ring-1 ring-inset ring-indigo-100 transition hover:bg-indigo-50"
            >
              View details
            </Link>
          </Card>
        ))}
      </div>
    </div>
  );
}
