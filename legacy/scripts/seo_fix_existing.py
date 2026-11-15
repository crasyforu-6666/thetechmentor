#!/usr/bin/env python3
"""One-off (idempotent) SEO and conversion clean-up for existing blog pages.

- shortens <title> tags over 62 characters and meta descriptions over 158
- removes the visible "Primary Keyword" label and fake "Download PDF" cards
- adds Article + BreadcrumbList structured data where missing
- marks thin, old template posts (<900 words) noindex until the AI writer rewrites them
- switches the share image to PNG
- loads lead tracking + payment scripts and adds the free-kit opt-in form
Run from the repo root:  python3 scripts/seo_fix_existing.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
SITE = "https://youronementor.com"
NOINDEX_WORDS = 400  # template stubs this short stay out of Google until rewritten

OPTIN = """
      <!-- LEAD OPT-IN -->
      <div class="ai-optin" id="lead-optin">
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
"""


def words(page):
    body = re.sub(r"(?is)<(script|style|head|nav|header|footer)[^>]*>.*?</\1>", " ", page)
    return len(re.sub(r"<[^>]+>", " ", body).split())


def short_title(t, limit=62):
    if len(t) <= limit:
        return t
    t = re.sub(r"\s*\|\s*theTechMentor\s*$", "", t)
    if len(t) <= limit:
        return t
    for sep in (" — ", " - ", ": ", " | "):
        if sep in t and len(t.split(sep)[0]) >= 25:
            head = t.split(sep)[0]
            if len(head) <= limit:
                return head
    cut = t[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(":,-—|& ")


def short_desc(d, limit=158):
    if len(d) <= limit:
        return d
    cut = d[:155].rsplit(" ", 1)[0].rstrip(",;:-—")
    return cut + "."


def fix_page(path, slug):
    with open(path, encoding="utf-8") as f:
        page = f.read()
    orig = page
    is_ai = 'class="article-content ai-article"' in page

    page = page.replace("images/og-cover.svg", "images/og-cover.png")
    if is_ai:
        return page != orig and page

    # Title
    m = re.search(r"<title>(.*?)</title>", page, re.S)
    if m:
        t = html.unescape(m.group(1).strip())
        nt = short_title(t)
        if nt != t:
            page = page.replace(m.group(0), f"<title>{html.escape(nt, quote=False)}</title>", 1)

    # Meta description
    m = re.search(r'<meta name="description" content="([^"]*)"\s*/?>', page)
    if m:
        d = html.unescape(m.group(1))
        nd = short_desc(d)
        if nd != d:
            page = page.replace(m.group(0), f'<meta name="description" content="{html.escape(nd, quote=True)}" />', 1)

    # Visible "Primary Keyword" metadata cell
    page = re.sub(
        r'\s*<div style="border-left: 3px solid #[0-9a-f]{6}; padding-left: 0\.85rem;">\s*<span[^>]*>Primary Keyword:</span>\s*<code[^>]*>.*?</code>\s*</div>',
        "", page, flags=re.S)

    # Fake "Download PDF" cards (they linked back to the same page)
    page = re.sub(r"\s*<!-- (?:TOP |FOOTER )?PDF DOWNLOAD CARD -->\s*<div[^>]*>.*?</a>\s*</div>", "", page, flags=re.S)

    # Structured data
    if "application/ld+json" not in page:
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
        headline = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else slug
        headline = html.unescape(headline)[:110]
        desc = re.search(r'<meta name="description" content="([^"]*)"', page)
        date = re.search(r'(?:data-date|datetime)="(\d{4}-\d{2}-\d{2})"', page)
        url = f"{SITE}/blog/{slug}.html"
        ld = [
            {"@context": "https://schema.org", "@type": "Article", "headline": headline,
             "description": html.unescape(desc.group(1)) if desc else "",
             "image": f"{SITE}/images/og-cover.png",
             **({"datePublished": date.group(1)} if date else {}),
             "author": {"@type": "Person", "name": "Anshuman Behuria",
                        "url": "https://www.linkedin.com/in/anshuman-behuria-946860130"},
             "publisher": {"@type": "Organization", "name": "theTechMentor", "url": SITE},
             "mainEntityOfPage": url},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": headline, "item": url}]},
        ]
        tag = '  <script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"
        page = page.replace("</head>", tag + "</head>", 1)

    # Thin template posts stay out of Google until rewritten
    if words(page) < NOINDEX_WORDS and 'name="robots"' not in page:
        page = page.replace("</head>", '  <meta name="robots" content="noindex,follow" />\n</head>', 1)

    # Lead capture + working payment buttons
    if "ai-article.css" not in page:
        page = page.replace("</head>", '  <link rel="stylesheet" href="ai-article.css" />\n</head>', 1)
    if "site-config.js" not in page:
        page = page.replace("</head>",
                            '  <script src="../site-config.js"></script>\n  <script src="../tracking.js"></script>\n</head>', 1)
    if "ttm-optin-form" not in page:
        block = OPTIN.replace("{slug}", slug)
        if '<div class="blog-course-cta"' in page:
            i = page.index('<div class="blog-course-cta"')
            j = page.rfind("<!--", 0, i)
            at = j if j != -1 and page[j:i].strip().startswith("<!--") and "-->" in page[j:i] else i
            page = page[:at] + block.lstrip() + "\n      " + page[at:]
        elif "</article>" in page:
            page = page.replace("</article>", block + "    </article>", 1)
    tail = ""
    if "../script.js" not in page:
        tail += '  <script src="../script.js?v=5" defer></script>\n'
    if "blog-leads.js" not in page:
        tail += '  <script src="blog-leads.js"></script>\n'
    if tail:
        page = page.replace("</body>", tail + "</body>", 1)

    return page != orig and page


def main():
    changed = 0
    for name in sorted(os.listdir(BLOG)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(BLOG, name)
        if name == "article.html":
            with open(path, encoding="utf-8") as f:
                p = f.read()
            if 'name="robots"' not in p:
                p = p.replace("</head>", '  <meta name="robots" content="noindex,follow" />\n</head>', 1)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(p)
                changed += 1
            continue
        if name == "index.html":
            with open(path, encoding="utf-8") as f:
                p = f.read()
            np = p.replace("images/og-cover.svg", "images/og-cover.png")
            if np != p:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(np)
                changed += 1
            continue
        new = fix_page(path, name[:-5])
        if new:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            changed += 1
    for extra in ("index.html", "blog/custom-blogs.js"):
        p = os.path.join(ROOT, extra)
        with open(p, encoding="utf-8") as f:
            s = f.read()
        ns = s.replace("images/og-cover.svg", "images/og-cover.png")
        if ns != s:
            with open(p, "w", encoding="utf-8") as f:
                f.write(ns)
            changed += 1
    print(f"updated {changed} files")


if __name__ == "__main__":
    main()
