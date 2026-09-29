import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, RotateCcw, AlertOctagon } from "lucide-react";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import { TextareaField } from "../../components/ui/Field";
import StatusBadge from "../components/StatusBadge";
import Modal from "../components/Modal";
import SourceInfoCard from "../components/SourceInfoCard";
import ExamInfoCard from "../components/ExamInfoCard";
import EligibilityInfoCard from "../components/EligibilityInfoCard";
import RuleGroup from "../components/RuleGroup";
import EvidencePanel from "../components/EvidencePanel";
import ConflictPanel from "../components/ConflictPanel";
import ValidationPanel from "../components/ValidationPanel";
import {
  getExtractionById,
  approveExtraction,
  rejectExtraction,
  retryExtraction,
} from "../api/adminExtractions";
import { formatDate } from "../../utils/date";

export default function ExtractionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [extraction, setExtraction] = useState(undefined);
  const [showApprove, setShowApprove] = useState(false);
  const [showReject, setShowReject] = useState(false);
  const [rejectFeedback, setRejectFeedback] = useState("");
  const [rejectError, setRejectError] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setExtraction(undefined);
    setError("");

    getExtractionById(id)
      .then((data) => {
        if (active) setExtraction(data);
      })
      .catch((err) => {
        if (active) setError(err.message || "Could not load extraction.");
      });

    return () => {
      active = false;
    };
  }, [id]);

  async function handleApprove() {
    setBusy(true);
    try {
      await approveExtraction(id);
      navigate(extraction.examId ? `/admin/exams/${extraction.examId}` : "/admin/extractions");
    } catch (err) {
      setError(err.message || "Failed to approve extraction.");
      setShowApprove(false);
    } finally {
      setBusy(false);
    }
  }

  async function handleReject() {
    if (!rejectFeedback.trim()) {
      setRejectError("Feedback is required to reject the extraction.");
      return;
    }

    setBusy(true);
    try {
      await rejectExtraction(id, rejectFeedback);
      navigate("/admin/extractions");
    } catch (err) {
      setRejectError(err.message || "Failed to reject extraction.");
    } finally {
      setBusy(false);
    }
  }

  async function handleRetry() {
    setBusy(true);
    try {
      const retried = await retryExtraction(id);
      navigate(`/admin/extractions/${retried.id}`);
    } catch (err) {
      setError(err.message || "Failed to retry extraction.");
    } finally {
      setBusy(false);
    }
  }

  if (extraction === undefined) {
    return <p className="text-sm text-slate-400">Loading extraction...</p>;
  }

  if (extraction === null) {
    return (
      <Card>
        <p className="text-sm text-slate-500">We couldn't find that extraction.</p>
        <Link to="/admin/extractions" className="mt-3 inline-block text-sm font-medium text-gold hover:underline">
          Back to extraction history
        </Link>
      </Card>
    );
  }

  const backLink = (
    <Link to="/admin/extractions" className="flex w-fit items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-ink">
      <ArrowLeft size={15} /> Back to extraction history
    </Link>
  );

  const header = (
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          {extraction.examName}
        </h1>
        <p className="mt-1 text-slate-500">
          Extraction #{String(extraction.id)} · Version {extraction.version}
        </p>
      </div>
      <StatusBadge status={extraction.status} />
    </div>
  );

  if (extraction.status === "FAILED") {
    return (
      <div className="flex flex-col gap-6">
        {backLink}
        {header}
        <div className="rounded-2xl border-2 border-red-200 bg-red-50 p-5">
          <div className="flex items-center gap-2 text-red-700">
            <AlertOctagon size={18} />
            <h2 className="font-display text-base font-semibold">Extraction Failed</h2>
          </div>
          <p className="mt-3 text-sm text-ink">{extraction.changeDetails || "The backend reported that this extraction failed."}</p>
          <Button onClick={handleRetry} loading={busy} className="mt-5">
            <RotateCcw size={15} /> Retry
          </Button>
        </div>
      </div>
    );
  }

  const isPending = extraction.status === "PENDING_REVIEW";
  const isRejected = extraction.status === "REJECTED";

  return (
    <div className="flex flex-col gap-6 pb-10">
      {backLink}
      {header}

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {isRejected && extraction.rejectFeedback && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-5">
          <p className="text-sm font-medium text-red-700">Rejected with feedback</p>
          <p className="mt-1 text-sm text-red-600">{extraction.rejectFeedback}</p>
        </div>
      )}

      {isPending && <ConflictPanel conflicts={extraction.conflicts} />}
      {isPending && <ValidationPanel issues={extraction.validationIssues} />}

      <SourceInfoCard source={extraction.source} />
      <ExamInfoCard examName={extraction.examName} info={extraction.examInformation} />
      <EligibilityInfoCard info={extraction.eligibilityInformation} />

      <Card>
        <h2 className="mb-4 font-mono text-xs uppercase tracking-wide text-slate-400">Eligibility Rule Tree</h2>
        <RuleGroup group={extraction.eligibilityRules} />
      </Card>

      <EvidencePanel evidence={extraction.evidence} sourceUrl={extraction.source?.url} />

      {extraction.aiSummary && (
        <Card>
          <h2 className="mb-2 font-mono text-xs uppercase tracking-wide text-slate-400">AI Summary</h2>
          <p className="text-sm leading-6 text-slate-600">{extraction.aiSummary}</p>
        </Card>
      )}

      {isRejected && (
        <Card className="border-indigo-200 bg-indigo-50/50">
          <h2 className="mb-2 font-display text-base font-semibold text-ink">AI Retry</h2>
          <p className="mb-1 text-xs uppercase tracking-wide text-slate-400">Previous administrator feedback</p>
          <p className="mb-4 text-sm text-slate-600">"{extraction.rejectFeedback}"</p>
          <p className="mb-4 text-sm text-slate-500">
            The backend will re-run extraction against the original document and create a new pending extraction.
          </p>
          <Button onClick={handleRetry} loading={busy}>
            <RotateCcw size={15} /> Retry Extraction
          </Button>
        </Card>
      )}

      {isPending && (
        <div className="sticky bottom-4 flex justify-end gap-3 rounded-2xl border border-slate-200 bg-surface/95 p-4 shadow-card backdrop-blur">
          <Button variant="danger" onClick={() => setShowReject(true)}>
            Reject
          </Button>
          <Button onClick={() => setShowApprove(true)}>Approve</Button>
        </div>
      )}

      <Modal open={showApprove} title="Approve Extraction?" onClose={() => setShowApprove(false)}>
        <p className="text-sm text-slate-600">
          This extraction will become the authoritative examination data for{" "}
          <span className="font-medium text-ink">{extraction.examName}</span>.
        </p>
        <div className="mt-6 flex justify-end gap-3">
          <Button variant="ghost" onClick={() => setShowApprove(false)}>Cancel</Button>
          <Button onClick={handleApprove} loading={busy}>Confirm Approval</Button>
        </div>
      </Modal>

      <Modal open={showReject} title="Reject Extraction" onClose={() => setShowReject(false)}>
        <TextareaField
          id="rejectFeedback"
          label="Reason / Feedback"
          required
          placeholder="e.g. Application end date is incorrect. Please re-check the official notification."
          value={rejectFeedback}
          error={rejectError}
          onChange={(e) => {
            setRejectFeedback(e.target.value);
            setRejectError("");
          }}
        />
        <div className="mt-6 flex justify-end gap-3">
          <Button variant="ghost" onClick={() => setShowReject(false)}>Cancel</Button>
          <Button variant="danger" onClick={handleReject} loading={busy}>Reject Extraction</Button>
        </div>
      </Modal>
    </div>
  );
}
