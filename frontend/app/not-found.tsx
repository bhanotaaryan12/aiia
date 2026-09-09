import Link from "next/link";

export default function NotFound() {
  return <main className="flex min-h-screen items-center justify-center bg-slate-50 px-5"><div className="max-w-md border border-slate-200 bg-white p-8"><p className="text-sm font-semibold text-teal-700">404</p><h1 className="mt-2 text-2xl font-semibold text-slate-950">This page is not part of the prototype</h1><p className="mt-3 text-sm leading-6 text-slate-600">Return to the presentation workspace or review the demo guide.</p><div className="mt-6 flex gap-3"><Link href="/dashboard" className="rounded-md bg-teal-700 px-4 py-2.5 text-sm font-semibold text-white">Open workspace</Link><Link href="/faq" className="rounded-md border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800">FAQ</Link></div></div></main>;
}
