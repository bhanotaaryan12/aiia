"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, Legend } from "recharts";

const COLORS = ["#1e40af", "#0d9488", "#d97706", "#dc2626", "#7c3aed", "#059669"];

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/analytics/dashboard").then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-96 bg-gray-200 rounded-xl" /></div>;
  if (!data) return <div className="text-gray-400 text-center py-12">No analytics data</div>;

  const k = data.kpis;
  const enrollData = (data.enrollment_by_site?.labels || []).map((l: string, i: number) => ({ name: l, count: data.enrollment_by_site.datasets[0]?.data[i] || 0 }));
  const funnelData = (data.participant_funnel?.labels || []).map((l: string, i: number) => ({ name: l, count: data.participant_funnel.datasets[0]?.data[i] || 0 }));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Analytics & Reports</h1>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.total_participants}</p><p className="text-sm text-gray-500">Total Participants</p></div>
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.enrollment_rate}%</p><p className="text-sm text-gray-500">Enrollment Rate</p></div>
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.visit_compliance}%</p><p className="text-sm text-gray-500">Visit Compliance</p></div>
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.total_aes}</p><p className="text-sm text-gray-500">Adverse Events</p></div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Enrollment by Site</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={enrollData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{fontSize: 10}} angle={-20} /><YAxis /><Tooltip /><Bar dataKey="count" fill="#1e40af" radius={[4,4,0,0]} /></BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl border p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Participant Lifecycle Funnel</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={funnelData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{fontSize: 11}} /><YAxis /><Tooltip /><Bar dataKey="count" fill="#7c3aed" radius={[4,4,0,0]} /></BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
