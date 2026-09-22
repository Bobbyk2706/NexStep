// The one visual element that repeats everywhere eligibility is shown:
// dashboard, eligibility list, exam details, search, upcoming exams.
// A filled dot means "you're in", an outline means "not this one",
<<<<<<< HEAD
// amber means the door is closing. Deliberately a bordered tag rather
// than a filled pill — reads as a small printed label, not a SaaS chip.
=======
// amber means the door is closing.
>>>>>>> origin/main

function daysUntil(dateStr) {
  const d = new Date(dateStr);
  if (isNaN(d)) return null;
  const diff = Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
  return diff;
}

export default function EligibilityPill({ eligible, deadline, size = "md" }) {
  const days = deadline ? daysUntil(deadline) : null;
  const closingSoon = eligible && days !== null && days >= 0 && days <= 14;

<<<<<<< HEAD
  const sizeClasses = size === "sm" ? "text-[10px] px-2 py-1" : "text-[11px] px-2.5 py-1.5";
  const base = `inline-flex items-center gap-2 border font-mono uppercase tracking-wide ${sizeClasses}`;

  if (closingSoon) {
    return (
      <span className={`${base} border-amber-300 text-amber-600`}>
        <span className="h-1.5 w-1.5 shrink-0 bg-amber-500" />
=======
  const sizeClasses = size === "sm" ? "text-xs px-2.5 py-1" : "text-sm px-3 py-1.5";

  if (closingSoon) {
    return (
      <span
        className={`inline-flex items-center gap-1.5 rounded-full font-medium ${sizeClasses} bg-amber-50 text-amber-600 ring-1 ring-inset ring-amber-200`}
      >
        <span className="h-1.5 w-1.5 rounded-full bg-amber-500" />
>>>>>>> origin/main
        Closes in {days}d
      </span>
    );
  }

  if (eligible) {
    return (
<<<<<<< HEAD
      <span className={`${base} border-signal-200 text-signal-600`}>
        <span className="h-1.5 w-1.5 shrink-0 bg-signal-500" />
=======
      <span
        className={`inline-flex items-center gap-1.5 rounded-full font-medium ${sizeClasses} bg-signal-50 text-signal-600 ring-1 ring-inset ring-signal-200`}
      >
        <span className="h-1.5 w-1.5 rounded-full bg-signal-500" />
>>>>>>> origin/main
        Eligible
      </span>
    );
  }

  return (
<<<<<<< HEAD
    <span className={`${base} border-slate-200 text-slate-500`}>
      <span className="h-1.5 w-1.5 shrink-0 border border-slate-400" />
=======
    <span
      className={`inline-flex items-center gap-1.5 rounded-full font-medium ${sizeClasses} bg-slate-50 text-slate-600 ring-1 ring-inset ring-slate-200`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-slate-400" />
>>>>>>> origin/main
      Not eligible
    </span>
  );
}
