import {
  advisor,
  announce,
  blog,
  brand,
  contact,
  ctaBand,
  faq,
  footer,
  formats,
  hero,
  mentor,
  outcomes,
  paths,
  skipLink,
  stats,
  stickyBar,
  strip,
  why,
} from "@/content/site";
import CurriculumTabs from "./CurriculumTabs";
import LeadForm from "./LeadForm";
import { JumpLink, ResetLink } from "./Links";

const ext = { target: "_blank", rel: "noopener noreferrer" } as const;

function SecHead({ eyebrow, title, sub, center }: { eyebrow: string; title: string; sub?: string; center?: boolean }) {
  return (
    <div className={`sec-head${center ? " center" : ""}`}>
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
        {sub && <p className="sub">{sub}</p>}
      </div>
    </div>
  );
}

export function SkipLink() {
  return (
    <a className="skip-link" href={skipLink.href}>
      {skipLink.label}
    </a>
  );
}

export function Announce() {
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

export function Hero() {
  const v = hero.visual;
  return (
    <section className="hero">
      <div className="wrap hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">{hero.eyebrow}</p>
          <h1>
            {hero.titleLine1}
            <br />
            <span className="hl">{hero.titleHighlight}</span>
            {hero.titleRest}
          </h1>
          <p className="lead">{hero.lead}</p>
          <a href={hero.cta.href} className="btn btn-primary">
            {hero.cta.label}
          </a>
          <div className="popular">
            <span>{hero.popularLabel}</span>
            {hero.popular.map((p) =>
              p.jump ? (
                <JumpLink key={p.label} href={p.href} jump={p.jump}>
                  {p.label}
                </JumpLink>
              ) : (
                <ResetLink key={p.label} href={p.href}>
                  {p.label}
                </ResetLink>
              ),
            )}
          </div>
          <ul className="hero-proof">
            {hero.proof.map((p) => (
              <li key={p.strong}>
                <strong>{p.strong}</strong>
                {p.text}
              </li>
            ))}
          </ul>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="hv-card hv-main">
            <img src={v.image} alt="" />
            <div className="hv-body">
              <span className="tag tag-live">{v.tag}</span>
              <strong>{v.title}</strong>
              <span className="muted">{v.meta}</span>
              <div className="hv-progress">
                <span style={{ width: `${v.progress}%` }}></span>
              </div>
              <span className="muted small">{v.progressLabel}</span>
            </div>
          </div>
          {v.chips.map((c, i) => (
            <div key={c.title} className={`hv-chip hv-chip-${i + 1}`}>
              <span className="ic">{c.icon}</span>
              <div>
                <strong>{c.title}</strong>
                <span>{c.text}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Strip() {
  return (
    <section className="strip">
      <div className="wrap strip-inner">
        <span className="strip-title">{strip.title}</span>
        <ul>
          {strip.companies.map((c) => (
            <li key={c}>{c}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export function Stats() {
  return (
    <section className="stats">
      <div className="wrap stats-grid">
        {stats.map((s) => (
          <div key={s.label}>
            <strong>{s.value}</strong>
            <span>{s.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export function Why() {
  return (
    <section className="section alt" id="why">
      <div className="wrap">
        <SecHead eyebrow={why.eyebrow} title={why.title} center />
        <div className="why-grid">
          {why.items.map((w) => (
            <div className="why" key={w.title}>
              <span className="why-ic">{w.icon}</span>
              <h3>{w.title}</h3>
              <p>{w.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Paths() {
  return (
    <section className="section" id="paths">
      <div className="wrap">
        <SecHead eyebrow={paths.eyebrow} title={paths.title} />
        <div className="paths">
          {paths.items.map((p) => (
            <div className={`path${p.featured ? " featured" : ""}`} key={p.title}>
              <span className="path-tag">{p.tag}</span>
              <h3>{p.title}</h3>
              <ol>
                {p.steps.map((s) => (
                  <li key={s}>{s}</li>
                ))}
              </ol>
              <ResetLink href={p.cta.href} className={`btn ${p.featured ? "btn-primary" : "btn-ghost"}`}>
                {p.cta.label}
              </ResetLink>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Curriculum() {
  return (
    <section className="section alt" id="curriculum">
      <CurriculumTabs />
    </section>
  );
}

export function Formats() {
  return (
    <section className="section" id="formats">
      <div className="wrap">
        <SecHead eyebrow={formats.eyebrow} title={formats.title} center />
        <div className="formats formats-2">
          {formats.items.map((f) => (
            <div className={`format${f.featured ? " featured" : ""}`} key={f.title}>
              {f.ribbon && <span className="ribbon">{f.ribbon}</span>}
              <h3>{f.title}</h3>
              <p className="fprice">{f.price}</p>
              <p className="fsplit">{f.split}</p>
              <ul>
                {f.points.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ul>
              <JumpLink href={f.cta.href} jump={f.cta.jump} className={`btn ${f.featured ? "btn-primary" : "btn-ghost"}`}>
                {f.cta.label}
              </JumpLink>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Outcomes() {
  return (
    <section className="section alt" id="outcomes">
      <div className="wrap">
        <SecHead eyebrow={outcomes.eyebrow} title={outcomes.title} center />
        <div className="outcomes">
          {outcomes.items.map((o) => (
            <div className="outcome" key={o.company}>
              <span className="co">{o.company}</span>
              <div className="move">
                <div>
                  <small>{outcomes.beforeLabel}</small>
                  {o.before}
                </div>
                <span>{outcomes.arrow}</span>
                <div>
                  <small>{outcomes.afterLabel}</small>
                  {o.after}
                </div>
              </div>
              <p>{o.quote}</p>
            </div>
          ))}
        </div>
        <p className="fineprint">{outcomes.fineprint}</p>
      </div>
    </section>
  );
}

export function Mentor() {
  return (
    <section className="section" id="mentors">
      <div className="wrap mentor">
        <img className="mentor-photo" src={mentor.photo} alt={mentor.photoAlt} width={400} height={400} loading="lazy" />
        <div>
          <p className="eyebrow">{mentor.eyebrow}</p>
          <h2>{mentor.name}</h2>
          <p className="role">{mentor.role}</p>
          <p>{mentor.bio}</p>
          <ul className="ticks">
            {mentor.ticks.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
          <a className="btn btn-ghost" href={mentor.cta.href} {...ext}>
            {mentor.cta.label}
          </a>
        </div>
      </div>
    </section>
  );
}

export function Blog() {
  return (
    <section className="section alt" id="blog">
      <div className="wrap">
        <div className="sec-head">
          <div>
            <p className="eyebrow">{blog.eyebrow}</p>
            <h2>{blog.title}</h2>
            <p className="sub">{blog.sub}</p>
          </div>
          <div className="head-actions">
            <a className="btn btn-ghost" id="playlist-youtube-link" href={blog.playlistCta.href} {...ext}>
              {blog.playlistCta.label}
            </a>
            <a className="btn btn-primary" href={blog.allCta.href}>
              {blog.allCta.label}
            </a>
          </div>
        </div>
        <div className="blog-grid" id="blog-grid">
          {blog.posts.map((p) => (
            <article className="blog-card" data-cat="tutorial" data-date={p.date} key={p.slug}>
              <div
                className="blog-thumb"
                style={{ background: `#0b1220 url('blog/covers/${p.slug}.svg') center/cover no-repeat` }}
              ></div>
              <div className="blog-body">
                <span className={`blog-post-badge blog-post-badge--${p.tone}`}>{p.badge}</span>
                <div className="blog-post-title">{p.title}</div>
                <div className="blog-meta-line">
                  {blog.byPrefix}{blog.author} &middot; {p.minutes}{blog.minRead} &middot; {p.dateLabel}
                </div>
                <a href={`blog/${p.slug}.html`} className="blog-read-link">
                  {blog.readLabel}
                </a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export function Advisor() {
  return (
    <section className="section advisor" id="advisor">
      <div className="wrap two-col">
        <div className="advisor-copy" id="enroll">
          <p className="eyebrow">{advisor.eyebrow}</p>
          <h2>{advisor.title}</h2>
          <p className="sub">{advisor.sub}</p>
          <ul className="ticks">
            {advisor.ticks.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
          <div className="contact">
            <a href={contact.whatsappUrl} {...ext}>
              {advisor.contactWhatsapp}
            </a>
            <a href={contact.emailUrl}>{advisor.contactEmail}</a>
          </div>
        </div>
        <LeadForm />
      </div>
    </section>
  );
}

export function Faq() {
  return (
    <section className="section" id="faq">
      <div className="wrap narrow">
        <SecHead eyebrow={faq.eyebrow} title={faq.title} center />
        {faq.items.map((f) => (
          <details className="faq" key={f.q}>
            <summary>{f.q}</summary>
            <p>
              {f.a}
              {f.link && <a href={f.link.href}>{f.link.label}</a>}
              {f.after}
            </p>
          </details>
        ))}
      </div>
    </section>
  );
}

export function CtaBand() {
  return (
    <section className="cta-band">
      <div className="wrap cta-inner">
        <div>
          <h2>{ctaBand.title}</h2>
          <p>{ctaBand.text}</p>
        </div>
        <div className="cta-actions">
          <a href={ctaBand.primary.href} className="btn btn-white">
            {ctaBand.primary.label}
          </a>
          <a href={ctaBand.secondary.href} className="btn btn-outline-white">
            {ctaBand.secondary.label}
          </a>
        </div>
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="footer">
      <div className="wrap footer-grid">
        <div className="footer-brand">
          <a href="#top" className="brand brand-light">
            <img src={brand.logo} alt="" width={32} height={32} />
            <span>
              {brand.pre}
              <b>{brand.bold}</b>
              {brand.post}
            </span>
          </a>
          <p>{footer.tagline}</p>
        </div>
        {footer.columns.map((col) => (
          <div key={col.title}>
            <h4>{col.title}</h4>
            <ul>
              {col.links.map((l) => (
                <li key={l.label}>
                  {!l.href ? (
                    l.label
                  ) : l.jump ? (
                    <JumpLink href={l.href} jump={l.jump}>
                      {l.label}
                    </JumpLink>
                  ) : (
                    <a href={l.href} {...(l.external ? ext : {})}>
                      {l.label}
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="wrap footer-bottom">
        <p>{footer.copyright}</p>
      </div>
      <div className="footer-wordmark" aria-hidden="true">
        <img src={footer.wordmark} alt="" width={2000} height={306} loading="lazy" />
      </div>
    </footer>
  );
}

export function StickyBar() {
  return (
    <div className="sticky-mobile-bar" id="sticky-mobile-bar">
      <a href={stickyBar.primary.href} className="sticky-btn sticky-buy">
        {stickyBar.primary.label}
      </a>
      <a href={stickyBar.secondary.href} className="sticky-btn sticky-call">
        {stickyBar.secondary.label}
      </a>
    </div>
  );
}
