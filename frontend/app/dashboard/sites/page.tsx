"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { statusColor } from "@/lib/utils";

export default function SitesPage() {
  const [sites, setSites] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/sites/").then(r => { setSites(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3].map(i => <div key={i} className="h-16 bg-gray-200 rounded-lg" />)}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-gray-900">Research Sites</h1><p className="text-sm text-gray-500">{sites.length} sites registered</p></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sites.map(s => (
          <div key={s.id} className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition">
            <div className="flex items-start justify-between mb-3">
              <span className="text-2xl">🏥</span>
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(s.status)}`}>{s.status}</span>
            </div>
            <h3 className="font-semibold text-gray-900">{s.name}</h3>
            <p className="text-sm text-gray-500">{s.institution}</p>
            <p className="text-xs text-gray-400 mt-1">{s.city}, {s.state}</p>
            <div className="mt-4 pt-3 border-t border-gray-100 flex justify-between text-xs text-gray-500">
              <span>Target: {s.target_enrollment || "—"}</span>
              <span>Enrolled: {s.participant_count || 0}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
