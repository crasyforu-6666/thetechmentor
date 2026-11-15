import { strip } from "@/content/site";

export default function Employers() {
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
