import Card from "../../components/ui/Card";
import { formatDate } from "../../utils/date";

function Field({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-400">{label}</p>
      <p className="mt-0.5 text-sm font-medium text-ink">{value || "Not specified"}</p>
    </div>
  );
}

export default function ExamInfoCard({ examName, info }) {
  if (!info) return null;
  return (
    <Card>
      <h2 className="mb-4 font-mono text-xs uppercase tracking-wide text-slate-400">Exam Information</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Exam Name" value={examName} />
        <Field label="Conducting Body" value={info.conductingBody} />
        <Field label="Release / Notification Date" value={formatDate(info.releaseDate)} />
        <Field label="Application Start Date" value={formatDate(info.applicationStartDate)} />
        <Field label="Application End Date" value={formatDate(info.applicationEndDate)} />
        <div>
          <p className="text-xs text-slate-400">Examination Dates</p>
          <div className="mt-0.5 flex flex-col gap-0.5">
            {(info.examDates || []).length === 0 && <p className="text-sm font-medium text-ink">Not specified</p>}
            {(info.examDates || []).map((d, i) => (
              <p key={i} className="text-sm font-medium text-ink">{formatDate(d)}</p>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
}
