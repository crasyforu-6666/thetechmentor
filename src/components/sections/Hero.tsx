import { hero } from "@/content/site";
import { JumpLink, ResetLink } from "@/components/shared/Links";

export default function Hero() {
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
