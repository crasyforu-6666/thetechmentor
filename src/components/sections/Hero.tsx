import { Fragment } from "react";
import { hero } from "@/content/site";
import { JumpLink, ResetLink } from "@/components/shared/Links";
import BatchFinder from "./BatchFinder";

/** Splits a phrase into words that rise in one after another (pure CSS, staggered by --i). */
function Words({ text, start }: { text: string; start: number }) {
  const lead = text.startsWith(" ");
  return (
    <span aria-hidden="true">
      {lead && " "}
      {text
        .trim()
        .split(" ")
        .map((w, i) => (
          <Fragment key={i}>
            {i > 0 && " "}
            <span className="kw" style={{ ["--i" as string]: start + i }}>
              <span>{w}</span>
            </span>
          </Fragment>
        ))}
    </span>
  );
}

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-spot" aria-hidden="true" />
      <div className="hero-grid-bg" aria-hidden="true" />
      <div className="wrap hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">{hero.eyebrow}</p>
          <h1 className="kinetic" aria-label={`${hero.titleLine1} ${hero.titleHighlight}${hero.titleRest}`}>
            <Words text={hero.titleLine1} start={0} />
            <br />
            <span className="hl">
              <Words text={hero.titleHighlight} start={hero.titleLine1.split(" ").length} />
            </span>
            <Words text={hero.titleRest} start={hero.titleLine1.split(" ").length + hero.titleHighlight.split(" ").length} />
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
