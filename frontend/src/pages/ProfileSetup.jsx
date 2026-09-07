import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, Trash2, GraduationCap } from "lucide-react";
import Logo from "../components/ui/Logo";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import { TextField, SelectField } from "../components/ui/Field";
import { useAuth } from "../context/AuthContext";
import * as profileApi from "../api/profile";

const YEAR_OPTIONS = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Final Year", "Graduated"];
const QUALIFICATION_LEVELS = ["10th", "12th / Senior Secondary", "Diploma", "Bachelor's", "Master's", "PhD", "Other"];

const emptyQualification = () => ({ level: "12th / Senior Secondary", institution: "", field: "", yearCompleted: "", score: "" });
const emptyWorkExperience = () => ({ company: "", role: "", duration: "" });
const emptyPreviousQualification = () => ({ level: "Bachelor's", institution: "", field: "", yearCompleted: "", score: "" });

export default function ProfileSetup() {
  const navigate = useNavigate();
  const { markProfileComplete } = useAuth();

  const [form, setForm] = useState({
    name: "",
    dob: "",
    nationality: "",
    state: "",
    college: "",
    branch: "",
    yearOfStudy: "",
    cgpa: "",
    percentage: "",
  });
  const [qualifications, setQualifications] = useState([emptyQualification()]);
  const [workExperience, setWorkExperience] = useState([]);
  const [hasHigherQualification, setHasHigherQualification] = useState(false);
  const [previousQualification, setPreviousQualification] = useState(emptyPreviousQualification());
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    profileApi.getProfile().then((existing) => {
      if (!existing) return;
      setForm({
        name: existing.name || "",
        dob: existing.dob || "",
        nationality: existing.nationality || "",
        state: existing.state || "",
        college: existing.college || "",
        branch: existing.branch || "",
        yearOfStudy: existing.yearOfStudy || "",
        cgpa: existing.cgpa || "",
        percentage: existing.percentage || "",
      });
      if (existing.qualifications?.length) setQualifications(existing.qualifications);
      if (existing.workExperience?.length) setWorkExperience(existing.workExperience);
      setHasHigherQualification(Boolean(existing.hasHigherQualification));
      if (existing.previousQualification) setPreviousQualification(existing.previousQualification);
    });
  }, []);

  function updateField(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  function updateQualification(index, key, value) {
    setQualifications((rows) => rows.map((row, i) => (i === index ? { ...row, [key]: value } : row)));
  }

  function updateWorkExperience(index, key, value) {
    setWorkExperience((rows) => rows.map((row, i) => (i === index ? { ...row, [key]: value } : row)));
  }

  function validate() {
    const next = {};
    if (!form.name.trim()) next.name = "Required.";
    if (!form.dob) next.dob = "Required.";
    if (!form.nationality.trim()) next.nationality = "Required.";
    if (!form.state.trim()) next.state = "Required.";
    if (!form.college.trim()) next.college = "Required.";
    if (!form.branch.trim()) next.branch = "Required.";
    if (!form.yearOfStudy) next.yearOfStudy = "Required.";
    if (!form.cgpa && !form.percentage) next.cgpa = "Enter a CGPA or percentage.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;
    setSaving(true);
    try {
      await profileApi.saveProfile({
        ...form,
        qualifications,
        workExperience,
        hasHigherQualification,
        previousQualification: hasHigherQualification ? previousQualification : null,
      });
      markProfileComplete();
      navigate("/dashboard");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="min-h-screen bg-paper pb-20">
      <header className="border-b border-slate-200/70 px-6 py-4">
        <Logo />
      </header>

      <div className="mx-auto max-w-2xl px-6 py-10">
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          Build your profile
        </h1>
        <p className="mt-2 text-slate-600">
          This is what NexStep checks against every exam's eligibility rules — the more complete, the
          more accurate your matches.
        </p>

        <form onSubmit={handleSubmit} noValidate className="mt-8 flex flex-col gap-6">
          <Card className="flex flex-col gap-5">
            <h2 className="font-display text-base font-semibold text-ink">Personal details</h2>
            <div className="grid gap-5 sm:grid-cols-2">
              <TextField id="name" label="Full name" required value={form.name} error={errors.name} onChange={(e) => updateField("name", e.target.value)} />
              <TextField id="dob" label="Date of birth" type="date" required value={form.dob} error={errors.dob} onChange={(e) => updateField("dob", e.target.value)} />
              <TextField id="nationality" label="Nationality" required value={form.nationality} error={errors.nationality} onChange={(e) => updateField("nationality", e.target.value)} />
              <TextField id="state" label="State" required value={form.state} error={errors.state} onChange={(e) => updateField("state", e.target.value)} />
            </div>
          </Card>

          <Card className="flex flex-col gap-5">
            <h2 className="font-display text-base font-semibold text-ink">Academic details</h2>
            <div className="grid gap-5 sm:grid-cols-2">
              <TextField id="college" label="College" required value={form.college} error={errors.college} onChange={(e) => updateField("college", e.target.value)} />
              <TextField id="branch" label="Branch" required value={form.branch} error={errors.branch} onChange={(e) => updateField("branch", e.target.value)} />
              <SelectField id="yearOfStudy" label="Year of study" required value={form.yearOfStudy} error={errors.yearOfStudy} onChange={(e) => updateField("yearOfStudy", e.target.value)}>
                <option value="" disabled>Select year</option>
                {YEAR_OPTIONS.map((y) => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </SelectField>
              <div className="grid grid-cols-2 gap-3">
                <TextField id="cgpa" label="CGPA" placeholder="e.g. 8.7" error={errors.cgpa} value={form.cgpa} onChange={(e) => updateField("cgpa", e.target.value)} />
                <TextField id="percentage" label="Percentage" placeholder="e.g. 82%" value={form.percentage} onChange={(e) => updateField("percentage", e.target.value)} />
              </div>
            </div>
          </Card>

          <Card className="flex flex-col gap-5">
            <div className="flex items-start gap-3 rounded-xl bg-indigo-50 p-4">
              <GraduationCap size={18} className="mt-0.5 shrink-0 text-indigo-700" />
              <label className="flex flex-1 cursor-pointer items-start gap-3 text-sm text-slate-700">
                <input
                  type="checkbox"
                  className="mt-0.5 h-4 w-4 rounded border-slate-300 text-indigo-700 focus:ring-indigo-500"
                  checked={hasHigherQualification}
                  onChange={(e) => setHasHigherQualification(e.target.checked)}
                />
                I'm pursuing or have completed a Master's/PhD — I'll add my previous qualification too.
              </label>
            </div>

            {hasHigherQualification && (
              <div className="grid gap-5 sm:grid-cols-2">
                <SelectField
                  id="prevLevel"
                  label="Previous qualification"
                  value={previousQualification.level}
                  onChange={(e) => setPreviousQualification((p) => ({ ...p, level: e.target.value }))}
                >
                  {QUALIFICATION_LEVELS.map((l) => (
                    <option key={l} value={l}>{l}</option>
                  ))}
                </SelectField>
                <TextField
                  id="prevInstitution"
                  label="Institution"
                  value={previousQualification.institution}
                  onChange={(e) => setPreviousQualification((p) => ({ ...p, institution: e.target.value }))}
                />
                <TextField
                  id="prevField"
                  label="Field of study"
                  value={previousQualification.field}
                  onChange={(e) => setPreviousQualification((p) => ({ ...p, field: e.target.value }))}
                />
                <TextField
                  id="prevYear"
                  label="Year completed"
                  value={previousQualification.yearCompleted}
                  onChange={(e) => setPreviousQualification((p) => ({ ...p, yearCompleted: e.target.value }))}
                />
                <TextField
                  id="prevScore"
                  label="CGPA / Percentage"
                  value={previousQualification.score}
                  onChange={(e) => setPreviousQualification((p) => ({ ...p, score: e.target.value }))}
                />
              </div>
            )}
          </Card>

          <Card className="flex flex-col gap-5">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-base font-semibold text-ink">Educational qualifications</h2>
              <Button
                type="button"
                variant="secondary"
                className="px-3 py-1.5 text-sm"
                onClick={() => setQualifications((rows) => [...rows, emptyQualification()])}
              >
                <Plus size={15} /> Add
              </Button>
            </div>
            {qualifications.map((row, i) => (
              <div key={i} className="grid gap-4 border-t border-slate-100 pt-5 first:border-none first:pt-0 sm:grid-cols-2">
                <SelectField id={`qlevel-${i}`} label="Level" value={row.level} onChange={(e) => updateQualification(i, "level", e.target.value)}>
                  {QUALIFICATION_LEVELS.map((l) => (
                    <option key={l} value={l}>{l}</option>
                  ))}
                </SelectField>
                <TextField id={`qinst-${i}`} label="Institution" value={row.institution} onChange={(e) => updateQualification(i, "institution", e.target.value)} />
                <TextField id={`qfield-${i}`} label="Field of study" value={row.field} onChange={(e) => updateQualification(i, "field", e.target.value)} />
                <div className="flex gap-3">
                  <TextField id={`qyear-${i}`} label="Year completed" className="flex-1" value={row.yearCompleted} onChange={(e) => updateQualification(i, "yearCompleted", e.target.value)} />
                  <TextField id={`qscore-${i}`} label="Score" className="flex-1" value={row.score} onChange={(e) => updateQualification(i, "score", e.target.value)} />
                  {qualifications.length > 1 && (
                    <button
                      type="button"
                      aria-label="Remove qualification"
                      onClick={() => setQualifications((rows) => rows.filter((_, idx) => idx !== i))}
                      className="mt-7 h-fit shrink-0 rounded-lg p-2.5 text-slate-400 hover:bg-amber-50 hover:text-amber-600"
                    >
                      <Trash2 size={16} />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </Card>

          <Card className="flex flex-col gap-5">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-display text-base font-semibold text-ink">Work experience</h2>
                <p className="text-sm text-slate-500">Optional — skip if you're a fresh graduate.</p>
              </div>
              <Button
                type="button"
                variant="secondary"
                className="px-3 py-1.5 text-sm"
                onClick={() => setWorkExperience((rows) => [...rows, emptyWorkExperience()])}
              >
                <Plus size={15} /> Add
              </Button>
            </div>
            {workExperience.map((row, i) => (
              <div key={i} className="grid gap-4 border-t border-slate-100 pt-5 first:border-none first:pt-0 sm:grid-cols-3">
                <TextField id={`wcompany-${i}`} label="Company" value={row.company} onChange={(e) => updateWorkExperience(i, "company", e.target.value)} />
                <TextField id={`wrole-${i}`} label="Role" value={row.role} onChange={(e) => updateWorkExperience(i, "role", e.target.value)} />
                <div className="flex gap-3">
                  <TextField id={`wduration-${i}`} label="Duration" className="flex-1" placeholder="e.g. 6 months" value={row.duration} onChange={(e) => updateWorkExperience(i, "duration", e.target.value)} />
                  <button
                    type="button"
                    aria-label="Remove work experience"
                    onClick={() => setWorkExperience((rows) => rows.filter((_, idx) => idx !== i))}
                    className="mt-7 h-fit shrink-0 rounded-lg p-2.5 text-slate-400 hover:bg-amber-50 hover:text-amber-600"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            ))}
          </Card>

          <Button type="submit" loading={saving} className="w-full">
            Save profile & see my matches
          </Button>
        </form>
      </div>
    </div>
  );
}
