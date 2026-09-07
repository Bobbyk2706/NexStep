import { Link } from "react-router-dom";
import { ListChecks, BellRing, CalendarClock, UserRound, ArrowRight } from "lucide-react";
import PublicNavbar from "../components/layout/PublicNavbar";

const STEPS = [
  { n: "01", title: "Sign up", desc: "Create your NexStep account in under a minute.", lift: "md:translate-y-0" },
  { n: "02", title: "Build your profile", desc: "Academics, qualifications, and work experience — once.", lift: "md:-translate-y-6" },
  { n: "03", title: "Get matched", desc: "NexStep checks every exam's rules against your profile.", lift: "md:-translate-y-12" },
  { n: "04", title: "Apply on time", desc: "See deadlines and exam dates before they sneak up on you.", lift: "md:-translate-y-[4.5rem]" },
];

const FEATURES = [
  {
    icon: ListChecks,
    title: "No searching required",
    desc: "NexStep checks your profile against every exam's eligibility rules automatically — you never pick an exam first.",
  },
  {
    icon: CalendarClock,
    title: "Deadlines that find you",
    desc: "Application windows and exam dates for everything you qualify for, laid out in one timeline.",
  },
  {
    icon: BellRing,
    title: "Told the moment it matters",
    desc: "Newly eligible for something? A deadline closing? You'll know without checking ten different websites.",
  },
  {
    icon: UserRound,
    title: "One profile, every exam",
    desc: "Enter your academic details once. NexStep re-checks them against new exams as they're added.",
  },
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-paper">
      <PublicNavbar />

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pb-20 pt-16 md:pb-28 md:pt-24">
        <div className="grid items-center gap-16 md:grid-cols-2">
          <div>
            <p className="mb-4 font-mono text-xs uppercase tracking-[0.2em] text-indigo-600">
              For students choosing what's next
            </p>
            <h1 className="font-display text-4xl font-semibold leading-[1.08] tracking-tight text-ink md:text-[3.4rem]">
              Stop searching exams.
              <br />
              Let them find <span className="text-indigo-700">you.</span>
            </h1>
            <p className="mt-6 max-w-md text-lg leading-relaxed text-slate-600">
              NexStep reads your academic profile and automatically shows every exam
              you're eligible for — GATE, CAT, GRE, UPSC and more — with deadlines
              tracked from day one.
            </p>
            <div className="mt-9 flex flex-wrap items-center gap-4">
              <Link
                to="/signup"
                className="group inline-flex items-center gap-2 rounded-xl bg-indigo-700 px-5 py-3 text-[15px] font-medium text-white transition hover:bg-indigo-600"
              >
                Get started
                <ArrowRight size={16} className="transition group-hover:translate-x-0.5" />
              </Link>
              <Link
                to="/login"
                className="inline-flex items-center gap-2 rounded-xl px-5 py-3 text-[15px] font-medium text-slate-700 ring-1 ring-inset ring-slate-200 transition hover:bg-white"
              >
                I already have an account
              </Link>
            </div>
          </div>

          {/* Signature: ascending step cards, a literal "next step" */}
          <div id="how-it-works" className="relative mx-auto flex w-full max-w-sm flex-col gap-4 md:flex-row md:items-end md:gap-3">
            <div className="pointer-events-none absolute left-[10px] top-2 hidden h-[calc(100%-1rem)] w-px step-line md:block" />
            {STEPS.map((step) => (
              <div key={step.n} className={`relative flex-1 ${step.lift}`}>
                <div className="rounded-2xl border border-slate-200/70 bg-white p-4 shadow-card">
                  <span className="font-mono text-xs text-indigo-400">{step.n}</span>
                  <h3 className="mt-1 font-display text-[15px] font-semibold text-ink">{step.title}</h3>
                  <p className="mt-1 text-xs leading-relaxed text-slate-500">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="border-t border-slate-200/70 bg-white/60">
        <div className="mx-auto max-w-6xl px-6 py-20">
          <h2 className="max-w-lg font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
            Introducing NexStep
          </h2>
          <p className="mt-3 max-w-xl text-slate-600">
            One place that knows what you've studied, what you've scored, and what
            that qualifies you for right now.
          </p>
          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="rounded-2xl border border-slate-200/70 bg-paper p-5">
                <div className="mb-4 flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-700 text-white">
                  <Icon size={17} />
                </div>
                <h3 className="font-display text-[15px] font-semibold text-ink">{title}</h3>
                <p className="mt-1.5 text-sm leading-relaxed text-slate-500">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-6xl px-6 py-20 text-center">
        <h2 className="mx-auto max-w-xl font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
          Your profile already qualifies you for something. Find out what.
        </h2>
        <Link
          to="/signup"
          className="mt-8 inline-flex items-center gap-2 rounded-xl bg-indigo-700 px-6 py-3 text-[15px] font-medium text-white transition hover:bg-indigo-600"
        >
          Create your NexStep account
          <ArrowRight size={16} />
        </Link>
      </section>

      <footer className="border-t border-slate-200/70 px-6 py-8 text-center text-xs text-slate-400">
        NexStep — built for students figuring out what's next.
      </footer>
    </div>
  );
}
