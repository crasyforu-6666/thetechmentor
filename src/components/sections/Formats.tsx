import { formats } from "@/content/site";
import { JumpLink } from "@/components/shared/Links";
import SecHead from "./SecHead";

export default function Formats() {
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
