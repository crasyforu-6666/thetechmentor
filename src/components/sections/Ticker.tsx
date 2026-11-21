import { ticker } from "@/content/site";

export default function Ticker() {
  const row = ticker.items.flatMap((t) => [t, ticker.separator]);
  return (
    <section className="ticker" aria-label={ticker.items.join(", ")}>
      <div className="ticker-row" aria-hidden="true">
        <div className="ticker-track" data-velocity>
          {[0, 1].map((k) => (
            <span className="ticker-chunk" key={k}>
              {row.map((t, i) => (
                <span key={i} className={t === ticker.separator ? "ticker-sep" : i % 4 === 0 ? "ticker-solid" : "ticker-outline"}>
                  {t}
                </span>
              ))}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
