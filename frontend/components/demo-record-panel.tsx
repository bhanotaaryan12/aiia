"use client";

import { Check, Circle, Loader2, Shield, User, FileText, CheckCircle2, RotateCcw, ArrowRight, Award } from "lucide-react";
import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";

type RecordItem = {
  label: string;
  detail: string;
  role?: string;
  priority?: "CRITICAL" | "HIGH" | "STANDARD" | string;
  tag?: string;
  status?: string;
};

type DemoRecord = {
  title: string;
  trial_ref?: string;
  pi_name?: string;
  version?: string;
  summary: string;
  status: string;
  completion_rate?: string;
  items: RecordItem[];
};

const RECORD_NAV = [
  { key: "protocol_review", label: "1. Protocol Review", href: "/dashboard/study/protocol-review" },
  { key: "operational_handoff", label: "2. Operational Handoff", href: "/dashboard/study/operational-handoff" },
  { key: "data_safeguards", label: "3. Data Safeguards", href: "/dashboard/study/data-safeguards" },
  { key: "clinical_monitoring", label: "Clinical Monitoring", href: "/dashboard/study/clinical-monitoring" },
  { key: "safety_surveillance", label: "Safety Surveillance", href: "/dashboard/study/safety-surveillance" },
  { key: "cdisc_standards_validation", label: "CDISC Export", href: "/dashboard/study/cdisc-standards" },
];

export default function DemoRecordPanel({ recordKey }: { recordKey: string }) {
  const [record, setRecord] = useState<DemoRecord | null>(null);
  const [covered, setCovered] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    setError("");
    api.get("/demo/records")
      .then((response) => {
        const data = response.data.records[recordKey] || null;
        setRecord(data);
        if (data && data.items) {
          // Pre-populate initial items or restore session state
          const saved = sessionStorage.getItem(`demo_covered_${recordKey}`);
          if (saved) {
            try {
              setCovered(JSON.parse(saved));
            } catch {
              setCovered(data.items.slice(0, 3).map((it: RecordItem) => it.label));
            }
          } else {
            // Default first half as checked to demonstrate interactive state
            setCovered(data.items.slice(0, Math.ceil(data.items.length / 2)).map((it: RecordItem) => it.label));
          }
        }
        setLoading(false);
      })
      .catch((requestError) => {
        setError(requestError.response?.data?.detail || "This walkthrough content is unavailable for the current user role.");
        setLoading(false);
      });
  }, [recordKey]);

  const toggleItem = (label: string) => {
    setCovered((prev) => {
      const next = prev.includes(label) ? prev.filter((l) => l !== label) : [...prev, label];
      try {
        sessionStorage.setItem(`demo_covered_${recordKey}`, JSON.stringify(next));
      } catch {}
      return next;
    });
  };

  const markAll = () => {
    if (!record) return;
    const all = record.items.map((i) => i.label);
    setCovered(all);
    try {
      sessionStorage.setItem(`demo_covered_${recordKey}`, JSON.stringify(all));
    } catch {}
  };

  const resetAll = () => {
    setCovered([]);
    try {
      sessionStorage.removeItem(`demo_covered_${recordKey}`);
    } catch {}
  };

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-red-900 shadow-sm">
        <div className="flex items-center gap-3">
          <Shield className="h-6 w-6 text-red-600" />
          <h2 className="text-lg font-semibold">Presentation Access Restriction</h2>
        </div>
        <p className="mt-2 text-sm text-red-700 leading-relaxed">{error}</p>
        <p className="mt-4 text-xs font-mono text-red-600">
          Tip: Sign in with the designated presentation account: <strong>admin@aiia.gov.in</strong>
        </p>
      </div>
    );
  }

  if (loading || !record) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-slate-500">
        <Loader2 size={28} className="animate-spin text-teal-700" aria-hidden="true" />
        <p className="mt-3 text-sm font-medium">Loading presentation record...</p>
      </div>
    );
  }

  const totalItems = record.items.length;
  const completedCount = covered.length;
  const percentComplete = totalItems > 0 ? Math.round((completedCount / totalItems) * 100) : 0;

  return (
    <div className="space-y-6">
      {/* Workflow Navigation Pills */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-4">
        {RECORD_NAV.map((nav) => {
          const isActive = nav.key === recordKey;
          return (
            <Link
              key={nav.key}
              href={nav.href}
              className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-semibold transition ${
                isActive
                  ? "bg-teal-700 text-white shadow-sm"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200 hover:text-slate-900"
              }`}
            >
              {nav.label}
            </Link>
          );
        })}
      </div>

      {/* Main Governance Card */}
      <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm" aria-label={record.title}>
        {/* Card Header */}
        <header className="border-b border-slate-200 bg-gradient-to-r from-slate-50 via-white to-slate-50 p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-md bg-teal-100 px-2.5 py-1 text-xs font-bold text-teal-900">
                <CheckCircle2 size={13} className="text-teal-700" />
                {record.status}
              </span>
              {record.version && (
                <span className="rounded-md border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-600">
                  {record.version}
                </span>
              )}
            </div>
            <div className="text-xs font-semibold text-slate-500">
              Demo Mode · Lead Principal Investigator
            </div>
          </div>

          <h1 className="mt-3 text-2xl font-bold text-slate-950">{record.title}</h1>

          {record.trial_ref && (
            <p className="mt-1 text-sm font-semibold text-teal-800">
              {record.trial_ref}
            </p>
          )}

          {record.pi_name && (
            <p className="mt-1 flex items-center gap-1.5 text-xs font-medium text-slate-500">
              <User size={13} /> {record.pi_name}
            </p>
          )}

          <p className="mt-3 text-sm leading-relaxed text-slate-600">{record.summary}</p>

          {/* Progress Tracker Bar */}
          <div className="mt-5 rounded-lg border border-slate-200 bg-white p-4">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
              <span>
                Verification Progress: <strong className="text-teal-800">{completedCount} of {totalItems} Verified</strong>
              </span>
              <span className="text-teal-700">{percentComplete}% Complete</span>
            </div>
            <div className="mt-2 h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-gradient-to-r from-teal-600 to-emerald-500 transition-all duration-300"
                style={{ width: `${percentComplete}%` }}
              />
            </div>

            <div className="mt-3 flex items-center justify-between gap-2 pt-2 border-t border-slate-100">
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={markAll}
                  className="inline-flex items-center gap-1 rounded bg-teal-50 px-2.5 py-1 text-xs font-medium text-teal-800 hover:bg-teal-100 transition"
                >
                  <Check size={12} /> Mark All Verified
                </button>
                <button
                  type="button"
                  onClick={resetAll}
                  className="inline-flex items-center gap-1 rounded bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-200 transition"
                >
                  <RotateCcw size={12} /> Reset
                </button>
              </div>
              <span className="text-[11px] text-slate-400">
                Interactive demonstration controls
              </span>
            </div>
          </div>
        </header>

        {/* Checklist Items */}
        <div className="divide-y divide-slate-100">
          {record.items.map((item, idx) => {
            const isCovered = covered.includes(item.label);
            return (
              <div
                key={item.label}
                className={`flex items-start gap-4 p-5 transition ${
                  isCovered ? "bg-slate-50/70" : "bg-white hover:bg-slate-50/40"
                }`}
              >
                <button
                  type="button"
                  onClick={() => toggleItem(item.label)}
                  aria-pressed={isCovered}
                  aria-label={`${isCovered ? "Unmark" : "Mark"} ${item.label} as verified`}
                  className={`mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-md border transition ${
                    isCovered
                      ? "border-teal-700 bg-teal-700 text-white shadow-sm"
                      : "border-slate-300 text-slate-400 hover:border-teal-600 hover:text-teal-600"
                  }`}
                >
                  {isCovered ? <Check size={15} strokeWidth={3} aria-hidden="true" /> : <span className="text-xs">{idx + 1}</span>}
                </button>

                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className={`font-semibold text-slate-950 ${isCovered ? "line-through text-slate-500" : ""}`}>
                      {item.label}
                    </h2>
                    {item.tag && (
                      <span className="rounded bg-slate-100 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-slate-600">
                        {item.tag}
                      </span>
                    )}
                    {item.priority === "CRITICAL" && (
                      <span className="rounded bg-red-100 px-1.5 py-0.5 text-[10px] font-bold text-red-800">
                        CRITICAL
                      </span>
                    )}
                    {item.role && (
                      <span className="ml-auto text-[11px] font-medium text-slate-500">
                        Role: <span className="text-teal-900 font-semibold">{item.role}</span>
                      </span>
                    )}
                  </div>
                  <p className="mt-1 text-sm leading-relaxed text-slate-600">{item.detail}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Card Footer */}
        <footer className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-200 bg-slate-50 px-6 py-4 text-xs text-slate-600">
          <span className="flex items-center gap-1.5">
            <Award size={14} className="text-teal-700" />
            Designed to demonstrate GCP E6(R2) and 21 CFR Part 11 compliant Ayurveda trial workflows.
          </span>
          <span className="font-mono text-[11px] text-slate-400">
            Account: admin@aiia.gov.in
          </span>
        </footer>
      </section>
    </div>
  );
}
