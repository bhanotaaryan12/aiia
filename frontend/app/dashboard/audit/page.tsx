"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function AuditPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/audit/?limit=100").then(r => { setLogs(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Audit Logs</h1>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Timestamp</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">User</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Action</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Entity</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Details</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {logs.map((l: any) => (
              <tr key={l.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-xs text-gray-500">{formatDate(l.timestamp)}</td>
                <td className="px-4 py-3 text-gray-600">{l.user_email || "—"}</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs font-medium">{l.action}</span></td>
                <td className="px-4 py-3 text-gray-600">{l.entity_type}</td>
                <td className="px-4 py-3 text-gray-500 text-xs truncate max-w-xs">{l.details || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {logs.length === 0 && <div className="text-center py-12 text-gray-400">No audit logs</div>}
      </div>
    </div>
  );
}
