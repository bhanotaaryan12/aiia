"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";

export default function NewTrialPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ title: "", short_title: "", protocol_number: "", phase: "Phase 2", study_type: "Interventional", therapeutic_area: "Ayurveda", ayurveda_system: "", primary_objective: "", planned_sample_size: 60, sponsor: "AIIA", start_date: "", expected_end_date: "", inclusion_criteria: "", exclusion_criteria: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/trials/", { ...form, planned_sample_size: Number(form.planned_sample_size) || null, start_date: form.start_date || null, expected_end_date: form.expected_end_date || null });
      router.push(`/dashboard/trials/${res.data.id}`);
    } catch (err: any) { alert(err.response?.data?.detail || "Failed to create trial"); }
    setLoading(false);
  };

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Create New Trial</h1>
      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Trial Title *</label><input required value={form.title} onChange={e => setForm({...form, title: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Short Title</label><input value={form.short_title} onChange={e => setForm({...form, short_title: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Protocol Number</label><input value={form.protocol_number} onChange={e => setForm({...form, protocol_number: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Phase</label><select value={form.phase} onChange={e => setForm({...form, phase: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"><option>Phase 1</option><option>Phase 2</option><option>Phase 3</option><option>Phase 4</option></select></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Study Type</label><select value={form.study_type} onChange={e => setForm({...form, study_type: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"><option>Interventional</option><option>Observational</option></select></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Ayurveda System</label><input value={form.ayurveda_system} onChange={e => setForm({...form, ayurveda_system: e.target.value})} placeholder="e.g. Rasayana Chikitsa" className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Sample Size</label><input type="number" value={form.planned_sample_size} onChange={e => setForm({...form, planned_sample_size: parseInt(e.target.value) || 0})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label><input type="date" value={form.start_date} onChange={e => setForm({...form, start_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Expected End Date</label><input type="date" value={form.expected_end_date} onChange={e => setForm({...form, expected_end_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Primary Objective</label><textarea value={form.primary_objective} onChange={e => setForm({...form, primary_objective: e.target.value})} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
        </div>
        <div className="flex gap-3 pt-4">
          <button type="submit" disabled={loading} className="px-6 py-2 bg-blue-800 text-white text-sm font-medium rounded-lg hover:bg-blue-900 disabled:opacity-50">{loading ? "Creating..." : "Create Trial"}</button>
          <button type="button" onClick={() => router.back()} className="px-6 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">Cancel</button>
        </div>
      </form>
    </div>
  );
}
