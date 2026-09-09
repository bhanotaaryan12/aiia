"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function VisitsPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/visits/?limit=100").then(r => { setData(Array.isArray(r.data) ? r.data : []); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3].map(i => <div key={i} className="h-12 bg-gray-200 rounded" />)}</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Visit Schedule</h1>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Visit</th><th className="text-left px-4 py-3 font-medium text-gray-600">Status</th><th className="text-left px-4 py-3 font-medium text-gray-600">Scheduled</th><th className="text-left px-4 py-3 font-medium text-gray-600">Actual</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {data.map((item: any, idx: number) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-gray-600">{String(item.visit_name ?? "—").substring(0, 60)}</td><td className="px-4 py-3 text-gray-600">{String(item.status ?? "—").substring(0, 60)}</td><td className="px-4 py-3 text-gray-600">{String(item.scheduled_date ?? "—").substring(0, 60)}</td><td className="px-4 py-3 text-gray-600">{String(item.actual_date ?? "—").substring(0, 60)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {data.length === 0 && <div className="text-center py-12 text-gray-400">No data available</div>}
      </div>
    </div>
  );
}
