"use client";

import { useEffect, useState } from "react";
import { announce, brand, nav, skipLink } from "@/content/site";
import { scrollToId, useHomeState } from "@/components/shared/HomeState";

function SkipLink() {
  return (
    <a className="skip-link" href={skipLink.href}>
      {skipLink.label}
    </a>
  );
}

function Announce() {
  return (
    <div className="announce">
      <div className="wrap">
        <span>
          <span className="dot" aria-hidden="true"></span> {announce.text}
        </span>
        <a href={announce.link.href}>{announce.link.label}</a>
      </div>
    </div>
  );
}

export default function Header() {
  const { query, setQuery } = useHomeState();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    let ticking = false;
    const update = () => {
      setScrolled(window.scrollY > 20);
      ticking = false;
    };
    update();
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const close = () => setOpen(false);

  return (
    <>
    <SkipLink />
    <Announce />
    <header className={`header${scrolled ? " is-scrolled" : ""}`} id="top">
      <nav className="nav wrap" aria-label={nav.ariaLabel}>
        <a href="#top" className="brand" aria-label={brand.homeLabel}>
          <img src={brand.logo} alt="" width={36} height={36} />
          <span>
            {brand.pre}
            <b>{brand.bold}</b>
            {brand.post}
          </span>
        </a>
        <form className="nav-search" role="search" action="#courses" onSubmit={(e) => e.preventDefault()}>
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-3.5-3.5" />
          </svg>
          <input
            type="search"
            id="course-search"
            placeholder={nav.searchPlaceholder}
            aria-label={nav.searchLabel}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                scrollToId("courses");
              }
            }}
          />
        </form>
        <button
          className="nav-toggle"
          aria-label={nav.toggleLabel}
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
        <ul className={`nav-links${open ? " open" : ""}`}>
          {nav.links.map((l) => (
            <li key={l.label}>
              <a href={l.href} onClick={close}>
                {l.label}
              </a>
            </li>
          ))}
          <li>
            <a href={nav.cta.href} className="btn btn-primary btn-sm" onClick={close}>
              {nav.cta.label}
            </a>
          </li>
        </ul>
      </nav>
    </header>
    </>
  );
}
