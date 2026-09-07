import { NavLink, Outlet, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  ListChecks,
  CalendarClock,
  Bell,
  Search,
  UserRound,
  LogOut,
} from "lucide-react";
import Logo from "../ui/Logo";
import { useAuth } from "../../context/AuthContext";
import { useNotifications } from "../../context/NotificationsContext";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/eligibility", label: "Eligibility", icon: ListChecks },
  { to: "/upcoming", label: "Upcoming", icon: CalendarClock },
  { to: "/notifications", label: "Notifications", icon: Bell, badge: true },
  { to: "/search", label: "Search exams", icon: Search },
  { to: "/settings", label: "Profile", icon: UserRound },
];

function NavItem({ to, label, icon: Icon, badge, unreadCount, mobile }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        mobile
          ? `flex flex-1 flex-col items-center gap-1 py-2 text-[11px] font-medium ${
              isActive ? "text-indigo-700" : "text-slate-400"
            }`
          : `relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${
              isActive ? "bg-indigo-50 text-indigo-700" : "text-slate-600 hover:bg-slate-50 hover:text-ink"
            }`
      }
    >
      <span className="relative">
        <Icon size={mobile ? 20 : 18} strokeWidth={2} />
        {badge && unreadCount > 0 && (
          <span className="absolute -right-1.5 -top-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-amber-500 px-1 text-[10px] font-semibold text-white">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </span>
      {label}
    </NavLink>
  );
}

export default function AppShell() {
  const { user, logout } = useAuth();
  const { unreadCount } = useNotifications();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <div className="min-h-screen bg-paper md:flex">
      {/* Desktop sidebar */}
      <aside className="hidden w-64 shrink-0 flex-col border-r border-slate-200/70 bg-white/60 px-4 py-6 md:flex">
        <div className="px-2 pb-8">
          <Logo />
        </div>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <NavItem key={item.to} {...item} unreadCount={unreadCount} />
          ))}
        </nav>
        <div className="mt-auto flex items-center justify-between gap-2 rounded-xl px-3 py-3">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-ink">{user?.name}</p>
            <p className="truncate text-xs text-slate-400">{user?.email}</p>
          </div>
          <button
            onClick={handleLogout}
            aria-label="Log out"
            className="rounded-lg p-2 text-slate-400 transition hover:bg-slate-50 hover:text-amber-600"
          >
            <LogOut size={16} />
          </button>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1">
        <main className="mx-auto max-w-5xl px-5 pb-24 pt-6 md:px-8 md:pb-10 md:pt-8">
          <Outlet />
        </main>
      </div>

      {/* Mobile bottom bar */}
      <nav className="fixed inset-x-0 bottom-0 z-30 flex border-t border-slate-200 bg-white/95 backdrop-blur md:hidden">
        {NAV_ITEMS.map((item) => (
          <NavItem key={item.to} {...item} unreadCount={unreadCount} mobile />
        ))}
      </nav>
    </div>
  );
}
