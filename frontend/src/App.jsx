import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProfileProvider } from "./context/ProfileContext";
import { NotificationsProvider } from "./context/NotificationsContext";
import { RequireAuth, RequireProfile } from "./routes/ProtectedRoute";
<<<<<<< HEAD
import { AdminAuthProvider } from "./admin/context/AdminAuthContext";
=======
>>>>>>> origin/main

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ProfileSetup from "./pages/ProfileSetup";
import Dashboard from "./pages/Dashboard";
import Eligibility from "./pages/Eligibility";
import ExamDetails from "./pages/ExamDetails";
import UpcomingExams from "./pages/UpcomingExams";
import Notifications from "./pages/Notifications";
import SearchExams from "./pages/SearchExams";
import Settings from "./pages/Settings";
<<<<<<< HEAD
import Assistant from "./pages/Assistant";
import AppShell from "./components/layout/AppShell";
import AdminApp from "./admin/AdminApp";
=======
import AppShell from "./components/layout/AppShell";
>>>>>>> origin/main

export default function App() {
  return (
    <AuthProvider>
<<<<<<< HEAD
      <AdminAuthProvider>
        <ProfileProvider>
          <NotificationsProvider>
            <BrowserRouter>
              <Routes>
                {/* Single entry point for everyone — Login itself asks Student or Admin */}
                <Route path="/" element={<Landing />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />

                <Route element={<RequireAuth />}>
                  <Route path="/profile/setup" element={<ProfileSetup />} />

                  <Route element={<RequireProfile />}>
                    <Route element={<AppShell />}>
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/assistant" element={<Assistant />} />
                      <Route path="/eligibility" element={<Eligibility />} />
                      <Route path="/exams/:id" element={<ExamDetails />} />
                      <Route path="/upcoming" element={<UpcomingExams />} />
                      <Route path="/notifications" element={<Notifications />} />
                      <Route path="/search" element={<SearchExams />} />
                      <Route path="/settings" element={<Settings />} />
                    </Route>
                  </Route>
                </Route>

                <Route path="/admin/*" element={<AdminApp />} />

                <Route path="*" element={<Landing />} />
              </Routes>
            </BrowserRouter>
          </NotificationsProvider>
        </ProfileProvider>
      </AdminAuthProvider>
=======
      <ProfileProvider>
        <NotificationsProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />

              <Route element={<RequireAuth />}>
                <Route path="/profile/setup" element={<ProfileSetup />} />

                <Route element={<RequireProfile />}>
                  <Route element={<AppShell />}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/eligibility" element={<Eligibility />} />
                    <Route path="/exams/:id" element={<ExamDetails />} />
                    <Route path="/upcoming" element={<UpcomingExams />} />
                    <Route path="/notifications" element={<Notifications />} />
                    <Route path="/search" element={<SearchExams />} />
                    <Route path="/settings" element={<Settings />} />
                  </Route>
                </Route>
              </Route>

              <Route path="*" element={<Landing />} />
            </Routes>
          </BrowserRouter>
        </NotificationsProvider>
      </ProfileProvider>
>>>>>>> origin/main
    </AuthProvider>
  );
}
