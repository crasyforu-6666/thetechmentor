import { brand, footer, stickyBar } from "@/content/site";
import { JumpLink } from "@/components/shared/Links";

const ext = { target: "_blank", rel: "noopener noreferrer" } as const;

function StickyBar() {
  return (
    <div className="sticky-mobile-bar" id="sticky-mobile-bar">
      <a href={stickyBar.primary.href} className="sticky-btn sticky-buy">
        {stickyBar.primary.label}
      </a>
      <a href={stickyBar.secondary.href} className="sticky-btn sticky-call">
        {stickyBar.secondary.label}
      </a>
    </div>
  );
}

export default function Footer() {
  return (
    <>
    <footer className="footer">
      <div className="wrap footer-grid">
        <div className="footer-brand">
          <a href="#top" className="brand brand-light">
            <img src={brand.logo} alt="" width={32} height={32} />
            <span>
              {brand.pre}
              <b>{brand.bold}</b>
              {brand.post}
            </span>
          </a>
          <p>{footer.tagline}</p>
        </div>
        {footer.columns.map((col) => (
          <div key={col.title}>
            <h4>{col.title}</h4>
            <ul>
              {col.links.map((l) => (
                <li key={l.label}>
                  {!l.href ? (
                    l.label
                  ) : l.jump ? (
                    <JumpLink href={l.href} jump={l.jump}>
                      {l.label}
                    </JumpLink>
                  ) : (
                    <a href={l.href} {...(l.external ? ext : {})}>
                      {l.label}
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div className="wrap footer-bottom">
        <p>{footer.copyright}</p>
      </div>
      <div className="footer-wordmark" aria-hidden="true">
        <img src={footer.wordmark} alt="" width={2000} height={306} loading="lazy" />
      </div>
    </footer>
    <StickyBar />
    </>
  );
}
