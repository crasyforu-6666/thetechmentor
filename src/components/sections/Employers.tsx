import { strip } from "@/content/site";

export default function Employers() {
  const half = [...strip.companies, ...strip.companies];
  return (
    <section className="strip">
      <div className="wrap strip-inner">
        <span className="strip-title">{strip.title}</span>
        <div className="marquee">
          <div className="marquee-track">
            <ul>
              {half.map((c, i) => (
                <li key={`${c}-${i}`} aria-hidden={i >= strip.companies.length || undefined}>
                  {c}
                </li>
              ))}
            </ul>
            <ul aria-hidden="true">
              {half.map((c, i) => (
                <li key={`${c}-dup-${i}`}>{c}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
