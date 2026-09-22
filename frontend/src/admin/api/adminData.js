// Mock data for the admin extraction/review workflow. Shape mirrors the
// backend contract described in the spec (extraction, evidence, recursive
// eligibility_rules.rule_groups) so wiring in the real API later means
// replacing the bodies in api/adminExtractions.js, not reshaping the UI.

export const STAGE_SEQUENCE = [
  { key: "DISCOVERING_SOURCE", label: "Source Discovery" },
  { key: "VERIFYING_SOURCE", label: "Source Verification" },
  { key: "DOWNLOADING_DOCUMENT", label: "Official Document Download" },
  { key: "EXTRACTING_DOCUMENT", label: "PDF Page Extraction" },
  { key: "CHUNKING_DOCUMENT", label: "Lossless Document Chunking" },
  { key: "EXTRACTING_INFORMATION", label: "AI Information Extraction" },
  { key: "AGGREGATING", label: "Chunk Aggregation" },
  { key: "NORMALIZING", label: "Normalization" },
  { key: "VALIDATING", label: "Validation" },
  { key: "PREPARING_REVIEW", label: "Preparing Review" },
];

export const TERMINAL_STATUSES = ["PENDING_REVIEW", "APPROVED", "REJECTED", "FAILED"];

export function isProcessingStatus(status) {
  return STAGE_SEQUENCE.some((s) => s.key === status);
}

let idCounter = 13;
export function nextId() {
  idCounter += 1;
  return `ext-${idCounter}`;
}

export const mockExtractions = [
  // --- Flagship example: reject -> retry -> pending, with a conflict ---
  {
    id: "ext-12",
    examId: "upsc-cse-2026",
    examName: "Civil Services Examination 2026",
    version: 1,
    status: "REJECTED",
    createdDate: "2026-09-14",
    rejectFeedback: "Application end date is incorrect. Please re-check the official notification.",
    source: {
      url: "https://upsc.gov.in/notification/csp-2026",
      document: "Notif-CSP-2026-Engl-060226Rev.pdf",
      downloadedDate: "2026-09-14",
    },
    examInformation: {
      conductingBody: "Union Public Service Commission",
      releaseDate: "2026-02-04",
      applicationStartDate: "2026-02-04",
      applicationEndDate: "2026-02-24",
      examDates: ["2026-05-24"],
    },
    eligibilityInformation: {
      minAge: 21,
      maxAge: 32,
      educationalQualification: "Graduate degree",
      nationality: "India",
      workExperience: "Not specified",
      otherRequirements: "Not specified",
    },
    eligibilityRules: {
      logicalOperator: "AND",
      rules: [{ attribute: "Educational Qualification", operator: "=", value: "Graduate" }],
      childGroups: [
        {
          logicalOperator: "OR",
          rules: [
            { attribute: "Nationality", operator: "=", value: "India" },
            { attribute: "Nationality", operator: "=", value: "Nepal" },
          ],
          childGroups: [],
        },
      ],
    },
    evidence: [
      {
        id: "ev-12-1",
        field: "Application End Date",
        chunkNumber: 1,
        pageNumbers: [2],
        sourceText: "Applications must be submitted online on or before 24th February 2026.",
      },
    ],
    conflicts: [],
    validationIssues: [],
    feedbackHistory: [],
  },
  {
    id: "ext-13",
    examId: "upsc-cse-2026",
    examName: "Civil Services Examination 2026",
    version: 2,
    previousExtractionId: "ext-12",
    status: "PENDING_REVIEW",
    createdDate: "2026-09-15",
    source: {
      url: "https://upsc.gov.in/notification/csp-2026",
      document: "Notif-CSP-2026-Engl-060226Rev.pdf",
      downloadedDate: "2026-09-15",
    },
    examInformation: {
      conductingBody: "Union Public Service Commission",
      releaseDate: "2026-02-04",
      applicationStartDate: "2026-02-04",
      applicationEndDate: "2026-02-27",
      examDates: ["2026-05-24"],
    },
    eligibilityInformation: {
      minAge: 21,
      maxAge: 32,
      educationalQualification: "Graduate degree",
      nationality: "India (Nepal/Bhutan under conditions)",
      workExperience: "Not specified",
      otherRequirements: "Number of attempts restricted by category",
    },
    eligibilityRules: {
      logicalOperator: "AND",
      rules: [{ attribute: "Educational Qualification", operator: "=", value: "Graduate" }],
      childGroups: [
        {
          logicalOperator: "OR",
          rules: [
            { attribute: "Nationality", operator: "=", value: "India" },
            { attribute: "Nationality", operator: "=", value: "Nepal" },
          ],
          childGroups: [],
        },
        {
          logicalOperator: "OR",
          rules: [
            { attribute: "CGPA", operator: ">=", value: "7" },
            { attribute: "Percentage", operator: ">=", value: "70" },
          ],
          childGroups: [],
        },
      ],
    },
    evidence: [
      {
        id: "ev-13-1",
        field: "Educational Qualification",
        chunkNumber: 3,
        pageNumbers: [12, 13],
        sourceText: "Candidates must possess a Bachelor's degree from a recognized university or an equivalent qualification.",
      },
      {
        id: "ev-13-2",
        field: "Application End Date",
        chunkNumber: 1,
        pageNumbers: [2],
        sourceText: "Applications must be submitted online on or before 24th February 2026.",
      },
      {
        id: "ev-13-3",
        field: "Application End Date",
        chunkNumber: 2,
        pageNumbers: [3],
        sourceText: "Note: the last date for submission of applications is 27th February 2026, till 6:00 PM, superseding earlier communication.",
      },
      {
        id: "ev-13-4",
        field: "CGPA",
        chunkNumber: 5,
        pageNumbers: [17],
        sourceText: "Candidates applying under the technical services category must have a minimum CGPA of 7.0, or 70% aggregate marks.",
      },
    ],
    conflicts: [
      {
        field: "Application End Date",
        options: [
          { value: "24 Feb 2026", source: "Page 2", evidenceId: "ev-13-2" },
          { value: "27 Feb 2026", source: "Page 3", evidenceId: "ev-13-3" },
        ],
      },
    ],
    validationIssues: [
      "Unsupported eligibility attribute: Age",
      "Application start date is after application end date on one extracted value",
    ],
    feedbackHistory: [
      { version: 1, feedback: "Application end date is incorrect. Please re-check the official notification.", date: "2026-09-14" },
    ],
  },

  // --- Approved example ---
  {
    id: "ext-08",
    examId: "gate-2027",
    examName: "GATE 2027",
    version: 2,
    status: "APPROVED",
    createdDate: "2026-09-14",
    approvedDate: "2026-09-14",
    source: {
      url: "https://gate.iitk.ac.in/notification",
      document: "GATE-2027-Information-Brochure.pdf",
      downloadedDate: "2026-09-13",
    },
    examInformation: {
      conductingBody: "IISc / IIT consortium",
      releaseDate: "2026-08-01",
      applicationStartDate: "2026-08-24",
      applicationEndDate: "2026-10-03",
      examDates: ["2027-02-06", "2027-02-07", "2027-02-13", "2027-02-14"],
    },
    eligibilityInformation: {
      minAge: "Not specified",
      maxAge: "Not specified",
      educationalQualification: "Bachelor's degree in Engineering/Technology/Science",
      nationality: "Not restricted",
      workExperience: "Not specified",
      otherRequirements: "Final-year students may apply provisionally.",
    },
    eligibilityRules: {
      logicalOperator: "AND",
      rules: [
        { attribute: "Educational Qualification", operator: "=", value: "Graduate" },
        { attribute: "Specialization", operator: "=", value: "Engineering" },
      ],
      childGroups: [],
    },
    evidence: [
      {
        id: "ev-08-1",
        field: "Educational Qualification",
        chunkNumber: 2,
        pageNumbers: [4],
        sourceText: "Candidates in the final year of the B.E./B.Tech/B.Arch/B.Sc programme are also eligible to appear.",
      },
    ],
    conflicts: [],
    validationIssues: [],
    feedbackHistory: [],
  },

  // --- Approved example ---
  {
    id: "ext-05",
    examId: "nda-2027",
    examName: "NDA 2027",
    version: 1,
    status: "APPROVED",
    createdDate: "2026-09-10",
    approvedDate: "2026-09-11",
    source: {
      url: "https://upsc.gov.in/notification/nda-2027",
      document: "NDA-I-2027-Notification.pdf",
      downloadedDate: "2026-09-09",
    },
    examInformation: {
      conductingBody: "Union Public Service Commission",
      releaseDate: "2026-12-20",
      applicationStartDate: "2026-12-20",
      applicationEndDate: "2027-01-10",
      examDates: ["2027-04-18"],
    },
    eligibilityInformation: {
      minAge: 16.5,
      maxAge: 19.5,
      educationalQualification: "12th pass",
      nationality: "India",
      workExperience: "Not specified",
      otherRequirements: "Unmarried candidates only.",
    },
    eligibilityRules: {
      logicalOperator: "AND",
      rules: [
        { attribute: "Educational Qualification", operator: "=", value: "12th Pass" },
        { attribute: "Nationality", operator: "=", value: "India" },
      ],
      childGroups: [],
    },
    evidence: [
      {
        id: "ev-05-1",
        field: "Educational Qualification",
        chunkNumber: 1,
        pageNumbers: [1],
        sourceText: "Candidates must have passed Class 12 under the 10+2 pattern of school education.",
      },
    ],
    conflicts: [],
    validationIssues: [],
    feedbackHistory: [],
  },

  // --- Rejected example, retryable ---
  {
    id: "ext-09",
    examId: "cat-2026",
    examName: "CAT 2026",
    version: 1,
    status: "REJECTED",
    createdDate: "2026-09-13",
    rejectFeedback: "Percentage threshold looks off — the notification specifies 50% for general category and 45% for reserved categories separately. Please re-extract both values.",
    source: {
      url: "https://iimcat.ac.in/notification",
      document: "CAT-2026-Notification.pdf",
      downloadedDate: "2026-09-13",
    },
    examInformation: {
      conductingBody: "IIM consortium",
      releaseDate: "2026-08-01",
      applicationStartDate: "2026-08-01",
      applicationEndDate: "2026-09-20",
      examDates: ["2026-11-29"],
    },
    eligibilityInformation: {
      minAge: "Not specified",
      maxAge: "Not specified",
      educationalQualification: "Bachelor's degree",
      nationality: "Not specified",
      workExperience: "Not specified",
      otherRequirements: "Not specified",
    },
    eligibilityRules: {
      logicalOperator: "AND",
      rules: [{ attribute: "Percentage", operator: ">=", value: "50" }],
      childGroups: [],
    },
    evidence: [
      {
        id: "ev-09-1",
        field: "Percentage",
        chunkNumber: 4,
        pageNumbers: [6],
        sourceText: "Candidates must hold a Bachelor's Degree with at least 50% marks.",
      },
    ],
    conflicts: [],
    validationIssues: [],
    feedbackHistory: [],
  },

  // --- Failed example ---
  {
    id: "ext-10",
    examId: "clat-pg-2026",
    examName: "CLAT PG 2026",
    version: 1,
    status: "FAILED",
    createdDate: "2026-09-12",
    failedAt: "2026-09-12",
    failedStage: "EXTRACTING_INFORMATION",
    failedError: "Document parser timed out while extracting tables from page 9 — the source PDF appears to be a scanned image without a text layer.",
    source: {
      url: "https://consortiumofnlus.ac.in/clat-pg-2026",
      document: "CLAT-PG-2026-Notification.pdf",
      downloadedDate: "2026-09-12",
    },
  },
];

// --- Notifications (section 21, basic) ---
export const mockAdminNotifications = [
  {
    id: "an1",
    examName: "UPSC CSE 2026",
    change: "Application deadline changed",
    affectedStudents: 342,
    status: "Sent",
    date: "2026-09-15",
  },
  {
    id: "an2",
    examName: "GATE 2027",
    change: "New exam date session added",
    affectedStudents: 1180,
    status: "Sent",
    date: "2026-09-13",
  },
  {
    id: "an3",
    examName: "CLAT PG 2026",
    change: "Extraction failed — no notification sent",
    affectedStudents: 0,
    status: "Blocked",
    date: "2026-09-12",
  },
];
