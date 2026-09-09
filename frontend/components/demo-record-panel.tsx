"use client";

import { Check, Circle, Loader2 } from "lucide-react";
import { useEffect, useState } from "react";
import api from "@/lib/api";

type RecordItem = { label: string; detail: string };
type DemoRecord = { title: string; summary: string; status: string; items: RecordItem[] };

export default function DemoRecordPanel({ recordKey }: { recordKey: string }) {
  const [record, setRecord] = useState<DemoRecord | null>(null);
  const [covered, setCovered] = useState<string[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/demo/records")
      .then((response) => setRecord(response.data.records[recordKey] || null))
      .catch((requestError) => setError(requestError.response?.data?.detail || "This walkthrough content is unavailable."));
  }, [recordKey]);

  if (error) return <p role="alert" className="border-l-4 border-red-700 bg-red-50 px-4 py-3 text-sm text-red-800">{error}</p>;
  if (!record) return <div className="flex items-center gap-2 text-sm text-slate-600"><Loader2 size={16} className="animate-spin" aria-hidden="true" />Loading presentation record</div>;

  return (
    <section className="border border-slate-200 bg-white" aria-label={record.title}>
      <header className="border-b border-slate-200 p-5"><p className="text-sm font-semibold text-teal-700">{record.status}</p><h1 className="mt-2 text-2xl font-semibold text-slate-950">{record.title}</h1><p className="mt-2 text-sm leading-6 text-slate-600">{record.summary}</p></header>
      <div className="divide-y divide-slate-200">
        {record.items.map((item) => {
          const isCovered = covered.includes(item.label);
          return <div key={item.label} className="flex items-start gap-4 p-5"><button type="button" onClick={() => setCovered((current) => isCovered ? current.filter((label) => label !== item.label) : [...current, item.label])} aria-pressed={isCovered} aria-label={`${isCovered ? "Unmark" : "Mark"} ${item.label} as covered`} className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-md border border-slate-300 text-teal-800 hover:bg-teal-50">{isCovered ? <Check size={16} aria-hidden="true" /> : <Circle size={15} aria-hidden="true" />}</button><div><h2 className="font-semibold text-slate-950">{item.label}</h2><p className="mt-1 text-sm leading-6 text-slate-600">{item.detail}</p></div></div>;
        })}
      </div>
      <footer className="border-t border-slate-200 bg-slate-50 px-5 py-3 text-xs text-slate-600">Checklist selections are local to this presentation session and are not stored as clinical records.</footer>
    </section>
  );
}
