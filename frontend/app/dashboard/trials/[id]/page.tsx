"use client";
import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function TrialDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [trial, setTrial] = useState<any>(null);
  const [arms, setArms] = useState<any[]>([]);
  const [participants, setParticipants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState("overview");

  useEffect(() => {
    Promise.all([
      api.get(`/trials/${id}`),
      api.get(`/trials/${id}/arms`),
      api.get(`/participants/?trial_id=${id}&limit=20`),
    ]).then(([t, a, p]) => {
      setTrial(t.data); setArms(a.data); setParticipants(p.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="animate-pulse space-y-4"><div className="h-32 bg-gray-200 rounded-xl" /><div className="h-64 bg-gray-200 rounded-xl" /></div>;
  if (!trial) return <div className="text-center py-12 text-gray-400">Trial not found</div>;

  const tabs = ["overview", "participants", "sites", "safety"];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColor(trial.status)}`}>{trial.status}</span>
              <span className="text-sm text-gray-500">{trial.protocol_number}</span>
              {trial.phase && <span className="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full">{trial.phase}</span>}
            </div>
            <h1 className="text-xl font-bold text-gray-900">{trial.title}</h1>
            <p className="text-sm text-gray-500 mt-1">{trial.therapeutic_area} · {trial.ayurveda_system}</p>
          </div>
        </div>
        <div className="grid grid-cols-4 gap-4 mt-6 pt-4 border-t border-gray-100">
          <div><p className="text-xs text-gray-400">Sponsor</p><p className="text-sm font-medium">{trial.sponsor || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Sample Size</p><p className="text-sm font-medium">{trial.planned_sample_size || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Start Date</p><p className="text-sm font-medium">{formatDate(trial.start_date)}</p></div>
          <div><p className="text-xs text-gray-400">End Date</p><p className="text-sm font-medium">{formatDate(trial.expected_end_date)}</p></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        {tabs.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition ${tab === t ? "border-blue-800 text-blue-800" : "border-transparent text-gray-500 hover:text-gray-700"}`}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {tab === "overview" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Primary Objective</h3>
            <p className="text-sm text-gray-600">{trial.primary_objective || "Not specified"}</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Study Arms ({arms.length})</h3>
            {arms.map((a: any) => (
              <div key={a.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-medium">{a.name}</p>
                  <p className="text-xs text-gray-400">{a.arm_type}</p>
                </div>
                <span className="text-xs text-gray-500">Ratio: {a.allocation_ratio}</span>
              </div>
            ))}
            {arms.length === 0 && <p className="text-sm text-gray-400">No study arms defined</p>}
          </div>
        </div>
      )}

      {tab === "participants" && (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b"><tr>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Participant ID</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Age</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Gender</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Enrolled</th>
            </tr></thead>
            <tbody className="divide-y divide-gray-100">
              {participants.map((p: any) => (
                <tr key={p.id} onClick={() => router.push(`/dashboard/participants/${p.id}`)} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-4 py-3 font-medium">{p.participant_id}</td>
                  <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(p.status)}`}>{p.status}</span></td>
                  <td className="px-4 py-3 text-gray-600">{p.age || "—"}</td>
                  <td className="px-4 py-3 text-gray-600">{p.gender || "—"}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(p.enrollment_date)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {participants.length === 0 && <div className="text-center py-8 text-gray-400">No participants yet</div>}
        </div>
      )}
    </div>
  );
}
