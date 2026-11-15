import { mentor } from "@/content/site";

const ext = { target: "_blank", rel: "noopener noreferrer" } as const;

export default function Mentor() {
  return (
    <section className="section" id="mentors">
      <div className="wrap mentor">
        <img className="mentor-photo" src={mentor.photo} alt={mentor.photoAlt} width={400} height={400} loading="lazy" />
        <div>
          <p className="eyebrow">{mentor.eyebrow}</p>
          <h2>{mentor.name}</h2>
          <p className="role">{mentor.role}</p>
          <p>{mentor.bio}</p>
          <ul className="ticks">
            {mentor.ticks.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
          <a className="btn btn-ghost" href={mentor.cta.href} {...ext}>
            {mentor.cta.label}
          </a>
        </div>
      </div>
    </section>
  );
}
