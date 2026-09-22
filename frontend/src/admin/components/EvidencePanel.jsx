import { useState } from "react";
import { ChevronDown } from "lucide-react";
import Card from "../../components/ui/Card";

function EvidenceItem({ item, sourceUrl }) {
  return (
    <div className="rounded-lg border border-slate-100 bg-slate-50 p-3">
      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
        <span>Chunk <span className="font-mono text-ink">{item.chunkNumber}</span></span>
        <span>Pages <span className="font-mono text-ink">{item.pageNumbers.join(", ")}</span></span>
      </div>
      <blockquote className="mt-2 border-l-2 border-indigo-200 pl-3 text-sm italic text-slate-600">
        "{item.sourceText}"
      </blockquote>
      {sourceUrl && (
        <a href={sourceUrl} target="_blank" rel="noreferrer" className="mt-2 inline-block text-xs font-medium text-gold hover:underline">
          View Source
        </a>
      )}
    </div>
  );
}

function FieldGroup({ field, items, sourceUrl }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border-b border-slate-100 py-3 last:border-none">
      <button type="button" onClick={() => setOpen((o) => !o)} className="flex w-full items-center justify-between gap-3 text-left">
        <span className="text-sm font-medium text-ink">{field}</span>
        <span className="flex items-center gap-2 text-xs text-slate-400">
          {items.length} evidence entr{items.length === 1 ? "y" : "ies"}
          <ChevronDown size={14} className={`transition-transform ${open ? "rotate-180" : ""}`} />
        </span>
      </button>
      {open && (
        <div className="mt-3 flex flex-col gap-2">
          {items.map((item) => (
            <EvidenceItem key={item.id} item={item} sourceUrl={sourceUrl} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function EvidencePanel({ evidence = [], sourceUrl }) {
  if (evidence.length === 0) return null;
  const byField = evidence.reduce((acc, item) => {
    acc[item.field] = acc[item.field] || [];
    acc[item.field].push(item);
    return acc;
  }, {});

  return (
    <Card>
      <h2 className="mb-1 font-mono text-xs uppercase tracking-wide text-slate-400">Evidence / Provenance</h2>
      <p className="mb-3 text-xs text-slate-400">Every extracted value traces back to a chunk, page, and the original document text.</p>
      <div className="flex flex-col">
        {Object.entries(byField).map(([field, items]) => (
          <FieldGroup key={field} field={field} items={items} sourceUrl={sourceUrl} />
        ))}
      </div>
    </Card>
  );
}
