#!/usr/bin/env python3
"""Topic selection without repeats.

- Topics come from content/topic-backlog.json (curated, interleaved by module).
- Every topic used is recorded in content/topic-history.json.
- A topic is skipped when its title is too similar to any published post
  (including old posts still waiting to be rewritten) or to a used topic.
- Duplicate posts can be retired: the page is removed and a permanent
  redirect to the kept article is added to vercel.json.
"""
import datetime
import html
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
BACKLOG = os.path.join(BASE_DIR, "content", "topic-backlog.json")
HISTORY = os.path.join(BASE_DIR, "content", "topic-history.json")
VERCEL = os.path.join(BASE_DIR, "vercel.json")

STOP = set("""
a an and the of in on for to with vs versus by from at as is are how what why when which your you
sap s4hana s 4hana hana s/4hana 2025 2026 2027 guide complete step practical masterclass deep dive
explained explanation overview basics configuration configure setup set up tutorial blueprint
architect architects solution consultant consultants every must know top best master mastering
advanced comprehensive ultimate full process flow management managing part
mm ewm sd fico wm end question questions answer answers lifecycle new
""".split())

SIMILARITY_LIMIT = 0.55
MODULE_WORDS = {"mm", "ewm", "sd", "fico", "wm"}


def _tokens(text: str) -> set:
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or "")).lower()
    words = re.findall(r"[a-z0-9]+", text.replace("/", " "))
    syn = {"decentralised": "decentral", "decentralized": "decentral", "decentralize": "decentral",
           "o2c": "ordertocash", "p2p": "procuretopay", "atp": "availability"}
    out = set()
    for w in words:
        w = syn.get(w, w)
        if w in STOP or len(w) < 2:
            continue
        out.add(w[:-1] if len(w) > 4 and w.endswith("s") else w)  # crude singular
    return out


def _modules(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", (text or "").lower())) & MODULE_WORDS


def similarity(a: str, b: str) -> float:
    ma, mb = _modules(a), _modules(b)
    if ma and mb and not (ma & mb):
        return 0.0  # e.g. an MM topic is never a duplicate of an EWM topic
    if re.search(r"\binterview questions?\b", a.lower()) and re.search(r"\binterview questions?\b", b.lower()) and (ma == mb):
        return 1.0  # one interview-questions post per module is enough
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    jaccard = inter / len(ta | tb)
    # containment only counts when several meaningful words overlap
    small = min(len(ta), len(tb))
    full = inter == small and small >= 2  # every key word of the shorter title appears in the other
    containment = inter / small if (inter >= 3 or full) else 0.0
    return max(jaccard, containment * 0.85)


def published_titles() -> list:
    """[(slug, title, is_ai_article)] for every blog page."""
    out = []
    for name in sorted(os.listdir(BLOG_DIR)):
        if not name.endswith(".html") or name in ("index.html", "article.html"):
            continue
        with open(os.path.join(BLOG_DIR, name), encoding="utf-8", errors="ignore") as f:
            page = f.read()
        m = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else name[:-5]
        out.append((name[:-5], title, 'class="article-content ai-article"' in page))
    return out


def load_history() -> list:
    if os.path.exists(HISTORY):
        with open(HISTORY, encoding="utf-8") as f:
            return json.load(f)
    return []


def mark_used(topic_title: str, slug: str = "", article_title: str = "", module: str = ""):
    hist = load_history()
    if not module:
        for item in json.load(open(BACKLOG, encoding="utf-8")) if os.path.exists(BACKLOG) else []:
            if item["title"] == topic_title:
                module = item["module"]
    hist.append({"topic": topic_title, "module": module, "slug": slug, "title": article_title,
                 "date": datetime.date.today().isoformat()})
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=1, ensure_ascii=False)


def find_duplicate(title: str, exclude_slug: str = None, ai_only: bool = False):
    """Return (slug, title, score) of the most similar existing post above the limit, else None."""
    best = None
    for slug, t, is_ai in published_titles():
        if slug == exclude_slug or (ai_only and not is_ai):
            continue
        s = similarity(title, t)
        if s >= SIMILARITY_LIMIT and (best is None or s > best[2]):
            best = (slug, t, s)
    return best


def next_topic(log=print) -> dict:
    """Next unused, non-duplicate topic from the backlog (None when exhausted)."""
    with open(BACKLOG, encoding="utf-8") as f:
        backlog = json.load(f)
    hist = load_history()
    used = {h["topic"] for h in hist}
    used_same_module = lambda mod: [x for h in hist if h.get("module") == mod for x in (h["topic"], h.get("title", ""))]
    for item in backlog:
        title = item["title"]
        if title in used:
            continue
        if any(u and similarity(title, u) >= SIMILARITY_LIMIT for u in used_same_module(item["module"])):
            mark_used(title, "", "(skipped: similar to an earlier topic)")
            continue
        dup = find_duplicate(title)
        if dup:
            log(f"⏭️ Skipping '{title}' — too similar to existing post '{dup[1]}' ({dup[2]:.2f})")
            mark_used(title, dup[0], "(skipped: already covered)")
            continue
        return {"title": title, "keyword": title.split(":")[0].lower(), "module": item["module"],
                "role": "SAP MM / EWM learners and consultants in India", "sections": [], "faqs": []}
    return None


# --------------------------------------------------------------------------- #
# Retiring duplicate posts
# --------------------------------------------------------------------------- #

def _add_redirect(old_slug: str, new_slug: str):
    cfg = {}
    if os.path.exists(VERCEL):
        with open(VERCEL, encoding="utf-8") as f:
            cfg = json.load(f)
    redirects = [r for r in cfg.get("redirects", []) if r.get("source") != f"/blog/{old_slug}.html"]
    # keep chains short: anything pointing at old_slug now points at new_slug
    for r in redirects:
        if r.get("destination") == f"/blog/{old_slug}.html":
            r["destination"] = f"/blog/{new_slug}.html"
    redirects.append({"source": f"/blog/{old_slug}.html", "destination": f"/blog/{new_slug}.html", "permanent": True})
    cfg["redirects"] = redirects
    with open(VERCEL, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


def _remove_cards(slug: str):
    pat_card = re.compile(r'\s*(?:<!--[^>]*-->\s*)?<article class="blog-card"(?:(?!</article>).)*?href="(?:blog/)?'
                          + re.escape(slug) + r'\.html"(?:(?!</article>).)*?</article>', re.S)
    for path in (os.path.join(BASE_DIR, "index.html"), os.path.join(BLOG_DIR, "index.html")):
        with open(path, encoding="utf-8") as f:
            page = f.read()
        new = pat_card.sub("", page)
        if new != page:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
    js = os.path.join(BLOG_DIR, "custom-blogs.js")
    with open(js, encoding="utf-8") as f:
        data = f.read()
    new = re.sub(r',?\s*\{(?:(?!\{|\}).)*?slug:\s*"' + re.escape(slug) + r'"(?:(?!\{|\}).)*?\}', "", data, flags=re.S)
    new = new.replace("[,", "[")
    if new != data:
        with open(js, "w", encoding="utf-8") as f:
            f.write(new)


def retire(old_slug: str, keep_slug: str, log=print):
    """Remove a duplicate post and permanently redirect it to keep_slug."""
    for path in (os.path.join(BLOG_DIR, f"{old_slug}.html"),
                 os.path.join(BLOG_DIR, "covers", f"{old_slug}.svg"),
                 os.path.join(BLOG_DIR, "covers", f"{old_slug}.png"),
                 os.path.join(BASE_DIR, "content", "articles", f"{old_slug}.json")):
        if os.path.exists(path):
            os.remove(path)
    _remove_cards(old_slug)
    _add_redirect(old_slug, keep_slug)
    log(f"🔀 Retired duplicate {old_slug} → {keep_slug}")
