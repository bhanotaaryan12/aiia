"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function ParticipantDetail() {
  const { id } = useParams();
  const [p, setP] = useState<any>(null);
  const [visits, setVisits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get(`/participants/${id}`), api.get(`/visits/?participant_id=${id}`)]).then(([pr, vr]) => {
      setP(pr.data); setVisits(vr.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="animate-pulse"><div className="h-48 bg-gray-200 rounded-xl" /></div>;
  if (!p) return <div className="text-gray-400 text-center py-12">Participant not found</div>;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 bg-blue-100 text-blue-800 rounded-xl flex items-center justify-center text-xl font-bold">👤</div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">{p.participant_id}</h1>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(p.status)}`}>{p.status}</span>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-100">
          <div><p className="text-xs text-gray-400">Age</p><p className="text-sm font-medium">{p.age || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Gender</p><p className="text-sm font-medium">{p.gender || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Screening Date</p><p className="text-sm font-medium">{formatDate(p.screening_date)}</p></div>
          <div><p className="text-xs text-gray-400">Enrollment Date</p><p className="text-sm font-medium">{formatDate(p.enrollment_date)}</p></div>
        </div>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h3 className="text-sm font-semibold text-gray-700 mb-4">Visits ({visits.length})</h3>
        <div className="space-y-2">
          {visits.map((v: any) => (
            <div key={v.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="text-sm font-medium">{v.visit_name || "Visit"}</p>
                <p className="text-xs text-gray-400">Scheduled: {formatDate(v.scheduled_date)}</p>
              </div>
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(v.status)}`}>{v.status}</span>
            </div>
          ))}
          {visits.length === 0 && <p className="text-sm text-gray-400">No visits recorded</p>}
        </div>
      </div>
    </div>
  );
}
