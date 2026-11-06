#!/usr/bin/env python3
"""Re-render every AI-written article with the current design.

Uses content/articles/<slug>.json when present; otherwise rebuilds the data
from the published HTML. Run after changing the design or adding screenshots:
    python3 scripts/rerender_articles.py
"""
import html
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from scripts import ai_writer, article_design  # noqa: E402
from scripts.auto_daily_blog_scheduler import set_card_cover  # noqa: E402

BLOG = os.path.join(BASE_DIR, "blog")
MARK = 'class="article-content ai-article"'


def guess_module(text: str) -> str:
    t = text.lower()
    if "ewm" in t or "warehouse" in t:
        return "EWM"
    if "joule" in t or " ai " in f" {t} " or "autonomous" in t:
        return "AI"
    if re.search(r"\bsd\b|order to cash|pricing procedure.*condition", t):
        return "SD"
    if any(k in t for k in ("fico", "acdoca", "universal journal", "ledger", "financial close")):
        return "FICO"
    if "career" in t or "salary" in t:
        return "Career"
    return "MM"


def _text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse_page(page: str, slug: str) -> dict:
    g = lambda pat: (re.search(pat, page, re.S) or [None, ""])[1]
    art_start = page.index(MARK)
    body = page[page.index(">", art_start) + 1:]
    intro_m = re.search(r'<div class="ai-intro">(.*?)</div>\s*<div class="ai-box ai-takeaways">', body, re.S) \
        or re.search(r"^(.*?)<div class=\"ai-box ai-takeaways\">", body, re.S)
    sections = []
    parts = re.split(r'<h2 id="sec-\d+">', body)[1:]
    for part in parts:
        head, _, rest = part.partition("</h2>")
        head = re.sub(r'<span class="h2-n">.*?</span>', "", head)
        rest = re.split(r'<h2 id="(?:faqs|screens)"|<div class="ai-optin"|<h2 id="sec-', rest)[0]
        sections.append({"heading": _text(head), "html": ai_writer.sanitize(rest.strip())})
    faqs = [{"question": _text(q), "answer": _text(a)}
            for q, a in re.findall(r'<details class="ai-faq"><summary>(.*?)</summary><p>(.*?)</p></details>', page, re.S)]
    takeaways = [_text(x) for x in re.findall(r"<li>(.*?)</li>",
                 (re.search(r'ai-takeaways">(.*?)</ul>', page, re.S) or [None, ""])[1], re.S)]
    h1 = _text(g(r"<h1[^>]*>(.*?)</h1>"))
    published = g(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"') or None
    art = {
        "seo_title": _text(g(r"<title>(.*?)</title>")),
        "h1": h1,
        "meta_description": html.unescape(g(r'<meta name="description" content="([^"]*)"')),
        "slug": slug,
        "category": _text(g(r'<nav class="blog-breadcrumb"[^>]*>.*?<span>(.*?)</span>')) or "Tutorial",
        "badge": _text(g(r'class="(?:sp-badge[^"]*|ai-pill)">(.*?)</span>')) or "SAP GUIDE",
        "excerpt": "",
        "module": guess_module(h1 + " " + slug),
        "level": "Beginner → Consultant",
        "intro_html": ai_writer.sanitize(intro_m.group(1).strip() if intro_m else ""),
        "sections": sections,
        "key_takeaways": takeaways,
        "faqs": faqs,
        "process_flow": [],
        "screenshot_ideas": [],
        "published": published,
    }
    desc = art["meta_description"]
    art["excerpt"] = desc if len(desc) < 200 else desc[:197] + "…"
    return art


def main():
    count = 0
    data_dir = os.path.join(BASE_DIR, "content", "articles")
    for name in sorted(os.listdir(BLOG)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(BLOG, name)
        with open(path, encoding="utf-8") as f:
            page = f.read()
        if MARK not in page:
            continue
        slug = name[:-5]
        jpath = os.path.join(data_dir, f"{slug}.json")
        if os.path.exists(jpath):
            with open(jpath, encoding="utf-8") as f:
                art = json.load(f)
        else:
            art = parse_page(page, slug)
        published = art.pop("published", None)
        art["word_count"] = ai_writer.word_count(art)
        with open(path, "w", encoding="utf-8") as f:
            f.write(ai_writer.render_article(art, published_iso=published))
        set_card_cover(slug)
        count += 1
        print(f"re-rendered {slug} ({art['module']}, {len(art['sections'])} sections, {len(art['faqs'])} FAQs)")
    print(f"{count} article(s) re-rendered")
    covers_for_other_posts()


def covers_for_other_posts():
    """Give hand-written / older posts a generated cover for cards and share previews."""
    n = 0
    for name in sorted(os.listdir(BLOG)):
        if not name.endswith(".html") or name in ("index.html", "article.html"):
            continue
        path = os.path.join(BLOG, name)
        with open(path, encoding="utf-8") as f:
            page = f.read()
        if MARK in page:
            continue
        slug = name[:-5]
        h1 = _text((re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S) or [None, slug])[1])
        title = _text((re.search(r"<title>(.*?)</title>", page, re.S) or [None, h1])[1])
        art = {"slug": slug, "h1": h1, "seo_title": title, "module": guess_module(h1 + " " + slug)}
        _, og = article_design.write_cover(art)
        new = re.sub(r'(<meta property="og:image" content=")[^"]*(")', lambda m: m.group(1) + og + m.group(2), page)
        if new != page:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
        set_card_cover(slug)
        n += 1
    print(f"covers generated for {n} other post(s)")


if __name__ == "__main__":
    main()
