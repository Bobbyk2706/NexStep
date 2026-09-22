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

// Auth (AdminAuthProvider) is mounted once at the App root now, alongside the
// student AuthProvider — that's what lets the single /login page authenticate
// either role. This sub-router only owns the /admin/* screens themselves.
export default function AdminApp() {
  return (
    <Routes>
      <Route element={<RequireAdminAuth />}>
        <Route element={<AdminShell />}>
          <Route path="dashboard" element={<AdminDashboard />} />
          <Route path="exams" element={<AllExams />} />
          <Route path="exams/new" element={<AddExam />} />
          <Route path="exams/:examId" element={<ExamDetailAdmin />} />
          <Route path="extractions" element={<ExtractionHistory />} />
          <Route path="extractions/:id" element={<ExtractionDetail />} />
          <Route path="notifications" element={<AdminNotifications />} />
        </Route>
      </Route>

      {/* Any unmatched /admin/* path (including the old /admin/login bookmark)
          lands on the guarded dashboard route, which bounces to /login if
          there's no admin session. */}
      <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
    </Routes>
  );
}
