"""
AIIA CTMS Frontend Generator - Complete Next.js Application
"""
import os, json

BASE = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\frontend"

def w(path, content):
    fp = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))

# ================================================================
# package.json
# ================================================================
pkg = {
    "name": "aiia-ctms-frontend",
    "version": "1.0.0",
    "private": True,
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint"
    },
    "dependencies": {
        "next": "14.2.5",
        "react": "^18.3.1",
        "react-dom": "^18.3.1",
        "axios": "^1.7.2",
        "recharts": "^2.12.7",
        "lucide-react": "^0.400.0",
        "date-fns": "^3.6.0",
        "clsx": "^2.1.1",
        "tailwind-merge": "^2.4.0",
        "react-hook-form": "^7.52.1",
        "@hookform/resolvers": "^3.9.0",
        "zod": "^3.23.8"
    },
    "devDependencies": {
        "@types/node": "^20",
        "@types/react": "^18",
        "@types/react-dom": "^18",
        "typescript": "^5",
        "tailwindcss": "^3.4.4",
        "postcss": "^8",
        "autoprefixer": "^10"
    }
}
w("package.json", json.dumps(pkg, indent=2))

# ================================================================
# next.config.js
# ================================================================
w("next.config.js", '''
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL ? `${process.env.NEXT_PUBLIC_API_URL.replace('/api/v1', '')}/:path*` : 'http://localhost:8000/api/:path*',
      },
    ];
  },
};
module.exports = nextConfig;
''')

# ================================================================
# tsconfig.json
# ================================================================
w("tsconfig.json", json.dumps({
    "compilerOptions": {
        "lib": ["dom", "dom.iterable", "esnext"],
        "allowJs": True,
        "skipLibCheck": True,
        "strict": True,
        "noEmit": True,
        "esModuleInterop": True,
        "module": "esnext",
        "moduleResolution": "bundler",
        "resolveJsonModule": True,
        "isolatedModules": True,
        "jsx": "preserve",
        "incremental": True,
        "plugins": [{"name": "next"}],
        "paths": {"@/*": ["./*"]}
    },
    "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
    "exclude": ["node_modules"]
}, indent=2))

# ================================================================
# postcss.config.js
# ================================================================
w("postcss.config.js", '''
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
''')

# ================================================================
# tailwind.config.ts
# ================================================================
w("tailwind.config.ts", '''
import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}", "./lib/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { 50: "#eff6ff", 100: "#dbeafe", 200: "#bfdbfe", 300: "#93c5fd", 400: "#60a5fa", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8", 800: "#1e40af", 900: "#1e3a8a" },
        clinical: { DEFAULT: "#1e40af", light: "#3b82f6", dark: "#1e3a8a" },
      },
    },
  },
  plugins: [],
};
export default config;
''')

# ================================================================
# Dockerfile
# ================================================================
w("Dockerfile", '''
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
''')

# ================================================================
# app/globals.css
# ================================================================
w("app/globals.css", '''
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root { --font-sans: 'Inter', system-ui, sans-serif; }
body { font-family: var(--font-sans); }

@layer base {
  * { @apply border-gray-200; }
  body { @apply bg-gray-50 text-gray-900; }
}

@layer utilities {
  .scrollbar-thin { scrollbar-width: thin; }
  .scrollbar-thin::-webkit-scrollbar { width: 6px; }
  .scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
  .scrollbar-thin::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 3px; }
}
''')

# ================================================================
# lib/api.ts
# ================================================================
w("lib/api.ts", '''
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({ baseURL: API_URL, headers: { "Content-Type": "application/json" } });

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;

export async function login(email: string, password: string) {
  const res = await api.post("/auth/login", { email, password });
  const { access_token, refresh_token } = res.data;
  localStorage.setItem("access_token", access_token);
  localStorage.setItem("refresh_token", refresh_token);
  const me = await api.get("/auth/me");
  localStorage.setItem("user", JSON.stringify(me.data));
  return me.data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
  window.location.href = "/login";
}

export function getUser() {
  if (typeof window === "undefined") return null;
  const u = localStorage.getItem("user");
  return u ? JSON.parse(u) : null;
}

export function isAuthenticated() {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem("access_token");
}
''')

# ================================================================
# lib/utils.ts
# ================================================================
w("lib/utils.ts", '''
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }

export function formatDate(d: string | null | undefined): string {
  if (!d) return "—";
  return new Date(d).toLocaleDateString("en-IN", { year: "numeric", month: "short", day: "numeric" });
}

export function statusColor(status: string): string {
  const colors: Record<string, string> = {
    PLANNING: "bg-gray-100 text-gray-700",
    ETHICS_PENDING: "bg-yellow-100 text-yellow-800",
    ETHICS_APPROVED: "bg-blue-100 text-blue-800",
    REGULATORY_PENDING: "bg-orange-100 text-orange-800",
    REGISTERED: "bg-indigo-100 text-indigo-800",
    RECRUITING: "bg-emerald-100 text-emerald-800",
    ACTIVE: "bg-green-100 text-green-800",
    COMPLETED: "bg-teal-100 text-teal-800",
    SUSPENDED: "bg-red-100 text-red-800",
    TERMINATED: "bg-red-200 text-red-900",
    SCREENED: "bg-gray-100 text-gray-700",
    ELIGIBLE: "bg-blue-100 text-blue-700",
    CONSENTED: "bg-indigo-100 text-indigo-700",
    ENROLLED: "bg-cyan-100 text-cyan-800",
    RANDOMIZED: "bg-purple-100 text-purple-800",
    WITHDRAWN: "bg-red-100 text-red-700",
    SCHEDULED: "bg-blue-100 text-blue-700",
    OVERDUE: "bg-red-100 text-red-700",
    MISSED: "bg-gray-200 text-gray-600",
    OPEN: "bg-amber-100 text-amber-800",
    CLOSED: "bg-gray-100 text-gray-600",
    MILD: "bg-green-100 text-green-700",
    MODERATE: "bg-yellow-100 text-yellow-800",
    SEVERE: "bg-red-100 text-red-700",
    SERIOUS: "bg-red-200 text-red-800",
    NON_SERIOUS: "bg-gray-100 text-gray-700",
    APPROVED: "bg-green-100 text-green-800",
    REJECTED: "bg-red-100 text-red-800",
    SUBMITTED: "bg-blue-100 text-blue-700",
    UNDER_REVIEW: "bg-yellow-100 text-yellow-800",
    DRAFT: "bg-gray-100 text-gray-600",
    REPORTED: "bg-orange-100 text-orange-800",
    NOT_STARTED: "bg-gray-100 text-gray-600",
    PREPARING: "bg-yellow-100 text-yellow-700",
  };
  return colors[status] || "bg-gray-100 text-gray-700";
}
''')

# ================================================================
# app/layout.tsx (Root)
# ================================================================
w("app/layout.tsx", '''
import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIIA Clinical Trials Dashboard",
  description: "Clinical Trial Management System for Ayurveda Research",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
''')

# ================================================================
# app/page.tsx (Root redirect)
# ================================================================
w("app/page.tsx", '''
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/api";

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace(isAuthenticated() ? "/dashboard" : "/login");
  }, [router]);
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-800"></div>
    </div>
  );
}
''')

# ================================================================
# app/login/page.tsx
# ================================================================
w("app/login/page.tsx", '''
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-teal-50">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-blue-800 text-white text-2xl font-bold mb-4">A</div>
            <h1 className="text-2xl font-bold text-gray-900">AIIA Clinical Trials</h1>
            <p className="text-sm text-gray-500 mt-1">Clinical Trial Management System</p>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">{error}</div>}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="admin@aiia.gov.in" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition" placeholder="••••••••" />
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-2.5 px-4 bg-blue-800 hover:bg-blue-900 text-white font-medium rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed">
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>
          <div className="mt-6 pt-6 border-t border-gray-100">
            <p className="text-xs text-gray-500 text-center">Demo: admin@aiia.gov.in / Demo@12345</p>
          </div>
        </div>
        <p className="text-xs text-gray-400 text-center mt-4">Designed to support GCP-aligned clinical research workflows</p>
      </div>
    </div>
  );
}
''')

# ================================================================
# components/layout/sidebar.tsx
# ================================================================
w("components/layout/sidebar.tsx", '''
"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const nav = [
  { name: "Dashboard", href: "/dashboard", icon: "📊" },
  { name: "Trials", href: "/dashboard/trials", icon: "🧪" },
  { name: "Sites", href: "/dashboard/sites", icon: "🏥" },
  { name: "Participants", href: "/dashboard/participants", icon: "👥" },
  { name: "Visits", href: "/dashboard/visits", icon: "📅" },
  { name: "Clinical Data", href: "/dashboard/clinical-data", icon: "📋" },
  { name: "Ethics", href: "/dashboard/ethics", icon: "🛡️" },
  { name: "Regulatory", href: "/dashboard/regulatory", icon: "📜" },
  { name: "Pharmacovigilance", href: "/dashboard/pharmacovigilance", icon: "⚠️" },
  { name: "Documents", href: "/dashboard/documents", icon: "📄" },
  { name: "Analytics", href: "/dashboard/analytics", icon: "📈" },
  { name: "Audit Logs", href: "/dashboard/audit", icon: "🔍" },
  { name: "Administration", href: "/dashboard/admin", icon: "⚙️" },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="fixed left-0 top-0 h-full w-60 bg-white border-r border-gray-200 flex flex-col z-40">
      <div className="p-4 border-b border-gray-100">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-blue-800 text-white flex items-center justify-center font-bold text-lg">A</div>
          <div>
            <h1 className="text-sm font-bold text-gray-900 leading-tight">AIIA CTMS</h1>
            <p className="text-[10px] text-gray-500 leading-tight">Clinical Trials Dashboard</p>
          </div>
        </Link>
      </div>
      <nav className="flex-1 overflow-y-auto py-2 scrollbar-thin">
        {nav.map((item) => {
          const active = pathname === item.href || (item.href !== "/dashboard" && pathname.startsWith(item.href));
          return (
            <Link key={item.href} href={item.href}
              className={cn("flex items-center gap-3 px-4 py-2.5 mx-2 rounded-lg text-sm font-medium transition-colors",
                active ? "bg-blue-50 text-blue-800" : "text-gray-600 hover:bg-gray-50 hover:text-gray-900")}>
              <span className="text-base">{item.icon}</span>
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-3 border-t border-gray-100 text-[10px] text-gray-400 text-center">
        AIIA CTMS v1.0
      </div>
    </aside>
  );
}
''')

# ================================================================
# components/layout/topbar.tsx
# ================================================================
w("components/layout/topbar.tsx", '''
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUser, logout } from "@/lib/api";
import api from "@/lib/api";

export default function Topbar() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [unread, setUnread] = useState(0);
  const [showMenu, setShowMenu] = useState(false);
  const [search, setSearch] = useState("");
  const [searchResults, setSearchResults] = useState<any[]>([]);

  useEffect(() => {
    setUser(getUser());
    api.get("/notifications/unread-count").then(r => setUnread(r.data.count)).catch(() => {});
  }, []);

  const handleSearch = async (q: string) => {
    setSearch(q);
    if (q.length < 2) { setSearchResults([]); return; }
    try {
      const r = await api.get(`/search/?q=${encodeURIComponent(q)}`);
      setSearchResults(r.data.results || []);
    } catch { setSearchResults([]); }
  };

  return (
    <header className="fixed top-0 left-60 right-0 h-14 bg-white border-b border-gray-200 flex items-center justify-between px-6 z-30">
      <div className="relative flex-1 max-w-lg">
        <input type="text" placeholder="Search trials, participants, sites..." value={search} onChange={(e) => handleSearch(e.target.value)}
          className="w-full pl-9 pr-4 py-2 text-sm bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" />
        <span className="absolute left-3 top-2.5 text-gray-400 text-sm">🔍</span>
        {searchResults.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-64 overflow-auto z-50">
            {searchResults.map((r: any, i: number) => (
              <button key={i} onClick={() => { setSearch(""); setSearchResults([]); router.push(`/dashboard/${r.type === "trial" ? "trials" : r.type === "participant" ? "participants" : r.type === "site" ? "sites" : r.type === "adverse_event" ? "pharmacovigilance" : r.type + "s"}/${r.id}`); }}
                className="w-full text-left px-4 py-2 hover:bg-gray-50 flex items-center gap-3 text-sm border-b border-gray-100 last:border-0">
                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded capitalize">{r.type}</span>
                <span className="font-medium">{r.title}</span>
                <span className="text-gray-400 text-xs ml-auto">{r.subtitle}</span>
              </button>
            ))}
          </div>
        )}
      </div>
      <div className="flex items-center gap-4 ml-4">
        <button onClick={() => router.push("/dashboard/notifications")} className="relative p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg">
          🔔 {unread > 0 && <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">{unread}</span>}
        </button>
        <div className="relative">
          <button onClick={() => setShowMenu(!showMenu)} className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-gray-100 transition">
            <div className="w-8 h-8 rounded-full bg-blue-800 text-white flex items-center justify-center text-sm font-medium">
              {user?.full_name?.[0] || "U"}
            </div>
            <div className="text-left hidden sm:block">
              <p className="text-sm font-medium text-gray-700">{user?.full_name || "User"}</p>
              <p className="text-[10px] text-gray-400">{user?.roles?.[0] || ""}</p>
            </div>
          </button>
          {showMenu && (
            <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
              <div className="px-4 py-3 border-b border-gray-100">
                <p className="text-sm font-medium">{user?.full_name}</p>
                <p className="text-xs text-gray-400">{user?.email}</p>
              </div>
              <button onClick={() => { setShowMenu(false); logout(); }}
                className="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50">Sign Out</button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
''')

# ================================================================
# app/(dashboard)/layout.tsx
# ================================================================
w("app/(dashboard)/layout.tsx", '''
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/api";
import Sidebar from "@/components/layout/sidebar";
import Topbar from "@/components/layout/topbar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) { router.replace("/login"); return; }
    setReady(true);
  }, [router]);

  if (!ready) return <div className="min-h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-800" /></div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <Topbar />
      <main className="ml-60 mt-14 p-6">{children}</main>
    </div>
  );
}
''')

print("Frontend foundation generated.")

# ================================================================
# MAIN DASHBOARD PAGE
# ================================================================
w("app/(dashboard)/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area, Legend, LineChart, Line } from "recharts";

const COLORS = ["#1e40af", "#0d9488", "#d97706", "#dc2626", "#7c3aed", "#059669", "#ea580c", "#64748b"];

function KPICard({ title, value, icon, color, subtitle }: any) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${color || "bg-blue-50 text-blue-700"}`}>{subtitle || ""}</span>
      </div>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-500 mt-1">{title}</p>
    </div>
  );
}

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/analytics/dashboard")
      .then((r) => { setData(r.data); setLoading(false); })
      .catch((e) => { setError("Failed to load dashboard data"); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1,2,3,4,5,6,7,8].map(i => <div key={i} className="bg-white rounded-xl border border-gray-200 p-5 h-28 animate-pulse"><div className="h-4 bg-gray-200 rounded w-1/2 mb-3"></div><div className="h-8 bg-gray-200 rounded w-1/3"></div></div>)}
      </div>
    </div>
  );

  if (error) return <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">{error}</div>;

  const k = data?.kpis || {};
  const trialStatusData = (data?.trial_status_distribution?.labels || []).map((l: string, i: number) => ({
    name: l.replace(/_/g, " "), value: data.trial_status_distribution.datasets[0]?.data[i] || 0,
  }));
  const enrollmentData = (data?.enrollment_by_site?.labels || []).map((l: string, i: number) => ({
    name: l, enrolled: data.enrollment_by_site.datasets[0]?.data[i] || 0,
  }));
  const funnelData = (data?.participant_funnel?.labels || []).map((l: string, i: number) => ({
    name: l, count: data.participant_funnel.datasets[0]?.data[i] || 0,
  }));
  const aeData = (data?.ae_trend?.labels || []).map((l: string, i: number) => ({
    name: l, count: data.ae_trend.datasets[0]?.data[i] || 0,
  }));
  const recruitmentData = (data?.recruitment_trend?.labels || []).map((l: string, i: number) => ({
    name: l, enrolled: data.recruitment_trend.datasets[0]?.data[i] || 0,
  }));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clinical Trials Dashboard</h1>
          <p className="text-sm text-gray-500">Real-time overview of all active clinical research</p>
        </div>
        <div className="text-xs text-gray-400">Last updated: {new Date().toLocaleString()}</div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Active Trials" value={k.active_trials} icon="🧪" subtitle={`${k.recruiting_trials} recruiting`} color="bg-blue-50 text-blue-700" />
        <KPICard title="Total Participants" value={k.total_participants} icon="👥" subtitle={`${k.enrollment_rate}% enrolled`} color="bg-green-50 text-green-700" />
        <KPICard title="Active Sites" value={k.active_sites} icon="🏥" subtitle="across India" color="bg-teal-50 text-teal-700" />
        <KPICard title="Visit Compliance" value={`${k.visit_compliance}%`} icon="📅" subtitle={`${k.overdue_visits} overdue`} color={k.overdue_visits > 0 ? "bg-amber-50 text-amber-700" : "bg-green-50 text-green-700"} />
        <KPICard title="Open SAEs" value={k.open_saes} icon="🚨" subtitle={k.open_saes > 0 ? "requires attention" : "none"} color={k.open_saes > 0 ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700"} />
        <KPICard title="Total AEs" value={k.total_aes} icon="⚠️" subtitle="reported" color="bg-amber-50 text-amber-700" />
        <KPICard title="Pending Ethics" value={k.pending_ethics} icon="🛡️" subtitle={k.pending_ethics > 0 ? "under review" : "none"} color="bg-indigo-50 text-indigo-700" />
        <KPICard title="Data Queries" value={k.open_data_queries} icon="❓" subtitle="open" color="bg-purple-50 text-purple-700" />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Recruitment Over Time</h3>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={recruitmentData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{fontSize: 12}} />
              <YAxis tick={{fontSize: 12}} />
              <Tooltip />
              <Line type="monotone" dataKey="enrolled" stroke="#1e40af" strokeWidth={2} dot={{ fill: "#1e40af" }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Enrollment by Site</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={enrollmentData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{fontSize: 12}} />
              <YAxis dataKey="name" type="category" width={120} tick={{fontSize: 11}} />
              <Tooltip />
              <Bar dataKey="enrolled" fill="#0d9488" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Trial Status Distribution</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={trialStatusData} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="value" label={({name, value}: any) => `${name}: ${value}`}>
                {trialStatusData.map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Participant Funnel</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={funnelData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{fontSize: 11}} />
              <YAxis tick={{fontSize: 12}} />
              <Tooltip />
              <Bar dataKey="count" fill="#7c3aed" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">AE Severity Distribution</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={aeData} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="count" label>
                {aeData.map((_: any, i: number) => <Cell key={i} fill={["#16a34a", "#d97706", "#dc2626"][i] || "#64748b"} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Activity & Deadlines */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Recent Activity</h3>
          <div className="space-y-3 max-h-64 overflow-auto">
            {(data?.recent_activity || []).map((a: any, i: number) => (
              <div key={i} className="flex items-start gap-3 text-sm border-b border-gray-50 pb-2">
                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded mt-0.5">{a.action}</span>
                <div className="flex-1">
                  <p className="text-gray-700">{a.details || `${a.action} ${a.entity_type}`}</p>
                  <p className="text-xs text-gray-400">{a.user_email} · {formatDate(a.timestamp)}</p>
                </div>
              </div>
            ))}
            {(!data?.recent_activity || data.recent_activity.length === 0) && <p className="text-gray-400 text-sm">No recent activity</p>}
          </div>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Upcoming Deadlines</h3>
          <div className="space-y-3 max-h-64 overflow-auto">
            {(data?.upcoming_deadlines || []).map((d: any, i: number) => (
              <div key={i} className="flex items-center gap-3 text-sm border-b border-gray-50 pb-2">
                <span className="text-xs bg-amber-50 text-amber-700 px-2 py-0.5 rounded">{d.type}</span>
                <span className="flex-1 text-gray-700">{d.detail}</span>
                <span className="text-xs text-gray-400">{formatDate(d.date)}</span>
              </div>
            ))}
            {(!data?.upcoming_deadlines || data.upcoming_deadlines.length === 0) && <p className="text-gray-400 text-sm">No upcoming deadlines</p>}
          </div>
        </div>
      </div>
    </div>
  );
}
''')

print("Dashboard page generated.")

# ================================================================
# TRIALS PAGES
# ================================================================
w("app/(dashboard)/trials/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function TrialsPage() {
  const router = useRouter();
  const [trials, setTrials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    api.get("/trials/").then(r => { setTrials(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const filtered = filter ? trials.filter(t => t.status === filter) : trials;

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3].map(i => <div key={i} className="h-16 bg-gray-200 rounded-lg" />)}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clinical Trials</h1>
          <p className="text-sm text-gray-500">{trials.length} trials registered</p>
        </div>
        <button onClick={() => router.push("/dashboard/trials/new")}
          className="px-4 py-2 bg-blue-800 text-white text-sm font-medium rounded-lg hover:bg-blue-900 transition">
          + New Trial
        </button>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["", "PLANNING", "RECRUITING", "ACTIVE", "COMPLETED", "ETHICS_PENDING"].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            className={`px-3 py-1.5 text-xs font-medium rounded-full transition ${filter === s ? "bg-blue-800 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>
            {s || "All"}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Trial</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Protocol #</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Phase</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Sites</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Participants</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Start</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filtered.map((t) => (
              <tr key={t.id} onClick={() => router.push(`/dashboard/trials/${t.id}`)}
                className="hover:bg-gray-50 cursor-pointer transition">
                <td className="px-4 py-3">
                  <p className="font-medium text-gray-900">{t.short_title || t.title?.substring(0, 40)}</p>
                  <p className="text-xs text-gray-400 truncate max-w-xs">{t.title}</p>
                </td>
                <td className="px-4 py-3 text-gray-600">{t.protocol_number || "—"}</td>
                <td className="px-4 py-3 text-gray-600">{t.phase || "—"}</td>
                <td className="px-4 py-3"><span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColor(t.status)}`}>{t.status}</span></td>
                <td className="px-4 py-3 text-gray-600">{t.site_count}</td>
                <td className="px-4 py-3 text-gray-600">{t.participant_count}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(t.start_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <div className="text-center py-12 text-gray-400">No trials found</div>}
      </div>
    </div>
  );
}
''')

w("app/(dashboard)/trials/new/page.tsx", '''
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";

export default function NewTrialPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ title: "", short_title: "", protocol_number: "", phase: "Phase 2", study_type: "Interventional", therapeutic_area: "Ayurveda", ayurveda_system: "", primary_objective: "", planned_sample_size: 60, sponsor: "AIIA", start_date: "", expected_end_date: "", inclusion_criteria: "", exclusion_criteria: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/trials/", { ...form, planned_sample_size: Number(form.planned_sample_size) || null, start_date: form.start_date || null, expected_end_date: form.expected_end_date || null });
      router.push(`/dashboard/trials/${res.data.id}`);
    } catch (err: any) { alert(err.response?.data?.detail || "Failed to create trial"); }
    setLoading(false);
  };

  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Create New Trial</h1>
      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200 p-6 space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Trial Title *</label><input required value={form.title} onChange={e => setForm({...form, title: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Short Title</label><input value={form.short_title} onChange={e => setForm({...form, short_title: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Protocol Number</label><input value={form.protocol_number} onChange={e => setForm({...form, protocol_number: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Phase</label><select value={form.phase} onChange={e => setForm({...form, phase: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"><option>Phase 1</option><option>Phase 2</option><option>Phase 3</option><option>Phase 4</option></select></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Study Type</label><select value={form.study_type} onChange={e => setForm({...form, study_type: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"><option>Interventional</option><option>Observational</option></select></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Ayurveda System</label><input value={form.ayurveda_system} onChange={e => setForm({...form, ayurveda_system: e.target.value})} placeholder="e.g. Rasayana Chikitsa" className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Sample Size</label><input type="number" value={form.planned_sample_size} onChange={e => setForm({...form, planned_sample_size: parseInt(e.target.value) || 0})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label><input type="date" value={form.start_date} onChange={e => setForm({...form, start_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          <div><label className="block text-sm font-medium text-gray-700 mb-1">Expected End Date</label><input type="date" value={form.expected_end_date} onChange={e => setForm({...form, expected_end_date: e.target.value})} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" /></div>
          <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Primary Objective</label><textarea value={form.primary_objective} onChange={e => setForm({...form, primary_objective: e.target.value})} rows={3} className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" /></div>
        </div>
        <div className="flex gap-3 pt-4">
          <button type="submit" disabled={loading} className="px-6 py-2 bg-blue-800 text-white text-sm font-medium rounded-lg hover:bg-blue-900 disabled:opacity-50">{loading ? "Creating..." : "Create Trial"}</button>
          <button type="button" onClick={() => router.back()} className="px-6 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-200">Cancel</button>
        </div>
      </form>
    </div>
  );
}
''')

w("app/(dashboard)/trials/[id]/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function TrialDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [trial, setTrial] = useState<any>(null);
  const [arms, setArms] = useState<any[]>([]);
  const [participants, setParticipants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState("overview");

  useEffect(() => {
    Promise.all([
      api.get(`/trials/${id}`),
      api.get(`/trials/${id}/arms`),
      api.get(`/participants/?trial_id=${id}&limit=20`),
    ]).then(([t, a, p]) => {
      setTrial(t.data); setArms(a.data); setParticipants(p.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="animate-pulse space-y-4"><div className="h-32 bg-gray-200 rounded-xl" /><div className="h-64 bg-gray-200 rounded-xl" /></div>;
  if (!trial) return <div className="text-center py-12 text-gray-400">Trial not found</div>;

  const tabs = ["overview", "participants", "sites", "safety"];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColor(trial.status)}`}>{trial.status}</span>
              <span className="text-sm text-gray-500">{trial.protocol_number}</span>
              {trial.phase && <span className="text-xs bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full">{trial.phase}</span>}
            </div>
            <h1 className="text-xl font-bold text-gray-900">{trial.title}</h1>
            <p className="text-sm text-gray-500 mt-1">{trial.therapeutic_area} · {trial.ayurveda_system}</p>
          </div>
        </div>
        <div className="grid grid-cols-4 gap-4 mt-6 pt-4 border-t border-gray-100">
          <div><p className="text-xs text-gray-400">Sponsor</p><p className="text-sm font-medium">{trial.sponsor || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Sample Size</p><p className="text-sm font-medium">{trial.planned_sample_size || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Start Date</p><p className="text-sm font-medium">{formatDate(trial.start_date)}</p></div>
          <div><p className="text-xs text-gray-400">End Date</p><p className="text-sm font-medium">{formatDate(trial.expected_end_date)}</p></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        {tabs.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition ${tab === t ? "border-blue-800 text-blue-800" : "border-transparent text-gray-500 hover:text-gray-700"}`}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {tab === "overview" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Primary Objective</h3>
            <p className="text-sm text-gray-600">{trial.primary_objective || "Not specified"}</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-5">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Study Arms ({arms.length})</h3>
            {arms.map((a: any) => (
              <div key={a.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-medium">{a.name}</p>
                  <p className="text-xs text-gray-400">{a.arm_type}</p>
                </div>
                <span className="text-xs text-gray-500">Ratio: {a.allocation_ratio}</span>
              </div>
            ))}
            {arms.length === 0 && <p className="text-sm text-gray-400">No study arms defined</p>}
          </div>
        </div>
      )}

      {tab === "participants" && (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b"><tr>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Participant ID</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Age</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Gender</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Enrolled</th>
            </tr></thead>
            <tbody className="divide-y divide-gray-100">
              {participants.map((p: any) => (
                <tr key={p.id} onClick={() => router.push(`/dashboard/participants/${p.id}`)} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-4 py-3 font-medium">{p.participant_id}</td>
                  <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(p.status)}`}>{p.status}</span></td>
                  <td className="px-4 py-3 text-gray-600">{p.age || "—"}</td>
                  <td className="px-4 py-3 text-gray-600">{p.gender || "—"}</td>
                  <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(p.enrollment_date)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {participants.length === 0 && <div className="text-center py-8 text-gray-400">No participants yet</div>}
        </div>
      )}
    </div>
  );
}
''')

print("Trial pages generated.")

# ================================================================
# REMAINING PAGES (Sites, Participants, Visits, etc.)
# ================================================================
w("app/(dashboard)/sites/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { statusColor } from "@/lib/utils";

export default function SitesPage() {
  const [sites, setSites] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/sites/").then(r => { setSites(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3].map(i => <div key={i} className="h-16 bg-gray-200 rounded-lg" />)}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-gray-900">Research Sites</h1><p className="text-sm text-gray-500">{sites.length} sites registered</p></div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sites.map(s => (
          <div key={s.id} className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition">
            <div className="flex items-start justify-between mb-3">
              <span className="text-2xl">🏥</span>
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(s.status)}`}>{s.status}</span>
            </div>
            <h3 className="font-semibold text-gray-900">{s.name}</h3>
            <p className="text-sm text-gray-500">{s.institution}</p>
            <p className="text-xs text-gray-400 mt-1">{s.city}, {s.state}</p>
            <div className="mt-4 pt-3 border-t border-gray-100 flex justify-between text-xs text-gray-500">
              <span>Target: {s.target_enrollment || "—"}</span>
              <span>Enrolled: {s.participant_count || 0}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
''')

w("app/(dashboard)/participants/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function ParticipantsPage() {
  const router = useRouter();
  const [participants, setParticipants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    let url = "/participants/?limit=100";
    if (filter) url += `&status=${filter}`;
    if (search) url += `&search=${search}`;
    api.get(url).then(r => { setParticipants(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, [filter, search]);

  if (loading) return <div className="animate-pulse space-y-4">{[1,2,3,4,5].map(i => <div key={i} className="h-12 bg-gray-200 rounded" />)}</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-gray-900">Participants</h1><p className="text-sm text-gray-500">{participants.length} participants</p></div>
      </div>
      <div className="flex gap-2 flex-wrap items-center">
        <input type="text" placeholder="Search by ID..." value={search} onChange={e => setSearch(e.target.value)} className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm w-48" />
        {["", "SCREENED", "CONSENTED", "ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED", "WITHDRAWN"].map(s => (
          <button key={s} onClick={() => setFilter(s)} className={`px-3 py-1.5 text-xs font-medium rounded-full ${filter === s ? "bg-blue-800 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}>{s || "All"}</button>
        ))}
      </div>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">ID</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Age</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Gender</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Screening</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Enrollment</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {participants.map(p => (
              <tr key={p.id} onClick={() => router.push(`/dashboard/participants/${p.id}`)} className="hover:bg-gray-50 cursor-pointer">
                <td className="px-4 py-3 font-medium text-blue-800">{p.participant_id}</td>
                <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(p.status)}`}>{p.status}</span></td>
                <td className="px-4 py-3 text-gray-600">{p.age || "—"}</td>
                <td className="px-4 py-3 text-gray-600">{p.gender || "—"}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(p.screening_date)}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(p.enrollment_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {participants.length === 0 && <div className="text-center py-12 text-gray-400">No participants found</div>}
      </div>
    </div>
  );
}
''')

w("app/(dashboard)/participants/[id]/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function ParticipantDetail() {
  const { id } = useParams();
  const [p, setP] = useState<any>(null);
  const [visits, setVisits] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get(`/participants/${id}`), api.get(`/visits/?participant_id=${id}`)]).then(([pr, vr]) => {
      setP(pr.data); setVisits(vr.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="animate-pulse"><div className="h-48 bg-gray-200 rounded-xl" /></div>;
  if (!p) return <div className="text-gray-400 text-center py-12">Participant not found</div>;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-14 h-14 bg-blue-100 text-blue-800 rounded-xl flex items-center justify-center text-xl font-bold">👤</div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">{p.participant_id}</h1>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(p.status)}`}>{p.status}</span>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-100">
          <div><p className="text-xs text-gray-400">Age</p><p className="text-sm font-medium">{p.age || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Gender</p><p className="text-sm font-medium">{p.gender || "—"}</p></div>
          <div><p className="text-xs text-gray-400">Screening Date</p><p className="text-sm font-medium">{formatDate(p.screening_date)}</p></div>
          <div><p className="text-xs text-gray-400">Enrollment Date</p><p className="text-sm font-medium">{formatDate(p.enrollment_date)}</p></div>
        </div>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h3 className="text-sm font-semibold text-gray-700 mb-4">Visits ({visits.length})</h3>
        <div className="space-y-2">
          {visits.map((v: any) => (
            <div key={v.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="text-sm font-medium">{v.visit_name || "Visit"}</p>
                <p className="text-xs text-gray-400">Scheduled: {formatDate(v.scheduled_date)}</p>
              </div>
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(v.status)}`}>{v.status}</span>
            </div>
          ))}
          {visits.length === 0 && <p className="text-sm text-gray-400">No visits recorded</p>}
        </div>
      </div>
    </div>
  );
}
''')

# Remaining pages
for page, title, endpoint, cols in [
    ("visits", "Visit Schedule", "/visits/?limit=100", [("visit_name", "Visit"), ("status", "Status"), ("scheduled_date", "Scheduled"), ("actual_date", "Actual")]),
    ("ethics", "Ethics Management", "/ethics/submissions", [("title", "Submission"), ("submission_type", "Type"), ("status", "Status"), ("submission_date", "Date")]),
    ("regulatory", "Regulatory Tracking", "/regulatory/records", [("record_type", "Type"), ("registration_number", "Registration #"), ("status", "Status"), ("submission_date", "Date")]),
    ("documents", "Documents", "/documents/", [("title", "Title"), ("document_type", "Type"), ("version", "Version"), ("status", "Status")]),
    ("notifications", "Notifications", "/notifications/", [("title", "Title"), ("message", "Message"), ("type", "Type"), ("is_read", "Read")]),
]:
    w(f"app/(dashboard)/{page}/page.tsx", f'''
"use client";
import {{ useState, useEffect }} from "react";
import api from "@/lib/api";
import {{ formatDate, statusColor }} from "@/lib/utils";

export default function {page.capitalize().replace("-", "")}Page() {{
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    api.get("{endpoint}").then(r => {{ setData(Array.isArray(r.data) ? r.data : []); setLoading(false); }}).catch(() => setLoading(false));
  }}, []);

  if (loading) return <div className="animate-pulse space-y-4">{{[1,2,3].map(i => <div key={{i}} className="h-12 bg-gray-200 rounded" />)}}</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            {"".join(f'<th className="text-left px-4 py-3 font-medium text-gray-600">{c[1]}</th>' for c in cols)}
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {{data.map((item: any, idx: number) => (
              <tr key={{idx}} className="hover:bg-gray-50">
                {"".join(f'<td className="px-4 py-3 text-gray-600">{{String(item.{c[0]} ?? "—").substring(0, 60)}}</td>' for c in cols)}
              </tr>
            ))}}
          </tbody>
        </table>
        {{data.length === 0 && <div className="text-center py-12 text-gray-400">No data available</div>}}
      </div>
    </div>
  );
}}
''')

# Pharmacovigilance page (special - with safety cards)
w("app/(dashboard)/pharmacovigilance/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { formatDate, statusColor } from "@/lib/utils";

export default function PharmacovigilancePage() {
  const [aes, setAEs] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>({});
  const [saes, setSAEs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/pharmacovigilance/adverse-events"),
      api.get("/pharmacovigilance/summary"),
      api.get("/pharmacovigilance/serious-adverse-events"),
    ]).then(([a, s, se]) => {
      setAEs(a.data); setSummary(s.data); setSAEs(se.data); setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse space-y-4"><div className="h-24 bg-gray-200 rounded-xl" /><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Pharmacovigilance</h1>

      {/* Safety Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{summary.total_aes || 0}</p>
          <p className="text-sm text-gray-500">Total AEs</p>
        </div>
        <div className="bg-white rounded-xl border border-red-200 p-5 bg-red-50">
          <p className="text-3xl font-bold text-red-700">{summary.total_saes || 0}</p>
          <p className="text-sm text-red-600">Total SAEs</p>
        </div>
        <div className="bg-white rounded-xl border border-amber-200 p-5 bg-amber-50">
          <p className="text-3xl font-bold text-amber-700">{summary.open_saes || 0}</p>
          <p className="text-sm text-amber-600">Open SAEs</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <div className="flex gap-2 text-xs">
            <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded">Mild: {summary.by_severity?.mild || 0}</span>
            <span className="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">Mod: {summary.by_severity?.moderate || 0}</span>
            <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded">Severe: {summary.by_severity?.severe || 0}</span>
          </div>
          <p className="text-sm text-gray-500 mt-2">By Severity</p>
        </div>
      </div>

      {/* AE Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-200"><h3 className="font-semibold">Adverse Events</h3></div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Event Term</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Severity</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Seriousness</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Causality</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Outcome</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Onset</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {aes.map(ae => (
              <tr key={ae.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{ae.event_term}</td>
                <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ae.severity)}`}>{ae.severity}</span></td>
                <td className="px-4 py-3"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor(ae.seriousness)}`}>{ae.seriousness}</span></td>
                <td className="px-4 py-3 text-gray-600">{ae.causality}</td>
                <td className="px-4 py-3 text-gray-600">{ae.outcome}</td>
                <td className="px-4 py-3 text-gray-500 text-xs">{formatDate(ae.onset_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
''')

# Clinical Data page
w("app/(dashboard)/clinical-data/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function ClinicalDataPage() {
  const [forms, setForms] = useState<any[]>([]);
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [queries, setQueries] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get("/forms/"), api.get("/forms/submissions"), api.get("/forms/queries")])
      .then(([f, s, q]) => { setForms(f.data); setSubmissions(s.data); setQueries(q.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Clinical Data (eCRF)</h1>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{forms.length}</p>
          <p className="text-sm text-gray-500">Form Definitions</p>
        </div>
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <p className="text-3xl font-bold text-gray-900">{submissions.length}</p>
          <p className="text-sm text-gray-500">Submissions</p>
        </div>
        <div className="bg-white rounded-xl border border-amber-200 p-5 bg-amber-50">
          <p className="text-3xl font-bold text-amber-700">{queries.filter((q: any) => q.status === "OPEN").length}</p>
          <p className="text-sm text-amber-600">Open Queries</p>
        </div>
      </div>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-5 py-4 border-b"><h3 className="font-semibold">Forms</h3></div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Form Name</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Code</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Version</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {forms.map((f: any) => (
              <tr key={f.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{f.name}</td>
                <td className="px-4 py-3 text-gray-600">{f.code || "—"}</td>
                <td className="px-4 py-3 text-gray-600">{f.version}</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700">{f.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
''')

# Analytics page
w("app/(dashboard)/analytics/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, Legend } from "recharts";

const COLORS = ["#1e40af", "#0d9488", "#d97706", "#dc2626", "#7c3aed", "#059669"];

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/analytics/dashboard").then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-96 bg-gray-200 rounded-xl" /></div>;
  if (!data) return <div className="text-gray-400 text-center py-12">No analytics data</div>;

  const k = data.kpis;
  const enrollData = (data.enrollment_by_site?.labels || []).map((l: string, i: number) => ({ name: l, count: data.enrollment_by_site.datasets[0]?.data[i] || 0 }));
  const funnelData = (data.participant_funnel?.labels || []).map((l: string, i: number) => ({ name: l, count: data.participant_funnel.datasets[0]?.data[i] || 0 }));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Analytics & Reports</h1>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.total_participants}</p><p className="text-sm text-gray-500">Total Participants</p></div>
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.enrollment_rate}%</p><p className="text-sm text-gray-500">Enrollment Rate</p></div>
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.visit_compliance}%</p><p className="text-sm text-gray-500">Visit Compliance</p></div>
        <div className="bg-white rounded-xl border p-5"><p className="text-2xl font-bold">{k.total_aes}</p><p className="text-sm text-gray-500">Adverse Events</p></div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Enrollment by Site</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={enrollData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{fontSize: 10}} angle={-20} /><YAxis /><Tooltip /><Bar dataKey="count" fill="#1e40af" radius={[4,4,0,0]} /></BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl border p-5">
          <h3 className="text-sm font-semibold text-gray-700 mb-4">Participant Lifecycle Funnel</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={funnelData}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" tick={{fontSize: 11}} /><YAxis /><Tooltip /><Bar dataKey="count" fill="#7c3aed" radius={[4,4,0,0]} /></BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
''')

# Audit page
w("app/(dashboard)/audit/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";
import { formatDate } from "@/lib/utils";

export default function AuditPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/audit/?limit=100").then(r => { setLogs(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Audit Logs</h1>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Timestamp</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">User</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Action</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Entity</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Details</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {logs.map((l: any) => (
              <tr key={l.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-xs text-gray-500">{formatDate(l.timestamp)}</td>
                <td className="px-4 py-3 text-gray-600">{l.user_email || "—"}</td>
                <td className="px-4 py-3"><span className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs font-medium">{l.action}</span></td>
                <td className="px-4 py-3 text-gray-600">{l.entity_type}</td>
                <td className="px-4 py-3 text-gray-500 text-xs truncate max-w-xs">{l.details || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {logs.length === 0 && <div className="text-center py-12 text-gray-400">No audit logs</div>}
      </div>
    </div>
  );
}
''')

# Admin page
w("app/(dashboard)/admin/page.tsx", '''
"use client";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function AdminPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/users/").then(r => { setUsers(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse"><div className="h-64 bg-gray-200 rounded-xl" /></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Administration</h1>
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <div className="px-5 py-4 border-b"><h3 className="font-semibold">Users ({users.length})</h3></div>
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b"><tr>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Email</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Roles</th>
            <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
          </tr></thead>
          <tbody className="divide-y divide-gray-100">
            {users.map((u: any) => (
              <tr key={u.id} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">{u.full_name}</td>
                <td className="px-4 py-3 text-gray-600">{u.email}</td>
                <td className="px-4 py-3"><div className="flex gap-1 flex-wrap">{(u.roles || []).map((r: string) => <span key={r} className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded text-xs">{r}</span>)}</div></td>
                <td className="px-4 py-3">{u.is_active ? <span className="text-green-600 text-xs font-medium">Active</span> : <span className="text-red-600 text-xs">Inactive</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
''')

w("app/(dashboard)/sites/[id]/page.tsx", '''
"use client";
import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export default function SiteDetail() {
  const { id } = useParams();
  const [site, setSite] = useState<any>(null);
  useEffect(() => { api.get(`/sites/${id}`).then(r => setSite(r.data)).catch(() => {}); }, [id]);
  if (!site) return <div className="animate-pulse"><div className="h-48 bg-gray-200 rounded-xl" /></div>;
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6">
      <h1 className="text-xl font-bold mb-4">{site.name}</h1>
      <p className="text-gray-600">{site.institution}</p>
      <p className="text-sm text-gray-500">{site.city}, {site.state}</p>
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div><p className="text-xs text-gray-400">Target Enrollment</p><p className="font-medium">{site.target_enrollment || "—"}</p></div>
        <div><p className="text-xs text-gray-400">Participants</p><p className="font-medium">{site.participant_count || 0}</p></div>
      </div>
    </div>
  );
}
''')

print("All frontend pages generated successfully!")
