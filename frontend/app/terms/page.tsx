import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = { title: "Terms of use", description: "Terms for using the AIIA Study Workspace presentation prototype.", alternates: { canonical: "/terms" } };

export default function TermsPage() {
  return <main className="mx-auto min-h-screen max-w-3xl px-5 py-14"><Link href="/login" className="text-sm font-medium text-teal-800 underline underline-offset-2">Back to sign in</Link><h1 className="mt-8 text-3xl font-semibold text-slate-950">Terms of use</h1><div className="mt-5 space-y-7 text-sm leading-7 text-slate-700"><p>This is a presentation prototype, not a production clinical trial management system. It is provided solely to demonstrate interface concepts and workflow discussion points.</p><section><h2 className="text-lg font-semibold text-slate-950">Permitted use</h2><p>Use only the supplied demonstration account. Do not upload protected health information, enter real study records, or rely on the prototype for clinical, regulatory, or operational decisions.</p></section><section><h2 className="text-lg font-semibold text-slate-950">Security</h2><p>Do not share credentials. A production deployment requires organisation-managed identity, approved hosting, documented access controls, and a security review.</p></section><section><h2 className="text-lg font-semibold text-slate-950">Changes</h2><p>These terms describe this prototype only and must be replaced with organisation-approved terms before any public or production use.</p></section></div></main>;
}
