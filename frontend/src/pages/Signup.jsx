import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PublicNavbar from "../components/layout/PublicNavbar";
import { TextField } from "../components/ui/Field";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [loading, setLoading] = useState(false);

  function validate() {
    const next = {};
    if (!form.name.trim()) next.name = "Enter your full name.";
    if (!/^\S+@\S+\.\S+$/.test(form.email)) next.email = "Enter a valid email address.";
    if (form.password.length < 6) next.password = "Password must be at least 6 characters.";
    if (form.confirm !== form.password) next.confirm = "Passwords don't match.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setFormError("");
    if (!validate()) return;
    setLoading(true);
    try {
      await signup(form);
      navigate("/profile/setup");
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
        <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">Create your account</h1>
        <p className="mt-2 text-slate-600">Takes a minute. Your eligibility results take zero.</p>

        <form onSubmit={handleSubmit} noValidate className="mt-8 flex flex-col gap-5">
          {formError && (
            <p className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
              {formError}
            </p>
          )}
          <TextField
            id="name"
            label="Full name"
            autoComplete="name"
            required
            value={form.name}
            error={errors.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
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
            autoComplete="new-password"
            required
            hint="At least 6 characters."
            value={form.password}
            error={errors.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <TextField
            id="confirm"
            label="Confirm password"
            type="password"
            autoComplete="new-password"
            required
            value={form.confirm}
            error={errors.confirm}
            onChange={(e) => setForm({ ...form, confirm: e.target.value })}
          />
          <Button type="submit" loading={loading} className="mt-2 w-full">
            Create account
          </Button>
        </form>

        <p className="mt-8 text-center text-sm text-slate-500">
          Already on NexStep?{" "}
          <Link to="/login" className="font-medium text-indigo-700 hover:underline">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
