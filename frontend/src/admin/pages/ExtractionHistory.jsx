import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import Card from "../../components/ui/Card";
import StatusBadge from "../components/StatusBadge";
import { listExtractions } from "../api/adminExtractions";
import { formatDate } from "../../utils/date";

const FILTERS = ["All", "PENDING_REVIEW", "APPROVED", "REJECTED", "FAILED"];
const FILTER_LABELS = { All: "All", PENDING_REVIEW: "Pending", APPROVED: "Approved", REJECTED: "Rejected", FAILED: "Failed" };

export default function ExtractionHistory() {
  const [searchParams, setSearchParams] = useSearchParams();
  const status = searchParams.get("status") || "All";
  const [query, setQuery] = useState("");
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    listExtractions({ status }).then((data) => {
      setRows(data);
      setLoading(false);
    });
  }, [status]);

  const filtered = useMemo(() => {
    if (!query.trim()) return rows;
    const q = query.trim().toLowerCase();
    return rows.filter((r) => r.examName.toLowerCase().includes(q));
  }, [rows, query]);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Extraction History</h1>
        <p className="mt-1.5 text-slate-600">Every extraction ever generated, across every version.</p>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap gap-2">
          {FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setSearchParams(f === "All" ? {} : { status: f })}
              className={`rounded-xl px-3.5 py-1.5 text-sm font-medium transition ${
                status === f ? "bg-indigo-700 text-white" : "bg-surface text-slate-600 ring-1 ring-inset ring-slate-200 hover:bg-slate-50"
              }`}
            >
              {FILTER_LABELS[f]}
            </button>
          ))}
        </div>
        <div className="relative">
          <Search size={15} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search exam name..."
            className="w-56 rounded-xl border border-slate-200 bg-slate-50 py-2 pl-9 pr-3 text-sm text-ink placeholder:text-slate-400 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
          />
        </div>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
                <th className="pb-2 font-medium">Exam</th>
                <th className="pb-2 font-medium">Version</th>
                <th className="pb-2 font-medium">Status</th>
                <th className="pb-2 font-medium">Created</th>
                <th className="pb-2 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {!loading && filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="py-6 text-center text-sm text-slate-400">No extractions match this view.</td>
                </tr>
              )}
              {filtered.map((row) => (
                <tr key={row.id} className="border-b border-slate-50 last:border-none">
                  <td className="py-3 font-medium text-ink">{row.examName}</td>
                  <td className="py-3 text-slate-500">{row.version}</td>
                  <td className="py-3"><StatusBadge status={row.status} size="sm" /></td>
                  <td className="py-3 text-slate-500">{formatDate(row.createdDate)}</td>
                  <td className="py-3 text-right">
                    <Link to={`/admin/extractions/${row.id}`} className="font-medium text-gold hover:underline">
                      {row.status === "PENDING_REVIEW" ? "Review" : "View"}
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
