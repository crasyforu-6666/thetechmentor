import { blog } from "@/content/site";

const ext = { target: "_blank", rel: "noopener noreferrer" } as const;

export default function LearningHub() {
  return (
    <section className="section alt" id="blog">
      <div className="wrap">
        <div className="sec-head">
          <div>
            <p className="eyebrow">{blog.eyebrow}</p>
            <h2>{blog.title}</h2>
            <p className="sub">{blog.sub}</p>
          </div>
          <div className="head-actions">
            <a className="btn btn-ghost" id="playlist-youtube-link" href={blog.playlistCta.href} {...ext}>
              {blog.playlistCta.label}
            </a>
            <a className="btn btn-primary" href={blog.allCta.href}>
              {blog.allCta.label}
            </a>
          </div>
        </div>
        <div className="blog-grid" id="blog-grid">
          {blog.posts.map((p) => (
            <article className="blog-card" data-cat="tutorial" data-date={p.date} key={p.slug}>
              <div
                className="blog-thumb"
                style={{ background: `#0b1220 url('blog/covers/${p.slug}.svg') center/cover no-repeat` }}
              ></div>
              <div className="blog-body">
                <span className={`blog-post-badge blog-post-badge--${p.tone}`}>{p.badge}</span>
                <div className="blog-post-title">{p.title}</div>
                <div className="blog-meta-line">
                  {blog.byPrefix}{blog.author} &middot; {p.minutes}{blog.minRead} &middot; {p.dateLabel}
                </div>
                <a href={`blog/${p.slug}.html`} className="blog-read-link">
                  {blog.readLabel}
                </a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
