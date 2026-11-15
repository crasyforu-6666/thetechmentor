import { ctaBand } from "@/content/site";

export default function ClosingCTA() {
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
