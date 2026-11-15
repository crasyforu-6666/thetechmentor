import { faq } from "@/content/site";
import SecHead from "./SecHead";

export default function FAQ() {
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
