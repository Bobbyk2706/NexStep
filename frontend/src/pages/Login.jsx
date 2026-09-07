import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PublicNavbar from "../components/layout/PublicNavbar";
import { TextField } from "../components/ui/Field";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
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

  async function handleSubmit(e) {
    e.preventDefault();
    setFormError("");
    if (!validate()) return;
    setLoading(true);
    try {
      const res = await login(form);
      navigate(res.hasProfile ? "/dashboard" : "/profile/setup");
    } catch (err) {
      setFormError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-paper">
      <PublicNavbar />
      <div className="mx-auto flex max-w-md flex-col px-6 py-16">
        <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">Welcome back</h1>
        <p className="mt-2 text-slate-600">Log in to see what you're eligible for.</p>

        <form onSubmit={handleSubmit} noValidate className="mt-8 flex flex-col gap-5">
          {formError && (
            <p className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
              {formError}
            </p>
          )}
          <TextField
            id="email"
            label="Email"
            type="email"
            autoComplete="email"
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
        </p>
      </div>
    </div>
  );
}
