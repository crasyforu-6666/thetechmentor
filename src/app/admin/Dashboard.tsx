"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { admin as t, brand } from "@/content/site";

/* ---------- API shape ---------- */
type Card = { value: number; change: number | null; series: number[] };
type Api = {
  configured: boolean;
  missing: string[];
  generatedAt: string;
  rangeDays: number;
  gaError?: string;
  razorpayError?: string;
  ga?: {
    days: string[];
    cards: { visitors: Card; signups: Card; paidUsers: Card; revenue: Card };
    traffic: {
      sessions: number;
      pageViews: number;
      sessionsSeries: number[];
      sources: { name: string; sessions: number; users: number }[];
      pages: { path: string; views: number; users: number }[];
    };
    events: Record<string, { count: number; users: number; change: number | null }>;
    modules: { name: string; count: number }[] | null;
  };
  razorpay?: {
    payments: number;
    paidUsers: number;
    revenue: number;
    series: number[];
    recent: { id: string; amount: number; at: number; method: string; description: string }[];
  };
};

const KEY = "ttm_admin_key";
const nf = (n: number) => Math.round(n).toLocaleString("en-IN");
const inr = (n: number) => "₹" + Math.round(n).toLocaleString("en-IN");
const dayLabel = (d: string) =>
  new Date(`${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}T00:00:00`).toLocaleDateString("en-IN", { day: "numeric", month: "short" });

/* ---------- Charts ---------- */
function Sparkline({ series }: { series: number[] }) {
  const w = 200, h = 44, max = Math.max(1, ...series);
  const pts = series.map((v, i) => `${(i / Math.max(1, series.length - 1)) * w},${h - 4 - (v / max) * (h - 8)}`).join(" ");
  return (
    <svg className="adm-spark" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" aria-hidden="true">
      <polyline points={pts} fill="none" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}

function LineChart({ series, days, label }: { series: number[]; days: string[]; label: string }) {
  const [hover, setHover] = useState<number | null>(null);
  const ref = useRef<SVGSVGElement>(null);
  const w = 720, h = 220, padL = 36, padB = 26, padT = 12;
  const max = Math.max(1, ...series);
  const nice = Math.ceil(max / 4) * 4 || 4;
  const x = (i: number) => padL + (i / Math.max(1, series.length - 1)) * (w - padL - 8);
  const y = (v: number) => padT + (1 - v / nice) * (h - padT - padB);
  const path = series.map((v, i) => `${i ? "L" : "M"}${x(i)},${y(v)}`).join(" ");
  const area = `${path} L${x(series.length - 1)},${y(0)} L${x(0)},${y(0)} Z`;
  const onMove = (e: React.PointerEvent) => {
    const r = ref.current!.getBoundingClientRect();
    const px = ((e.clientX - r.left) / r.width) * w;
    const i = Math.round(((px - padL) / (w - padL - 8)) * (series.length - 1));
    setHover(Math.max(0, Math.min(series.length - 1, i)));
  };
  return (
    <div className="adm-chart">
      <svg ref={ref} viewBox={`0 0 ${w} ${h}`} role="img" aria-label={label} onPointerMove={onMove} onPointerLeave={() => setHover(null)}>
        {[0, 1, 2, 3, 4].map((g) => (
          <g key={g}>
            <line x1={padL} x2={w - 8} y1={y((nice / 4) * g)} y2={y((nice / 4) * g)} className="adm-grid" />
            <text x={padL - 6} y={y((nice / 4) * g) + 4} className="adm-axis" textAnchor="end">{nf((nice / 4) * g)}</text>
          </g>
        ))}
        {days.map((d, i) => ((i % 7 === 0 && i <= days.length - 4) || i === days.length - 1 ? <text key={d} x={x(i)} y={h - 6} className="adm-axis" textAnchor="middle">{dayLabel(d)}</text> : null))}
        <path d={area} className="adm-area" />
        <path d={path} className="adm-line" />
        {hover !== null && (
          <g>
            <line x1={x(hover)} x2={x(hover)} y1={padT} y2={y(0)} className="adm-cross" />
            <circle cx={x(hover)} cy={y(series[hover])} r="5" className="adm-dot" />
          </g>
        )}
      </svg>
      {hover !== null && (
        <div className="adm-tip" style={{ left: `${(x(hover) / w) * 100}%` }}>
          <strong>{nf(series[hover])}</strong> {label.toLowerCase()}
          <span>{dayLabel(days[hover])}</span>
        </div>
      )}
    </div>
  );
}

function Bars({ rows, valueLabel }: { rows: { name: string; value: number }[]; valueLabel: string }) {
  if (!rows.length) return <p className="adm-empty">{t.noData}</p>;
  const max = Math.max(1, ...rows.map((r) => r.value));
  return (
    <ul className="adm-bars">
      {rows.map((r) => (
        <li key={r.name} title={`${r.name}: ${nf(r.value)} ${valueLabel.toLowerCase()}`}>
          <span className="adm-bar-name">{r.name}</span>
          <span className="adm-bar-track"><span className="adm-bar-fill" style={{ width: `${(r.value / max) * 100}%` }} /></span>
          <span className="adm-bar-val">{nf(r.value)}</span>
        </li>
      ))}
    </ul>
  );
}

function Change({ v }: { v: number | null }) {
  if (v === null || !isFinite(v)) return null;
  const up = v >= 0;
  return <span className={`adm-change ${up ? "up" : "down"}`}>{up ? "↑" : "↓"}{Math.abs(v)}%</span>;
}

/* ---------- Page ---------- */
export default function Dashboard() {
  const [key, setKey] = useState<string | null>(null);
  const [pw, setPw] = useState("");
  const [data, setData] = useState<Api | null>(null);
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const [now, setNow] = useState(Date.now());
  const [active, setActive] = useState("home");

  const load = useCallback(async (k: string) => {
    setLoading(true);
    setErr("");
    try {
      const r = await fetch("/api/dashboard", { headers: { "x-admin-key": k }, cache: "no-store" });
      const j = await r.json().catch(() => ({}));
      if (r.status === 401) {
        try { sessionStorage.removeItem(KEY); } catch {}
        setKey(null);
        setErr(t.wrongPassword);
        return;
      }
      if (r.status === 503) { setData(j as Api); setKey(k); return; }
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setData(j as Api);
      setKey(k);
      try { sessionStorage.setItem(KEY, k); } catch {}
    } catch (e) {
      setErr(String((e as Error).message || e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let saved: string | null = null;
    try { saved = sessionStorage.getItem(KEY); } catch {}
    if (saved) load(saved);
  }, [load]);

  useEffect(() => {
    const tick = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(tick);
  }, []);
  useEffect(() => {
    if (!key) return;
    const auto = setInterval(() => load(key), 5 * 60 * 1000);
    return () => clearInterval(auto);
  }, [key, load]);

  const ago = data?.generatedAt ? Math.max(0, Math.round((now - new Date(data.generatedAt).getTime()) / 1000)) : 0;
  const ga = data?.ga;
  const rp = data?.razorpay;

  const cards = useMemo(() => {
    if (!ga) return [];
    return [
      { id: "visitors", label: t.cards.visitors, value: nf(ga.cards.visitors.value), c: ga.cards.visitors },
      { id: "signups", label: t.cards.signups, value: nf(ga.cards.signups.value), c: ga.cards.signups },
      rp
        ? { id: "paid", label: t.cards.paidUsers, value: nf(rp.paidUsers), c: { value: rp.paidUsers, change: null, series: rp.series } }
        : { id: "paid", label: t.cards.paidUsers, value: nf(ga.cards.paidUsers.value), c: ga.cards.paidUsers },
      rp
        ? { id: "rev", label: t.cards.revenue, value: inr(rp.revenue), c: { value: rp.revenue, change: null, series: rp.series } }
        : { id: "rev", label: t.cards.revenue, value: inr(ga.cards.revenue.value), c: ga.cards.revenue },
    ];
  }, [ga, rp]);

  const go = (id: string) => {
    setActive(id);
    document.getElementById(`adm-${id}`)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  /* ----- login ----- */
  if (!key) {
    return (
      <div className="adm adm-login-wrap">
        <form
          className="adm-login"
          onSubmit={(e) => {
            e.preventDefault();
            if (pw) load(pw);
          }}
        >
          <img src={brand.logo} alt="" width={44} height={44} />
          <h1>{t.loginTitle}</h1>
          <p>{t.loginSub}</p>
          <label htmlFor="adm-pw">{t.passwordLabel}</label>
          <input id="adm-pw" type="password" autoComplete="current-password" value={pw} onChange={(e) => setPw(e.target.value)} autoFocus />
          {err && <p className="adm-err" role="alert">{err}</p>}
          <button type="submit" disabled={loading || !pw}>{loading ? "…" : t.loginButton}</button>
        </form>
      </div>
    );
  }

  const ev = ga?.events || {};
  const signupRows = ["whatsapp_batch_click", "lead"].map((n) => ({ name: t.eventLabels[n], value: ev[n]?.count || 0 }));
  const productRows = ["product_page_view", "free_document_open", "share_click", "begin_checkout"].map((n) => ({ name: t.eventLabels[n], value: ev[n]?.count || 0 }));

  return (
    <div className="adm">
      <aside className="adm-side">
        <a className="adm-brand" href="/" aria-label={brand.homeLabel}>
          <img src={brand.logo} alt="" width={30} height={30} />
          <span>{brand.pre}<b>{brand.bold}</b>{brand.post}</span>
        </a>
        <nav>
          {t.nav.map((n) => (
            <button key={n.id} className={active === n.id ? "on" : ""} onClick={() => go(n.id)}>
              <span aria-hidden="true">{n.icon}</span>{n.label}
            </button>
          ))}
        </nav>
        <button
          className="adm-logout"
          onClick={() => {
            try { sessionStorage.removeItem(KEY); } catch {}
            setKey(null);
            setData(null);
            setPw("");
          }}
        >
          {t.logout}
        </button>
      </aside>

      <main className="adm-main">
        <header className="adm-top" id="adm-home">
          <p>{t.tagline}</p>
          <button className="adm-refresh" onClick={() => load(key)} disabled={loading}>{loading ? "…" : `↻ ${t.refresh}`}</button>
        </header>

        {data?.missing?.includes("ADMIN_PASSWORD") && <div className="adm-box adm-warn">{t.passwordMissing}</div>}
        {err && <div className="adm-box adm-warn">{err}</div>}
        {data?.gaError && (
          <div className="adm-box adm-warn"><strong>{t.gaErrorTitle}:</strong> {data.gaError}</div>
        )}

        <h2 className="adm-h">{t.rangeLabel}</h2>
        {ga ? (
          <div className="adm-cards">
            {cards.map((c) => (
              <div className="adm-card" key={c.id}>
                <div className="adm-card-top">
                  <span>{c.label}</span>
                  <small>🕒 {t.updated(ago)}</small>
                </div>
                <div className="adm-card-val">{c.value}<Change v={c.c.change} /></div>
                <Sparkline series={c.c.series} />
              </div>
            ))}
          </div>
        ) : (
          !data?.configured && <p className="adm-empty">—</p>
        )}
        {ga && <p className="adm-note">{t.sourceLabel(!!rp)}</p>}

        {ga && (
          <>
            <section className="adm-panel" id="adm-traffic">
              <h3>{t.sections.traffic}</h3>
              <p className="adm-sub">{t.sessionsLabel}: <b>{nf(ga.traffic.sessions)}</b> · {t.pageViewsLabel}: <b>{nf(ga.traffic.pageViews)}</b></p>
              <LineChart series={ga.cards.visitors.series} days={ga.days} label={t.cards.visitors} />
            </section>

            <div className="adm-grid2">
              <section className="adm-panel">
                <h3>{t.sections.sources}</h3>
                <Bars rows={ga.traffic.sources.map((s) => ({ name: s.name, value: s.sessions }))} valueLabel={t.sessionsLabel} />
              </section>
              <section className="adm-panel" id="adm-signups">
                <h3>{t.sections.signups}</h3>
                <Bars rows={signupRows} valueLabel={t.countLabel} />
                <h3 className="adm-h3b">{t.sections.modules}</h3>
                {ga.modules ? <Bars rows={ga.modules.map((m) => ({ name: m.name, value: m.count }))} valueLabel={t.countLabel} /> : <p className="adm-hint">{t.modulesHint}</p>}
              </section>
            </div>

            <div className="adm-grid2">
              <section className="adm-panel" id="adm-products">
                <h3>{t.sections.products}</h3>
                <Bars rows={productRows} valueLabel={t.countLabel} />
              </section>
              <section className="adm-panel" id="adm-pages">
                <h3>{t.sections.pages}</h3>
                <table className="adm-table">
                  <thead><tr><th>Page</th><th>{t.viewsLabel}</th><th>{t.usersLabel}</th></tr></thead>
                  <tbody>
                    {ga.traffic.pages.map((p) => (
                      <tr key={p.path}><td title={p.path}>{p.path}</td><td>{nf(p.views)}</td><td>{nf(p.users)}</td></tr>
                    ))}
                  </tbody>
                </table>
              </section>
            </div>
          </>
        )}

        <section className="adm-panel" id="adm-payments">
          <h3>{t.sections.payments}</h3>
          {data?.razorpayError && <p className="adm-err">{data.razorpayError}</p>}
          {rp ? (
            rp.recent.length ? (
              <table className="adm-table">
                <thead><tr><th>Date</th><th>Amount</th><th>Method</th><th>For</th></tr></thead>
                <tbody>
                  {rp.recent.map((p) => (
                    <tr key={p.id}>
                      <td>{new Date(p.at * 1000).toLocaleString("en-IN", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" })}</td>
                      <td>{inr(p.amount)}</td><td>{p.method}</td><td>{p.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : <p className="adm-empty">{t.noData}</p>
          ) : <p className="adm-hint">{t.paymentsHint}</p>}
        </section>

        <section className="adm-panel" id="adm-setup">
          <h3>{t.setupTitle}</h3>
          {data && !data.configured && data.missing.length > 0 && (
            <p className="adm-err">{t.missingLabel} {data.missing.join(", ")}</p>
          )}
          <p className="adm-sub">{t.setupIntro}</p>
          <ol className="adm-steps">{t.setupSteps.map((s) => <li key={s}>{s}</li>)}</ol>
        </section>
      </main>
    </div>
  );
}
