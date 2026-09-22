import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Card from "../../components/ui/Card";
import { listApprovedExams } from "../api/adminExams";
import { formatDate } from "../../utils/date";

export default function AllExams() {
  const [exams, setExams] = useState(undefined);

  useEffect(() => {
    listApprovedExams().then(setExams);
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">All Exams</h1>
        <p className="mt-1.5 text-slate-600">Approved exams currently live as authoritative data.</p>
      </div>

      <div className="flex flex-col gap-3">
        {exams?.length === 0 && (
          <Card><p className="text-sm text-slate-500">No exams approved yet.</p></Card>
        )}
        {exams?.map((exam) => (
          <Card key={exam.examId} className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 className="font-display font-semibold text-ink">{exam.examName}</h3>
              <p className="mt-1 text-sm text-slate-500">{exam.examInformation?.conductingBody}</p>
              <p className="mt-1.5 font-mono text-xs text-slate-400">
                Last updated {formatDate(exam.approvedDate)} · Version {exam.version}
              </p>
            </div>
            <Link
              to={`/admin/exams/${exam.examId}`}
              className="shrink-0 rounded-xl px-4 py-2 text-center text-sm font-medium text-gold ring-1 ring-inset ring-indigo-100 transition hover:bg-indigo-50"
            >
              View details
            </Link>
          </Card>
        ))}
      </div>
    </div>
  );
}
