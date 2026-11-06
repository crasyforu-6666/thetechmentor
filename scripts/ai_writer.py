#!/usr/bin/env python3
"""
AI article writer for the theTechMentor blog (youronementor.com).

Writes complete, expert-level SAP articles with Claude and renders them into the
site's blog design. Every article must pass a quality gate before it can be
published; if it fails twice, nothing is published (thin pages hurt rankings).

Credentials (GitHub Actions secrets), any one is enough:
  GEMINI_API_KEY           free Google AI Studio key  -> used for new articles
  CLAUDE_CODE_OAUTH_TOKEN  Claude Pro/Max login token -> used for rewrites
  ANTHROPIC_API_KEY        paid Anthropic API key
Editorial rules are read from AGENTS.md in the repo root when it exists, so the
owner's existing blog instructions always apply.
"""

import datetime
import html
import json
import os
import re
from html.parser import HTMLParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
SITE = "https://youronementor.com"
OG_IMAGE = f"{SITE}/images/og-cover.png"

MODEL = "claude-opus-5-5"
MIN_WORDS = 1500
MIN_SECTIONS = 5
MIN_FAQS = 4
CATEGORIES = ["Tutorial", "Interview prep", "Career", "SAP news"]

# Phrases from the old template generator. Their presence means boilerplate.
BANNED_PHRASES = [
    "deep dive into key configuration parameters",
    "primary keyword",
    "download original pdf",
    "as an ai",
    "in today's fast-paced",
    "in conclusion,",
]

DEFAULT_STANDARDS = """
EDITORIAL STANDARDS (theTechMentor)
- Author voice: Anshuman Behuria, SAP MM & EWM consultant with 12+ years of S/4HANA
  implementation experience, training career-switchers in India. Practical, direct,
  first-hand. Explain *why*, not just *what*.
- Audience: Indian professionals (logistics, IT support, freshers, junior SAP
  consultants) moving into SAP MM / EWM roles, plus working consultants.
- Every article must teach something concrete: real transaction codes, SPRO menu
  paths, table names, configuration steps, worked examples with sample values,
  common errors with their message text and the fix, and interview angles.
- Be accurate. Never invent transaction codes, tables, notes or release features.
  If something differs between ECC and S/4HANA, or between embedded and
  decentralized EWM, say so. If unsure, leave it out rather than guess.
- No filler, no generic intros, no repeated sentences, no keyword stuffing.
  Use the primary keyword naturally in the H1, the first 100 words, one H2 and
  the meta description.
- Structure: short intro that states the problem and what the reader will be
  able to do; 5–9 H2 sections; use tables for comparisons and config steps;
  ordered lists for procedures; a "Common mistakes" or "Troubleshooting" section;
  an "Interview questions on this topic" section where relevant.
- Mention the training naturally at most once (e.g. practising on an S/4HANA
  sandbox); never be salesy. Never promise jobs, salaries or placement.
- Internal links: link 2–4 related existing articles from the list provided,
  using their exact relative href (e.g. <a href="slug.html">anchor</a>).
- Indian context where useful (salary bands in LPA, Indian companies hiring),
  but only general, well-known facts.
"""

ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "seo_title": {"type": "string", "description": "<title> tag, 45-60 characters, keyword near the start, no brand suffix"},
        "h1": {"type": "string", "description": "On-page headline, may be slightly longer than seo_title"},
        "meta_description": {"type": "string", "description": "120-155 characters, includes keyword, ends with a reason to click"},
        "slug": {"type": "string", "description": "lowercase-hyphenated URL slug, 3-8 words, no year unless essential"},
        "category": {"type": "string", "enum": CATEGORIES},
        "badge": {"type": "string", "description": "Short uppercase label, e.g. 'SAP MM TUTORIAL'"},
        "excerpt": {"type": "string", "description": "1-2 sentence card summary, under 200 characters"},
        "intro_html": {"type": "string", "description": "1-3 <p> paragraphs"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "heading": {"type": "string", "description": "H2 text, no numbering"},
                    "html": {"type": "string", "description": "Section body HTML: p, h3, ul, ol, li, table, thead, tbody, tr, th, td, strong, em, code, pre, blockquote, a"},
                },
                "required": ["heading", "html"],
                "additionalProperties": False,
            },
        },
        "key_takeaways": {"type": "array", "items": {"type": "string"}},
        "faqs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string", "description": "Plain text, 2-4 sentences"},
                },
                "required": ["question", "answer"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["seo_title", "h1", "meta_description", "slug", "category", "badge", "excerpt",
                 "intro_html", "sections", "key_takeaways", "faqs"],
    "additionalProperties": False,
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def load_standards() -> str:
    for name in ("AGENTS.md", "agents.md", "BLOG_STANDARDS.md"):
        path = os.path.join(BASE_DIR, name)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return f.read() + "\n\n" + DEFAULT_STANDARDS
    return DEFAULT_STANDARDS


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def word_count(article: dict) -> int:
    text = article.get("intro_html", "") + " ".join(s["html"] for s in article.get("sections", []))
    return len(strip_tags(text).split())


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)[:80].strip("-")


class _Sanitizer(HTMLParser):
    """Keeps a safe subset of HTML; drops scripts, styles, events and unknown tags."""
    ALLOWED = {"p", "h3", "h4", "ul", "ol", "li", "strong", "em", "b", "i", "code", "pre",
               "table", "thead", "tbody", "tr", "th", "td", "blockquote", "a", "br"}
    VOID = {"br"}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "iframe"):
            self.skip += 1
            return
        if self.skip or tag not in self.ALLOWED:
            return
        attr = ""
        if tag == "a":
            href = dict(attrs).get("href", "") or ""
            if re.match(r"^(https://|[a-z0-9-]+\.html(#[\w-]+)?$|\.\./)", href):
                ext = href.startswith("https://") and "youronementor.com" not in href
                attr = f' href="{html.escape(href, quote=True)}"' + (' rel="noopener" target="_blank"' if ext else "")
            else:
                return
        self.out.append(f"<{tag}{attr}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in self.ALLOWED or tag in self.VOID:
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))

    def handle_entityref(self, name):
        if not self.skip:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skip:
            self.out.append(f"&#{name};")


def sanitize(fragment: str) -> str:
    p = _Sanitizer()
    p.feed(fragment or "")
    p.close()
    return "".join(p.out)


def existing_posts() -> list:
    """[(slug, title)] of published articles, for internal links and de-duplication."""
    posts = []
    for name in sorted(os.listdir(BLOG_DIR)):
        if not name.endswith(".html") or name in ("index.html", "article.html"):
            continue
        with open(os.path.join(BLOG_DIR, name), encoding="utf-8", errors="ignore") as f:
            m = re.search(r"<h1[^>]*>(.*?)</h1>", f.read(), re.S)
        posts.append((name[:-5], strip_tags(m.group(1)) if m else name[:-5]))
    return posts


# --------------------------------------------------------------------------- #
# Quality gate
# --------------------------------------------------------------------------- #

def quality_problems(article: dict, taken_slugs: set, fixed_slug: str = None) -> list:
    problems = []
    words = word_count(article)
    if words < MIN_WORDS:
        problems.append(f"Body has {words} words; it must be at least {MIN_WORDS} words of substantive content.")
    if len(article.get("sections", [])) < MIN_SECTIONS:
        problems.append(f"Needs at least {MIN_SECTIONS} H2 sections.")
    if len(article.get("faqs", [])) < MIN_FAQS:
        problems.append(f"Needs at least {MIN_FAQS} FAQs.")
    if not 30 <= len(article.get("seo_title", "")) <= 62:
        problems.append(f"seo_title is {len(article.get('seo_title', ''))} characters; keep it 45-60.")
    if not 110 <= len(article.get("meta_description", "")) <= 160:
        problems.append(f"meta_description is {len(article.get('meta_description', ''))} characters; keep it 120-155.")
    if not fixed_slug and slugify(article.get("slug", "")) in taken_slugs:
        problems.append("slug already exists on the site; choose a different angle and slug.")
    full = (article.get("intro_html", "") + " ".join(s["html"] for s in article.get("sections", []))).lower()
    for phrase in BANNED_PHRASES:
        if phrase in full:
            problems.append(f"Remove the boilerplate phrase '{phrase}'.")
    paras = [strip_tags(p).lower() for p in re.findall(r"<p>(.*?)</p>", full, re.S)]
    paras = [p for p in paras if len(p) > 60]
    if len(paras) != len(set(paras)):
        problems.append("Some paragraphs are repeated; every paragraph must be unique.")
    return problems


# --------------------------------------------------------------------------- #
# Model backends
#   gemini      - Google AI Studio free-tier key (GEMINI_API_KEY)
#   claude-code - Claude Code CLI with a Claude Pro/Max login token (CLAUDE_CODE_OAUTH_TOKEN)
#   anthropic   - paid Anthropic API key (ANTHROPIC_API_KEY)
# --------------------------------------------------------------------------- #

GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
CLAUDE_CODE_MODEL = os.environ.get("CLAUDE_CODE_MODEL", "")  # empty = account default


def available_backends() -> list:
    out = []
    if os.environ.get("GEMINI_API_KEY"):
        out.append("gemini")
    if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        out.append("claude-code")
    if os.environ.get("ANTHROPIC_API_KEY"):
        out.append("anthropic")
    return out


def choose_backend(mode: str) -> str:
    """Refreshes (quality-critical rewrites) prefer Claude; new posts prefer free Gemini."""
    forced = os.environ.get("WRITER_BACKEND")
    have = available_backends()
    if forced:
        if forced not in have:
            raise RuntimeError(f"WRITER_BACKEND={forced} but its credential is not set")
        return forced
    order = ["claude-code", "anthropic", "gemini"] if mode == "refresh" else ["gemini", "claude-code", "anthropic"]
    for b in order:
        if b in have:
            return b
    raise RuntimeError("No writer credential set (GEMINI_API_KEY, CLAUDE_CODE_OAUTH_TOKEN or ANTHROPIC_API_KEY)")


def _gemini_schema(node):
    """Gemini's response schema doesn't accept additionalProperties; strip it."""
    if isinstance(node, dict):
        return {k: _gemini_schema(v) for k, v in node.items() if k != "additionalProperties"}
    if isinstance(node, list):
        return [_gemini_schema(v) for v in node]
    return node


def _request_gemini(system: str, user: str) -> dict:
    from google import genai
    from google.genai import types

    # v1beta is required for system instructions and JSON-schema output.
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"],
                          http_options=types.HttpOptions(api_version="v1beta"))
    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            response_json_schema=_gemini_schema(ARTICLE_SCHEMA),
            max_output_tokens=32768,
        ),
    )
    if not resp.text:
        raise RuntimeError(f"Gemini returned no text (finish reason: {getattr(resp.candidates[0], 'finish_reason', '?') if resp.candidates else 'blocked'})")
    return json.loads(resp.text)


def _request_claude_code(system: str, user: str) -> dict:
    import shutil
    import subprocess

    exe = shutil.which("claude")
    if not exe:
        raise RuntimeError("Claude Code CLI not installed (npm install -g @anthropic-ai/claude-code)")
    cmd = [exe, "-p", "--output-format", "json", "--tools", "",
           "--json-schema", json.dumps(ARTICLE_SCHEMA), "--system-prompt", system]
    if CLAUDE_CODE_MODEL:
        cmd += ["--model", CLAUDE_CODE_MODEL]
    res = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=1500)
    if res.returncode != 0:
        raise RuntimeError(f"claude CLI failed ({res.returncode}): {(res.stderr or res.stdout)[-800:]}")
    envelope = json.loads(res.stdout)
    if envelope.get("is_error"):
        raise RuntimeError(f"claude CLI error: {str(envelope.get('result'))[:800]}")
    data = envelope.get("structured_output")
    if isinstance(data, dict):
        return data
    text = envelope.get("result", "")
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        raise RuntimeError("claude CLI returned no JSON article")
    return json.loads(text[start:end + 1])


def _request_article(client, system: str, user: str) -> dict:
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        thinking={"type": "adaptive"},
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": ARTICLE_SCHEMA}},
        system=system,
        messages=[{"role": "user", "content": user}],
    ) as stream:
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        raise RuntimeError(f"Model declined the topic: {getattr(message.stop_details, 'category', None)}")
    if message.stop_reason == "max_tokens":
        raise RuntimeError("Article was cut off (max_tokens).")
    text = next(b.text for b in message.content if b.type == "text")
    return json.loads(text)


def write_article(topic: dict, mode: str = "new", fixed_slug: str = None, old_text: str = "") -> dict:
    """Returns a validated article dict, or raises RuntimeError if it can't meet the bar."""
    backend = choose_backend(mode)
    client = None
    if backend == "anthropic":
        import anthropic  # imported lazily so the module loads without the SDK installed
        client = anthropic.Anthropic()
    print(f"[ai_writer] backend: {backend}")
    posts = existing_posts()
    taken = {s for s, _ in posts}
    others = [(s, t) for s, t in posts if s != fixed_slug]
    post_list = "\n".join(f"- {t} -> {s}.html" for s, t in others)

    faqs = "\n".join(f"- {q}" for q, _ in topic.get("faqs", [])) or "(none supplied)"
    outline = "\n".join(f"- {s[0]}: {s[1]}" for s in topic.get("sections", [])) or "(decide yourself)"

    system = (
        "You write long-form SAP training articles for youronementor.com (theTechMentor). "
        "Return only the JSON object described by the schema.\n\n" + load_standards()
    )
    if mode == "refresh":
        task = (
            f"REWRITE an existing thin article into a complete, expert guide. Keep the same topic "
            f"and search intent. The URL slug must stay exactly '{fixed_slug}'.\n\n"
            f"Current headline: {topic['title']}\n"
            f"Current (thin) text, for reference only:\n{old_text[:4000]}\n"
        )
    else:
        task = (
            f"Write a NEW article.\n\nWorking title: {topic['title']}\n"
            f"Primary keyword: {topic.get('keyword', '')}\n"
            f"Target reader: {topic.get('role', 'SAP MM / EWM learners and consultants')}\n"
            f"Suggested outline (improve it freely):\n{outline}\n"
            f"Real Google 'People also ask' questions to answer in the FAQ:\n{faqs}\n"
            f"Do not duplicate an existing article; pick a distinct angle if the topic overlaps.\n"
        )
    user = (
        f"{task}\nToday's date: {datetime.date.today().isoformat()}.\n"
        f"Minimum {MIN_WORDS} words in intro + sections (aim for 1,800-2,500), "
        f"{MIN_SECTIONS}+ H2 sections, {MIN_FAQS}-8 FAQs, 4-6 key takeaways.\n\n"
        f"Existing articles you may link to (use the exact href):\n{post_list}\n"
    )

    last_problems = []
    for attempt in range(3):
        prompt = user
        if last_problems:
            prompt += "\n\nYour previous draft failed these checks. Fix all of them:\n- " + "\n- ".join(last_problems)
        if backend == "gemini":
            article = _request_gemini(system, prompt)
        elif backend == "claude-code":
            article = _request_claude_code(system, prompt)
        else:
            article = _request_article(client, system, prompt)
        article["slug"] = fixed_slug or slugify(article.get("slug") or article["h1"])
        article["intro_html"] = sanitize(article["intro_html"])
        for s in article["sections"]:
            s["heading"] = strip_tags(s["heading"])
            s["html"] = sanitize(s["html"])
        last_problems = quality_problems(article, taken, fixed_slug)
        if not last_problems:
            article["word_count"] = word_count(article)
            return article
    raise RuntimeError("Quality gate failed: " + "; ".join(last_problems))


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def _e(s: str) -> str:
    return html.escape(s or "", quote=True)


def related_posts(slug: str, h1: str, limit: int = 3) -> list:
    words = set(re.findall(r"[a-z0-9]{3,}", h1.lower())) - {"sap", "s4hana", "guide", "the", "and", "for", "with", "2026", "2027"}
    scored = []
    for s, t in existing_posts():
        if s == slug:
            continue
        overlap = len(words & set(re.findall(r"[a-z0-9]{3,}", t.lower())))
        scored.append((overlap, s, t))
    scored.sort(key=lambda x: -x[0])
    return [(s, t) for _, s, t in scored[:limit]]


def render_article(article: dict, published_iso: str = None) -> str:
    today = datetime.date.today()
    published_iso = published_iso or today.isoformat()
    published_human = datetime.date.fromisoformat(published_iso).strftime("%b %d, %Y")
    modified_iso = today.isoformat()
    slug = article["slug"]
    url = f"{SITE}/blog/{slug}.html"
    read_min = max(5, round(article.get("word_count", word_count(article)) / 220))

    toc = "".join(
        f'<li><a href="#sec-{i}">{_e(s["heading"])}</a></li>' for i, s in enumerate(article["sections"], 1)
    ) + '<li><a href="#faqs">Frequently asked questions</a></li>'

    sections = "".join(
        f'<h2 id="sec-{i}">{_e(s["heading"])}</h2>\n{s["html"]}\n' for i, s in enumerate(article["sections"], 1)
    )
    takeaways = "".join(f"<li>{_e(t)}</li>" for t in article.get("key_takeaways", []))
    faqs = "".join(
        f'<details class="ai-faq"><summary>{_e(f["question"])}</summary><p>{_e(f["answer"])}</p></details>'
        for f in article["faqs"]
    )
    related = "".join(
        f'<li><a href="{s}.html">{_e(t)}</a></li>' for s, t in related_posts(slug, article["h1"])
    )

    ld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article["h1"][:110],
            "description": article["meta_description"],
            "image": OG_IMAGE,
            "datePublished": published_iso,
            "dateModified": modified_iso,
            "author": {"@type": "Person", "name": "Anshuman Behuria",
                       "url": "https://www.linkedin.com/in/anshuman-behuria-946860130"},
            "publisher": {"@type": "Organization", "name": "theTechMentor", "url": SITE},
            "mainEntityOfPage": url,
            "wordCount": article.get("word_count", word_count(article)),
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": article["h1"][:110], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f["question"],
                 "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}}
                for f in article["faqs"]
            ],
        },
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
  <meta property="og:image" content="{OG_IMAGE}" />
  <meta property="og:site_name" content="theTechMentor" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta property="article:published_time" content="{published_iso}" />
  <meta property="article:modified_time" content="{modified_iso}" />
  <link rel="stylesheet" href="../styles.css?v=4" />
  <link rel="stylesheet" href="blog.css" />
  <link rel="stylesheet" href="ai-article.css" />
  <script type="application/ld+json">{ld_json}</script>
  <script src="../site-config.js"></script>
  <script src="../tracking.js"></script>
</head>
<body>
  <div class="reading-progress" id="reading-progress-bar"></div>
  <header class="header">
    <nav class="nav container">
      <a href="../index.html" class="logo"><span class="logo-mark">SAP</span><span class="logo-text">theTechMentor</span></a>
      <ul class="nav-links">
        <li><a href="../index.html#courses">Live Batches</a></li>
        <li><a href="../index.html#self-paced">Self-Paced</a></li>
        <li><a href="index.html">Blog</a></li>
        <li><a href="../index.html#pricing">Pricing</a></li>
        <li><a href="../index.html#enroll" class="btn btn-sm">Enroll Now</a></li>
      </ul>
    </nav>
  </header>

  <main class="blog-article-wrap">
    <nav class="blog-breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a> &gt; <a href="index.html">Blog</a> &gt; <span>{_e(article['category'])}</span>
    </nav>

    <header class="blog-header">
      <span class="sp-badge sp-badge--teal ai-badge">{_e(article['badge'])}</span>
      <h1 class="blog-title">{_e(article['h1'])}</h1>
      <div class="blog-meta">
        <div class="author-chip">
          <div class="author-avatar-ph">AB</div>
          <div class="author-info"><strong>Anshuman Behuria</strong><span>SAP MM &amp; EWM Consultant · 12+ yrs</span></div>
        </div>
        <span>•</span><span>Updated <time datetime="{modified_iso}">{today.strftime('%b %d, %Y')}</time></span>
        <span>•</span><span>⏱️ {read_min} min read</span>
      </div>
    </header>

    <article class="article-content ai-article">
      {article['intro_html']}

      <div class="ai-box ai-takeaways"><strong>Key takeaways</strong><ul>{takeaways}</ul></div>

      <nav class="ai-box ai-toc" aria-label="Contents"><strong>In this guide</strong><ol>{toc}</ol></nav>

      {sections}

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

      <h2 id="faqs">Frequently asked questions</h2>
      {faqs}

      <div class="ai-box"><strong>Related guides</strong><ul>{related}</ul></div>

      <div class="blog-course-cta">
        <h3>Learn SAP MM &amp; EWM hands-on with Anshuman Behuria</h3>
        <p>Live weekend batches or self-paced videos, with S/4HANA practice server access and interview preparation.</p>
        <div class="blog-cta-actions">
          <a href="../index.html#pricing" class="btn btn-primary">See programs &amp; fees</a>
          <a href="../index.html#enroll" class="btn btn-outline">Book a free 15-min call</a>
        </div>
      </div>
    </article>
  </main>

  <footer class="page-footer-lite">
    <a href="../privacy.html">Privacy</a> · <a href="../terms.html">Terms</a> · <a href="../refund.html">Refunds</a>
    <p>© {today.year} theTechMentor · Anshuman Behuria. SAP is a registered trademark of SAP SE; this site is not affiliated with SAP SE.</p>
  </footer>
  <script src="blog-leads.js"></script>
</body>
</html>
"""
