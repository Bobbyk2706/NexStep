import { request } from "./client";

export async function getExams() {
  return request("/exams");
}

export async function getExamById(id) {
  if (id === undefined || id === null || id === "") {
    throw new Error("Exam ID is required.");
  }

  return request(`/exams/${encodeURIComponent(id)}`);
}

export async function evaluateEligibility(id) {
  if (id === undefined || id === null || id === "") {
    throw new Error("Exam ID is required.");
  }

  return request(`/eligibility/${encodeURIComponent(id)}/evaluate`, {
    method: "POST",
  });
}

export async function getEligibility(id) {
  if (id === undefined || id === null || id === "") {
    throw new Error("Exam ID is required.");
  }

  return request(`/eligibility/${encodeURIComponent(id)}`);
}

function firstExamDate(notification) {
  const dates = notification?.exam_dates || [];

  if (dates.length === 0) {
    return null;
  }

  return [...dates].sort(
    (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
  )[0]?.start_date || null;
}

function mapEligibility(eligibility) {
  const eligible = eligibility?.eligibility_status === "ELIGIBLE";

  return {
    eligible,
    reason: eligibility?.reason || "No eligibility explanation was returned.",
    eligibility,
  };
}

function normalizeExam(exam, eligibility = null) {
  const notification = exam?.latest_approved_notification || null;
  const eligibilityData = mapEligibility(eligibility);

  return {
    ...exam,
    id: exam.exam_id,
    organization: exam.conducting_body?.name || "—",
    category: exam.type || "—",
    applicationStart: notification?.application_start_date || null,
    applicationDeadline: notification?.application_end_date || null,
    examDate: firstExamDate(notification),
    officialLink: exam.off_exam_page || exam.conducting_body?.main_website || null,
    eligibilityRule: eligibilityData.reason,
    eligible: eligibilityData.eligible,
    reason: eligibilityData.reason,
    eligibility: eligibilityData.eligibility,
  };
}

async function enrichExamList(exams) {
  return Promise.all(
    exams.map(async (exam) => {
      const [detailResult, eligibilityResult] = await Promise.allSettled([
        getExamById(exam.exam_id),
        evaluateEligibility(exam.exam_id),
      ]);

      const fullExam =
        detailResult.status === "fulfilled" ? detailResult.value : exam;
      const eligibility =
        eligibilityResult.status === "fulfilled"
          ? eligibilityResult.value
          : null;

      const normalized = normalizeExam(fullExam, eligibility);

      if (eligibilityResult.status === "rejected") {
        normalized.eligible = false;
        normalized.reason =
          eligibilityResult.reason?.message ||
          "Eligibility could not be evaluated for this exam.";
        normalized.eligibilityRule = normalized.reason;
      }

      return normalized;
    })
  );
}

export async function searchExams(query) {
  const trimmedQuery = query?.trim();

  if (!trimmedQuery) {
    return getExamsWithEligibility();
  }

  const exams = await request(`/exams/search?q=${encodeURIComponent(trimmedQuery)}`);
  return enrichExamList(exams);
}

export async function getExamsWithEligibility() {
  const exams = await getExams();
  return enrichExamList(exams);
}
