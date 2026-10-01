import { Routes, Route, Navigate } from "react-router-dom";
import { RequireAdminAuth } from "./routes/AdminProtectedRoute";
import AdminShell from "./components/AdminShell";

import AdminDashboard from "./pages/AdminDashboard";
import AddExam from "./pages/AddExam";
import ExtractionDetail from "./pages/ExtractionDetail";
import ExtractionHistory from "./pages/ExtractionHistory";
import AllExams from "./pages/AllExams";
import ExamDetailAdmin from "./pages/ExamDetailAdmin";
import AdminNotifications from "./pages/AdminNotifications";

import MonitoringReviews from "./pages/MonitoringReviews";
import MonitoringReviewDetail from "./pages/MonitoringReviewDetail";

// Auth (AdminAuthProvider) is mounted once at the App root now,
// alongside the student AuthProvider. This sub-router only owns
// the /admin/* screens themselves.
export default function AdminApp() {
  return (
    <Routes>
      <Route element={<RequireAdminAuth />}>
        <Route element={<AdminShell />}>
          {/* Dashboard */}
          <Route
            path="dashboard"
            element={<AdminDashboard />}
          />

          {/* Exams */}
          <Route
            path="exams"
            element={<AllExams />}
          />

          <Route
            path="exams/new"
            element={<AddExam />}
          />

          <Route
            path="exams/:examId"
            element={<ExamDetailAdmin />}
          />

          {/* Extraction pipeline */}
          <Route
            path="extractions"
            element={<ExtractionHistory />}
          />

          <Route
            path="extractions/:id"
            element={<ExtractionDetail />}
          />

          {/* Notifications */}
          <Route
            path="notifications"
            element={<AdminNotifications />}
          />

          {/* Document Monitoring */}
          <Route
            path="monitoring"
            element={<MonitoringReviews />}
          />

          <Route
            path="monitoring/reviews"
            element={<MonitoringReviews />}
          />

          <Route
            path="monitoring/reviews/:reviewId"
            element={<MonitoringReviewDetail />}
          />
        </Route>
      </Route>

      {/* Any unmatched /admin/* path lands on the guarded dashboard route.
          If there is no admin session, RequireAdminAuth redirects to /login. */}
      <Route
        path="*"
        element={<Navigate to="/admin/dashboard" replace />}
      />
    </Routes>
  );
}