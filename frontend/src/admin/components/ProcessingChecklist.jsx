import { Check, Circle } from "lucide-react";
import { STAGE_SEQUENCE } from "../api/adminData";

export default function ProcessingChecklist({ currentStatus }) {
  const currentIdx = STAGE_SEQUENCE.findIndex((s) => s.key === currentStatus);

  return (
    <div className="flex flex-col gap-1">
      {STAGE_SEQUENCE.map((stage, i) => {
        const done = i < currentIdx;
        const active = i === currentIdx;
        return (
          <div key={stage.key} className="flex items-center gap-3 py-1.5">
            <span
              className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full ${
                done ? "bg-signal-500 text-white" : active ? "bg-indigo-700 text-white" : "bg-slate-100 text-slate-300"
              }`}
            >
              {done ? <Check size={12} /> : active ? <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-surface" /> : <Circle size={8} />}
            </span>
            <span className={`text-sm ${done ? "text-slate-400 line-through" : active ? "font-medium text-ink" : "text-slate-400"}`}>
              {stage.label}
            </span>
          </div>
        );
      })}
    </div>
  );
}
