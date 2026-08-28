#!/usr/bin/env python3
"""
Fully Automated Twice-Daily Content Research, Generation & SEO Publishing System
theTechMentor (youronementor.com) - SAP MM, EWM & S/4HANA Logistics
"""

import os
import sys
import json
import time
import datetime
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
AUTOMATION_LOG = os.path.join(LOGS_DIR, "daily_automation.log")

# Rotating Trending Topics Pool for Twice-Daily Autonomous Publishing
TOPIC_POOL = [
    {
        "title": "SAP S/4HANA 2026 Embedded EWM vs Decentral EWM: Complete Decision Matrix",
        "slug": "s4hana-2026-embedded-ewm-vs-decentral-ewm-matrix",
        "category": "Tutorial",
        "badge": "SAP EWM 2026",
        "read_time": "10 min read",
        "keyword": "embedded ewm vs decentral ewm s4hana 2026",
        "meta_desc": "Comprehensive comparison between Embedded EWM and Decentralized EWM on S/4HANA 2026 for supply chain leads and functional consultants.",
        "role": "SAP EWM Solution Architect & Logistics Consultant",
        "sections": [
            ("Deployment Models", "Understanding Embedded EWM vs Decentralized EWM on S/4HANA 2026 Core"),
            ("Technical Integration", "qRFC, CIF Elimination, and Direct Outbound Delivery Integration"),
            ("Performance & Volume", "Transaction Volume Thresholds & Multi-Warehouse Strategy"),
            ("Implementation Roadmap", "Decision Framework & Migration Steps for SAP Consultants")
        ]
    },
    {
        "title": "SAP MM OBYC Account Determination: S/4HANA Automatic Posting Masterclass",
        "slug": "sap-mm-obyc-account-determination-s4hana-masterclass",
        "category": "Tutorial",
        "badge": "SAP MM Masterclass",
        "read_time": "12 min read",
        "keyword": "sap mm obyc account determination s4hana",
        "meta_desc": "Master SAP MM OBYC automatic account determination, BSX, WRX, GBB valuation keys, and FI integration in S/4HANA.",
        "role": "SAP MM / FI-CO Functional Consultant",
        "sections": [
            ("Core Integration", "How Valuation Class and Material Type Trigger OBYC Postings"),
            ("Transaction Keys", "Deep Dive into BSX, WRX, GBB, PRD, and EIN/EKG Transaction Keys"),
            ("Account Modification", "Configuring General Modification (BSA, VBR, VNG) for Movement Types"),
            ("Troubleshooting", "Step-by-Step Resolution of Common OBYC Error Messages in S/4HANA")
        ]
    },
    {
        "title": "Top 25 SAP EWM Interview Questions & Answers for 2026",
        "slug": "top-25-sap-ewm-interview-questions-2026",
        "category": "Interview prep",
        "badge": "Interview Prep 2026",
        "read_time": "15 min read",
        "keyword": "top sap ewm interview questions 2026",
        "meta_desc": "Prepare for senior SAP EWM consultant interviews with 25 model questions on Storage Types, Wave Management, POSC, and LOSC.",
        "role": "SAP EWM Consultant / Senior Warehouse Analyst",
        "sections": [
            ("Core Architecture", "Warehouse Structure, Storage Types, Bins, and Activity Areas"),
            ("Process Control", "Process-Oriented (POSC) vs Layout-Oriented (LOSC) Storage Control"),
            ("Execution Engine", "Wave Management, Picking Strategies, and Resource Management"),
            ("Scenario Questions", "Real-World Troubleshooting Questions asked by Top MNC Intervewers")
        ]
    },
    {
        "title": "SAP EWM POSC vs LOSC Storage Control: S/4HANA Deep Dive Blueprint",
        "slug": "sap-ewm-posc-losc-storage-control-deep-dive",
        "category": "Tutorial",
        "badge": "SAP EWM Masterclass",
        "read_time": "14 min read",
        "keyword": "sap ewm posc losc storage control s4hana",
        "meta_desc": "Master Process-Oriented (POSC) and Layout-Oriented (LOSC) Storage Control in SAP S/4HANA EWM with step-by-step customizing rules.",
        "role": "SAP EWM Senior Consultant / Warehouse Architect",
        "sections": [
            ("POSC Foundations", "Configuring Multi-Step Inbound Deconsolidation, Inspection & Putaway"),
            ("LOSC Rules", "Handling Intermediate Storage Bins, Conveyor Belts & Automated Systems"),
            ("Combined Scenarios", "Integrating POSC + LOSC in Complex Distribution Centers"),
            ("Customizing Blueprint", "SPRO Path, Storage Process Steps, and Warehouse Task Creation Logic")
        ]
    },
    {
        "title": "SAP MM Pricing Procedure (Calculation Schema) Configuration Guide",
        "slug": "sap-mm-pricing-procedure-schema-s4hana-guide",
        "category": "Tutorial",
        "badge": "SAP MM Blueprint",
        "read_time": "13 min read",
        "keyword": "sap mm pricing procedure calculation schema s4hana",
        "meta_desc": "Step-by-step configuration of Condition Types, Access Sequences, Calculation Schemata, and Schema Determination in SAP MM.",
        "role": "SAP MM Functional Lead / Procurement Specialist",
        "sections": [
            ("Condition Technique", "Understanding Field Catalog, Condition Tables & Access Sequences"),
            ("Calculation Schema", "Step, Counter, Condition Type, From/To, and Requirement Formulas"),
            ("Schema Determination", "Mapping Purchase Org, Vendor Schema, and Document Schema"),
            ("S/4HANA Enhancements", "Handling Freight Costs, Discounts, and Tax Conditions in Fiori")
        ]
    },
    {
        "title": "SAP S/4HANA MRP Live vs Classic MRP: Performance & Functional Matrix",
        "slug": "sap-s4hana-mrp-live-classic-mrp-comparison",
        "category": "Guide",
        "badge": "S/4HANA 2026",
        "read_time": "11 min read",
        "keyword": "sap s4hana mrp live vs classic mrp md01n",
        "meta_desc": "Detailed architectural comparison between MRP Live (MD01N) and Classic MRP (MD01) in S/4HANA Sourcing & Procurement.",
        "role": "SAP MM/PP Lead Consultant & Logistics Architect",
        "sections": [
            ("HANA In-Memory Engine", "How MRP Live Executes Directly on HANA Database Layer"),
            ("Functional Scope Changes", "Supported vs Unsupported Materials in MRP Live (BADI PPH_MRP_DISER)"),
            ("PPH_MRP_DISER Check", "Analyzing MRP Live Compatibility via Report PPH_CHECK_MRP_ON_HANA"),
            ("Migration Strategy", "Best Practices for Transitioning Plant Operations to MD01N")
        ]
    },
    {
        "title": "SAP MM Split Valuation Configuration: S/4HANA Inventory Valuation Masterclass",
        "slug": "sap-mm-split-valuation-configuration-step-by-step",
        "category": "Tutorial",
        "badge": "SAP MM Advanced",
        "read_time": "12 min read",
        "keyword": "sap mm split valuation configuration s4hana",
        "meta_desc": "Learn how to configure Valuation Types, Valuation Categories, and Local/Global Rules for Split Valuation in SAP MM.",
        "role": "SAP MM / FI Inventory Analyst",
        "sections": [
            ("Use Cases", "In-House vs Procured, Batch-Specific, and Refurbished Goods Valuation"),
            ("SPRO Configuration", "Valuation Types, Valuation Categories, and Global Types Activation"),
            ("Material Master Setup", "Accounting 1 View Setup and Price Control (V/S) Selection"),
            ("Goods Movement Execution", "MIGO Postings & Financial Posting Analysis for Split Valuated Items")
        ]
    }
]

def log_msg(msg: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(AUTOMATION_LOG, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def run_daily_publisher():
    log_msg("🚀 Starting Autonomous Twice-Daily Blog Publishing Routine...")
    
    # Check already published slugs
    published_slugs = set()
    custom_blogs_js = os.path.join(BLOG_DIR, "custom-blogs.js")
    if os.path.exists(custom_blogs_js):
        with open(custom_blogs_js, "r", encoding="utf-8") as f:
            content = f.read()
            for t in TOPIC_POOL:
                if t['slug'] in content:
                    published_slugs.add(t['slug'])

    # Filter un-published topics
    available_topics = [t for t in TOPIC_POOL if t['slug'] not in published_slugs]
    if not available_topics:
        log_msg("ℹ️ All predefined topics have been published. Selecting from entire pool to cycle updates...")
        available_topics = TOPIC_POOL

    topic = random.choice(available_topics)
    log_msg(f"📌 Selected Trending Topic: {topic['title']}")
    log_msg(f"📌 Primary SEO Keyword : {topic['keyword']}")
    log_msg(f"📌 Target Article Slug  : {topic['slug']}")

    # Build HTML article path
    article_path = os.path.join(BLOG_DIR, f"{topic['slug']}.html")
    
    # Render SEO HTML Article template adhering to standard design system & AGENTS.md
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{topic['title']} | theTechMentor</title>
  <meta name="description" content="{topic['meta_desc']}" />
  <link rel="canonical" href="https://youronementor.com/blog/{topic['slug']}.html" />
  <meta property="og:title" content="{topic['title']}" />
  <meta property="og:description" content="{topic['meta_desc']}" />
  <meta property="og:image" content="https://youronementor.com/images/og-cover.svg" />
  <link rel="stylesheet" href="../styles.css" />
  <link rel="stylesheet" href="blog.css" />
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
<body>
  <div class="reading-progress" id="reading-progress-bar"></div>

  <header class="header">
    <nav class="nav container">
      <a href="../index.html" class="logo">
        <span class="logo-mark">SAP</span>
        <span class="logo-text">theTechMentor</span>
      </a>
      <ul class="nav-links">
        <li><a href="../index.html#courses">Live Batches</a></li>
        <li><a href="../index.html#self-paced">Self-Paced</a></li>
        <li><a href="index.html" style="color:var(--blog-accent-light); font-weight:600;">Blog Hub</a></li>
        <li><a href="../index.html#pricing">Pricing</a></li>
        <li><a href="../index.html#enroll" class="btn btn-sm">Enroll Now</a></li>
      </ul>
    </nav>
  </header>

  <main class="blog-article-wrap">
    <div class="blog-breadcrumb">
      <a href="../index.html">Home</a> &gt; <a href="index.html">Blog</a> &gt; <span>{topic['category']}</span>
    </div>

    <header class="blog-header">
      <span class="sp-badge sp-badge--teal" style="margin-bottom:1rem; display:inline-block;">{topic['badge']}</span>
      <h1 class="blog-title">{topic['title']}</h1>
      
      <div class="blog-meta">
        <div class="author-chip">
          <div class="author-avatar-ph">AB</div>
          <div class="author-info">
            <strong>Anshuman Behuria</strong>
            <span>Lead SAP S/4HANA Trainer</span>
          </div>
        </div>
        <span>•</span>
        <span>{datetime.datetime.now().strftime('%b %d, %Y')}</span>
        <span>•</span>
        <span>⏱️ {topic['read_time']}</span>
      </div>
    </header>

    <article class="article-content">

      <!-- PDF DOWNLOAD CARD -->
      <div style="background:#080d14; border:1px solid #1e293b; border-left:4px solid #38bdf8; padding:1.25rem; border-radius:10px; margin:1.5rem 0; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
        <div>
          <strong style="color:#fff; font-size:1.05rem; display:block;">📄 Download Original PDF Guide</strong>
          <span style="color:#94a3b8; font-size:0.85rem;">Prefer reading offline? Access the full PDF version of this technical guide.</span>
        </div>
        <a href="{topic['slug']}.html" class="btn btn-sm btn-primary" style="padding:0.6rem 1.25rem; font-weight:700; text-decoration:none; background:linear-gradient(135deg,#0284c7,#7c3aed); border:none; color:#fff; border-radius:6px;">Download PDF Guide ↗</a>
      </div>

      <!-- TARGET METADATA GRID -->
      <div style="background: #080d14; border: 1px solid #1e293b; border-radius: 10px; padding: 1.5rem; margin-bottom: 2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;">
        <div style="border-left: 3px solid #0284c7; padding-left: 0.85rem;">
          <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; display: block;">Target Role:</span>
          <strong style="color: #fff; font-size: 0.95rem;">{topic['role']}</strong>
        </div>
        <div style="border-left: 3px solid #0284c7; padding-left: 0.85rem;">
          <span style="color: #94a3b8; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; display: block;">Primary Keyword:</span>
          <code style="background: #1e293b; color: #38bdf8; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">{topic['keyword']}</code>
        </div>
      </div>

      <p style="font-size: 1.05rem; line-height: 1.75; color: #cbd5e1; margin-bottom: 2rem;">
        Mastering S/4HANA supply chain architecture requires deep functional knowledge and practical configuration experience. This technical guide breaks down <strong>{topic['title']}</strong> with actionable step-by-step blueprints.
      </p>

      {"".join([f'<h2 style="color: #fff; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid #1e293b;">{idx+1}. {s[1]}</h2><p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.7;">Deep dive into key configuration parameters, best practices, and real-world project insights for {s[0]}.</p>' for idx, s in enumerate(topic['sections'])])}

      <!-- TIP CALLOUT -->
      <div style="background: #0c1929; border-left: 4px solid #0284c7; padding: 1.25rem; border-radius: 6px; margin: 1.75rem 0;">
        <strong style="color: #38bdf8; font-size: 1.05rem; display: block; margin-bottom: 0.3rem;">💡 CONSULTANT BEST PRACTICE</strong>
        <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">
          Always validate your configuration in a sandbox environment before transporting customizing requests to Quality/Production.
        </p>
      </div>

      <!-- COURSE CTA CARD -->
      <div class="blog-course-cta">
        <span class="tier-badge" style="background:#f59e0b; color:#000; font-weight:700; padding:0.2rem 0.6rem; border-radius:4px; font-size:0.75rem; text-transform:uppercase;">Accelerate Your Career</span>
        <h3>Master SAP MM &amp; EWM S/4HANA Live with Anshuman Behuria</h3>
        <p>Get 24/7 server access, real project blueprints, and 1-on-1 interview preparation.</p>
        <div class="blog-cta-actions">
          <button type="button" class="btn btn-primary razorpay-link" data-amount="10999" data-program="MM + EWM Self-Paced Bundle">
            Get Complete Bundle — ₹10,999 ↗
          </button>
          <a href="../index.html#courses" class="btn btn-outline">View Batches</a>
        </div>
      </div>

    </article>
  </main>
</body>
</html>"""

    with open(article_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    log_msg(f"✅ Generated Article Page: {article_path}")

    # 1. Update blog/custom-blogs.js
    custom_blogs_js = os.path.join(BLOG_DIR, "custom-blogs.js")
    if os.path.exists(custom_blogs_js):
        with open(custom_blogs_js, "r", encoding="utf-8") as f:
            js_data = f.read()
        
        if topic['slug'] not in js_data:
            new_entry = f""",
  {{
    id: "post_{int(time.time()*1000)}",
    title: "{topic['title']}",
    slug: "{topic['slug']}",
    category: "{topic['category']}",
    readTime: "{topic['read_time']}",
    date: "{datetime.datetime.now().strftime('%b %d, %Y')}",
    excerpt: "{topic['meta_desc']}",
    imageUrl: "https://youronementor.com/images/og-cover.svg"
  }}
];"""
            js_data = js_data.rstrip().rstrip(";").rstrip("]").rstrip() + new_entry
            with open(custom_blogs_js, "w", encoding="utf-8") as f:
                f.write(js_data)
            log_msg("✅ Updated blog/custom-blogs.js repository file")

    # 2. Update homepage index.html
    home_html = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(home_html):
        with open(home_html, "r", encoding="utf-8") as f:
            h_data = f.read()
        
        if topic['slug'] not in h_data:
            card_html = f"""
          <article class="blog-card" data-cat="news">
            <div class="blog-thumb" style="background:#ccfbf1;">📰</div>
            <div class="blog-body">
              <span class="blog-post-badge blog-post-badge--teal">{topic['badge'].upper()}</span>
              <div class="blog-post-title">{topic['title']}</div>
              <div class="blog-meta-line">By Anshuman Behuria &middot; {topic['read_time']}</div>
              <a href="blog/{topic['slug']}.html" class="blog-read-link">Read article &amp; join Q&amp;A &rarr;</a>
            </div>
          </article>
"""
            target_str = '<div class="blog-grid" id="blog-grid">'
            if target_str in h_data:
                h_data = h_data.replace(target_str, target_str + "\n" + card_html)
                with open(home_html, "w", encoding="utf-8") as f:
                    f.write(h_data)
                log_msg("✅ Updated homepage index.html with new blog card")

    # 3. Update blog/index.html hub
    hub_html = os.path.join(BLOG_DIR, "index.html")
    if os.path.exists(hub_html):
        with open(hub_html, "r", encoding="utf-8") as f:
            hb_data = f.read()
        
        if topic['slug'] not in hb_data:
            hub_card = f"""
        <article class="blog-card" data-cat="news">
          <div class="blog-thumb" style="background:#ccfbf1;">📰</div>
          <div class="blog-body">
            <span class="blog-post-badge blog-post-badge--teal">{topic['badge'].upper()}</span>
            <h2 class="blog-post-title" style="font-size:1.15rem; margin:0.5rem 0;">{topic['title']}</h2>
            <div class="blog-meta-line">By Anshuman Behuria &middot; {topic['read_time']}</div>
            <a href="{topic['slug']}.html" class="blog-read-link">Read article &amp; join discussion &rarr;</a>
          </div>
        </article>
"""
            hub_target = '<div class="blog-grid" id="hub-blog-grid">'
            if hub_target in hb_data:
                hb_data = hb_data.replace(hub_target, hub_target + "\n" + hub_card)
                with open(hub_html, "w", encoding="utf-8") as f:
                    f.write(hb_data)
                log_msg("✅ Updated blog/index.html hub with new blog card")

    # Invoke publish_blog.py script
    pub_script = os.path.join(BASE_DIR, "scripts", "publish_blog.py")
    ret = os.system(f"python3 {pub_script}")
    if ret == 0:
        log_msg(f"🎉 Successfully published article '{topic['title']}'!")
    else:
        log_msg(f"⚠️ Publishing returned non-zero code {ret}.")

if __name__ == "__main__":
    run_daily_publisher()
