"use client";

import { useEffect, useMemo, useState } from "react";
import { batches, batchFinder as t, type BatchData, type BatchModule } from "@/content/site";

type Source = "search" | "default" | "deeplink";

const DAY = 86_400_000;

function parseDate(iso: string): Date | null {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso.trim());
  return m ? new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3])) : null;
}

function daysUntil(iso: string, today: Date): number | null {
  const d = parseDate(iso);
  return d ? Math.round((d.getTime() - today.getTime()) / DAY) : null;
}

function startOfToday() {
  const n = new Date();
  return new Date(n.getFullYear(), n.getMonth(), n.getDate());
}

/** Minimal CSV parser (quoted fields, commas inside quotes, "" escapes). */
function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') q = false;
      else cell += c;
    } else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(cell); cell = "";
      if (row.some((x) => x.trim())) rows.push(row);
      row = [];
    } else cell += c;
  }
  row.push(cell);
  if (row.some((x) => x.trim())) rows.push(row);
  return rows;
}

function modulesFromCsv(text: string): BatchModule[] {
  const [head, ...rows] = parseCsv(text);
  if (!head) return [];
  const idx = (k: string) => head.findIndex((h) => h.trim().toLowerCase() === k.toLowerCase());
  const col = (r: string[], k: string) => (idx(k) >= 0 ? (r[idx(k)] || "").trim() : "");
  return rows
    .map((r) => ({
      id: col(r, "id"),
      name: col(r, "name"),
      aliases: col(r, "aliases").split(",").map((a) => a.trim()).filter(Boolean),
      startDate: col(r, "startDate"),
      time: col(r, "time"),
      mode: col(r, "mode"),
      whatsappLink: col(r, "whatsappLink"),
    }))
    .filter((m) => m.id && m.name);
}

function validate(mods: BatchModule[]) {
  for (const m of mods) {
    if (!m.startDate || !parseDate(m.startDate)) console.warn(`[batches] module "${m.id || m.name}" is missing a valid startDate (YYYY-MM-DD)`);
    if (!m.whatsappLink) console.warn(`[batches] module "${m.id || m.name}" is missing whatsappLink — falling back to the general group`);
  }
}

function matches(m: BatchModule, q: string) {
  return [m.name, m.id, ...m.aliases].some((x) => x.toLowerCase().includes(q));
}

function track(m: { id: string; name: string }, source: Source) {
  const w = window as Window & { ttmTrack?: (e: string, p: Record<string, string>) => void };
  w.ttmTrack?.(t.trackEvent, { module_id: m.id, module_name: m.name, source });
}

export default function BatchFinder() {
  const [data, setData] = useState<BatchData>(batches);
  const [input, setInput] = useState("");
  const [query, setQuery] = useState("");
  const [deepId, setDeepId] = useState<string | null>(null);
  const [deepQuery, setDeepQuery] = useState<string | null>(null);
  const [today, setToday] = useState<Date | null>(null);

  // Load: optional Google Sheet CSV, validation, today's date (client-only to avoid stale static dates).
  useEffect(() => {
    setToday(startOfToday());
    let cancelled = false;
    const finish = (d: BatchData) => {
      if (cancelled) return;
      validate(d.modules);
      setData(d);
    };
    if (batches.sheetCsvUrl) {
      fetch(batches.sheetCsvUrl)
        .then((r) => (r.ok ? r.text() : Promise.reject(r.status)))
        .then((txt) => {
          const mods = modulesFromCsv(txt);
          finish(mods.length ? { ...batches, modules: mods } : batches);
        })
        .catch(() => finish(batches));
    } else finish(batches);
    return () => { cancelled = true; };
  }, []);

  // Deep link: ?module=mm pre-fills the search and highlights that module.
  useEffect(() => {
    const id = new URLSearchParams(window.location.search).get(t.deepLinkParam)?.trim().toLowerCase();
    if (!id) return;
    const m = data.modules.find((x) => x.id.toLowerCase() === id);
    const q = m ? m.name : id;
    setDeepId(m ? m.id : null);
    setDeepQuery(q);
    setInput(q);
    setQuery(q);
  }, [data]);

  // Debounce typing.
  useEffect(() => {
    const h = setTimeout(() => setQuery(input), t.debounceMs);
    return () => clearTimeout(h);
  }, [input]);

  const q = query.trim().toLowerCase();
  const source: Source = !q ? "default" : deepQuery !== null && query === deepQuery ? "deeplink" : "search";

  const list = useMemo(() => {
    const byDate = (a: BatchModule, b: BatchModule) => a.startDate.localeCompare(b.startDate);
    if (q) return data.modules.filter((m) => matches(m, q)).sort(byDate);
    if (!today) return [];
    return data.modules
      .filter((m) => (daysUntil(m.startDate, today) ?? -1) >= 0)
      .sort(byDate)
      .slice(0, t.upcomingCount);
  }, [data, q, today]);

  const fmt = (iso: string) =>
    parseDate(iso)?.toLocaleDateString(t.dateLocale, { day: "numeric", month: "short", year: "numeric" }) ?? iso;

  const general = { id: t.generalId, name: t.generalName };
  const showGeneral = list.length === 0 && (q !== "" || today !== null);

  return (
    <div className="hv-card w-full max-w-[440px] justify-self-center self-center p-5 grid grid-cols-[minmax(0,1fr)] gap-3" aria-label={t.title}>
      <label className="grid gap-1.5">
        <span className="text-sm font-bold text-[var(--ink)]">{t.title}</span>
        <input
          type="search"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t.searchPlaceholder}
          aria-label={t.searchLabel}
          className="w-full rounded-xl border border-[var(--line)] bg-white px-3.5 py-2.5 text-[.95rem] outline-none focus:border-[var(--blue)]"
        />
      </label>

      <ul className="m-0 grid grid-cols-[minmax(0,1fr)] list-none gap-2.5 p-0" aria-live="polite">
        {list.map((m) => {
          const days = today ? daysUntil(m.startDate, today) : null;
          const passed = days === null || days < 0;
          const href = m.whatsappLink || data.defaultWhatsappLink;
          const highlight = deepId === m.id && source === "deeplink";
          return (
            <li
              key={m.id}
              data-module={m.id}
              className={`grid grid-cols-[minmax(0,1fr)] gap-1.5 rounded-xl border p-3.5 ${highlight ? "border-[var(--blue)] bg-[var(--blue-50)] shadow-[0_0_0_3px_rgba(37,99,235,.18)]" : "border-[var(--line)] bg-white"}`}
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <strong className="text-base text-[var(--ink)]">{m.name}</strong>
                <span
                  className={`rounded-full px-2.5 py-0.5 text-xs font-bold ${passed ? "bg-[var(--bg-alt)] text-[var(--muted)]" : "bg-[#ecfdf5] text-[var(--green)]"}`}
                >
                  {passed ? t.comingSoon : days === 0 ? t.startsToday : t.startsIn(days)}
                </span>
              </div>
              {!passed && (
                <span className="text-sm text-[var(--muted)]">
                  {fmt(m.startDate)} · {m.time} · {m.mode}
                </span>
              )}
              <a
                className="btn btn-primary btn-block"
                style={{ whiteSpace: "normal", textAlign: "center" }}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => track(m, source)}
              >
                {t.joinLabel(m.name)}
              </a>
            </li>
          );
        })}
        {showGeneral && (
          <li className="grid gap-2 rounded-xl border border-dashed border-[var(--line)] p-3.5">
            <span className="text-sm text-[var(--ink-2)]">{q ? t.noMatch : t.noUpcoming}</span>
            <a
              className="btn btn-ghost btn-block"
              href={data.defaultWhatsappLink}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => track(general, source)}
            >
              {t.noMatchButton}
            </a>
          </li>
        )}
      </ul>
    </div>
  );
}
