// Copies legacy pages/assets that are not yet ported to Next.js into public/,
// so `next build` (output: "export") ships them unchanged. Generated; git-ignored.
import { cpSync, existsSync, rmSync } from "node:fs";

const ENTRIES = [
  "blog",
  "products",
  "downloads",
  "digital-products.html",
  "digital-products.js",
  "privacy.html",
  "terms.html",
  "refund.html",
  "thank-you.html",
  "robots.txt",
  "sitemap.xml",
  "site.css",
  "page.css",
  "styles.css",
  "theme-2030.css",
  "script.js",
  "tracking.js",
  "site-config.js",
];

for (const e of ENTRIES) {
  const src = `legacy/${e}`;
  const dest = `public/${e}`;
  if (!existsSync(src)) continue;
  rmSync(dest, { recursive: true, force: true });
  cpSync(src, dest, { recursive: true });
}
console.log(`sync-legacy: ${ENTRIES.length} entries copied to public/`);
