"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function ParticipantsPage() {
  const router = useRouter();
  const [participants, setParticipants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    let url = "/participants/?limit=100";
    if (filter) url += `&status=${filter}`;
    if (search) url += `&search=${search}`;
    api.get(url).then(r => { setParticipants(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, [filter, search]);

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3,4,5].map(i => <div key={i} className="h-12 bg-gray-200 rounded" />)}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-gray-900">Participants</h1><p className="text-sm text-gray-500">{participants.length} participants</p></div>
      </div>
      <div className="flex gap-2 flex-wrap items-center">
        <input type="text" placeholder="Search by ID..." value={search} onChange={e => setSearch(e.target.value)} className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm w-48" />
        {["", "SCREENED", "CONSENTED", "ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED", "WITHDRAWN"].map(s => (
          <button key={s} onClick={() => setFilter(s)} className={`px-3 py-1.5 text-xs font-medium rounded-full ${filter === s ? "bg-blue-800 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>{s || "All"}</button>
        ))}
      </div>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">ID</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Age</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Gender</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Screening</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Enrollment</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {participants.map(p => (
              <tr key={p.id} onClick={() => router.push(`/dashboard/participants/${p.id}`)} className="hover:bg-gray-50 cursor-pointer">
                <td className="px-4 py-3 font-medium text-blue-800">{p.participant_id}</td>
                <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(p.status)}`}>{p.status}</span></td>
                <td className="px-4 py-3 text-gray-600">{p.age || "—"}</td>
                <td className="px-4 py-3 text-gray-600">{p.gender || "—"}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(p.screening_date)}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(p.enrollment_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {participants.length === 0 && <div className="text-center py-12 text-gray-400">No participants found</div>}
      </div>
    </div>
  );
}
