import { hero } from "@/content/site";
import { JumpLink, ResetLink } from "@/components/shared/Links";
import BatchFinder from "./BatchFinder";

export default function Hero() {
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
        <BatchFinder />
      </div>
    </section>
  );
}
