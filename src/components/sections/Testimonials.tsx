import { outcomes } from "@/content/site";
import SecHead from "./SecHead";

export default function Testimonials() {
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
