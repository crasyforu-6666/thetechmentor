export default function SecHead({ eyebrow, title, sub, center }: { eyebrow: string; title: string; sub?: string; center?: boolean }) {
  return (
    <div className={`sec-head${center ? " center" : ""}`}>
      <div>
        <p className="eyebrow">{eyebrow}</p>
        <h2>{title}</h2>
        {sub && <p className="sub">{sub}</p>}
      </div>
    </div>
  );
}
