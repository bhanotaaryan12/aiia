import type { MetadataRoute } from "next";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";
export default function sitemap(): MetadataRoute.Sitemap { return ["/", "/privacy", "/terms", "/faq"].map((path) => ({ url: new URL(path, siteUrl).toString(), lastModified: new Date(), changeFrequency: "yearly", priority: 0.4 })); }
