import { adminRequest } from "./adminClient";
import { getExtractionById, listExtractions } from "./adminExtractions";

function firstExamDate(notification) {
  const dates = notification?.exam_dates || [];
  if (dates.length === 0) return null;

  return [...dates].sort(
    (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
  )[0]?.start_date || null;
}

function normalizeApprovedExam(exam, extraction) {
  const notification = exam.latest_approved_notification || null;

  return {
    id: extraction?.id || null,
    examId: exam.exam_id,
    examName: exam.name,
    status: "APPROVED",
    version: extraction?.version || 1,
    approvedDate: extraction?.createdDate || notification?.release_date || null,
    source: {
      url: notification?.official_url || exam.off_exam_page || null,
      document: notification?.document_url || notification?.title || "Official notification",
      downloadedDate: notification?.release_date || null,
    },
    examInformation: {
      conductingBody: exam.conducting_body?.name || null,
      releaseDate: notification?.release_date || null,
      applicationStartDate: notification?.application_start_date || null,
      applicationEndDate: notification?.application_end_date || null,
      examDates: (notification?.exam_dates || []).map((dateRange) => ({
        startDate: dateRange.start_date,
        endDate: dateRange.end_date,
      })),
    },
    eligibilityInformation: null,
    eligibilityRules: null,
  };
}

export async function listApprovedExams() {
  const [publicExams, approvedExtractions] = await Promise.all([
    adminRequest("/api/exams"),
    listExtractions({ status: "APPROVED" }),
  ]);

  const latestExtractionByExam = new Map();

  for (const extraction of approvedExtractions) {
    const existing = latestExtractionByExam.get(extraction.examId);
    if (!existing || new Date(extraction.createdDate || 0) > new Date(existing.createdDate || 0)) {
      latestExtractionByExam.set(extraction.examId, extraction);
    }
  }

  return Promise.all(
    (publicExams || []).map(async (exam) => {
      try {
        const detail = await adminRequest(`/api/exams/${encodeURIComponent(exam.exam_id)}`);
        return normalizeApprovedExam(detail, latestExtractionByExam.get(exam.exam_id));
      } catch {
        return null;
      }
    })
  ).then((rows) => rows.filter(Boolean));
}

export async function getApprovedExamByExamId(examId) {
  const exams = await listApprovedExams();
  const exam = exams.find((item) => String(item.examId) === String(examId));

  if (!exam) return null;
  if (!exam.id) return exam;

  try {
    const extraction = await getExtractionById(exam.id);
    return {
      ...exam,
      examInformation: extraction.examInformation || exam.examInformation,
      eligibilityInformation: extraction.eligibilityInformation,
      eligibilityRules: extraction.eligibilityRules,
      source: extraction.source || exam.source,
      version: extraction.version || exam.version,
      approvedDate: extraction.createdDate || exam.approvedDate,
    };
  } catch {
    return exam;
  }
}
