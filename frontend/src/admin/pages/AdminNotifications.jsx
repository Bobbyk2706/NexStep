import { useEffect, useState } from "react";
import Card from "../../components/ui/Card";
import { listExtractions } from "../api/adminExtractions";
import { formatDate } from "../../utils/date";

export default function AdminNotifications() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    listExtractions()
      .then((data) => {
        if (!active) return;
        setRows(data.filter((row) => row.changeDetected || row.changeDetails));
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Notifications</h1>
        <p className="mt-1.5 text-slate-600">
          Extraction records where the backend detected a change or stored review details.
        </p>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
                <th className="pb-2 font-medium">Exam</th>
                <th className="pb-2 font-medium">Change</th>
                <th className="pb-2 font-medium">Status</th>
                <th className="pb-2 font-medium">Date</th>
              </tr>
            </thead>
            <tbody>
              {!loading && rows.length === 0 && (
                <tr>
                  <td colSpan={4} className="py-6 text-center text-sm text-slate-400">
                    No change notifications have been recorded.
                  </td>
                </tr>
              )}
              {rows.map((row) => (
                <tr key={row.id} className="border-b border-slate-50 last:border-none">
                  <td className="py-3 font-medium text-ink">{row.examName}</td>
                  <td className="max-w-md py-3 text-slate-600">
                    {row.changeDetails || "Change detected by backend."}
                  </td>
                  <td className="py-3">
                    <span className="border border-slate-200 px-2.5 py-1 font-mono text-[11px] uppercase tracking-wide text-slate-500">
                      {row.status}
                    </span>
                  </td>
                  <td className="py-3 text-slate-500">{formatDate(row.createdDate)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
