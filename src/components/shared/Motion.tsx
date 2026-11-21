"use client";

import { useEffect } from "react";

const REVEAL =
  ".sec-head, .cat-head, .course, .why, .path, .format, .outcome, .blog-card, .stats-grid > div, .mentor > *, .advisor-copy, .form-card, details.faq, .cta-inner > *, .weeks li, .footer-grid > div";
const GLOW = ".course, .why, .path, .format, .outcome, .blog-card";

/** Page-wide motion: scroll reveal, stat count-up, cursor glow, hero spotlight, scroll progress. */
export default function Motion() {
  useEffect(() => {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const cleanups: (() => void)[] = [];

    // Scroll progress
    const bar = document.querySelector<HTMLElement>(".scroll-progress");
    const onScroll = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar?.style.setProperty("--sp", String(max > 0 ? h.scrollTop / max : 0));
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    cleanups.push(() => window.removeEventListener("scroll", onScroll));

    // Cursor glow on cards (delegated)
    const onMove = (e: PointerEvent) => {
      const el = (e.target as Element | null)?.closest<HTMLElement>(GLOW);
      if (!el) return;
      const r = el.getBoundingClientRect();
      el.style.setProperty("--mx", `${e.clientX - r.left}px`);
      el.style.setProperty("--my", `${e.clientY - r.top}px`);
    };
    document.addEventListener("pointermove", onMove, { passive: true });
    cleanups.push(() => document.removeEventListener("pointermove", onMove));

    // Hero spotlight follows the pointer
    const hero = document.querySelector<HTMLElement>(".hero");
    const onHero = (e: PointerEvent) => {
      if (!hero) return;
      const r = hero.getBoundingClientRect();
      hero.style.setProperty("--hx", `${((e.clientX - r.left) / r.width) * 100}%`);
      hero.style.setProperty("--hy", `${((e.clientY - r.top) / r.height) * 100}%`);
    };
    hero?.addEventListener("pointermove", onHero, { passive: true });
    cleanups.push(() => hero?.removeEventListener("pointermove", onHero));

    if (reduce) return () => cleanups.forEach((c) => c());

    // Scroll reveal with per-group stagger
    const els = Array.from(document.querySelectorAll<HTMLElement>(REVEAL));
    const seen = new Map<Element | null, number>();
    els.forEach((el) => {
      const i = seen.get(el.parentElement) ?? 0;
      seen.set(el.parentElement, i + 1);
      el.dataset.reveal = "";
      el.style.setProperty("--rd", `${Math.min(i, 6) * 0.07}s`);
    });
    document.documentElement.classList.add("reveal-ready");
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        }),
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 },
    );
    els.forEach((el) => io.observe(el));
    cleanups.push(() => io.disconnect());

    // Count-up for stats ("1,000+", "12+ yrs", "24/7" stays as is)
    const nums = Array.from(document.querySelectorAll<HTMLElement>(".stats strong, .hero-proof strong"));
    const cio = new IntersectionObserver(
      (entries) =>
        entries.forEach((en) => {
          if (!en.isIntersecting) return;
          cio.unobserve(en.target);
          const el = en.target as HTMLElement;
          const final = el.textContent || "";
          const m = /^([\d,]+)(\D.*)?$/.exec(final);
          if (!m || final.includes("/")) return;
          const target = Number(m[1].replace(/,/g, ""));
          const suffix = m[2] || "";
          const t0 = performance.now();
          const dur = 1400;
          const tick = (now: number) => {
            const p = Math.min(1, (now - t0) / dur);
            const v = Math.round(target * (1 - Math.pow(1 - p, 3)));
            el.textContent = v.toLocaleString("en-IN") + suffix;
            if (p < 1) requestAnimationFrame(tick);
            else el.textContent = final;
          };
          requestAnimationFrame(tick);
        }),
      { threshold: 0.6 },
    );
    nums.forEach((n) => cio.observe(n));
    cleanups.push(() => cio.disconnect());

    return () => cleanups.forEach((c) => c());
  }, []);

  return <div className="scroll-progress" aria-hidden="true" />;
}
