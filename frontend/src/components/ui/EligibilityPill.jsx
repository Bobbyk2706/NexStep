// The one visual element that repeats everywhere eligibility is shown:
// dashboard, eligibility list, exam details, search, upcoming exams.
// A filled dot means "you're in", an outline means "not this one",
// amber means the door is closing. Deliberately a bordered tag rather
// than a filled pill — reads as a small printed label, not a SaaS chip.

function daysUntil(dateStr) {
  const d = new Date(dateStr);
  if (isNaN(d)) return null;
  const diff = Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
  return diff;
}

export default function EligibilityPill({ eligible, deadline, size = "md" }) {
  const days = deadline ? daysUntil(deadline) : null;
  const closingSoon = eligible && days !== null && days >= 0 && days <= 14;

  const sizeClasses = size === "sm" ? "text-[10px] px-2 py-1" : "text-[11px] px-2.5 py-1.5";
  const base = `inline-flex items-center gap-2 border font-mono uppercase tracking-wide ${sizeClasses}`;

  if (closingSoon) {
    return (
      <span className={`${base} border-amber-300 text-amber-600`}>
        <span className="h-1.5 w-1.5 shrink-0 bg-amber-500" />
        Closes in {days}d
      </span>
    );
  }

  if (eligible) {
    return (
      <span className={`${base} border-signal-200 text-signal-600`}>
        <span className="h-1.5 w-1.5 shrink-0 bg-signal-500" />
        Eligible
      </span>
    );
  }

  return (
    <span className={`${base} border-slate-200 text-slate-500`}>
      <span className="h-1.5 w-1.5 shrink-0 border border-slate-400" />
      Not eligible
    </span>
  );
}
