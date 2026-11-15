"use client";

import { flushSync } from "react-dom";
import { brand, catalog, type Course } from "@/content/site";
import { useHomeState } from "./HomeState";
import { AdvisorLink } from "./Links";

function matches(c: Course, filter: string, query: string) {
  const okFilter = filter === "all" || filter === c.format || c.cats.split(" ").includes(filter);
  const q = query.trim().toLowerCase();
  if (!q) return okFilter;
  const text = [c.tags, c.formatTag, c.badge, c.formatLabel, c.name, c.skills, ...c.meta, c.feat, c.price, c.priceNote, catalog.enrollLabel, catalog.advisorLabel]
    .join(" ")
    .toLowerCase();
  return okFilter && q.split(/\s+/).every((w) => text.includes(w));
}

function CourseCard({ c, hidden }: { c: Course; hidden: boolean }) {
  return (
    <article className="course" id={c.id} data-format={c.format} hidden={hidden}>
      <div className="course-thumb">
        <img src={c.image} alt={c.name} loading="lazy" width={1200} height={630} />
        <span className={`tag ${c.format === "live" ? "tag-live" : "tag-self"}`}>{c.formatTag}</span>
        {c.badge && <span className="tag tag-hot">{c.badge}</span>}
      </div>
      <div className="course-body">
        <p className="provider">
          <img src={brand.logo} alt="" width={18} height={18} /> {catalog.providerPrefix}
          {c.formatLabel}
        </p>
        <h3>{c.name}</h3>
        <p className="skills">
          <b>{catalog.skillsLabel}</b> {c.skills}
        </p>
        <ul className="meta">
          {c.meta.map((m) => (
            <li key={m}>{m}</li>
          ))}
        </ul>
        <p className="feat">{c.feat}</p>
        <div className="price">
          <strong>{c.price}</strong>
          <span className="emi">{c.priceNote}</span>
        </div>
        <div className="actions">
          <a className="btn btn-primary" href={c.enrollHref} target="_blank" rel="noopener noreferrer">
            {catalog.enrollLabel}
          </a>
          <AdvisorLink href={catalog.advisorHref} className="btn btn-ghost" course={c.short} format={c.formatLabel}>
            {catalog.advisorLabel}
          </AdvisorLink>
        </div>
      </div>
    </article>
  );
}

export default function Catalog() {
  const { filter, query, setFilter, reset } = useHomeState();
  let shown = 0;
  const sections = catalog.sections.map((sec) => {
    const vis = sec.courses.map((c) => matches(c, filter, query));
    const n = vis.filter(Boolean).length;
    shown += n;
    return { sec, vis, n };
  });

  return (
    <section className="section" id="courses">
      <div className="wrap">
        <div className="sec-head">
          <div>
            <p className="eyebrow">{catalog.eyebrow}</p>
            <h2>{catalog.title}</h2>
            <p className="sub">{catalog.sub}</p>
          </div>
        </div>
        <div className="filters" role="toolbar" aria-label={catalog.filtersLabel}>
          {catalog.filters.map((f) => (
            <button
              key={f.key}
              type="button"
              className={`chip${filter === f.key ? " active" : ""}`}
              onClick={() => flushSync(() => setFilter(f.key))}
            >
              {f.label}
            </button>
          ))}
        </div>

        {sections.map(({ sec, vis, n }) => (
          <div className="cat-section" id={sec.id} key={sec.id} hidden={n === 0}>
            <div className="cat-head">
              <div>
                <h3>{sec.title}</h3>
                <p className="sub">{sec.sub}</p>
              </div>
              <p className="cat-price">{sec.price}</p>
            </div>
            <div className="catalog">
              {sec.courses.map((c, i) => (
                <CourseCard key={c.id} c={c} hidden={!vis[i]} />
              ))}
            </div>
          </div>
        ))}
        <p className="no-results" id="no-results" hidden={shown > 0}>
          {catalog.noResults}{" "}
          <button type="button" className="link" onClick={reset}>
            {catalog.resetLabel}
          </button>
        </p>
      </div>
    </section>
  );
}
