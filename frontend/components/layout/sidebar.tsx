"use client";

import Link from "next/link";
import { BookOpen, FileText, LayoutPanelTop } from "lucide-react";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const nav = [
  { name: "Workspace", href: "/dashboard", icon: LayoutPanelTop },
  { name: "Study record", href: "/dashboard/study", icon: FileText },
  { name: "Demo guide", href: "/dashboard/guide", icon: BookOpen },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="fixed inset-y-0 left-0 z-40 hidden w-60 border-r border-slate-200 bg-white lg:flex lg:flex-col">
      <div className="border-b border-slate-200 p-5">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-teal-700 text-sm font-bold text-white">A</div>
          <div><p className="text-sm font-semibold text-slate-950">AIIA CTMS</p><p className="text-xs text-slate-500">Presentation workspace</p></div>
        </Link>
      </div>
      <nav className="flex-1 p-3" aria-label="Presentation navigation">
        {nav.map(({ name, href, icon: Icon }) => {
          const active = pathname === href;
          return <Link key={href} href={href} className={cn("mb-1 flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition", active ? "bg-teal-50 text-teal-900" : "text-slate-600 hover:bg-slate-50 hover:text-slate-950")}><Icon size={17} aria-hidden="true" />{name}</Link>;
        })}
      </nav>
      <div className="border-t border-slate-200 p-4 text-xs leading-5 text-slate-500">Presentation prototype<br />No live trial data</div>
    </aside>
  );
}
