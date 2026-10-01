import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ExternalLink, Sparkles } from "lucide-react";
import Card from "../../components/ui/Card";
import { TextField } from "../../components/ui/Field";
import Button from "../../components/ui/Button";
import { createExamExtraction } from "../api/adminExtractions";

export default function AddExam() {
  const navigate = useNavigate();
  const [examName, setExamName] = useState("");
  const [error, setError] = useState("");
  const [officialUrl, setOfficialUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!examName.trim()) {
      setError("Enter an exam name to start.");
      setOfficialUrl(null);
      return;
    }
    setError("");
    setOfficialUrl(null);
    setLoading(true);
    try {
      const extraction = await createExamExtraction(examName);
      navigate(`/admin/extractions/${extraction.id}`);
    } catch (err) {
      setError(err?.message || "Something went wrong. Please try again.");
      if (err?.code === "NO_NOTIFICATION_FOUND" && err.officialUrl) {
        setOfficialUrl(err.officialUrl);
      }
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
            <div className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
              <p>{error}</p>
              {officialUrl && (
                <a
                  href={officialUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="mt-2 inline-flex items-center gap-1.5 font-medium underline"
                >
                  Open official site <ExternalLink size={14} />
                </a>
              )}
            </div>
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