import { Link } from "react-router-dom";
import Logo from "../ui/Logo";

export default function PublicNavbar() {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/70 bg-paper/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="flex items-center gap-2">
          <Logo />
        </Link>
        <nav className="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
          <a href="#features" className="hover:text-ink">Features</a>
          <a href="#how-it-works" className="hover:text-ink">How it works</a>
        </nav>
        <div className="flex items-center gap-3">
          <Link to="/login" className="text-sm font-medium text-slate-700 hover:text-ink">
            Log in
          </Link>
          <Link
            to="/signup"
            className="rounded-xl bg-indigo-700 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-600"
          >
            Sign up
          </Link>
        </div>
      </div>
    </header>
  );
}
