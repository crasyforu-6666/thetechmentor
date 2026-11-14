#!/usr/bin/env python3
"""Build digital-products.html from data/digital-products.json.

Product cards are rendered as static HTML (good for SEO); the same JSON is
embedded in the page for digital-products.js (pricing, modals, filters).
Phase 2: replace the JSON file with an API/DB export and re-run this script
(or have the Admin Panel call it after edits).

    python3 scripts/build_digital_products.py
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "digital-products.json")
OUT = os.path.join(ROOT, "digital-products.html")
e = lambda s: html.escape(str(s), quote=True)


def inr(n: int) -> str:
    s = str(n)
    if len(s) <= 3:
        return "₹" + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts) + "," + tail


ICONS = {"resumes": "📄", "interview": "🎯", "notes": "📘"}


def product_card(p, cat_label):
    free = p["price"] == 0
    badge = '<span class="dp-badge dp-free">FREE</span>' if free else f'<span class="dp-badge dp-paid">{inr(p["price"])}</span>'
    cta = ('<button type="button" class="btn btn-primary" data-dp-action="free">Download Free PDF</button>' if free
           else '<button type="button" class="btn btn-primary" data-dp-action="buy">Buy Now</button>')
    return f'''
        <article class="dp-card" data-id="{e(p['id'])}" data-category="{e(p['category'])}" data-free="{str(free).lower()}">
          <div class="dp-card-top">
            <span class="dp-icon" aria-hidden="true">{ICONS.get(p['category'], '📄')}</span>
            {badge}
          </div>
          <p class="dp-cat">{e(cat_label)}</p>
          <h3>{e(p['title'])}</h3>
          <p class="dp-summary">{e(p['summary'])}</p>
          <ul class="meta"><li>{e(p['format'])}</li><li>{e(p['pages'])} pages</li>{'<li>Instant access</li>' if free else '<li>Lifetime access</li>'}</ul>
          <div class="dp-actions">
            {cta}
            <button type="button" class="btn btn-ghost" data-dp-action="preview">Preview sample pages</button>
          </div>
        </article>'''


def build():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    cats = {c["id"]: c["label"] for c in data["categories"]}
    srv = data["server"]
    mod_opts = "".join(f'<option value="{e(m["id"])}">{e(m["label"])}</option>' for m in srv["modules"])
    dur_opts = "".join(
        f'<option value="{e(d["id"])}"{" selected" if d["id"] == "3m" else ""}>{e(d["label"])}{" — " + e(d["tag"]) if d["tag"] else ""}</option>'
        for d in srv["durations"])
    highlights = "".join(f"<li>{e(h)}</li>" for h in srv["highlights"])
    core, spec = srv["pricing"]["core"], srv["pricing"]["specialized"]
    def plan_list(tbl):
        return " · ".join(f"{d['label'].replace(' Access', '')}: {inr(tbl[d['id']])}" for d in srv["durations"])
    if core == spec:
        price_note = "All modules — " + plan_list(core)
    else:
        price_note = ("Core modules (MM, SD, FICO, ABAP, BASIS) — " + plan_list(core) +
                      "<br />EWM, TM &amp; Logistics — " + plan_list(spec))
    cards = "".join(product_card(p, cats[p["category"]]) for p in data["products"])
    tabs = "".join(f'<button type="button" class="chip" data-dp-filter="{e(c["id"])}">{e(c["label"])}</button>' for c in data["categories"])
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    ld = {
        "@context": "https://schema.org", "@type": "ItemList", "name": "SAP Digital Products & Practice Servers",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {
                "@type": "Product", "name": p["title"], "description": p["summary"], "brand": {"@type": "Brand", "name": "theTechMentor"},
                "offers": {"@type": "Offer", "price": str(p["price"]), "priceCurrency": "INR", "availability": "https://schema.org/InStock",
                           "url": f"https://youronementor.com/digital-products#{p['id']}"}}}
            for i, p in enumerate(data["products"])] + [
            {"@type": "ListItem", "position": len(data["products"]) + 1, "item": {
                "@type": "Product", "name": srv["title"], "description": "24/7 SAP S/4HANA practice server access for " + ", ".join(m["label"] for m in srv["modules"]),
                "brand": {"@type": "Brand", "name": "theTechMentor"},
                "offers": {"@type": "AggregateOffer", "lowPrice": str(min(core.values())), "highPrice": str(max(spec.values())), "priceCurrency": "INR"}}}],
    }
    ld_json = json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SAP Digital Products & S/4HANA Practice Servers | theTechMentor</title>
  <meta name="description" content="24/7 SAP S/4HANA practice servers for MM, SD, FICO, ABAP, BASIS, EWM, TM and Logistics, plus SAP resumes, interview Q&amp;A banks and configuration notes — free and paid PDFs." />
  <link rel="canonical" href="https://youronementor.com/digital-products" />
  <link rel="icon" href="images/logo-mark.svg" type="image/svg+xml" />
  <meta name="theme-color" content="#1d4ed8" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://youronementor.com/digital-products" />
  <meta property="og:title" content="SAP Digital Products & Practice Servers — theTechMentor" />
  <meta property="og:description" content="24/7 S/4HANA sandbox servers, SAP resumes, interview Q&amp;A banks and configuration blueprints." />
  <meta property="og:image" content="https://youronementor.com/images/og-cover.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" />
  <link rel="stylesheet" href="site.css?v=7" />
  <script type="application/ld+json">{ld_json}</script>
  <script src="site-config.js"></script>
  <script src="tracking.js"></script>
</head>
<body class="dp-page">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="header" id="top">
    <nav class="nav wrap" aria-label="Main">
      <a href="index.html" class="brand" aria-label="theTechMentor home"><img src="images/logo-mark.svg" alt="" width="36" height="36" /><span>the<b>Tech</b>Mentor</span></a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <ul class="nav-links">
        <li><a href="index.html#courses">Courses</a></li>
        <li><a href="digital-products" aria-current="page">Digital Products</a></li>
        <li><a href="index.html#paths">Career paths</a></li>
        <li><a href="blog/index.html">Blog</a></li>
        <li><a href="index.html#advisor" class="btn btn-ghost btn-sm">Free counselling</a></li>
        <li><a href="index.html#courses" class="btn btn-primary btn-sm">Explore courses</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="dp-hero">
      <div class="wrap">
        <span class="dp-hero-badge">SAP S/4HANA Resources &amp; Practice Systems</span>
        <h1>SAP Digital Products &amp; Practice Servers</h1>
        <p class="lead">Get instant access to 24/7 S/4HANA sandbox servers, real-time SAP resumes, interview Q&amp;A banks, and configuration blueprints.</p>
      </div>
    </section>

    <section class="section dp-section">
      <div class="wrap">
        <div class="dp-filters" role="toolbar" aria-label="Filter products">
          <div class="filters">
            <button type="button" class="chip active" data-dp-filter="all">All Products</button>
            <button type="button" class="chip" data-dp-filter="servers">SAP Practice Servers</button>
            {tabs}
          </div>
          <label class="dp-switch"><input type="checkbox" id="dp-free-only" /><span class="dp-switch-ui" aria-hidden="true"></span> Free Only</label>
        </div>

        <!-- Featured: practice server -->
        <article class="dp-server" id="{e(srv['id'])}" data-category="servers" data-free="false">
          <div class="dp-server-copy">
            <span class="tag tag-live">Most requested</span>
            <h2>{e(srv['title'])}</h2>
            <p class="sub">Practise every configuration and transaction on your own S/4HANA system — any module, any time.</p>
            <ul class="ticks">{highlights}</ul>
            <p class="dp-table-note">{price_note}</p>
          </div>
          <div class="dp-server-box">
            <div class="form-row"><label for="dp-module">Select SAP module</label><select id="dp-module">{mod_opts}</select></div>
            <div class="form-row"><label for="dp-duration">Select duration</label><select id="dp-duration">{dur_opts}</select></div>
            <div class="dp-price-box">
              <div><span class="dp-price" id="dp-price">—</span> <s class="muted" id="dp-was"></s></div>
              <p class="dp-price-meta" id="dp-price-meta"></p>
              <span class="tag tag-save" id="dp-save" hidden></span>
            </div>
            <ul class="dp-included" id="dp-included"></ul>
            <button type="button" class="btn btn-primary btn-block dp-order" data-dp-action="server">Order Server Access</button>
            <p class="fineprint">Digital product · all sales final · credentials on WhatsApp &amp; email</p>
          </div>
        </article>

        <div class="dp-grid" id="dp-grid">{cards}
        </div>
        <p class="no-results" id="dp-empty" hidden>No products match this filter.</p>
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap cta-inner">
        <div><h2>Want guided learning instead?</h2><p>Recorded courses from ₹4,999 and live mentored batches from ₹29,999.</p></div>
        <div class="cta-actions"><a href="index.html#courses" class="btn btn-white">Explore courses</a><a href="index.html#advisor" class="btn btn-outline-white">Free counselling</a></div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="wrap footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="brand brand-light"><img src="images/logo-mark.svg" alt="" width="32" height="32" /><span>the<b>Tech</b>Mentor</span></a>
        <p>Online SAP S/4HANA academy for logistics, procurement and warehouse careers.</p>
      </div>
      <div><h4>Courses</h4><ul><li><a href="index.html#recorded">Recorded Sessions</a></li><li><a href="index.html#live">Live Mentored Sessions</a></li><li><a href="index.html#paths">Career paths</a></li></ul></div>
      <div><h4>Resources</h4><ul><li><a href="digital-products">Digital Products</a></li><li><a href="blog/index.html">Blog</a></li><li><a href="index.html#faq">FAQ</a></li><li><a href="index.html#advisor">Free counselling</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="mailto:info@youronementor.com">info@youronementor.com</a></li><li><a href="https://wa.me/917848942021" target="_blank" rel="noopener noreferrer">WhatsApp +91 78489 42021</a></li></ul></div>
      <div><h4>Legal</h4><ul><li><a href="privacy.html">Privacy policy</a></li><li><a href="terms.html">Terms</a></li><li><a href="refund.html">Refunds</a></li></ul></div>
    </div>
    <div class="wrap footer-bottom"><p>© 2026 theTechMentor. SAP and S/4HANA are trademarks of SAP SE; theTechMentor is not affiliated with SAP SE.</p></div>
    <div class="footer-wordmark" aria-hidden="true"><img src="images/footer-wordmark.webp?v=3" alt="" width="2000" height="306" loading="lazy" /></div>
  </footer>

  <!-- Unlock / order modal (shared) -->
  <div class="modal-backdrop" id="dp-modal" hidden>
    <div class="modal-card dp-modal" role="dialog" aria-modal="true" aria-labelledby="dp-modal-title">
      <button type="button" class="modal-close" data-dp-close aria-label="Close">×</button>
      <div id="dp-modal-body">
        <p class="eyebrow" id="dp-modal-kind"></p>
        <h3 id="dp-modal-title"></h3>
        <div class="dp-summary-box" id="dp-modal-summary"></div>
        <form id="dp-form" novalidate>
          <div class="form-row"><label for="dp-name">Full name *</label><input id="dp-name" name="name" required autocomplete="name" placeholder="Your name" /></div>
          <div class="form-row"><label for="dp-email">Email *</label><input id="dp-email" name="email" type="email" required autocomplete="email" placeholder="you@email.com" /></div>
          <div class="form-row"><label for="dp-phone">WhatsApp number *</label><input id="dp-phone" name="phone" type="tel" required autocomplete="tel" inputmode="tel" placeholder="+91 98765 43210" pattern="[+0-9 ()-]{{8,}}" /></div>
          <button type="submit" class="btn btn-primary btn-block" id="dp-submit"></button>
          <p class="fineprint" id="dp-fineprint"></p>
        </form>
      </div>
      <div id="dp-modal-done" hidden></div>
    </div>
  </div>

  <!-- Preview drawer -->
  <div class="modal-backdrop" id="dp-preview" hidden>
    <aside class="dp-drawer" role="dialog" aria-modal="true" aria-labelledby="dp-preview-title">
      <button type="button" class="modal-close" data-dp-close aria-label="Close">×</button>
      <p class="eyebrow">Preview · table of contents</p>
      <h3 id="dp-preview-title"></h3>
      <p class="muted" id="dp-preview-meta"></p>
      <ol class="dp-toc" id="dp-preview-list"></ol>
      <div class="dp-preview-cta" id="dp-preview-cta"></div>
    </aside>
  </div>

  <script type="application/json" id="dp-data">{payload}</script>
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
  <script src="script.js?v=8" defer></script>
  <script src="digital-products.js?v=1" defer></script>
</body>
</html>
'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {os.path.relpath(OUT, ROOT)} ({len(data['products'])} products)")


if __name__ == "__main__":
    build()
