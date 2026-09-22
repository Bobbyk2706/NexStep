import { isProcessingStatus } from "../api/adminData";

const META = {
  PENDING_REVIEW: { label: "Pending Review", className: "border-amber-300 text-amber-600" },
  APPROVED: { label: "Approved", className: "border-signal-200 text-signal-600" },
  REJECTED: { label: "Rejected", className: "border-red-300 text-red-600" },
  FAILED: { label: "Failed", className: "border-red-500 text-red-700" },
};

export default function StatusBadge({ status, size = "md" }) {
  const sizeClasses = size === "sm" ? "text-[10px] px-2 py-1" : "text-[11px] px-2.5 py-1.5";
  const base = `inline-flex items-center gap-2 border font-mono uppercase tracking-wide ${sizeClasses}`;

  if (isProcessingStatus(status)) {
    return (
      <span className={`${base} border-indigo-200 text-gold`}>
        <span className="h-1.5 w-1.5 shrink-0 animate-pulse bg-gold" />
        Processing
      </span>
    );
  }

  const meta = META[status] || { label: status, className: "border-slate-200 text-slate-500" };
  return (
    <span className={`${base} ${meta.className}`}>
      <span className="h-1.5 w-1.5 shrink-0 bg-current" />
      {meta.label}
    </span>
  );
}
