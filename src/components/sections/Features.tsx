import { why } from "@/content/site";
import SecHead from "./SecHead";

export default function Features() {
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
