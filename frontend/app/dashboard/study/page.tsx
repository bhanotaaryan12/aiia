import Link from "next/link";
import { ArrowRight, BadgeCheck, FileText, ShieldCheck, Activity, ShieldAlert, Database } from "lucide-react";

const record = [
  ["Study identifier", "Presentation study record"],
  ["Research focus", "Ayurveda clinical research workflow"],
  ["Current stage", "Ready for presentation review"],
  ["Data handling", "Illustrative content only"],
];

export default function StudyPage() {
  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <section className="border-b border-slate-200 pb-7"><p className="text-sm font-semibold text-teal-700">Study record</p><h1 className="mt-2 text-3xl font-semibold text-slate-950">Presentation study record</h1><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">A concise study profile designed to guide the demonstration. Details are illustrative and only accessible for the designated demo account.</p></section>
      <section className="overflow-hidden rounded-md border border-slate-200 bg-white" aria-label="Study record details">
        {record.map(([label, value]) => <div key={label} className="grid gap-1 border-b border-slate-200 px-5 py-4 last:border-0 sm:grid-cols-[12rem_1fr] sm:gap-6"><dt className="text-sm font-medium text-slate-600">{label}</dt><dd className="text-sm font-semibold text-slate-950">{value}</dd></div>)}
      </section>
      <section className="grid gap-4 md:grid-cols-3">
        <Link href="/dashboard/study/protocol-review" className="border border-slate-200 bg-white p-5 transition hover:border-teal-700"><FileText className="text-teal-700" size={20} aria-hidden="true" /><h2 className="mt-4 font-semibold text-slate-950">Protocol review</h2><p className="mt-2 text-sm leading-6 text-slate-600">Show the study brief, governance checkpoints, and responsible roles.</p><span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-teal-800">Open review <ArrowRight size={15} aria-hidden="true" /></span></Link>
        <Link href="/dashboard/study/operational-handoff" className="border border-slate-200 bg-white p-5 transition hover:border-teal-700"><BadgeCheck className="text-teal-700" size={20} aria-hidden="true" /><h2 className="mt-4 font-semibold text-slate-950">Operational handoff</h2><p className="mt-2 text-sm leading-6 text-slate-600">Walk through a clear handoff from study preparation to site coordination.</p><span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-teal-800">Open handoff <ArrowRight size={15} aria-hidden="true" /></span></Link>
        <Link href="/dashboard/study/data-safeguards" className="border border-slate-200 bg-white p-5 transition hover:border-teal-700"><ShieldCheck className="text-teal-700" size={20} aria-hidden="true" /><h2 className="mt-4 font-semibold text-slate-950">Data safeguards</h2><p className="mt-2 text-sm leading-6 text-slate-600">Explain that the presentation contains no patient information or production data.</p><span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-teal-800">Open safeguards <ArrowRight size={15} aria-hidden="true" /></span></Link>
        <Link href="/dashboard/study/clinical-monitoring" className="border border-slate-200 bg-white p-5 transition hover:border-teal-700"><Activity className="text-teal-700" size={20} aria-hidden="true" /><h2 className="mt-4 font-semibold text-slate-950">Clinical monitoring</h2><p className="mt-2 text-sm leading-6 text-slate-600">Review simulated SDV completion, investigational product logs, and adherence.</p><span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-teal-800">Open monitoring <ArrowRight size={15} aria-hidden="true" /></span></Link>
        <Link href="/dashboard/study/safety-surveillance" className="border border-slate-200 bg-white p-5 transition hover:border-teal-700"><ShieldAlert className="text-teal-700" size={20} aria-hidden="true" /><h2 className="mt-4 font-semibold text-slate-950">Safety surveillance</h2><p className="mt-2 text-sm leading-6 text-slate-600">Explore expedited reporting workflows, signal detection metrics, and DSMB review.</p><span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-teal-800">Open safety <ArrowRight size={15} aria-hidden="true" /></span></Link>
        <Link href="/dashboard/study/cdisc-standards" className="border border-slate-200 bg-white p-5 transition hover:border-teal-700"><Database className="text-teal-700" size={20} aria-hidden="true" /><h2 className="mt-4 font-semibold text-slate-950">CDISC export</h2><p className="mt-2 text-sm leading-6 text-slate-600">Verify SDTM mapping compliance across Demographics, Visits, and AE domains.</p><span className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-teal-800">Open CDISC <ArrowRight size={15} aria-hidden="true" /></span></Link>
      </section>
    </div>
  );
}
