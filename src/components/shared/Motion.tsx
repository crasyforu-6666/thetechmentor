"use client";

import { useEffect } from "react";

const REVEAL =
  ".sec-head, .cat-head, .course, .why, .path, .format, .outcome, .blog-card, .stats-grid > div, .mp-visual, .mp-copy > *, .advisor-copy, .form-card, details.faq, .cta-inner > *, .weeks li, .footer-grid > div";
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
    const nums = Array.from(document.querySelectorAll<HTMLElement>(".stats strong, .hero-proof strong, .mp-stat strong"));
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

    const fine = window.matchMedia("(pointer: fine)").matches;

    // One rAF loop for cursor aura/dot, 3D tilt easing, parallax and ticker velocity.
    const aura = document.querySelector<HTMLElement>(".cursor-aura");
    const dot = document.querySelector<HTMLElement>(".cursor-dot");
    let mx = innerWidth / 2, my = innerHeight / 2, ax = mx, ay = my, dx = mx, dy = my;
    const onPointer = (e: PointerEvent) => {
      mx = e.clientX;
      my = e.clientY;
      aura?.classList.add("on");
      dot?.classList.add("on");
      const hot = (e.target as Element | null)?.closest("a, button, input, select, summary, label");
      dot?.classList.toggle("big", !!hot);
    };
    const onLeave = () => { aura?.classList.remove("on"); dot?.classList.remove("on"); };
    if (fine) {
      window.addEventListener("pointermove", onPointer, { passive: true });
      document.documentElement.addEventListener("pointerleave", onLeave);
      cleanups.push(() => {
        window.removeEventListener("pointermove", onPointer);
        document.documentElement.removeEventListener("pointerleave", onLeave);
      });
    }

    // 3D tilt targets (desktop only)
    type Tilt = { el: HTMLElement; rx: number; ry: number; tx: number; ty: number; lift: number; tl: number };
    const tilts = new Map<HTMLElement, Tilt>();
    const onTilt = (e: PointerEvent) => {
      const el = (e.target as Element | null)?.closest<HTMLElement>(GLOW);
      tilts.forEach((t) => { if (t.el !== el) { t.tx = 0; t.ty = 0; t.tl = 0; } });
      if (!el || !el.classList.contains("is-in")) return;
      const r = el.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width - 0.5;
      const py = (e.clientY - r.top) / r.height - 0.5;
      const t = tilts.get(el) ?? { el, rx: 0, ry: 0, tx: 0, ty: 0, lift: 0, tl: 0 };
      t.tx = -py * 9; t.ty = px * 11; t.tl = 1;
      tilts.set(el, t);
    };
    if (fine) {
      document.addEventListener("pointermove", onTilt, { passive: true });
      cleanups.push(() => document.removeEventListener("pointermove", onTilt));
    }

    // Magnetic buttons
    const mags = Array.from(document.querySelectorAll<HTMLElement>(".btn-primary, .mp-btn, .btn-white, .btn-outline-white"));
    const magState = new Map<HTMLElement, { x: number; y: number; tx: number; ty: number }>();
    const onMag = (e: PointerEvent) => {
      for (const b of mags) {
        const r = b.getBoundingClientRect();
        const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        const ddx = e.clientX - cx, ddy = e.clientY - cy;
        const near = Math.abs(ddx) < r.width / 2 + 40 && Math.abs(ddy) < r.height / 2 + 40;
        const st = magState.get(b) ?? { x: 0, y: 0, tx: 0, ty: 0 };
        st.tx = near ? ddx * 0.28 : 0; st.ty = near ? ddy * 0.38 : 0;
        magState.set(b, st);
      }
    };
    if (fine) {
      window.addEventListener("pointermove", onMag, { passive: true });
      cleanups.push(() => window.removeEventListener("pointermove", onMag));
    }

    // Ticker: base drift + scroll-velocity boost, direction flips with scroll direction
    const track = document.querySelector<HTMLElement>(".ticker-track");
    let tickX = 0, lastY = scrollY, vel = 0, dir = -1;
    const heroBlobs = document.querySelector<HTMLElement>(".hero");
    const mpVisual = document.querySelector<HTMLElement>(".mp-photo");

    let raf = 0, last = performance.now();
    const loop = (now: number) => {
      const dt = Math.min(64, now - last) / 16.67; last = now;
      // cursor
      ax += (mx - ax) * 0.08 * dt; ay += (my - ay) * 0.08 * dt;
      dx += (mx - dx) * 0.35 * dt; dy += (my - dy) * 0.35 * dt;
      if (aura) aura.style.transform = `translate3d(${ax}px, ${ay}px, 0)`;
      if (dot) dot.style.transform = `translate3d(${dx}px, ${dy}px, 0)`;
      // tilt
      tilts.forEach((t, el) => {
        t.rx += (t.tx - t.rx) * 0.12 * dt; t.ry += (t.ty - t.ry) * 0.12 * dt; t.lift += (t.tl - t.lift) * 0.12 * dt;
        if (Math.abs(t.rx) < 0.01 && Math.abs(t.ry) < 0.01 && t.lift < 0.01 && t.tl === 0) {
          el.style.transform = ""; el.style.transition = ""; tilts.delete(el); return;
        }
        el.style.transition = "box-shadow .35s, border-color .35s";
        el.style.transform = `perspective(900px) rotateX(${t.rx}deg) rotateY(${t.ry}deg) translateY(${-6 * t.lift}px)`;
      });
      // magnets
      magState.forEach((st, b) => {
        st.x += (st.tx - st.x) * 0.15 * dt; st.y += (st.ty - st.y) * 0.15 * dt;
        b.style.translate = Math.abs(st.x) + Math.abs(st.y) < 0.05 ? "" : `${st.x}px ${st.y}px`;
      });
      // scroll velocity → ticker
      const y = scrollY; const dy2 = y - lastY; lastY = y;
      if (dy2 !== 0) dir = dy2 > 0 ? -1 : 1;
      vel += (Math.min(40, Math.abs(dy2)) - vel) * 0.1;
      if (track) {
        const half = track.scrollWidth / 2;
        tickX += dir * (1.1 + vel * 0.5) * dt;
        if (tickX <= -half) tickX += half;
        if (tickX > 0) tickX -= half;
        track.style.transform = `translate3d(${tickX}px, 0, 0)`;
      }
      // parallax
      if (heroBlobs) heroBlobs.style.setProperty("--py", `${Math.min(y, 900) * 0.25}px`);
      if (mpVisual) {
        const r = mpVisual.getBoundingClientRect();
        const c = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
        mpVisual.style.translate = `0 ${c * -40}px`;
      }
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    cleanups.push(() => cancelAnimationFrame(raf));

    return () => cleanups.forEach((c) => c());
  }, []);

  return (
    <>
      <div className="scroll-progress" aria-hidden="true" />
      <div className="cursor-aura" aria-hidden="true" />
      <div className="cursor-dot" aria-hidden="true" />
    </>
  );
}
