import { stats } from "@/content/site";

export default function Stats() {
  return (
    <section className="stats">
      <div className="wrap stats-grid">
        {stats.map((s) => (
          <div key={s.label}>
            <strong>{s.value}</strong>
            <span>{s.label}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
