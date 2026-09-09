"use client";

import Link from "next/link";
import { ArrowRight, CheckCircle2, FileCheck2, ShieldCheck, UsersRound } from "lucide-react";

const workflow = [
  { title: "Study setup", detail: "Protocol, investigator roles, and required records are prepared for review.", icon: FileCheck2 },
  { title: "Site readiness", detail: "The presentation follows a single-site handoff from activation to monitoring.", icon: CheckCircle2 },
  { title: "Participant privacy", detail: "The walkthrough uses no patient information and keeps the study record illustrative.", icon: UsersRound },
  { title: "Safety review", detail: "Safety and regulatory review are shown as governed workflow steps, not live operational data.", icon: ShieldCheck },
];

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <section className="border-b border-slate-200 pb-8">
        <p className="text-sm font-semibold text-teal-700">Presentation prototype</p>
        <h1 className="mt-2 text-3xl font-semibold text-slate-950">AIIA Study Workspace</h1>
        <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">A focused walkthrough of how one clinical study moves through setup, governance, and review.</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/dashboard/study" className="inline-flex items-center gap-2 rounded-md bg-teal-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-teal-800">Open study record <ArrowRight size={16} aria-hidden="true" /></Link>
          <Link href="/dashboard/guide" className="inline-flex items-center gap-2 rounded-md border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 transition hover:bg-slate-50">View demo guide</Link>
        </div>
      </section>

      <section aria-labelledby="walkthrough-heading">
        <h2 id="walkthrough-heading" className="text-xl font-semibold text-slate-950">Walkthrough sequence</h2>
        <p className="mt-1 text-sm text-slate-600">Illustrative states only. This prototype does not show live trial or participant data.</p>
        <div className="mt-5 grid gap-px overflow-hidden rounded-md border border-slate-200 bg-slate-200 md:grid-cols-2">
          {workflow.map(({ title, detail, icon: Icon }) => (
            <article key={title} className="bg-white p-5">
              <Icon className="text-teal-700" size={22} aria-hidden="true" />
              <h3 className="mt-4 text-base font-semibold text-slate-950">{title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="border-l-4 border-teal-700 bg-teal-50 px-5 py-4" aria-label="Demo data notice">
        <p className="text-sm font-semibold text-teal-950">Demo data notice</p>
        <p className="mt-1 text-sm leading-6 text-teal-900">This environment is for product presentation only. It contains no patient data, performance metrics, or live operational records.</p>
      </section>
    </div>
  );
}
