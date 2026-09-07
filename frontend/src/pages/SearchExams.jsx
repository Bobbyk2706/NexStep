import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Search } from "lucide-react";
import Card from "../components/ui/Card";
import EligibilityPill from "../components/ui/EligibilityPill";
import { useProfile } from "../context/ProfileContext";
import * as examsApi from "../api/exams";
import { formatDate } from "../utils/date";

export default function SearchExams() {
  const { profile, exams } = useProfile();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(exams);

  useEffect(() => {
    if (!query.trim()) {
      setResults(exams);
      return;
    }
    const handle = setTimeout(() => {
      examsApi.searchExams(query, profile).then(setResults);
    }, 200);
    return () => clearTimeout(handle);
  }, [query, profile, exams]);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Browse exams</h1>
        <p className="mt-1.5 text-slate-600">
          Search by name, organization, or category. Eligibility is still checked automatically.
        </p>
      </div>

      <div className="relative">
        <Search size={17} className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search exams, e.g. GATE, IIM, civil services..."
          className="w-full rounded-xl border border-slate-200 bg-white py-3 pl-10 pr-4 text-[15px] text-ink placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
        />
      </div>

      <div className="flex flex-col gap-3">
        {results.length === 0 && (
          <Card>
            <p className="text-sm text-slate-500">No exams match "{query}".</p>
          </Card>
        )}
        {results.map((exam) => (
          <Card key={exam.id} className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div className="min-w-0">
              <div className="flex items-center gap-2.5">
                <h3 className="font-display font-semibold text-ink">{exam.name}</h3>
                <EligibilityPill eligible={exam.eligible} deadline={exam.applicationDeadline} size="sm" />
              </div>
              <p className="mt-1 text-sm text-slate-500">{exam.organization} · {exam.category}</p>
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
