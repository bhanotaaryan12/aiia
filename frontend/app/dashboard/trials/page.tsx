"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function TrialsPage() {
  const router = useRouter();
  const [trials, setTrials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    api.get("/trials/").then(r => { setTrials(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const filtered = filter ? trials.filter(t => t.status === filter) : trials;

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3].map(i => <div key={i} className="h-16 bg-gray-200 rounded-lg" />)}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clinical Trials</h1>
          <p className="text-sm text-gray-500">{trials.length} trials registered</p>
        </div>
        <button onClick={() => router.push("/dashboard/trials/new")}
          className="px-4 py-2 bg-blue-800 text-white text-sm font-medium rounded-lg hover:bg-blue-900 transition">
          + New Trial
        </button>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["", "PLANNING", "RECRUITING", "ACTIVE", "COMPLETED", "ETHICS_PENDING"].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            className={`px-3 py-1.5 text-xs font-medium rounded-full transition ${filter === s ? "bg-blue-800 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>
            {s || "All"}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Trial</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Protocol #</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Phase</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Sites</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Participants</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Start</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.map((t) => (
              <tr key={t.id} onClick={() => router.push(`/dashboard/trials/${t.id}`)}
                className="hover:bg-gray-50 cursor-pointer transition">
                <td className="px-4 py-3">
                  <p className="font-medium text-gray-900">{t.short_title || t.title?.substring(0, 40)}</p>
                  <p className="text-xs text-gray-400 truncate max-w-xs">{t.title}</p>
                </td>
                <td className="px-4 py-3 text-gray-600">{t.protocol_number || "—"}</td>
                <td className="px-4 py-3 text-gray-600">{t.phase || "—"}</td>
                <td className="px-4 py-3"><span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColor(t.status)}`}>{t.status}</span></td>
                <td className="px-4 py-3 text-gray-600">{t.site_count}</td>
                <td className="px-4 py-3 text-gray-600">{t.participant_count}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(t.start_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="text-center py-12 text-gray-400">No trials found</div>}
      </div>
    </div>
  );
}
