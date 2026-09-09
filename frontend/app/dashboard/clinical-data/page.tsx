"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function ClinicalDataPage() {
  const [forms, setForms] = useState<any[]>([]);
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [queries, setQueries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get("/forms/"), api.get("/forms/submissions"), api.get("/forms/queries")])
      .then(([f, s, q]) => { setForms(f.data); setSubmissions(s.data); setQueries(q.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Clinical Data (eCRF)</h1>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{forms.length}</p>
          <p className="text-sm text-gray-500">Form Definitions</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{submissions.length}</p>
          <p className="text-sm text-gray-500">Submissions</p>
        </div>
        <div className="bg-white rounded-xl border border-amber-200 p-5 bg-amber-50">
          <p className="text-3xl font-bold text-amber-700">{queries.filter((q: any) => q.status === "OPEN").length}</p>
          <p className="text-sm text-amber-600">Open Queries</p>
        </div>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-5 py-4 border-b"><h3 className="font-semibold">Forms</h3></div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Form Name</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Code</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Version</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {forms.map((f: any) => (
              <tr key={f.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{f.name}</td>
                <td className="px-4 py-3 text-gray-600">{f.code || "—"}</td>
                <td className="px-4 py-3 text-gray-600">{f.version}</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">{f.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
