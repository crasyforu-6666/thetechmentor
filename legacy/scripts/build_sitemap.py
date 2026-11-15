#!/usr/bin/env python3
"""Regenerate sitemap.xml and robots.txt from the HTML pages in the repo.

Run from the repo root:  python3 scripts/build_sitemap.py
"""
import datetime
import os
import subprocess

BASE = "https://youronementor.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE = {"thank-you.html"}


def last_modified(rel_path):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel_path],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip()
        if out:
            return out
    except OSError:
        pass
    return datetime.date.today().isoformat()


def collect():
    pages = []
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html") and name not in EXCLUDE:
            pages.append(name)
    blog_dir = os.path.join(ROOT, "blog")
    for name in sorted(os.listdir(blog_dir)):
        if name.endswith(".html"):
            pages.append("blog/" + name)
    return [p for p in pages if not is_noindex(p)]


def is_noindex(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as f:
        head = f.read(6000)
    return 'name="robots" content="noindex' in head


def url_for(rel):
    if rel == "index.html":
        return BASE + "/"
    if rel == "blog/index.html":
        return BASE + "/blog/"
    if rel == "digital-products.html":
        return BASE + "/digital-products"
    return BASE + "/" + rel


def main():
    entries = []
    for rel in collect():
        if rel == "index.html":
            prio = "1.0"
        elif rel.startswith("blog/") and rel != "blog/index.html":
            prio = "0.7"
        elif rel in ("privacy.html", "terms.html", "refund.html"):
            prio = "0.2"
        else:
            prio = "0.8"
        entries.append(
            "  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>"
            % (url_for(rel), last_modified(rel), prio)
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /thank-you.html\n\n"
        "Sitemap: %s/sitemap.xml\n" % BASE
    )
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("sitemap.xml: %d URLs" % len(entries))


if __name__ == "__main__":
    main()
