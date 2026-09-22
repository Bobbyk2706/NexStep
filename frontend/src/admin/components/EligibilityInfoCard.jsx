import Card from "../../components/ui/Card";

function Field({ label, value }) {
  return (
    <div>
      <p className="text-xs text-slate-400">{label}</p>
      <p className={`mt-0.5 text-sm font-medium ${value ? "text-ink" : "text-slate-400"}`}>
        {value || "Not specified"}
      </p>
    </div>
  );
}

export default function EligibilityInfoCard({ info }) {
  if (!info) return null;
  return (
    <Card>
      <h2 className="mb-4 font-mono text-xs uppercase tracking-wide text-slate-400">Eligibility Information</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Minimum Age" value={info.minAge} />
        <Field label="Maximum Age" value={info.maxAge} />
        <Field label="Educational Qualification" value={info.educationalQualification} />
        <Field label="Nationality" value={info.nationality} />
        <Field label="Work Experience" value={info.workExperience} />
        <Field label="Other Requirements" value={info.otherRequirements} />
      </div>
    </Card>
  );
}
