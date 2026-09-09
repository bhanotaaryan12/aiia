"use client";

import Link from "next/link";
import { LogOut } from "lucide-react";
import { getUser, logout } from "@/lib/api";

export default function Topbar() {
  const user = getUser();
  return (
    <header className="fixed inset-x-0 top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 lg:left-60 lg:px-7">
      <Link href="/dashboard" className="flex items-center gap-2 lg:hidden"><span className="flex h-8 w-8 items-center justify-center rounded-md bg-teal-700 text-sm font-bold text-white">A</span><span className="text-sm font-semibold text-slate-950">AIIA CTMS</span></Link>
      <p className="hidden text-sm text-slate-500 lg:block">Study presentation walkthrough</p>
      <div className="flex items-center gap-3"><span className="hidden text-sm text-slate-600 sm:block">{user?.full_name || "Demo user"}</span><button onClick={() => void logout()} className="inline-flex items-center gap-2 rounded-md border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"><LogOut size={16} aria-hidden="true" /><span className="hidden sm:inline">Sign out</span></button></div>
    </header>
  );
}
