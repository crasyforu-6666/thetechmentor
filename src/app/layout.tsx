import type { Metadata, Viewport } from "next";
import Script from "next/script";
import { jsonLd, links, meta, trackingConfig } from "@/content/site";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(meta.siteUrl),
  title: meta.title,
  description: meta.description,
  alternates: { canonical: meta.canonical },
  icons: { icon: { url: meta.icon, type: "image/svg+xml" } },
  openGraph: {
    type: meta.og.type,
    url: meta.og.url,
    title: meta.og.title,
    description: meta.og.description,
    images: [{ url: meta.og.image, width: meta.og.imageWidth, height: meta.og.imageHeight }],
    locale: meta.og.locale,
    siteName: meta.og.siteName,
  },
  twitter: {
    card: meta.twitter.card,
    title: meta.twitter.title,
    description: meta.twitter.description,
    images: [meta.twitter.image],
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: meta.themeColor,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link rel="stylesheet" href={links.fonts} />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, "\\u003c") }}
        />
        <script dangerouslySetInnerHTML={{ __html: `window.TTM_CONFIG=${JSON.stringify(trackingConfig)};` }} />
      </head>
      <body>
        {children}
        <Script src="/tracking.js" strategy="afterInteractive" />
        <Script src={links.razorpayCheckout} strategy="lazyOnload" />
      </body>
    </html>
  );
}
