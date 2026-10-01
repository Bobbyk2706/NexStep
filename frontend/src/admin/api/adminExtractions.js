import { adminRequest } from "./adminClient";

const BACKEND_STATUS_TO_UI = {
  PENDING: "PENDING_REVIEW",
  PENDING_REVIEW: "PENDING_REVIEW",
  APPROVED: "APPROVED",
  REJECTED: "REJECTED",
  FAILED: "FAILED",
};

const UI_STATUS_TO_BACKEND = {
  PENDING_REVIEW: "PENDING",
  APPROVED: "APPROVED",
  REJECTED: "REJECTED",
  FAILED: "FAILED",
};

function mapGroup(group) {
  return {
    logicalOperator: group?.logical_operator || "AND",
    rules: (group?.rules || []).map((rule) => ({
      attribute: rule.attribute,
      operator: rule.operator,
      value: rule.value,
    })),
    childGroups: (group?.child_groups || []).map(mapGroup),
  };
}

function parseExtractedContent(value) {
  if (!value) return null;

  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function basename(value) {
  if (!value) return "Original document";
  return value.split(/[\\/]/).pop() || value;
}

function mapHistoryRow(row, version = 1) {
  return {
    id: row.extraction_id,
    extractionId: row.extraction_id,
    notificationId: row.notification_id,
    examId: row.exam_id,
    examName: row.exam_name,
    notificationTitle: row.notification_title,
    extractionType: row.extraction_type,
    version,
    status: BACKEND_STATUS_TO_UI[row.status] || row.status,
    createdDate: row.created_at,
    changeDetected: Boolean(row.change_detected),
    changeDetails: row.change_details || "",
  };
}

function withVersions(rows) {
  const sorted = [...rows].sort((a, b) => {
    const byNotification = Number(a.notification_id) - Number(b.notification_id);
    if (byNotification !== 0) return byNotification;

    const byDate = new Date(a.created_at || 0).getTime() - new Date(b.created_at || 0).getTime();
    if (byDate !== 0) return byDate;

    return Number(a.extraction_id) - Number(b.extraction_id);
  });

  const counters = new Map();

  return sorted.map((row) => {
    const next = (counters.get(row.notification_id) || 0) + 1;
    counters.set(row.notification_id, next);
    return mapHistoryRow(row, next);
  });
}

async function fetchHistoryRows() {
  return adminRequest("/admin/extractions");
}

export async function listExtractions({ status = "All" } = {}) {
  const rawRows = await fetchHistoryRows();
  const rows = withVersions(rawRows || []);
  const backendStatus = UI_STATUS_TO_BACKEND[status];

  return rows
    .filter((row) => !backendStatus || row.status === BACKEND_STATUS_TO_UI[backendStatus])
    .sort((a, b) => new Date(b.createdDate || 0).getTime() - new Date(a.createdDate || 0).getTime());
}

export async function getExtractionById(id) {
  if (id === undefined || id === null || id === "") {
    throw new Error("Extraction ID is required.");
  }

  const [detail, history] = await Promise.all([
    adminRequest(`/admin/extractions/${encodeURIComponent(id)}`),
    fetchHistoryRows(),
  ]);

  const rows = withVersions(history || []);
  const summary = rows.find((row) => String(row.id) === String(id));
  const parsed = parseExtractedContent(detail?.extracted_content);
  const extractionData = parsed?.extraction || {};
  const examInformation = extractionData.exam_information || {};
  const eligibilityInformation = examInformation.eligibility || {};
  const ruleGroups = extractionData.eligibility_rules?.rule_groups || [];

  const status = summary?.status || BACKEND_STATUS_TO_UI[detail?.status] || detail?.status;

  return {
    id: Number(detail.extraction_id),
    extractionId: Number(detail.extraction_id),
    notificationId: Number(detail.notification_id),
    examId: summary?.examId || null,
    examName: examInformation.exam_name || summary?.examName || "Exam extraction",
    version: summary?.version || 1,
    status,
    createdDate: detail.created_at || summary?.createdDate,
    source: {
      url: detail.official_url || null,
      document: basename(detail.original_document),
      downloadedDate: detail.created_at || summary?.createdDate,
    },
    examInformation: {
      conductingBody: examInformation.conducting_body || null,
      releaseDate: examInformation.release_date || null,
      applicationStartDate: examInformation.application_start_date || null,
      applicationEndDate: examInformation.application_end_date || null,
      examDates: (examInformation.exam_dates || []).map((dateRange) => ({
        startDate: dateRange.start_date,
        endDate: dateRange.end_date,
      })),
    },
    eligibilityInformation: {
      minAge: eligibilityInformation.minimum_age,
      maxAge: eligibilityInformation.maximum_age,
      educationalQualification: eligibilityInformation.educational_qualification,
      nationality: eligibilityInformation.nationality,
      workExperience: eligibilityInformation.work_experience,
      otherRequirements: Array.isArray(eligibilityInformation.other_requirements)
        ? eligibilityInformation.other_requirements.join("; ")
        : eligibilityInformation.other_requirements || null,
    },
    eligibilityRules: {
      logicalOperator: "AND",
      rules: [],
      childGroups: ruleGroups.map(mapGroup),
    },
    evidence: (parsed?.evidence || []).map((item, index) => ({
      id: `${detail.extraction_id}-evidence-${index}`,
      field: item.field || "Extracted evidence",
      chunkNumber: item.chunk_number,
      pageNumbers: item.page_numbers || [],
      sourceText: item.source_text,
      verified: item.verified ?? null,
      section: item.section || null,
    })),
    conflicts: (parsed?.conflicts || []).map((conflict) => ({
      field: conflict.field,
      chosen: conflict.chosen || null,
      reason: conflict.reason || "",
      options: (conflict.options || []).map((option) => ({
        value: option.value,
        source: [
          option.source,
          option.pages?.length ? `p. ${option.pages.join(", ")}` : "",
        ]
          .filter(Boolean)
          .join(" · "),
      })),
    })),
    validationIssues: (parsed?.issues || []).map((issue) => ({
      severity: issue.severity || "warning",
      message: issue.message,
      field: issue.field || null,
    })),
    pipeline: parsed?.pipeline || null,
    rejectFeedback: status === "REJECTED" ? detail.change_details || "" : "",
    feedbackHistory: [],
    aiSummary: detail.ai_summary || null,
    changeDetected: Boolean(detail.change_detected),
    changeDetails: detail.change_details || "",
  };
}

export async function createExamExtraction(examName) {
  const trimmed = examName?.trim();
  if (!trimmed) {
    throw new Error("Enter an exam name to start.");
  }

  const result = await adminRequest("/admin/extractions", {
    method: "POST",
    body: { exam_name: trimmed },
  });

  return {
    ...result,
    id: result.extraction_id ?? result.id,
    status: BACKEND_STATUS_TO_UI[result.status] || result.status,
  };
}

export async function approveExtraction(id) {
  return adminRequest(`/admin/extractions/${encodeURIComponent(id)}/approve`, {
    method: "POST",
  });
}

export async function rejectExtraction(id, feedback) {
  const trimmed = feedback?.trim();
  if (!trimmed) {
    throw new Error("Feedback is required to reject an extraction.");
  }

  return adminRequest(`/admin/extractions/${encodeURIComponent(id)}/reject`, {
    method: "POST",
    body: { feedback: trimmed },
  });
}

export async function retryExtraction(id) {
  const result = await adminRequest(`/admin/extractions/${encodeURIComponent(id)}/retry`, {
    method: "POST",
  });

  return {
    ...result,
    id: result.extraction_id,
    status: BACKEND_STATUS_TO_UI[result.status] || result.status,
  };
}

export async function getDashboardStats() {
  const rows = await listExtractions();

  return {
    pendingReviews: rows.filter((row) => row.status === "PENDING_REVIEW").length,
    approvedExams: rows.filter((row) => row.status === "APPROVED").length,
    rejectedExtractions: rows.filter((row) => row.status === "REJECTED").length,
    failedExtractions: rows.filter((row) => row.status === "FAILED").length,
    recent: rows.slice(0, 6),
  };
}
