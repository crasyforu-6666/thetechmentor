import { paths } from "@/content/site";
import { ResetLink } from "@/components/shared/Links";
import SecHead from "./SecHead";

export default function CareerPaths() {
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
