import { AlertTriangle } from "lucide-react";

export default function ConflictPanel({ conflicts = [] }) {
  if (conflicts.length === 0) return null;
  return (
    <div className="rounded-2xl border-2 border-red-200 bg-red-50 p-5">
      <div className="flex items-center gap-2 text-red-700">
        <AlertTriangle size={18} />
        <h2 className="font-display text-base font-semibold">Conflict Detected</h2>
      </div>
      <p className="mt-1 text-sm text-red-600">Administrator review required — the system will not select one value automatically.</p>
      <div className="mt-4 flex flex-col gap-4">
        {conflicts.map((conflict, i) => (
          <div key={i}>
            <p className="text-sm font-medium text-ink">{conflict.field}</p>
            <div className="mt-2 grid gap-2 sm:grid-cols-2">
              {conflict.options.map((opt, j) => (
                <div key={j} className="rounded-xl border border-red-200 bg-slate-50 p-3">
                  <p className="text-xs text-slate-400">Extraction {String.fromCharCode(65 + j)}</p>
                  <p className="mt-0.5 font-mono text-sm font-semibold text-ink">{opt.value}</p>
                  <p className="mt-0.5 text-xs text-slate-500">Source: {opt.source}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
