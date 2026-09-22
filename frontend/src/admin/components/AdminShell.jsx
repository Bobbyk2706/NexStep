import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { LayoutDashboard, FileStack, FilePlus2, Inbox, History, Bell, LogOut } from "lucide-react";
import { useAdminAuth } from "../context/AdminAuthContext";

const NAV_ITEMS = [
  { to: "/admin/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/admin/exams", label: "All Exams", icon: FileStack },
  { to: "/admin/exams/new", label: "Add Exam", icon: FilePlus2 },
  { to: "/admin/extractions?status=PENDING_REVIEW", label: "Pending Review", icon: Inbox },
  { to: "/admin/extractions", label: "Extraction History", icon: History, end: true },
  { to: "/admin/notifications", label: "Notifications", icon: Bell },
];

export default function AdminShell() {
  const { admin, logout } = useAdminAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-paper md:flex">
      <aside className="flex w-full shrink-0 flex-col bg-ink px-4 py-6 md:w-64 md:min-h-screen">
        <div className="flex items-center gap-2 px-2 pb-8">
          <span className="font-display text-lg font-semibold tracking-tight text-white">
            Nex<span className="text-indigo-300">Step</span>
          </span>
          <span className="rounded-md bg-white/10 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-indigo-200">
            Admin
          </span>
        </div>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to + item.label}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
                  isActive ? "bg-white/10 text-white" : "text-slate-300 hover:bg-white/5 hover:text-white"
                }`
              }
            >
              <item.icon size={17} strokeWidth={2} />
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-auto flex items-center justify-between gap-2 rounded-xl px-3 py-3">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-white">{admin?.name}</p>
            <p className="truncate text-xs text-slate-300">{admin?.email}</p>
          </div>
          <button onClick={handleLogout} aria-label="Log out" className="rounded-lg p-2 text-slate-300 transition hover:bg-white/10 hover:text-amber-300">
            <LogOut size={16} />
          </button>
        </div>
      </aside>

      <main className="flex-1">
        <div className="mx-auto max-w-5xl px-5 py-8 md:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
