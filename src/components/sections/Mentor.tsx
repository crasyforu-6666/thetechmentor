import { mentor } from "@/content/site";

const ext = { target: "_blank", rel: "noopener noreferrer" } as const;

export default function Mentor() {
  return (
    <section className="section mentor-dark" id="mentors">
      <div className="wrap mentor-pro">
        <div className="mp-visual">
          <div className="mp-glow" aria-hidden="true" />
          <div className="mp-photo">
            <img src={mentor.photo} alt={mentor.photoAlt} width={mentor.photoWidth} height={mentor.photoHeight} loading="lazy" />
          </div>
          <ul className="mp-stats">
            {mentor.stats.map((s, i) => (
              <li key={s.label} className={`mp-stat mp-stat-${i + 1}`}>
                <strong>{s.value}</strong>
                <span>{s.label}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="mp-copy">
          <p className="mp-eyebrow">{mentor.eyebrow}</p>
          <p className="mp-greet">{mentor.greeting}</p>
          <h2 className="mp-name">
            {mentor.firstName}
            <br />
            {mentor.lastName}
          </h2>
          <p className="mp-role">
            <span className="mp-role-lead">{mentor.roleLead}</span> <span className="mp-role-focus">{mentor.roleFocus}</span>
          </p>
          <p className="mp-bio">
            {mentor.bioParts.map((b, i) => (b.hl ? <b key={i}>{b.text}</b> : <span key={i}>{b.text}</span>))}
          </p>
          <ul className="mp-ticks">
            {mentor.ticks.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
          <a className="mp-btn" href={mentor.cta.href} {...ext}>
            {mentor.cta.label}
          </a>
        </div>
      </div>
    </section>
  );
}
