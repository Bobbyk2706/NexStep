import { listExtractions } from "./adminExtractions";

export async function listApprovedExams() {
  const approved = await listExtractions({ status: "APPROVED" });
  // one row per examId, keeping the highest version
  const byExam = new Map();
  for (const e of approved) {
    const existing = byExam.get(e.examId);
    if (!existing || e.version > existing.version) byExam.set(e.examId, e);
  }
  return [...byExam.values()];
  // Real version:
  // return request("/admin/exams");
}

export async function getApprovedExamByExamId(examId) {
  const approved = await listApprovedExams();
  return approved.find((e) => e.examId === examId) || null;
  // Real version:
  // return request(`/admin/exams/${examId}`);
}
