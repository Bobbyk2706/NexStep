import { ExternalLink, FileText } from "lucide-react";
import Card from "../../components/ui/Card";

export default function SourceInfoCard({ source }) {
  if (!source) return null;
  return (
    <Card>
      <h2 className="mb-4 font-mono text-xs uppercase tracking-wide text-slate-400">Official Source</h2>
      <div className="flex flex-col gap-3 text-sm">
        <div>
          <p className="text-xs text-slate-400">Source URL</p>
          <p className="truncate text-ink">{source.url}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Document</p>
          <p className="flex items-center gap-1.5 text-ink"><FileText size={14} className="shrink-0 text-slate-400" />{source.document}</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Downloaded</p>
          <p className="text-ink">{source.downloadedDate}</p>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <a
          href={source.url}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 rounded-xl px-3.5 py-2 text-sm font-medium text-gold ring-1 ring-inset ring-indigo-100 transition hover:bg-indigo-50"
        >
          Open Official Source <ExternalLink size={14} />
        </a>
        <a
          href={source.url}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-1.5 rounded-xl px-3.5 py-2 text-sm font-medium text-slate-600 ring-1 ring-inset ring-slate-200 transition hover:bg-slate-50"
        >
          View PDF <FileText size={14} />
        </a>
      </div>
    </Card>
  );
}
