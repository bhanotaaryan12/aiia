import Link from "next/link";
import { ArrowRight, BadgeCheck, FileText, ShieldCheck, Activity, ShieldAlert, Database, CheckCircle2, Lock, Sparkles } from "lucide-react";

const record = [
  ["Trial Protocol", "AYU-OA-2024 · Sandhigata Vata (Knee Osteoarthritis) Phase II"],
  ["Principal Investigator", "Dr. Rajesh Kumar, MD (Ayu), PhD (AIIA New Delhi)"],
  ["Lead Formulation", "Withania somnifera (Ashwagandha 500mg extract, >2.5% withanolides)"],
  ["Regulatory & CTRI", "CTRI/2024/03/064128 · Central Ethics Clearance ECR/1382/Inst/DL/2020"],
  ["Active Study Centers", "5 Certified Centers (Delhi, Jaipur, Jamnagar, Chennai, Bengaluru)"],
  ["Governance Status", "Ethics Cleared · Operational SIV Complete · 21 CFR Part 11 Enforced"],
];

export default function StudyPage() {
  return (
    <div className="mx-auto max-w-5xl space-y-8">
      {/* Header Banner */}
      <section className="rounded-xl border border-slate-200 bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 p-8 text-white shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-teal-700/60 px-3 py-1 text-xs font-semibold text-teal-200 border border-teal-500/30">
              <Sparkles size={12} />
              Presentation Demo Suite · Super Admin Access
            </div>
            <h1 className="mt-3 text-3xl font-bold tracking-tight">Clinical Study Governance & Demonstration Records</h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-teal-100">
              Authoritative demonstration workflows covering protocol scientific review, site operational handoff, and regulatory data safeguards for the lead Ayurveda clinical trial.
            </p>
          </div>
          <div className="rounded-lg border border-teal-600/40 bg-teal-800/40 p-4 text-right backdrop-blur-sm">
            <p className="text-xs uppercase tracking-wider text-teal-300 font-semibold">Demo Account</p>
            <p className="text-sm font-bold text-white">admin@aiia.gov.in</p>
            <p className="text-[11px] text-teal-300">Role: Super Admin / Lead PI</p>
          </div>
        </div>
      </section>

      {/* Trial Profile Summary */}
      <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm" aria-label="Study record details">
        <div className="border-b border-slate-200 bg-slate-50/80 px-6 py-4 flex items-center justify-between">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
            <CheckCircle2 size={16} className="text-teal-700" />
            Lead Clinical Trial Profile
          </h2>
          <span className="rounded bg-teal-100 px-2.5 py-0.5 text-xs font-bold text-teal-800">
            Active · Recruiting
          </span>
        </div>
        <dl className="divide-y divide-slate-100">
          {record.map(([label, value]) => (
            <div key={label} className="grid grid-cols-1 gap-1 px-6 py-3.5 sm:grid-cols-[14rem_1fr] sm:gap-4 hover:bg-slate-50/50 transition">
              <dt className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{label}</dt>
              <dd className="text-sm font-semibold text-slate-900">{value}</dd>
            </div>
          ))}
        </dl>
      </section>

      {/* Primary Walkthrough Triad */}
      <div>
        <div className="mb-4">
          <h2 className="text-lg font-bold text-slate-950 flex items-center gap-2">
            Core Governance & Safeguards Triad
          </h2>
          <p className="text-xs text-slate-500">Essential demonstration checkpoints for protocol approval, site handoff, and compliance.</p>
        </div>

        <section className="grid gap-5 md:grid-cols-3">
          {/* Protocol Review */}
          <Link
            href="/dashboard/study/protocol-review"
            className="group relative flex flex-col justify-between rounded-xl border-2 border-teal-600/30 bg-white p-6 shadow-sm transition hover:border-teal-700 hover:shadow-md"
          >
            <div>
              <div className="flex items-center justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-teal-100 text-teal-800 group-hover:bg-teal-700 group-hover:text-white transition">
                  <FileText size={20} aria-hidden="true" />
                </div>
                <span className="rounded bg-teal-50 px-2 py-0.5 text-[11px] font-bold text-teal-800">
                  Checkpoint 1
                </span>
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-950 group-hover:text-teal-800 transition">
                1. Protocol Review
              </h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-600">
                Evaluate scientific hypothesis, Kellgren-Lawrence inclusion criteria, WOMAC endpoints, and Central Ethics Committee clearance.
              </p>
            </div>
            <div className="mt-6 flex items-center gap-1.5 text-xs font-bold text-teal-800">
              Open Protocol Review <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Operational Handoff */}
          <Link
            href="/dashboard/study/operational-handoff"
            className="group relative flex flex-col justify-between rounded-xl border-2 border-teal-600/30 bg-white p-6 shadow-sm transition hover:border-teal-700 hover:shadow-md"
          >
            <div>
              <div className="flex items-center justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-100 text-emerald-800 group-hover:bg-emerald-700 group-hover:text-white transition">
                  <BadgeCheck size={20} aria-hidden="true" />
                </div>
                <span className="rounded bg-emerald-50 px-2 py-0.5 text-[11px] font-bold text-emerald-800">
                  Checkpoint 2
                </span>
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-950 group-hover:text-emerald-800 transition">
                2. Operational Handoff
              </h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-600">
                Verify multi-site initiation (SIV), investigational product batch quarantine, delegation of authority (DOA), and eCRF deployment.
              </p>
            </div>
            <div className="mt-6 flex items-center gap-1.5 text-xs font-bold text-emerald-800">
              Open Operational Handoff <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          {/* Data Safeguards */}
          <Link
            href="/dashboard/study/data-safeguards"
            className="group relative flex flex-col justify-between rounded-xl border-2 border-teal-600/30 bg-white p-6 shadow-sm transition hover:border-teal-700 hover:shadow-md"
          >
            <div>
              <div className="flex items-center justify-between">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 text-blue-800 group-hover:bg-blue-700 group-hover:text-white transition">
                  <ShieldCheck size={20} aria-hidden="true" />
                </div>
                <span className="rounded bg-blue-50 px-2 py-0.5 text-[11px] font-bold text-blue-800">
                  Checkpoint 3
                </span>
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-950 group-hover:text-blue-800 transition">
                3. Data Safeguards
              </h3>
              <p className="mt-2 text-xs leading-relaxed text-slate-600">
                Confirm dual-key pseudonymization, 21 CFR Part 11 append-only audit trail, multi-tenant memory isolation, and demo gatekeeping.
              </p>
            </div>
            <div className="mt-6 flex items-center gap-1.5 text-xs font-bold text-blue-800">
              Open Data Safeguards <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        </section>
      </div>

      {/* Additional Demonstration Modules */}
      <div>
        <div className="mb-4">
          <h2 className="text-base font-bold text-slate-900">
            Monitoring, Safety & Regulatory Standards
          </h2>
        </div>

        <section className="grid gap-4 md:grid-cols-3">
          <Link
            href="/dashboard/study/clinical-monitoring"
            className="rounded-xl border border-slate-200 bg-white p-5 transition hover:border-teal-700 hover:shadow-sm"
          >
            <Activity className="text-teal-700" size={20} aria-hidden="true" />
            <h3 className="mt-3 text-sm font-bold text-slate-950">Clinical Site Monitoring</h3>
            <p className="mt-1 text-xs leading-5 text-slate-600">Review 100% SDV completion on initial cohort and drug accountability logs.</p>
            <span className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-teal-800">
              Open Monitoring <ArrowRight size={13} />
            </span>
          </Link>

          <Link
            href="/dashboard/study/safety-surveillance"
            className="rounded-xl border border-slate-200 bg-white p-5 transition hover:border-teal-700 hover:shadow-sm"
          >
            <ShieldAlert className="text-teal-700" size={20} aria-hidden="true" />
            <h3 className="mt-3 text-sm font-bold text-slate-950">Safety Surveillance</h3>
            <p className="mt-1 text-xs leading-5 text-slate-600">Explore 24h expedited SAE escalation workflows and MedDRA clustering signals.</p>
            <span className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-teal-800">
              Open Safety <ArrowRight size={13} />
            </span>
          </Link>

          <Link
            href="/dashboard/study/cdisc-standards"
            className="rounded-xl border border-slate-200 bg-white p-5 transition hover:border-teal-700 hover:shadow-sm"
          >
            <Database className="text-teal-700" size={20} aria-hidden="true" />
            <h3 className="mt-3 text-sm font-bold text-slate-950">CDISC SDTM Export</h3>
            <p className="mt-1 text-xs leading-5 text-slate-600">Verify regulatory compliance across Demographics (DM), Visits (SV), and AE domains.</p>
            <span className="mt-4 inline-flex items-center gap-1 text-xs font-semibold text-teal-800">
              Open CDISC <ArrowRight size={13} />
            </span>
          </Link>
        </section>
      </div>
    </div>
  );
}
