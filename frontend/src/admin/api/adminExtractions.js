import { mockDelay } from "../../api/client";
import { mockExtractions, STAGE_SEQUENCE, nextId } from "./adminData";

let extractions = [...mockExtractions];

function clone(e) {
  return e ? JSON.parse(JSON.stringify(e)) : e;
}

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

export async function listExtractions({ status } = {}) {
  await mockDelay(250);
  let rows = [...extractions];
  if (status && status !== "All") {
    rows = rows.filter((e) => e.status === status);
  }
  return rows
    .sort((a, b) => new Date(b.createdDate) - new Date(a.createdDate))
    .map(clone);
  // Real version:
  // return request(`/admin/extractions${status ? `?status=${status}` : ""}`);
}

export async function getExtractionById(id) {
  await mockDelay(200);
  return clone(extractions.find((e) => e.id === id) || null);
  // Real version:
  // return request(`/admin/extractions/${id}`);
}

export async function createExamExtraction(examName) {
  await mockDelay(300);
  const examId = examName.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  const extraction = {
    id: nextId(),
    examId,
    examName: examName.trim(),
    version: 1,
    status: STAGE_SEQUENCE[0].key,
    createdDate: todayStr(),
    source: null,
    examInformation: null,
    eligibilityInformation: null,
    eligibilityRules: null,
    evidence: [],
    conflicts: [],
    validationIssues: [],
    feedbackHistory: [],
  };
  extractions = [extraction, ...extractions];
  return clone(extraction);
  // Real version:
  // return request("/admin/exams", { method: "POST", body: { examName } });
}

// Simulates one tick of backend processing — moves the extraction to the
// next pipeline stage, or into PENDING_REVIEW once the sequence completes.
// A real integration would instead poll GET /admin/extractions/{id} and
// read whatever status the backend reports.
export async function advanceProcessing(id) {
  await mockDelay(650);
  const idx = extractions.findIndex((e) => e.id === id);
  if (idx === -1) return null;
  const current = extractions[idx];
  const stageIdx = STAGE_SEQUENCE.findIndex((s) => s.key === current.status);
  if (stageIdx === -1) return clone(current); // already terminal

  if (stageIdx >= STAGE_SEQUENCE.length - 1) {
    // Finished "Preparing Review" — hydrate with mock extracted content and
    // land in PENDING_REVIEW. A real backend would already carry this data.
    const seedByExamId = mockExtractions.find((e) => e.examId === current.examId && e.examInformation);
    const updated = {
      ...current,
      status: "PENDING_REVIEW",
      source: seedByExamId?.source || {
        url: "https://example-official-source.gov.in",
        document: `${current.examName.replace(/\s+/g, "-")}-Notification.pdf`,
        downloadedDate: todayStr(),
      },
      examInformation: seedByExamId?.examInformation || {
        conductingBody: "Not specified",
        releaseDate: todayStr(),
        applicationStartDate: todayStr(),
        applicationEndDate: todayStr(),
        examDates: [],
      },
      eligibilityInformation: seedByExamId?.eligibilityInformation || {
        minAge: "Not specified",
        maxAge: "Not specified",
        educationalQualification: "Not specified",
        nationality: "Not specified",
        workExperience: "Not specified",
        otherRequirements: "Not specified",
      },
      eligibilityRules: seedByExamId?.eligibilityRules || { logicalOperator: "AND", rules: [], childGroups: [] },
      evidence: seedByExamId?.evidence || [],
      conflicts: seedByExamId?.conflicts || [],
      validationIssues: seedByExamId?.validationIssues || [],
    };
    extractions[idx] = updated;
    return clone(updated);
  }

  const updated = { ...current, status: STAGE_SEQUENCE[stageIdx + 1].key };
  extractions[idx] = updated;
  return clone(updated);
}

export async function approveExtraction(id) {
  await mockDelay(400);
  const idx = extractions.findIndex((e) => e.id === id);
  if (idx === -1) throw new Error("Extraction not found.");
  extractions[idx] = { ...extractions[idx], status: "APPROVED", approvedDate: todayStr() };
  return clone(extractions[idx]);
  // Real version:
  // return request(`/admin/extractions/${id}/approve`, { method: "POST" });
}

export async function rejectExtraction(id, feedback) {
  await mockDelay(400);
  if (!feedback?.trim()) throw new Error("Feedback is required to reject an extraction.");
  const idx = extractions.findIndex((e) => e.id === id);
  if (idx === -1) throw new Error("Extraction not found.");
  extractions[idx] = { ...extractions[idx], status: "REJECTED", rejectFeedback: feedback.trim() };
  return clone(extractions[idx]);
  // Real version:
  // return request(`/admin/extractions/${id}/reject`, { method: "POST", body: { feedback } });
}

export async function retryExtraction(id) {
  await mockDelay(400);
  const original = extractions.find((e) => e.id === id);
  if (!original) throw new Error("Extraction not found.");
  const retried = {
    id: nextId(),
    examId: original.examId,
    examName: original.examName,
    version: original.version + 1,
    previousExtractionId: original.id,
    status: STAGE_SEQUENCE[0].key,
    createdDate: todayStr(),
    source: null,
    examInformation: null,
    eligibilityInformation: null,
    eligibilityRules: null,
    evidence: [],
    conflicts: [],
    validationIssues: [],
    feedbackHistory: [
      ...(original.feedbackHistory || []),
      { version: original.version, feedback: original.rejectFeedback, date: original.createdDate },
    ],
  };
  extractions = [retried, ...extractions];
  return clone(retried);
  // Real version:
  // return request(`/admin/extractions/${id}/retry`, { method: "POST" });
}

export async function getDashboardStats() {
  await mockDelay(200);
  return {
    pendingReviews: extractions.filter((e) => e.status === "PENDING_REVIEW").length,
    approvedExams: extractions.filter((e) => e.status === "APPROVED").length,
    rejectedExtractions: extractions.filter((e) => e.status === "REJECTED").length,
    failedExtractions: extractions.filter((e) => e.status === "FAILED").length,
    recent: [...extractions]
      .sort((a, b) => new Date(b.createdDate) - new Date(a.createdDate))
      .slice(0, 6)
      .map(clone),
  };
}
