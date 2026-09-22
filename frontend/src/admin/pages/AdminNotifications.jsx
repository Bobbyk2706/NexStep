import { useEffect, useState } from "react";
import Card from "../../components/ui/Card";
import { mockAdminNotifications } from "../api/adminData";
import { formatDate } from "../../utils/date";

export default function AdminNotifications() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    // Mocked directly for now — real version:
    // request("/admin/notifications").then(setRows)
    setRows(mockAdminNotifications);
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Notifications</h1>
        <p className="mt-1.5 text-slate-600">
          Changes detected in approved exams and how many students were notified. More detail lands once
          monitoring/change detection is implemented.
        </p>
      </div>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-xs uppercase tracking-wide text-slate-400">
                <th className="pb-2 font-medium">Exam</th>
                <th className="pb-2 font-medium">Change Detected</th>
                <th className="pb-2 font-medium">Affected Students</th>
                <th className="pb-2 font-medium">Status</th>
                <th className="pb-2 font-medium">Date</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.id} className="border-b border-slate-50 last:border-none">
                  <td className="py-3 font-medium text-ink">{row.examName}</td>
                  <td className="py-3 text-slate-600">{row.change}</td>
                  <td className="py-3 text-slate-500">{row.affectedStudents}</td>
                  <td className="py-3">
                    <span className={`border px-2.5 py-1 font-mono text-[11px] uppercase tracking-wide ${row.status === "Sent" ? "border-signal-200 text-signal-600" : "border-slate-200 text-slate-500"}`}>
                      {row.status}
                    </span>
                  </td>
                  <td className="py-3 text-slate-500">{formatDate(row.date)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
