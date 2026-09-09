"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function CookieConsent() {
  const [visible, setVisible] = useState(false);
  useEffect(() => setVisible(!localStorage.getItem("cookie-preference")), []);
  if (!visible) return null;
  const choose = (value: "essential" | "declined") => { localStorage.setItem("cookie-preference", value); setVisible(false); };
  return <aside className="fixed inset-x-4 bottom-4 z-50 mx-auto max-w-xl border border-slate-300 bg-white p-4 shadow-lg" aria-label="Cookie preferences"><p className="text-sm font-semibold text-slate-950">Cookie choice</p><p className="mt-1 text-sm leading-6 text-slate-600">This demo uses essential browser storage for sign-in and your cookie preference. It does not run advertising or analytics cookies.</p><div className="mt-4 flex flex-wrap items-center gap-3"><button onClick={() => choose("essential")} className="rounded-md bg-teal-700 px-3 py-2 text-sm font-semibold text-white hover:bg-teal-800">Accept essential</button><button onClick={() => choose("declined")} className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50">Decline optional</button><Link href="/privacy" className="text-sm font-medium text-teal-800 underline underline-offset-2">Privacy details</Link></div></aside>;
}
