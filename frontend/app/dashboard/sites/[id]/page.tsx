"use client";
import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function SiteDetail() {
  const { id } = useParams();
  const [site, setSite] = useState<any>(null);
  useEffect(() => { api.get(`/sites/${id}`).then(r => setSite(r.data)).catch(() => {}); }, [id]);
  if (!site) return <div className="animate-pulse"><div className="h-48 bg-gray-200 rounded-xl" /></div>;
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h1 className="text-xl font-bold mb-4">{site.name}</h1>
      <p className="text-gray-600">{site.institution}</p>
      <p className="text-sm text-gray-500">{site.city}, {site.state}</p>
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div><p className="text-xs text-gray-400">Target Enrollment</p><p className="font-medium">{site.target_enrollment || "—"}</p></div>
        <div><p className="text-xs text-gray-400">Participants</p><p className="font-medium">{site.participant_count || 0}</p></div>
      </div>
    </div>
  );
}
