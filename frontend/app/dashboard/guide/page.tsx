const steps = [
  ["Start", "Introduce the workspace as a focused study governance walkthrough."],
  ["Open the study record", "Use the record to discuss setup, roles, and review readiness."],
  ["Explain safeguards", "Point out the demonstration-data notice and the legal documentation."],
  ["Close", "Use the prototype as a discussion tool, not a live clinical operations system."],
];

export default function GuidePage() {
  return (
    <div className="mx-auto max-w-3xl space-y-8"><section className="border-b border-slate-200 pb-7"><p className="text-sm font-semibold text-teal-700">Demo guide</p><h1 className="mt-2 text-3xl font-semibold text-slate-950">Presentation flow</h1><p className="mt-3 text-sm leading-6 text-slate-600">A short narrative for demonstrating the prototype without making claims about operational scale or live data.</p></section><ol className="border-l border-slate-300 pl-6">{steps.map(([title, detail]) => <li key={title} className="relative pb-7 last:pb-0"><span className="absolute -left-[29px] top-1.5 h-3 w-3 rounded-full bg-teal-700" aria-hidden="true" /><h2 className="font-semibold text-slate-950">{title}</h2><p className="mt-1 text-sm leading-6 text-slate-600">{detail}</p></li>)}</ol></div>
  );
}
