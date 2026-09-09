import "./globals.css";
import type { Metadata } from "next";
import CookieConsent from "@/components/cookie-consent";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: "AIIA Study Workspace", template: "%s | AIIA Study Workspace" },
  description: "A presentation prototype for an Ayurveda clinical study governance workflow.",
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    title: "AIIA Study Workspace",
    description: "A presentation prototype for an Ayurveda clinical study governance workflow.",
    url: "/",
    siteName: "AIIA Study Workspace",
  },
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}<CookieConsent /></body></html>;
}
