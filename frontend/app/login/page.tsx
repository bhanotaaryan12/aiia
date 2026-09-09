"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { KeyRound } from "lucide-react";
import { login } from "@/lib/api";

const demoEmail = "admin@aiia.gov.in";
const demoPassword = "Demo@12345";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const signIn = async (nextEmail: string, nextPassword: string) => {
    setError("");
    setLoading(true);
    try {
      await login(nextEmail, nextPassword);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Sign-in is unavailable. Confirm that the demo API is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <div className="w-full max-w-md border border-slate-200 bg-white p-7 shadow-sm sm:p-9">
        <div className="flex h-11 w-11 items-center justify-center rounded-md bg-teal-700 text-white"><KeyRound size={20} aria-hidden="true" /></div>
        <p className="mt-6 text-sm font-semibold text-teal-700">Presentation access</p>
        <h1 className="mt-2 text-2xl font-semibold text-slate-950">AIIA Study Workspace</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">Sign in to run the demonstration workflow. The prototype contains no live patient or trial data.</p>

        <form onSubmit={(event) => { event.preventDefault(); signIn(email, password); }} className="mt-7 space-y-4" noValidate>
          {error && <p role="alert" className="border-l-4 border-red-700 bg-red-50 px-4 py-3 text-sm text-red-800">{error}</p>}
          <label className="block text-sm font-medium text-slate-800">Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="email" required className="mt-1.5 w-full rounded-md border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-teal-700 focus:ring-2 focus:ring-teal-100" /></label>
          <label className="block text-sm font-medium text-slate-800">Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required className="mt-1.5 w-full rounded-md border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-teal-700 focus:ring-2 focus:ring-teal-100" /></label>
          <button type="submit" disabled={loading} className="w-full rounded-md bg-teal-700 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-60">{loading ? "Signing in" : "Sign in"}</button>
        </form>

        <div className="mt-6 border-t border-slate-200 pt-5">
          <button type="button" onClick={() => { setEmail(demoEmail); setPassword(demoPassword); signIn(demoEmail, demoPassword); }} disabled={loading} className="w-full rounded-md border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60">Use demo account</button>
          <p className="mt-3 text-center text-xs text-slate-500">Demo credentials are provided for this presentation environment.</p>
        </div>
        <p className="mt-6 text-center text-xs text-slate-500"><Link href="/privacy" className="underline underline-offset-2 hover:text-slate-900">Privacy</Link><span className="mx-2">·</span><Link href="/terms" className="underline underline-offset-2 hover:text-slate-900">Terms</Link></p>
      </div>
    </main>
  );
}
