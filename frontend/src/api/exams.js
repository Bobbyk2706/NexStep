import { mockExams } from "./mockData";
import { mockDelay } from "./client";

// --- Eligibility engine -----------------------------------------------
// This is a placeholder rule set standing in for the real eligibility
// service. It takes the student profile and one exam and returns
// { eligible, reason }. Swap the body of this function for a call to
// Vivek's eligibility endpoint — every page that shows eligibility reads
// through here, not from mockExams directly, so that's the only edit
// needed later.
export function computeEligibility(exam, profile) {
  if (!profile) return { eligible: false, reason: "Complete your profile to check eligibility." };

  const cgpaAsPercent = profile.cgpa ? Number(profile.cgpa) * 9.5 : Number(profile.percentage || 0);
  const isFinalOrGraduate = ["4th Year", "Final Year", "Graduated"].includes(profile.yearOfStudy);

  switch (exam.id) {
    case "gate-2027":
      return isFinalOrGraduate
        ? { eligible: true, reason: "Final-year status meets GATE's eligibility requirement." }
        : { eligible: false, reason: "GATE requires final-year standing or a completed degree." };
    case "cat-2026":
      return cgpaAsPercent >= 50
        ? { eligible: true, reason: "Your academic score clears CAT's 50% minimum." }
        : { eligible: false, reason: "CAT requires at least 50% aggregate (45% for reserved categories)." };
    case "gre-general":
      return isFinalOrGraduate
        ? { eligible: true, reason: "No fixed eligibility — open to final-year and graduate students." }
        : { eligible: false, reason: "Typically taken closer to your final year, once you're applying abroad." };
    case "upsc-cse-2027":
      return profile.yearOfStudy === "Graduated"
        ? { eligible: true, reason: "A completed bachelor's degree meets UPSC's requirement." }
        : { eligible: false, reason: "Requires a completed bachelor's degree in any discipline." };
    case "nda-2027":
      return { eligible: false, reason: "NDA is for 12th-pass candidates not yet pursuing a bachelor's degree." };
    case "clat-pg-2027":
      return { eligible: false, reason: "CLAT PG requires an LL.B. degree." };
    default:
      return { eligible: false, reason: "Eligibility rule not available yet." };
  }
}

function withEligibility(exams, profile) {
  return exams.map((exam) => ({ ...exam, ...computeEligibility(exam, profile) }));
}

export async function getExams(profile) {
  await mockDelay();
  return withEligibility(mockExams, profile);
  // Real version:
  // return request("/exams/eligibility", { method: "POST", body: profile });
}

export async function getExamById(id, profile) {
  await mockDelay(200);
  const exam = mockExams.find((e) => e.id === id);
  if (!exam) return null;
  return { ...exam, ...computeEligibility(exam, profile) };
  // Real version:
  // return request(`/exams/${id}?withEligibility=true`);
}

export async function searchExams(query, profile) {
  await mockDelay(200);
  const q = query.trim().toLowerCase();
  const results = mockExams.filter(
    (e) =>
      e.name.toLowerCase().includes(q) ||
      e.organization.toLowerCase().includes(q) ||
      e.category.toLowerCase().includes(q)
  );
  return withEligibility(results, profile);
  // Real version:
  // return request(`/exams/search?q=${encodeURIComponent(query)}`);
}
