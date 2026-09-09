"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/api";
import Sidebar from "@/components/layout/sidebar";
import Topbar from "@/components/layout/topbar";
import Link from "next/link";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) { router.replace("/login"); return; }
    setReady(true);
  }, [router]);

  if (!ready) return <div className="flex min-h-screen items-center justify-center bg-slate-50 text-sm text-slate-600">Checking presentation access</div>;

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <Topbar />
      <main className="px-4 pb-10 pt-24 lg:ml-60 lg:px-8">{children}</main>
      <footer className="border-t border-slate-200 px-4 py-5 text-center text-xs text-slate-500 lg:ml-60 lg:px-8">
        <Link href="/privacy" className="hover:text-slate-900">Privacy</Link><span className="mx-2">·</span><Link href="/terms" className="hover:text-slate-900">Terms</Link><span className="mx-2">·</span><Link href="/faq" className="hover:text-slate-900">FAQ</Link>
      </footer>
    </div>
  );
}
