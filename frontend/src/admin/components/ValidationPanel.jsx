import { AlertCircle } from "lucide-react";

export default function ValidationPanel({ issues = [] }) {
  if (issues.length === 0) return null;
  return (
    <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5">
      <div className="flex items-center gap-2 text-amber-600">
        <AlertCircle size={18} />
        <h2 className="font-display text-base font-semibold">Validation Issues</h2>
      </div>
      <ul className="mt-3 flex flex-col gap-1.5">
        {issues.map((issue, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-amber-700">
            <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-amber-500" />
            {issue}
          </li>
        ))}
      </ul>
    </div>
  );
}
