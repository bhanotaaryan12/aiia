import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = { title: "Frequently asked questions", description: "Questions about the AIIA Study Workspace presentation prototype.", alternates: { canonical: "/faq" } };

const items = [["Is this a live CTMS?", "No. It is a presentation prototype that uses illustrative workflow states and no live patient or trial records."], ["Can I enter trial data?", "No. Do not enter personal, clinical, or operational data into this environment."], ["Why is a demo login used?", "It lets a presenter show the authenticated workspace while keeping the prototype distinct from a production identity system."], ["Does the demo use analytics cookies?", "No advertising or analytics cookies are enabled by default. Essential local storage supports the demo session and consent choice."]];

export default function FaqPage() {
  return <main className="mx-auto min-h-screen max-w-3xl px-5 py-14"><Link href="/login" className="text-sm font-medium text-teal-800 underline underline-offset-2">Back to sign in</Link><h1 className="mt-8 text-3xl font-semibold text-slate-950">Frequently asked questions</h1><div className="mt-7 divide-y divide-slate-200 border-y border-slate-200">{items.map(([question, answer]) => <section key={question} className="py-5"><h2 className="font-semibold text-slate-950">{question}</h2><p className="mt-2 text-sm leading-6 text-slate-600">{answer}</p></section>)}</div></main>;
}
