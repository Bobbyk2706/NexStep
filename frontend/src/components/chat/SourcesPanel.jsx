import { useState } from "react";
import { ChevronDown } from "lucide-react";

export default function SourcesPanel({ sources = [] }) {
  const [expandedId, setExpandedId] = useState(null);
  if (sources.length === 0) return null;

  return (
    <div className="mt-4 border-t border-slate-200 pt-3">
      <p className="eyebrow mb-2">Sources</p>
      <div className="flex flex-col">
        {sources.map((source, i) => {
          const isOpen = expandedId === source.id;
          return (
            <button
              key={source.id}
              onClick={() => setExpandedId(isOpen ? null : source.id)}
              className="group flex flex-col gap-1 border-b border-slate-100 py-2 text-left last:border-none"
            >
              <span className="flex items-center justify-between gap-3">
                <span className="flex items-baseline gap-3">
                  <span className="font-mono text-[12px] text-gold">{String(i + 1).padStart(2, "0")}</span>
                  <span className="text-[13.5px] text-ink transition group-hover:text-slate-600">{source.title}</span>
                </span>
                <ChevronDown size={14} strokeWidth={1.5} className={`shrink-0 text-slate-400 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`} />
              </span>
              {isOpen && (
                <span className="pl-7 font-mono text-[10.5px] uppercase tracking-wide text-slate-400">
                  {source.category}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
