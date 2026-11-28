/**
 * GET /api/dashboard  — private analytics for the /admin dashboard.
 *
 * Auth:   header "x-admin-key" must equal env ADMIN_PASSWORD.
 * Data:   Google Analytics 4 Data API (service account, no SDK) and,
 *         optionally, Razorpay payments (verified revenue).
 *
 * Vercel environment variables:
 *   ADMIN_PASSWORD            password for /admin
 *   GA4_PROPERTY_ID           numeric GA4 property id (Admin → Property details), not the G- id
 *   GA_SERVICE_ACCOUNT_JSON   full JSON key of a Google Cloud service account that has
 *                             "Viewer" access on the GA4 property
 *   RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET   optional, for verified payments & revenue
 */
const crypto = require("crypto");

const DAYS = 30;
const SIGNUP_EVENTS = ["lead", "whatsapp_batch_click"];
const TRACKED_EVENTS = ["lead", "whatsapp_batch_click", "purchase", "begin_checkout", "product_page_view", "free_document_open", "share_click"];

/* ---------------- helpers ---------------- */
function safeEqual(a, b) {
  const x = Buffer.from(String(a || ""));
  const y = Buffer.from(String(b || ""));
  return x.length === y.length && x.length > 0 && crypto.timingSafeEqual(x, y);
}
const b64url = (buf) => Buffer.from(buf).toString("base64").replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_");

async function googleToken(sa) {
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const claim = b64url(JSON.stringify({
    iss: sa.client_email,
    scope: "https://www.googleapis.com/auth/analytics.readonly",
    aud: "https://oauth2.googleapis.com/token",
    iat: now,
    exp: now + 3600,
  }));
  const signer = crypto.createSign("RSA-SHA256");
  signer.update(`${header}.${claim}`);
  const jwt = `${header}.${claim}.${b64url(signer.sign(sa.private_key))}`;
  const r = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: jwt }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error("Google auth failed: " + (j.error_description || j.error || r.status));
  return j.access_token;
}

async function runReport(token, property, body) {
  const r = await fetch(`https://analyticsdata.googleapis.com/v1beta/properties/${property}:runReport`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const j = await r.json();
  if (!r.ok) throw new Error((j.error && j.error.message) || `GA4 error ${r.status}`);
  return j;
}

const rowsOf = (rep) =>
  (rep.rows || []).map((row) => ({
    d: (row.dimensionValues || []).map((v) => v.value),
    m: (row.metricValues || []).map((v) => Number(v.value)),
  }));

function dayList() {
  const out = [];
  const t = new Date();
  for (let i = DAYS - 1; i >= 0; i--) {
    const d = new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate() - i));
    out.push(d.toISOString().slice(0, 10).replace(/-/g, ""));
  }
  return out;
}

const eventFilter = (names) => ({ filter: { fieldName: "eventName", inListFilter: { values: names } } });
const pct = (cur, prev) => (prev > 0 ? Math.round(((cur - prev) / prev) * 100) : null);

/* ---------------- GA4 ---------------- */
async function ga4() {
  const sa = JSON.parse(process.env.GA_SERVICE_ACCOUNT_JSON);
  const property = process.env.GA4_PROPERTY_ID;
  const token = await googleToken(sa);
  const cur = { startDate: `${DAYS - 1}daysAgo`, endDate: "today" };
  const prev = { startDate: `${DAYS * 2 - 1}daysAgo`, endDate: `${DAYS}daysAgo` };
  const days = dayList();
  const seriesFrom = (rows, pick) => {
    const map = Object.fromEntries(days.map((d) => [d, 0]));
    rows.forEach((r) => { if (r.d[0] in map) map[r.d[0]] += pick(r); });
    return days.map((d) => map[d]);
  };

  const [daily, totals, evDaily, evTotals, sources, pages] = await Promise.all([
    runReport(token, property, { dateRanges: [cur], dimensions: [{ name: "date" }], metrics: [{ name: "activeUsers" }, { name: "sessions" }, { name: "screenPageViews" }], limit: 100 }),
    runReport(token, property, { dateRanges: [cur, prev], metrics: [{ name: "activeUsers" }, { name: "sessions" }, { name: "screenPageViews" }, { name: "totalRevenue" }] }),
    runReport(token, property, { dateRanges: [cur], dimensions: [{ name: "date" }, { name: "eventName" }], metrics: [{ name: "eventCount" }, { name: "totalUsers" }, { name: "eventValue" }], dimensionFilter: eventFilter(TRACKED_EVENTS), limit: 1000 }),
    runReport(token, property, { dateRanges: [cur, prev], dimensions: [{ name: "eventName" }], metrics: [{ name: "eventCount" }, { name: "totalUsers" }, { name: "eventValue" }], dimensionFilter: eventFilter(TRACKED_EVENTS) }),
    runReport(token, property, { dateRanges: [cur], dimensions: [{ name: "sessionSourceMedium" }], metrics: [{ name: "sessions" }, { name: "activeUsers" }], orderBys: [{ metric: { metricName: "sessions" }, desc: true }], limit: 8 }),
    runReport(token, property, { dateRanges: [cur], dimensions: [{ name: "pagePath" }], metrics: [{ name: "screenPageViews" }, { name: "activeUsers" }], orderBys: [{ metric: { metricName: "screenPageViews" }, desc: true }], limit: 10 }),
  ]);

  // totals: with two date ranges GA adds a "dateRange" dimension (date_range_0 = current)
  const tRows = rowsOf(totals);
  const tCur = (tRows.find((r) => r.d[0] === "date_range_0") || { m: [0, 0, 0, 0] }).m;
  const tPrev = (tRows.find((r) => r.d[0] === "date_range_1") || { m: [0, 0, 0, 0] }).m;

  const evT = rowsOf(evTotals);
  const ev = (name, range, idx) => (evT.find((r) => r.d[0] === name && r.d[1] === range) || { m: [0, 0, 0] }).m[idx];
  const evD = rowsOf(evDaily);

  const signups = SIGNUP_EVENTS.reduce((s, n) => s + ev(n, "date_range_0", 0), 0);
  const signupsPrev = SIGNUP_EVENTS.reduce((s, n) => s + ev(n, "date_range_1", 0), 0);
  const paid = ev("purchase", "date_range_0", 1);
  const paidPrev = ev("purchase", "date_range_1", 1);
  const revenue = ev("purchase", "date_range_0", 2) || tCur[3];
  const revenuePrev = ev("purchase", "date_range_1", 2) || tPrev[3];

  // optional breakdown by module (needs custom dimension "module_name" registered in GA4)
  let modules = null;
  try {
    const rep = await runReport(token, property, { dateRanges: [cur], dimensions: [{ name: "customEvent:module_name" }], metrics: [{ name: "eventCount" }], dimensionFilter: eventFilter(["whatsapp_batch_click"]), orderBys: [{ metric: { metricName: "eventCount" }, desc: true }], limit: 12 });
    modules = rowsOf(rep).filter((r) => r.d[0] && r.d[0] !== "(not set)").map((r) => ({ name: r.d[0], count: r.m[0] }));
  } catch (e) {
    modules = null; // custom dimension not registered yet
  }

  const dRows = rowsOf(daily);
  return {
    days,
    cards: {
      visitors: { value: tCur[0], change: pct(tCur[0], tPrev[0]), series: seriesFrom(dRows, (r) => r.m[0]) },
      signups: { value: signups, change: pct(signups, signupsPrev), series: seriesFrom(evD.filter((r) => SIGNUP_EVENTS.includes(r.d[1])), (r) => r.m[0]) },
      paidUsers: { value: paid, change: pct(paid, paidPrev), series: seriesFrom(evD.filter((r) => r.d[1] === "purchase"), (r) => r.m[1]) },
      revenue: { value: revenue, change: pct(revenue, revenuePrev), series: seriesFrom(evD.filter((r) => r.d[1] === "purchase"), (r) => r.m[2]) },
    },
    traffic: {
      sessions: tCur[1],
      pageViews: tCur[2],
      sessionsSeries: seriesFrom(dRows, (r) => r.m[1]),
      sources: rowsOf(sources).map((r) => ({ name: r.d[0], sessions: r.m[0], users: r.m[1] })),
      pages: rowsOf(pages).map((r) => ({ path: r.d[0], views: r.m[0], users: r.m[1] })),
    },
    events: Object.fromEntries(TRACKED_EVENTS.map((n) => [n, { count: ev(n, "date_range_0", 0), users: ev(n, "date_range_0", 1), change: pct(ev(n, "date_range_0", 0), ev(n, "date_range_1", 0)) }])),
    modules,
  };
}

/* ---------------- Razorpay (optional, verified money) ---------------- */
async function razorpay() {
  const auth = "Basic " + Buffer.from(`${process.env.RAZORPAY_KEY_ID}:${process.env.RAZORPAY_KEY_SECRET}`).toString("base64");
  const to = Math.floor(Date.now() / 1000);
  const from = to - DAYS * 86400;
  const items = [];
  for (let skip = 0; skip < 1000; skip += 100) {
    const r = await fetch(`https://api.razorpay.com/v1/payments?from=${from}&to=${to}&count=100&skip=${skip}`, { headers: { Authorization: auth } });
    const j = await r.json();
    if (!r.ok) throw new Error((j.error && j.error.description) || `Razorpay error ${r.status}`);
    items.push(...(j.items || []));
    if (!j.items || j.items.length < 100) break;
  }
  const captured = items.filter((p) => p.status === "captured");
  const days = dayList();
  const byDay = Object.fromEntries(days.map((d) => [d, 0]));
  captured.forEach((p) => {
    const d = new Date(p.created_at * 1000).toISOString().slice(0, 10).replace(/-/g, "");
    if (d in byDay) byDay[d] += p.amount / 100;
  });
  return {
    payments: captured.length,
    paidUsers: new Set(captured.map((p) => p.email || p.contact || p.id)).size,
    revenue: captured.reduce((s, p) => s + p.amount, 0) / 100,
    series: days.map((d) => byDay[d]),
    recent: captured.slice(0, 10).map((p) => ({ id: p.id, amount: p.amount / 100, at: p.created_at, method: p.method, description: p.description || p.notes?.program || "" })),
  };
}

/* ---------------- handler ---------------- */
module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Robots-Tag", "noindex");
  if (!process.env.ADMIN_PASSWORD) {
    return res.status(503).json({ configured: false, missing: ["ADMIN_PASSWORD"] });
  }
  if (!safeEqual(req.headers["x-admin-key"], process.env.ADMIN_PASSWORD)) {
    await new Promise((r) => setTimeout(r, 600)); // slow down guessing
    return res.status(401).json({ error: "Wrong password" });
  }
  const missing = ["GA4_PROPERTY_ID", "GA_SERVICE_ACCOUNT_JSON"].filter((k) => !process.env[k]);
  const out = { configured: missing.length === 0, missing, generatedAt: new Date().toISOString(), rangeDays: DAYS };
  const jobs = [];
  if (!missing.length) jobs.push(ga4().then((d) => { out.ga = d; }).catch((e) => { out.gaError = e.message; }));
  if (process.env.RAZORPAY_KEY_ID && process.env.RAZORPAY_KEY_SECRET) {
    jobs.push(razorpay().then((d) => { out.razorpay = d; }).catch((e) => { out.razorpayError = e.message; }));
  }
  await Promise.all(jobs);
  res.status(200).json(out);
};
