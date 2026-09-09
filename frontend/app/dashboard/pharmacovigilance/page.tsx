"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function PharmacovigilancePage() {
  const [aes, setAEs] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>({});
  const [saes, setSAEs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/pharmacovigilance/adverse-events"),
      api.get("/pharmacovigilance/summary"),
      api.get("/pharmacovigilance/serious-adverse-events"),
    ]).then(([a, s, se]) => {
      setAEs(a.data); setSummary(s.data); setSAEs(se.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse space-y-4"><div className="h-24 bg-gray-200 rounded-xl" /><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Pharmacovigilance</h1>

      {/* Safety Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{summary.total_aes || 0}</p>
          <p className="text-sm text-gray-500">Total AEs</p>
        </div>
        <div className="bg-white rounded-xl border border-red-200 p-5 bg-red-50">
          <p className="text-3xl font-bold text-red-700">{summary.total_saes || 0}</p>
          <p className="text-sm text-red-600">Total SAEs</p>
        </div>
        <div className="bg-white rounded-xl border border-amber-200 p-5 bg-amber-50">
          <p className="text-3xl font-bold text-amber-700">{summary.open_saes || 0}</p>
          <p className="text-sm text-amber-600">Open SAEs</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex gap-2 text-xs">
            <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded">Mild: {summary.by_severity?.mild || 0}</span>
            <span className="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">Mod: {summary.by_severity?.moderate || 0}</span>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded">Severe: {summary.by_severity?.severe || 0}</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">By Severity</p>
        </div>
      </div>

      {/* AE Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-200"><h3 className="font-semibold">Adverse Events</h3></div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Event Term</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Severity</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Seriousness</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Causality</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Outcome</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Onset</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {aes.map(ae => (
              <tr key={ae.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{ae.event_term}</td>
                <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ae.severity)}`}>{ae.severity}</span></td>
                <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ae.seriousness)}`}>{ae.seriousness}</span></td>
                <td className="px-4 py-3 text-gray-600">{ae.causality}</td>
                <td className="px-4 py-3 text-gray-600">{ae.outcome}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(ae.onset_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
