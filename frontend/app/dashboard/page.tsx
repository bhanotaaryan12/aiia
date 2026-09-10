"use client";

import Link from "next/link";
import { ArrowRight, CheckCircle2, FileCheck2, ShieldCheck, UsersRound, FileText, BadgeCheck, ShieldAlert, Database, Sparkles, Activity } from "lucide-react";

const triadCards = [
  {
    title: "1. Protocol Review",
    subtitle: "Scientific & Ethics Clearance",
    href: "/dashboard/study/protocol-review",
    icon: FileText,
    accent: "border-teal-600 bg-teal-50/30 text-teal-800",
    badge: "Checkpoint 1",
    description: "Scientific hypothesis for Withania somnifera, inclusion criteria, WOMAC primary endpoints, and Central Ethics Committee clearance (ECR/1382/Inst/DL/2020).",
  },
  {
    title: "2. Operational Handoff",
    subtitle: "Site Activation & Logistics",
    href: "/dashboard/study/operational-handoff",
    icon: BadgeCheck,
    accent: "border-emerald-600 bg-emerald-50/30 text-emerald-800",
    badge: "Checkpoint 2",
    description: "Multi-center Site Initiation Visit (SIV) completion, investigational product quarantine & CoA verification, delegation of authority (DOA) log, and CDASH eCRF activation.",
  },
  {
    title: "3. Data Safeguards",
    subtitle: "21 CFR Part 11 & Privacy Controls",
    href: "/dashboard/study/data-safeguards",
    icon: ShieldCheck,
    accent: "border-blue-600 bg-blue-50/30 text-blue-800",
    badge: "Checkpoint 3",
    description: "Dual-key subject pseudonymization, immutable append-only database audit logs, multi-tenant memory graph hashing, and demo endpoint RBAC gatekeeping.",
  },
];

const secondaryCards = [
  {
    title: "Clinical Site Monitoring",
    href: "/dashboard/study/clinical-monitoring",
    icon: Activity,
    description: "100% SDV audit on initial cohort of 30 subjects and drug accountability logs.",
  },
  {
    title: "Safety Surveillance",
    href: "/dashboard/study/safety-surveillance",
    icon: ShieldAlert,
    description: "24-hour statutory expedited SAE escalation workflow and MedDRA signal clustering.",
  },
  {
    title: "CDISC SDTM Export",
    href: "/dashboard/study/cdisc-standards",
    icon: Database,
    description: "Standardized export mapping for Demographics (DM), Subject Visits (SV), and Adverse Events (AE).",
  },
];

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-6xl space-y-8">
      {/* Hero Welcome Banner */}
      <section className="rounded-2xl border border-slate-200 bg-gradient-to-br from-teal-900 via-teal-800 to-slate-950 p-8 text-white shadow-md">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full bg-teal-500/20 px-3 py-1 text-xs font-semibold text-teal-200 border border-teal-400/30">
              <Sparkles size={13} className="text-teal-300" />
              Demo Account Presentation Session
            </div>
            <h1 className="mt-3 text-3xl font-extrabold tracking-tight sm:text-4xl">
              AIIA Clinical Trials Workspace
            </h1>
            <p className="mt-3 text-sm leading-relaxed text-teal-100 sm:text-base">
              A real-time Clinical Trial Management System for Ayurveda research with CDISC/FHIR interoperability, multi-center site governance, and immutable audit safeguards.
            </p>
          </div>
          <div className="flex flex-col items-end gap-2 rounded-xl border border-teal-500/30 bg-teal-950/40 p-5 backdrop-blur-md">
            <span className="text-[11px] font-bold uppercase tracking-wider text-teal-300">Authorized Investigator</span>
            <span className="text-base font-bold text-white">Dr. Rajesh Kumar</span>
            <span className="text-xs text-teal-200 font-mono">admin@aiia.gov.in · Super Admin</span>
            <div className="mt-2 flex gap-2">
              <Link
                href="/dashboard/study"
                className="inline-flex items-center gap-1.5 rounded-lg bg-teal-600 px-3 py-1.5 text-xs font-bold text-white shadow transition hover:bg-teal-500"
              >
                Study Master Record <ArrowRight size={13} />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Primary Triad Walkthrough Showcase */}
      <section aria-labelledby="triad-heading">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 id="triad-heading" className="text-xl font-bold text-slate-950 flex items-center gap-2">
              <CheckCircle2 className="text-teal-700" size={22} />
              Core Clinical Governance Workflows (Demo Only)
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Interactive demonstration records restricted exclusively to the demo account.
            </p>
          </div>
          <span className="rounded-full bg-teal-100 px-3 py-1 text-xs font-bold text-teal-900">
            3 Core Checkpoints
          </span>
        </div>

        <div className="grid gap-5 md:grid-cols-3">
          {triadCards.map((card) => {
            const Icon = card.icon;
            return (
              <Link
                key={card.title}
                href={card.href}
                className="group relative flex flex-col justify-between rounded-xl border-2 border-slate-200 bg-white p-6 shadow-sm transition hover:border-teal-700 hover:shadow-lg"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-teal-50 text-teal-800 group-hover:bg-teal-700 group-hover:text-white transition">
                      <Icon size={24} aria-hidden="true" />
                    </div>
                    <span className="rounded-md bg-teal-50 px-2 py-1 text-[11px] font-bold text-teal-900 border border-teal-100">
                      {card.badge}
                    </span>
                  </div>

                  <h3 className="mt-4 text-lg font-bold text-slate-950 group-hover:text-teal-800 transition">
                    {card.title}
                  </h3>
                  <p className="text-xs font-semibold text-teal-700">{card.subtitle}</p>

                  <p className="mt-2.5 text-xs leading-relaxed text-slate-600">
                    {card.description}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-xs font-bold text-teal-800 flex items-center gap-1">
                    Open Walkthrough <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
                  </span>
                  <span className="text-[10px] font-semibold text-slate-400">Verified</span>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Supporting Clinical Monitoring & Regulatory Cards */}
      <section aria-labelledby="secondary-heading">
        <h2 id="secondary-heading" className="text-base font-bold text-slate-900 mb-3">
          Clinical Operations & Interoperability
        </h2>
        <div className="grid gap-4 md:grid-cols-3">
          {secondaryCards.map((card) => {
            const Icon = card.icon;
            return (
              <Link
                key={card.title}
                href={card.href}
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-teal-700 hover:shadow"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-teal-800">
                    <Icon size={18} aria-hidden="true" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-950">{card.title}</h3>
                  </div>
                </div>
                <p className="mt-2.5 text-xs leading-relaxed text-slate-600">
                  {card.description}
                </p>
                <div className="mt-4 flex items-center gap-1 text-xs font-bold text-teal-800">
                  Inspect module <ArrowRight size={12} />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Compliance & Presentation Boundary Notice */}
      <section className="rounded-xl border-l-4 border-teal-700 bg-teal-50/80 p-5 shadow-sm" aria-label="Demo data notice">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm font-bold text-teal-950">Ayurveda Clinical Research Compliance Boundary</p>
            <p className="mt-1 text-xs leading-relaxed text-teal-900">
              This environment runs on simulated clinical research scenarios (Sandhigata Vata trial AYU-OA-2024 and Diabetes trial AYU-DM-2024). All records adhere to GCP E6(R2) and 21 CFR Part 11 requirements. Example records are protected by backend API gatekeepers accessible strictly to <code className="rounded bg-teal-200/60 px-1 py-0.5 font-mono text-[11px]">admin@aiia.gov.in</code>.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
