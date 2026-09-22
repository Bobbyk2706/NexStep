import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles } from "lucide-react";
import Card from "../../components/ui/Card";
import { TextField } from "../../components/ui/Field";
import Button from "../../components/ui/Button";
import { createExamExtraction } from "../api/adminExtractions";

export default function AddExam() {
  const navigate = useNavigate();
  const [examName, setExamName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!examName.trim()) {
      setError("Enter an exam name to start.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const extraction = await createExamExtraction(examName);
      navigate(`/admin/extractions/${extraction.id}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Add Examination</h1>
        <p className="mt-1.5 max-w-lg text-slate-600">
          Provide only the exam name. NexStep discovers the official source, downloads the notification,
          and extracts eligibility rules, dates, and syllabus automatically.
        </p>
      </div>

      <Card className="max-w-lg">
        <form onSubmit={handleSubmit} className="flex flex-col gap-5">
          {error && (
            <p className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
              {error}
            </p>
          )}
          <TextField
            id="examName"
            label="Exam Name"
            placeholder="e.g. Civil Services Examination 2026"
            required
            value={examName}
            onChange={(e) => setExamName(e.target.value)}
          />
          <Button type="submit" loading={loading} className="w-full">
            <Sparkles size={16} /> Start AI Discovery
          </Button>
        </form>
      </Card>

      <Card className="max-w-lg bg-indigo-50/50">
        <p className="text-sm text-slate-600">
          The admin should not manually enter eligibility rules, dates, source URLs, or PDFs — those
          are discovered and extracted by the system, then presented here for your review before
          anything becomes authoritative.
        </p>
      </Card>
    </div>
  );
}
