import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import PublicNavbar from "../components/layout/PublicNavbar";
import { TextField } from "../components/ui/Field";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const { startSignup, verifySignup, resendSignupCode } = useAuth();
  const navigate = useNavigate();

  const [step, setStep] = useState("form"); // "form" -> "verify"
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [code, setCode] = useState("");
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [cooldown, setCooldown] = useState(0);

  // Counts down the "resend" wait.
  useEffect(() => {
    if (cooldown <= 0) return undefined;
    const timer = setTimeout(() => setCooldown((s) => s - 1), 1000);
    return () => clearTimeout(timer);
  }, [cooldown]);

  function validate() {
    const next = {};
    if (!form.name.trim()) next.name = "Enter your full name.";
    if (!/^\S+@\S+\.\S{2,}$/.test(form.email.trim())) next.email = "Enter a valid email address.";
    if (form.password.length < 6) next.password = "Password must be at least 6 characters.";
    if (form.confirm !== form.password) next.confirm = "Passwords don't match.";
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  // Step 1: email the code. No account is created yet.
  async function handleStart(e) {
    e.preventDefault();
    setFormError("");
    setNotice("");
    if (!validate()) return;
    setLoading(true);
    try {
      const res = await startSignup(form);
      setCooldown(res?.resendAfterSeconds ?? 60);
      setCode("");
      setStep("verify");
    } catch (err) {
      setFormError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Step 2: confirm the code. The account is created only now.
  async function handleVerify(e) {
    e.preventDefault();
    setFormError("");
    setNotice("");
    if (!/^\d{6}$/.test(code)) {
      setFormError("Enter the 6-digit code from your email.");
      return;
    }
    setLoading(true);
    try {
      await verifySignup(form.email, code);
      navigate("/profile/setup");
    } catch (err) {
      setFormError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleResend() {
    setFormError("");
    setNotice("");
    setResending(true);
    try {
      const res = await resendSignupCode(form.email);
      setCooldown(res?.resendAfterSeconds ?? 60);
      setCode("");
      setNotice("We sent you a new code.");
    } catch (err) {
      setFormError(err.message);
    } finally {
      setResending(false);
    }
  }

  function backToForm() {
    setStep("form");
    setCode("");
    setFormError("");
    setNotice("");
  }

  return (
    <div className="min-h-screen bg-paper">
      <PublicNavbar />
      <div className="mx-auto flex max-w-md flex-col px-6 py-16">
        {step === "form" ? (
          <>
            <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">Create your account</h1>
            <p className="mt-2 text-slate-600">
              Takes a minute. We'll email you a code to confirm your address.
            </p>

            <form onSubmit={handleStart} noValidate className="mt-8 flex flex-col gap-5">
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
                Send verification code
              </Button>
            </form>

            <p className="mt-8 text-center text-sm text-slate-500">
              Already on NexStep?{" "}
              <Link to="/login" className="font-medium text-gold hover:underline">
                Log in
              </Link>
            </p>
          </>
        ) : (
          <>
            <h1 className="font-display text-3xl font-semibold tracking-tight text-ink">Check your email</h1>
            <p className="mt-2 text-slate-600">
              We sent a 6-digit code to <span className="font-medium text-ink">{form.email.trim()}</span>.
              It expires in 10 minutes. Your account is created once you confirm it.
            </p>

            <form onSubmit={handleVerify} noValidate className="mt-8 flex flex-col gap-5">
              {formError && (
                <p className="rounded-xl bg-amber-50 px-3.5 py-2.5 text-sm text-amber-600 ring-1 ring-inset ring-amber-200">
                  {formError}
                </p>
              )}
              {notice && (
                <p className="rounded-xl bg-signal-50 px-3.5 py-2.5 text-sm text-signal-600 ring-1 ring-inset ring-slate-200">
                  {notice}
                </p>
              )}
              <TextField
                id="code"
                label="Verification code"
                autoComplete="one-time-code"
                inputMode="numeric"
                placeholder="123456"
                required
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
              />
              <Button type="submit" loading={loading} className="w-full">
                Verify and create account
              </Button>
            </form>

            <div className="mt-6 flex flex-col items-center gap-2 text-sm text-slate-500">
              <button
                type="button"
                onClick={handleResend}
                disabled={cooldown > 0 || resending}
                className="font-medium text-gold hover:underline disabled:cursor-not-allowed disabled:opacity-50 disabled:no-underline"
              >
                {resending
                  ? "Sending…"
                  : cooldown > 0
                  ? `Resend code in ${cooldown}s`
                  : "Resend code"}
              </button>
              <button type="button" onClick={backToForm} className="hover:underline">
                Use a different email
              </button>
              <p className="text-xs text-slate-400">Can't find it? Check your spam folder.</p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}