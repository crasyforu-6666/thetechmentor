#!/usr/bin/env python3
"""Visual design for AI-written articles: per-module colour themes, generated cover
images, process-flow diagrams, callouts, T-code chips and owner screenshots.

Cover images: blog/covers/<slug>.svg (shown on the page and on cards) and
<slug>.png (social share previews; needs `pip install cairosvg`, otherwise the
site-wide share image is used).

Screenshots: drop PNG/JPG files into images/blog/<slug>/ named like
"01-me59n-selection-screen.png"; they are shown as a captioned gallery the next
time the article is rendered (python3 scripts/rerender_articles.py).
"""
import datetime
import html
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
COVER_DIR = os.path.join(BLOG_DIR, "covers")
SHOT_DIR = os.path.join(BASE_DIR, "images", "blog")
SITE = "https://youronementor.com"
DEFAULT_OG = f"{SITE}/images/og-cover.png"

MODULES = ["MM", "EWM", "SD", "FICO", "AI", "Career", "ABAP", "BASIS", "TM", "LOG"]

THEMES = {
    "MM":     {"name": "SAP MM",  "a": "#0284c7", "b": "#6366f1", "soft": "#e0f2fe", "icon": "procure"},
    "EWM":    {"name": "SAP EWM", "a": "#059669", "b": "#0ea5e9", "soft": "#d1fae5", "icon": "warehouse"},
    "SD":     {"name": "SAP SD",  "a": "#ea580c", "b": "#db2777", "soft": "#ffedd5", "icon": "sales"},
    "FICO":   {"name": "SAP FICO", "a": "#0d9488", "b": "#4f46e5", "soft": "#ccfbf1", "icon": "ledger"},
    "AI":     {"name": "SAP AI · Joule", "a": "#7c3aed", "b": "#db2777", "soft": "#ede9fe", "icon": "spark"},
    "Career": {"name": "SAP Career", "a": "#d97706", "b": "#dc2626", "soft": "#fef3c7", "icon": "rocket"},
    "ABAP":   {"name": "SAP ABAP", "a": "#4f46e5", "b": "#06b6d4", "soft": "#e0e7ff", "icon": "code"},
    "BASIS":  {"name": "SAP BASIS", "a": "#334155", "b": "#0ea5e9", "soft": "#e2e8f0", "icon": "server"},
    "TM":     {"name": "SAP TM", "a": "#c2410c", "b": "#f59e0b", "soft": "#ffedd5", "icon": "truck"},
    "LOG":    {"name": "SAP Logistics", "a": "#0f766e", "b": "#7c3aed", "soft": "#ccfbf1", "icon": "network"},
}


def theme(module: str) -> dict:
    return THEMES.get(module or "MM", THEMES["MM"])


def _e(s) -> str:
    return html.escape(str(s or ""), quote=True)


def _rich(s) -> str:
    """Escape plain text, then show `code` spans as <code> chips."""
    return re.sub(r"`([^`]{1,80})`", r"<code>\1</code>", _e(s))


# --------------------------------------------------------------------------- #
# Cover image
# --------------------------------------------------------------------------- #

def _wrap(text: str, max_chars: int, max_lines: int) -> list:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(",:;-") + "…"
    return lines


_ICONS = {
    # simple line illustrations drawn inside a 260x260 box
    "procure": '''<rect x="40" y="30" width="150" height="190" rx="14" fill="none" stroke="#fff" stroke-width="8" opacity=".9"/>
      <line x1="70" y1="80" x2="160" y2="80" stroke="#fff" stroke-width="8" stroke-linecap="round"/>
      <line x1="70" y1="115" x2="160" y2="115" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".7"/>
      <line x1="70" y1="150" x2="130" y2="150" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".5"/>
      <circle cx="195" cy="190" r="42" fill="#fff" opacity=".95"/><path d="M175 190 l14 14 l26 -28" stroke="{a}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>''',
    "warehouse": '''<path d="M20 110 L130 40 L240 110 V225 H20 Z" fill="none" stroke="#fff" stroke-width="8" stroke-linejoin="round" opacity=".9"/>
      <rect x="55" y="140" width="45" height="40" rx="4" fill="#fff" opacity=".9"/><rect x="108" y="140" width="45" height="40" rx="4" fill="#fff" opacity=".7"/>
      <rect x="161" y="140" width="45" height="40" rx="4" fill="#fff" opacity=".5"/><rect x="82" y="92" width="45" height="40" rx="4" fill="#fff" opacity=".6"/>
      <rect x="135" y="92" width="45" height="40" rx="4" fill="#fff" opacity=".8"/><line x1="20" y1="225" x2="240" y2="225" stroke="#fff" stroke-width="8"/>''',
    "sales": '''<rect x="30" y="150" width="40" height="70" rx="6" fill="#fff" opacity=".5"/><rect x="90" y="110" width="40" height="110" rx="6" fill="#fff" opacity=".7"/>
      <rect x="150" y="70" width="40" height="150" rx="6" fill="#fff" opacity=".9"/><path d="M30 110 L100 70 L150 85 L225 30" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="225" cy="30" r="12" fill="#fff"/>''',
    "ledger": '''<rect x="35" y="35" width="190" height="190" rx="18" fill="none" stroke="#fff" stroke-width="8" opacity=".9"/>
      <line x1="130" y1="35" x2="130" y2="225" stroke="#fff" stroke-width="6" opacity=".6"/>
      <text x="82" y="145" font-family="DejaVu Sans, Arial, sans-serif" font-size="64" font-weight="700" fill="#fff" text-anchor="middle">Dr</text>
      <text x="178" y="145" font-family="DejaVu Sans, Arial, sans-serif" font-size="64" font-weight="700" fill="#fff" text-anchor="middle" opacity=".8">Cr</text>''',
    "spark": '''<path d="M130 20 L150 105 L235 125 L150 145 L130 230 L110 145 L25 125 L110 105 Z" fill="#fff" opacity=".95"/>
      <circle cx="215" cy="45" r="16" fill="#fff" opacity=".7"/><circle cx="50" cy="210" r="11" fill="#fff" opacity=".6"/>''',
    "code": '''<rect x="20" y="40" width="220" height="170" rx="16" fill="none" stroke="#fff" stroke-width="8" opacity=".9"/>
      <line x1="20" y1="78" x2="240" y2="78" stroke="#fff" stroke-width="6" opacity=".6"/>
      <path d="M85 110 L55 140 L85 170" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M175 110 L205 140 L175 170" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="145" y1="100" x2="115" y2="180" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".8"/>''',
    "server": '''<rect x="40" y="30" width="180" height="56" rx="12" fill="none" stroke="#fff" stroke-width="8"/>
      <rect x="40" y="102" width="180" height="56" rx="12" fill="none" stroke="#fff" stroke-width="8" opacity=".8"/>
      <rect x="40" y="174" width="180" height="56" rx="12" fill="none" stroke="#fff" stroke-width="8" opacity=".6"/>
      <circle cx="190" cy="58" r="8" fill="#fff"/><circle cx="190" cy="130" r="8" fill="#fff"/><circle cx="190" cy="202" r="8" fill="#fff"/>
      <line x1="66" y1="58" x2="130" y2="58" stroke="#fff" stroke-width="7" stroke-linecap="round"/>''',
    "truck": '''<rect x="15" y="70" width="140" height="100" rx="10" fill="none" stroke="#fff" stroke-width="8"/>
      <path d="M155 100 H205 L240 135 V170 H155 Z" fill="none" stroke="#fff" stroke-width="8" stroke-linejoin="round"/>
      <circle cx="60" cy="190" r="22" fill="#fff"/><circle cx="200" cy="190" r="22" fill="#fff"/>
      <line x1="40" y1="105" x2="120" y2="105" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".7"/>''',
    "network": '''<circle cx="130" cy="125" r="34" fill="#fff" opacity=".95"/>
      <circle cx="40" cy="45" r="22" fill="#fff" opacity=".8"/><circle cx="220" cy="45" r="22" fill="#fff" opacity=".8"/>
      <circle cx="40" cy="210" r="22" fill="#fff" opacity=".8"/><circle cx="220" cy="210" r="22" fill="#fff" opacity=".8"/>
      <path d="M58 60 L105 102 M202 60 L155 102 M58 195 L105 148 M202 195 L155 148" stroke="#fff" stroke-width="7" stroke-linecap="round"/>''',
    "rocket": '''<path d="M130 20 C180 50 195 120 170 180 H90 C65 120 80 50 130 20 Z" fill="#fff" opacity=".95"/>
      <circle cx="130" cy="95" r="22" fill="{a}"/><path d="M90 150 L55 195 L95 185 Z M170 150 L205 195 L165 185 Z" fill="#fff" opacity=".7"/>
      <path d="M110 190 L130 240 L150 190 Z" fill="#fde68a"/>''',
}


def cover_title(article: dict) -> str:
    """Short punchy cover text: the part of the SEO title before ':' / '—'."""
    t = article.get("seo_title") or article.get("h1", "")
    head = re.split(r"\s*[:—|]\s*|\s+-\s+", t)[0].strip()
    return head if 12 <= len(head) <= 70 else t


def cover_svg(article: dict) -> str:
    t = theme(article.get("module"))
    lines = _wrap(cover_title(article), 22, 3)
    size = 62 if len(lines) <= 2 else 56
    y0 = 300 - (len(lines) - 1) * (size + 10) // 2
    text = "".join(
        f'<text x="70" y="{y0 + i * (size + 12)}" font-family="DejaVu Sans, Inter, Arial, sans-serif" '
        f'font-size="{size}" font-weight="800" fill="#ffffff">{_e(line)}</text>'
        for i, line in enumerate(lines)
    )
    icon = _ICONS[t["icon"]].replace("{a}", t["a"])
    badge = _e((article.get("cover_badge") or t["name"]).upper())
    badge_w = 28 + len(badge) * 15
    badge_svg = "" if article.get("cover_badge") == "" else (
        f'<rect x="70" y="60" width="{badge_w}" height="46" rx="23" fill="#ffffff" opacity=".18"/>'
        f'<text x="{70 + badge_w // 2}" y="91" font-family="DejaVu Sans, Inter, Arial, sans-serif" font-size="22" '
        f'font-weight="700" fill="#ffffff" text-anchor="middle" letter-spacing="2">{badge}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['a']}"/><stop offset="1" stop-color="{t['b']}"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0 H0 V40" fill="none" stroke="#ffffff" stroke-opacity=".08" stroke-width="2"/>
    </pattern>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#grid)"/>
  <circle cx="1060" cy="90" r="210" fill="#ffffff" opacity=".08"/>
  <circle cx="1130" cy="560" r="150" fill="#000000" opacity=".10"/>
  {badge_svg}
  {text}
  <g transform="translate(905 200)">{icon}</g>
  <rect x="70" y="520" width="6" height="52" rx="3" fill="#ffffff"/>
  <text x="92" y="545" font-family="DejaVu Sans, Inter, Arial, sans-serif" font-size="24" font-weight="700" fill="#ffffff">theTechMentor</text>
  <text x="92" y="575" font-family="DejaVu Sans, Inter, Arial, sans-serif" font-size="20" fill="#ffffff" opacity=".85">SAP S/4HANA Academy · youronementor.com</text>
</svg>'''


def write_cover(article: dict) -> tuple:
    """Writes covers; returns (svg_relative_to_blog, absolute_png_url_or_default)."""
    os.makedirs(COVER_DIR, exist_ok=True)
    slug = article["slug"]
    svg = cover_svg(article)
    with open(os.path.join(COVER_DIR, f"{slug}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    og = DEFAULT_OG
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=os.path.join(COVER_DIR, f"{slug}.png"))
        og = f"{SITE}/blog/covers/{slug}.png"
    except Exception as exc:  # cairosvg missing or font issue: keep the site default
        print(f"[design] PNG cover skipped: {exc}")
    return f"covers/{slug}.svg", og


# --------------------------------------------------------------------------- #
# Page components
# --------------------------------------------------------------------------- #

TCODE_RE = re.compile(r"^(?:/[A-Z0-9]+/[A-Z0-9_]+|[A-Z]{2,5}\d{1,3}[A-Z]?N?|SPRO|MIGO|MIRO|MMBE|OBYC|OMJJ|MRRL|MR11)$")


def tcodes_in(article: dict, limit: int = 8) -> list:
    found = []
    blob = article.get("intro_html", "") + " ".join(s["html"] for s in article.get("sections", []))
    for c in re.findall(r"<code>(.*?)</code>", blob):
        c = html.unescape(c).strip()
        if TCODE_RE.match(c) and c not in found:
            found.append(c)
    return found[:limit]


def flow_html(steps: list) -> str:
    if not steps:
        return ""
    items = "".join(
        f'<li><span class="flow-n">{i}</span><strong>{_rich(s.get("title"))}</strong><span>{_rich(s.get("detail"))}</span></li>'
        for i, s in enumerate(steps, 1)
    )
    return f'<div class="flow"><div class="flow-label">Process at a glance</div><ol class="flow-steps">{items}</ol></div>'


def screenshots_html(slug: str) -> str:
    folder = os.path.join(SHOT_DIR, slug)
    if not os.path.isdir(folder):
        return ""
    figs = []
    for name in sorted(os.listdir(folder)):
        if not re.search(r"\.(png|jpe?g|webp)$", name, re.I):
            continue
        caption = re.sub(r"^\d+[-_ ]*", "", os.path.splitext(name)[0]).replace("-", " ").replace("_", " ")
        caption = caption[:1].upper() + caption[1:]
        figs.append(
            f'<figure><img src="../images/blog/{slug}/{_e(name)}" alt="{_e(caption)}" loading="lazy" />'
            f'<figcaption>{_e(caption)}</figcaption></figure>'
        )
    if not figs:
        return ""
    return f'<h2 id="screens"><span class="h2-n">📸</span>Screens from a real S/4HANA system</h2><div class="shots">{"".join(figs)}</div>'


def related_cards(related: list) -> str:
    cards = []
    for slug, title in related:
        cover = f"covers/{slug}.svg" if os.path.exists(os.path.join(COVER_DIR, f"{slug}.svg")) else ""
        img = f'<img src="{cover}" alt="" loading="lazy" />' if cover else '<div class="rel-ph">📘</div>'
        cards.append(f'<a class="rel-card" href="{slug}.html">{img}<span>{_e(title)}</span></a>')
    return f'<div class="related"><div class="flow-label">Keep learning</div><div class="rel-grid">{"".join(cards)}</div></div>'


# --------------------------------------------------------------------------- #
# Full page
# --------------------------------------------------------------------------- #

def render(article: dict, related: list, word_count: int, published_iso: str = None) -> str:
    today = datetime.date.today()
    published_iso = published_iso or today.isoformat()
    modified_iso = today.isoformat()
    slug = article["slug"]
    url = f"{SITE}/blog/{slug}.html"
    t = theme(article.get("module"))
    cover_rel, og_image = write_cover(article)
    read_min = max(5, round(word_count / 220))
    tcodes = tcodes_in(article)

    toc = "".join(
        f'<li><a href="#sec-{i}"><span>{i:02d}</span>{_e(s["heading"])}</a></li>'
        for i, s in enumerate(article["sections"], 1)
    ) + '<li><a href="#faqs"><span>?</span>Frequently asked questions</a></li>'

    sections = "".join(
        f'<h2 id="sec-{i}"><span class="h2-n">{i:02d}</span>{_e(s["heading"])}</h2>\n{s["html"]}\n'
        for i, s in enumerate(article["sections"], 1)
    )
    takeaways = "".join(f"<li>{_rich(x)}</li>" for x in article.get("key_takeaways", []))
    faqs = "".join(
        f'<details class="ai-faq"><summary>{_e(f["question"].replace("`", ""))}</summary><p>{_rich(f["answer"])}</p></details>'
        for f in article["faqs"]
    )
    chips = "".join(f"<code>{_e(c)}</code>" for c in tcodes)
    glance = (
        f'<div class="glance">'
        f'<div><span>Module</span><strong>{_e(t["name"])}</strong></div>'
        f'<div><span>Read time</span><strong>{read_min} min</strong></div>'
        f'<div><span>Level</span><strong>{_e(article.get("level") or "Beginner → Consultant")}</strong></div>'
        + (f'<div class="glance-codes"><span>T-codes covered</span><p>{chips}</p></div>' if chips else "")
        + "</div>"
    )

    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": article["h1"][:110],
         "description": article["meta_description"], "image": og_image,
         "datePublished": published_iso, "dateModified": modified_iso,
         "author": {"@type": "Person", "name": "Anshuman Behuria",
                    "url": "https://www.linkedin.com/in/anshuman-behuria-946860130"},
         "publisher": {"@type": "Organization", "name": "theTechMentor", "url": SITE},
         "mainEntityOfPage": url, "wordCount": word_count},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": article["h1"][:110], "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["question"], "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}}
            for f in article["faqs"]]},
    ]
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_e(article['seo_title'])}</title>
  <meta name="description" content="{_e(article['meta_description'])}" />
  <link rel="canonical" href="{url}" />
  <meta name="robots" content="index,follow,max-image-preview:large" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{_e(article['h1'])}" />
  <meta property="og:description" content="{_e(article['meta_description'])}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:site_name" content="theTechMentor" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="article:published_time" content="{published_iso}" />
  <meta property="article:modified_time" content="{modified_iso}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" />
  <link rel="icon" href="../images/logo-mark.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="../site.css?v=5" />
  <link rel="stylesheet" href="ai-article.css?v=3" />
  <script type="application/ld+json">{ld_json}</script>
  <script src="../site-config.js"></script>
  <script src="../tracking.js"></script>
</head>
<body class="ai-page" style="--accent:{t['a']};--accent2:{t['b']};--accent-soft:{t['soft']};">
  <div class="reading-progress" id="reading-progress-bar"></div>
  <header class="header">
    <nav class="nav wrap" aria-label="Main">
      <a href="../index.html" class="brand" aria-label="theTechMentor home"><img src="../images/logo-mark.svg" alt="" width="36" height="36" /><span>the<b>Tech</b>Mentor</span></a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <ul class="nav-links">
        <li><a href="../index.html#courses">Courses</a></li>
        <li><a href="../index.html#paths">Career paths</a></li>
        <li><a href="index.html">Blog</a></li>
        <li><a href="../index.html#advisor" class="btn btn-ghost btn-sm">Free counselling</a></li>
        <li><a href="../index.html#courses" class="btn btn-primary btn-sm">Explore courses</a></li>
      </ul>
    </nav>
  </header>

  <main class="blog-article-wrap ai-wrap">
    <nav class="blog-breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a> &gt; <a href="index.html">Blog</a> &gt; <span>{_e(article['category'])}</span>
    </nav>

    <header class="ai-hero">
      <span class="ai-pill">{_e(article['badge'])}</span>
      <h1 class="blog-title">{_e(article['h1'])}</h1>
      <p class="ai-dek">{_e(article.get('excerpt', '').replace('`', ''))}</p>
      <div class="blog-meta">
        <div class="author-chip">
          <img class="author-photo" src="../images/anshuman-behuria-96.jpg" alt="Anshuman Behuria" width="40" height="40" />
          <div class="author-info"><strong>Anshuman Behuria</strong><span>Lead SAP Mentor · theTechMentor</span></div>
        </div>
        <span>Updated <time datetime="{modified_iso}">{today.strftime('%b %d, %Y')}</time></span>
      </div>
      <img class="ai-cover" src="{cover_rel}" width="1200" height="630" alt="{_e(article['h1'])}" />
    </header>

    <article class="article-content ai-article">
      {glance}

      <div class="ai-intro">{article['intro_html']}</div>

      <div class="ai-box ai-takeaways"><div class="box-label">⚡ Key takeaways</div><ul>{takeaways}</ul></div>

      {flow_html(article.get('process_flow') or [])}

      <nav class="ai-box ai-toc" aria-label="Contents"><div class="box-label">📑 In this guide</div><ol>{toc}</ol></nav>

      {sections}

      {screenshots_html(slug)}

      <div class="ai-optin" id="lead-optin">
        <div class="optin-icon">🎁</div>
        <strong>Free: SAP MM &amp; EWM video course + interview kit</strong>
        <p>Get the 40+ lesson playlist, the most-asked interview questions and our 90-day roadmap on WhatsApp.</p>
        <form class="ttm-optin-form" data-source="blog:{slug}">
          <input name="name" required placeholder="Your name" autocomplete="name" />
          <input name="phone" required placeholder="WhatsApp number" autocomplete="tel" inputmode="tel" />
          <input name="email" type="email" placeholder="Email (optional)" autocomplete="email" />
          <button type="submit" class="btn btn-primary">Send me the free kit</button>
        </form>
        <div class="ttm-optin-done" hidden></div>
      </div>

      <h2 id="faqs"><span class="h2-n">?</span>Frequently asked questions</h2>
      {faqs}

      {related_cards(related)}

      <div class="blog-course-cta ai-cta">
        <h3>Learn SAP hands-on with theTechMentor</h3>
        <p>Live weekday &amp; weekend batches or 24/7 recorded courses, with S/4HANA practice server access and interview preparation.</p>
        <div class="blog-cta-actions">
          <a href="../index.html#pricing" class="btn btn-primary">See programs &amp; fees</a>
          <a href="../index.html#enroll" class="btn btn-outline">Book a free 15-min call</a>
        </div>
      </div>
    </article>
  </main>

  <footer class="footer">
    <div class="wrap footer-grid">
      <div class="footer-brand">
        <a href="../index.html" class="brand brand-light"><img src="../images/logo-mark.svg" alt="" width="32" height="32" /><span>the<b>Tech</b>Mentor</span></a>
        <p>Online SAP S/4HANA academy for logistics, procurement and warehouse careers.</p>
      </div>
      <div><h4>Courses</h4><ul><li><a href="../index.html#courses">All courses</a></li><li><a href="../index.html#paths">Career paths</a></li><li><a href="../index.html#formats">Live vs self-paced</a></li></ul></div>
      <div><h4>Resources</h4><ul><li><a href="index.html">Blog</a></li><li><a href="../index.html#faq">FAQ</a></li><li><a href="../index.html#advisor">Free counselling</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="mailto:info@youronementor.com">info@youronementor.com</a></li><li><a href="https://wa.me/917848942021" target="_blank" rel="noopener noreferrer">WhatsApp +91 78489 42021</a></li></ul></div>
      <div><h4>Legal</h4><ul><li><a href="../privacy.html">Privacy</a></li><li><a href="../terms.html">Terms</a></li><li><a href="../refund.html">Refunds</a></li></ul></div>
    </div>
    <div class="wrap footer-bottom"><p>© {today.year} theTechMentor. SAP and S/4HANA are trademarks of SAP SE; theTechMentor is not affiliated with SAP SE.</p></div>
    <div class="footer-wordmark" aria-hidden="true"><img src="../images/footer-wordmark.webp?v=2" alt="" width="2000" height="306" loading="lazy" /></div>
  </footer>
  <script src="blog-leads.js"></script>
  <script>document.querySelector(".nav-toggle")?.addEventListener("click",function(){{var l=document.querySelector(".nav-links");var o=l.classList.toggle("open");this.setAttribute("aria-expanded",String(o));}});</script>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# Article data store (so pages can be re-rendered when the design changes)
# --------------------------------------------------------------------------- #

DATA_DIR = os.path.join(BASE_DIR, "content", "articles")


def save_article(article: dict, published_iso: str):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = dict(article, published=published_iso)
    with open(os.path.join(DATA_DIR, f"{article['slug']}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def screenshot_requests(article: dict):
    """Append the writer's screenshot ideas to a checklist the owner can work through."""
    ideas = article.get("screenshot_ideas") or []
    if not ideas:
        return
    path = os.path.join(BASE_DIR, "docs", "SCREENSHOTS-TODO.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new = not os.path.exists(path)
    if not new:
        with open(path, encoding="utf-8") as f:
            if f"images/blog/{article['slug']}/" in f.read():
                return
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write("# Screenshots to capture\n\nSave each as images/blog/<slug>/NN-short-description.png "
                    "(numbered in the order to show). They appear in the article on its next re-render.\n")
        f.write(f"\n## {article['h1']}\nFolder: `images/blog/{article['slug']}/`\n")
        for i, idea in enumerate(ideas, 1):
            f.write(f"- [ ] {i:02d}: {idea}\n")
