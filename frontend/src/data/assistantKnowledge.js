// Keyword-matching stand-in for a real retrieval/reasoning backend. Given
// the already eligibility-annotated `exams` list from ProfileContext, this
// can answer with the student's *actual* computed eligibility rather than
// generic text — replace findAnswer() with a real API call once a backend
// exists; the message/source shape below is what the chat UI expects.

export const suggestedQuestions = [
  "Am I eligible for GATE 2027?",
  "When does the CAT 2026 application close?",
  "How does NexStep decide what I'm eligible for?",
  "What happens if my CGPA changes?",
  "Am I eligible for UPSC Civil Services?",
  "How will I know about new deadlines?",
];

const EXAM_ALIASES = [
  { keys: ["gate"], examId: "gate-2027" },
  { keys: ["cat", "iim"], examId: "cat-2026" },
  { keys: ["gre"], examId: "gre-general" },
  { keys: ["upsc", "civil services", "ias"], examId: "upsc-cse-2027" },
  { keys: ["nda"], examId: "nda-2027" },
  { keys: ["clat"], examId: "clat-pg-2027" },
];

function formatDate(dateStr) {
  const d = new Date(dateStr);
  if (isNaN(d)) return dateStr;
  return d.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

function eligibilityAnswer(exam) {
  const verdict = exam.eligible ? "you're eligible for" : "you're not currently eligible for";
  const deadline = `Applications ${exam.eligible ? "close" : "closed or close"} ${formatDate(exam.applicationDeadline)}, with the exam on ${formatDate(exam.examDate)}.`;
  return `Based on your profile, ${verdict} ${exam.name}. ${exam.reason} ${deadline}`;
}

export function findAnswer(query, { profile, exams = [] }) {
  const q = query.toLowerCase();

  if (!profile) {
    return {
      content:
        "Your profile isn't complete yet, so I can't check eligibility against your academic details. Once it's filled in, I can answer exam-specific questions directly.",
      sources: [{ id: "profile-setup", title: "Complete your profile", category: "NexStep — Getting started" }],
    };
  }

  const examMatch = EXAM_ALIASES.find((a) => a.keys.some((k) => q.includes(k)));
  if (examMatch) {
    const exam = exams.find((e) => e.id === examMatch.examId);
    if (exam) {
      return {
        content: eligibilityAnswer(exam),
        sources: [
          { id: `${exam.id}-rule`, title: `${exam.name} — Eligibility rule`, category: exam.organization },
          { id: `${exam.id}-profile`, title: "Your profile", category: `${profile.branch}, ${profile.yearOfStudy}` },
        ],
      };
    }
  }

  if (q.includes("how") && (q.includes("decide") || q.includes("eligib") || q.includes("work"))) {
    return {
      content:
        "NexStep checks your saved profile — year of study, CGPA or percentage, branch, and qualifications — against each exam's published eligibility rules automatically. You never have to select an exam first; every exam in the database is checked, and the results update whenever your profile changes.",
      sources: [{ id: "eligibility-engine", title: "How automatic eligibility works", category: "NexStep — Eligibility" }],
    };
  }

  if (q.includes("cgpa") || q.includes("percentage") || (q.includes("profile") && q.includes("chang"))) {
    return {
      content:
        "Updating your CGPA, percentage, or year of study in Profile & Settings immediately re-checks every exam's eligibility rule against the new numbers — so if a change makes you newly eligible for something, it'll show up on your Eligibility Results right away.",
      sources: [{ id: "profile-settings", title: "Profile & Settings", category: "NexStep — Student Profile" }],
    };
  }

  if (q.includes("deadline") || q.includes("notif")) {
    return {
      content:
        "NexStep surfaces application deadlines and exam dates for everything you're eligible for on your Dashboard and the Upcoming page, and sends a notification when a deadline is approaching, when you become newly eligible for an exam, or when an exam's rules or dates change.",
      sources: [{ id: "notifications", title: "Notifications", category: "NexStep — Deadlines" }],
    };
  }

  return null;
}
