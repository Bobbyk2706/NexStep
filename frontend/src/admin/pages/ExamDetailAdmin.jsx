import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import Card from "../../components/ui/Card";
import StatusBadge from "../components/StatusBadge";
import SourceInfoCard from "../components/SourceInfoCard";
import ExamInfoCard from "../components/ExamInfoCard";
import EligibilityInfoCard from "../components/EligibilityInfoCard";
import RuleGroup from "../components/RuleGroup";
import { getApprovedExamByExamId } from "../api/adminExams";
import { formatDate } from "../../utils/date";

export default function ExamDetailAdmin() {
  const { examId } = useParams();
  const [exam, setExam] = useState(undefined);

  useEffect(() => {
    let active = true;
    setExam(undefined);
    getApprovedExamByExamId(examId).then((data) => {
      if (active) setExam(data);
    });
    return () => {
      active = false;
    };
  }, [examId]);

  if (exam === undefined) return <p className="text-sm text-slate-400">Loading exam...</p>;
  if (exam === null) {
    return (
      <Card>
        <p className="text-sm text-slate-500">No approved exam found for this id.</p>
        <Link to="/admin/exams" className="mt-3 inline-block text-sm font-medium text-gold hover:underline">
          Back to all exams
        </Link>
      </Card>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <Link to="/admin/exams" className="flex w-fit items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-ink">
        <ArrowLeft size={15} /> Back to all exams
      </Link>

      <div className="flex flex-wrap items-start justify-between gap-4">
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">{exam.examName}</h1>
        <StatusBadge status={exam.status} />
      </div>

      <SourceInfoCard source={exam.source} />
      <ExamInfoCard examName={exam.examName} info={exam.examInformation} />
      <EligibilityInfoCard info={exam.eligibilityInformation} />

      <Card>
        <h2 className="mb-4 font-mono text-xs uppercase tracking-wide text-slate-400">Eligibility Rules</h2>
        <RuleGroup group={exam.eligibilityRules} />
      </Card>

      <Card className="flex flex-wrap gap-x-10 gap-y-2 text-sm">
        <div>
          <p className="text-xs text-slate-400">Last Updated</p>
          <p className="font-medium text-ink">{formatDate(exam.approvedDate)}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Extraction Version</p>
          <p className="font-medium text-ink">{exam.version}</p>
        </div>
        <div>
          <Link to={`/admin/extractions/${exam.id}`} className="font-medium text-gold hover:underline">
            View source extraction
          </Link>
        </div>
      </Card>
    </div>
  );
}
