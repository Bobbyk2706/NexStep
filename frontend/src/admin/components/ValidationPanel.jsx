import { AlertCircle } from "lucide-react";

const SEVERITY_STYLE = {
  error: { dot: "bg-red-500", text: "text-red-700", label: "Blocks approval" },
  warning: { dot: "bg-amber-500", text: "text-amber-700", label: "Verify" },
  info: { dot: "bg-slate-400", text: "text-slate-600", label: "Note" },
};

// Accepts plain strings (legacy) or { severity, message, field } objects.
export default function ValidationPanel({ issues = [] }) {
  if (issues.length === 0) return null;

  const items = issues.map((issue) =>
    typeof issue === "string" ? { severity: "warning", message: issue } : issue
  );
  const hasError = items.some((item) => item.severity === "error");

  return (
    <div
      className={`rounded-2xl border p-5 ${
        hasError ? "border-red-200 bg-red-50" : "border-amber-200 bg-amber-50"
      }`}
    >
      <div className={`flex items-center gap-2 ${hasError ? "text-red-600" : "text-amber-600"}`}>
        <AlertCircle size={18} />
        <h2 className="font-display text-base font-semibold">
          Validation Issues
          <span className="ml-2 text-xs font-normal opacity-70">
            {items.length} item{items.length === 1 ? "" : "s"}
          </span>
        </h2>
      </div>
      <ul className="mt-3 flex flex-col gap-2">
        {items.map((item, i) => {
          const style = SEVERITY_STYLE[item.severity] || SEVERITY_STYLE.warning;
          return (
            <li key={i} className={`flex items-start gap-2 text-sm ${style.text}`}>
              <span className={`mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full ${style.dot}`} />
              <span>
                <span className="mr-2 rounded bg-white/70 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wide">
                  {style.label}
                </span>
                {item.message}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
