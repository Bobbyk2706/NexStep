import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
<<<<<<< HEAD
import { GraduationCap, ShieldCheck } from "lucide-react";
=======
>>>>>>> origin/main
import PublicNavbar from "../components/layout/PublicNavbar";
import { TextField } from "../components/ui/Field";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";
<<<<<<< HEAD
import { useAdminAuth } from "../admin/context/AdminAuthContext";

const ROLES = [
  { key: "student", label: "Student", icon: GraduationCap },
  { key: "admin", label: "Admin", icon: ShieldCheck },
];

const COPY = {
  student: {
    heading: "Welcome back",
    subheading: "Log in to see what you're eligible for.",
  },
  admin: {
    heading: "Admin sign in",
    subheading: "Review extractions and manage exam data.",
  },
};

// One login screen for both roles. The person picks Student or Admin, the
// same email/password form submits to whichever auth context matches, and
// each landing page/route guard already knows where to send them from there.
// Student and admin sessions are stored under separate keys (see
// api/client.js vs admin/api/adminAuth.js), so picking one here never signs
// the person into the other.
export default function Login() {
  const { login: studentLogin } = useAuth();
  const { login: adminLogin } = useAdminAuth();
  const navigate = useNavigate();

  const [role, setRole] = useState("student");
=======

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
>>>>>>> origin/main
  const [form, setForm] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [loading, setLoading] = useState(false);

  function validate() {
    const next = {};
    if (!/^\S+@\S+\.\S+$/.test(form.email)) next.email = "Enter a valid email address.";
    if (form.password.length < 6) next.password = "Password must be at least 6 characters.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

<<<<<<< HEAD
  function switchRole(nextRole) {
    if (nextRole === role) return;
    setRole(nextRole);
    setErrors({});
    setFormError("");
  }

=======
>>>>>>> origin/main
  async function handleSubmit(e) {
    e.preventDefault();
    setFormError("");
    if (!validate()) return;
    setLoading(true);
    try {
<<<<<<< HEAD
      if (role === "admin") {
        await adminLogin(form);
        navigate("/admin/dashboard");
      } else {
        const res = await studentLogin(form);
        navigate(res.hasProfile ? "/dashboard" : "/profile/setup");
      }
=======
      const res = await login(form);
      navigate(res.hasProfile ? "/dashboard" : "/profile/setup");
>>>>>>> origin/main
    } catch (err) {
      setFormError(err.message);
    } finally {
      setLoading(false);
    }
  }

<<<<<<< HEAD
  const copy = COPY[role];

=======
>>>>>>> origin/main
  return (
    <div className="min-h-screen bg-paper">
      <PublicNavbar />
      <div className="mx-auto flex max-w-md flex-col px-6 py-16">
<<<<<<< HEAD
        <div
          role="tablist"
          aria-label="Log in as"
          className="mb-7 inline-flex w-fit gap-1 rounded-xl bg-white p-1 ring-1 ring-inset ring-slate-200"
        >
          {ROLES.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              type="button"
              role="tab"
              aria-selected={role === key}
              onClick={() => switchRole(key)}
              className={`flex items-center gap-1.5 rounded-lg px-4 py-2 text-sm font-medium transition ${
                role === key ? "bg-indigo-700 text-white" : "text-slate-500 hover:text-ink"
              }`}
            >
              <Icon size={15} />
              {label}
            </button>
          ))}
        </div>

        <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">{copy.heading}</h1>
        <p className="mt-2 text-slate-600">{copy.subheading}</p>
=======
        <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">Welcome back</h1>
        <p className="mt-2 text-slate-600">Log in to see what you're eligible for.</p>
>>>>>>> origin/main

        <form onSubmit={handleSubmit} noValidate className="mt-8 flex flex-col gap-5">
          {formError && (
            <p className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
              {formError}
            </p>
          )}
          <TextField
            id="email"
<<<<<<< HEAD
            label={role === "admin" ? "Email / Username" : "Email"}
            type="email"
            autoComplete="username"
=======
            label="Email"
            type="email"
            autoComplete="email"
>>>>>>> origin/main
            required
            value={form.email}
            error={errors.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <TextField
            id="password"
            label="Password"
            type="password"
            autoComplete="current-password"
            required
            value={form.password}
            error={errors.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <Button type="submit" loading={loading} className="mt-2 w-full">
<<<<<<< HEAD
            {role === "admin" ? "Log in to admin" : "Log in"}
          </Button>
        </form>

        {role === "student" ? (
          <p className="mt-8 text-center text-sm text-slate-500">
            New to NexStep?{" "}
            <Link to="/signup" className="font-medium text-gold hover:underline">
              Create an account
            </Link>
          </p>
        ) : (
          <p className="mt-8 text-center text-sm text-slate-500">
            Admin accounts are provisioned by your team, not self-service.
          </p>
        )}

        <p className="mt-6 text-center text-xs text-slate-400">
          Mock authentication — any 6+ character password works for either role. Student and admin
          sessions are stored separately, so choosing one never affects the other.
=======
            Log in
          </Button>
        </form>

        <p className="mt-8 text-center text-sm text-slate-500">
          New to NexStep?{" "}
          <Link to="/signup" className="font-medium text-indigo-700 hover:underline">
            Create an account
          </Link>
        </p>
        <p className="mt-6 text-center text-xs text-slate-400">
          Authentication runs on a mock layer for now — any 6+ character password works. Real login
          connects through Vivek's JWT API.
>>>>>>> origin/main
        </p>
      </div>
    </div>
  );
}
