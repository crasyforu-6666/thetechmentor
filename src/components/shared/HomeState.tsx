"use client";

import { createContext, useCallback, useContext, useState } from "react";

type Prefill = { course: string; format: string; n: number };
type HomeStateValue = {
  filter: string;
  query: string;
  prefill: Prefill;
  setFilter: (f: string) => void;
  setQuery: (q: string) => void;
  reset: () => void;
  prefillForm: (course: string, format: string) => void;
};

const Ctx = createContext<HomeStateValue | null>(null);

export function HomeStateProvider({ children }: { children: React.ReactNode }) {
  const [filter, setFilter] = useState("all");
  const [query, setQuery] = useState("");
  const [prefill, setPrefill] = useState<Prefill>({ course: "", format: "", n: 0 });
  const reset = useCallback(() => {
    setFilter("all");
    setQuery("");
  }, []);
  const prefillForm = useCallback(
    (course: string, format: string) => setPrefill((p) => ({ course, format, n: p.n + 1 })),
    [],
  );
  return (
    <Ctx.Provider value={{ filter, query, prefill, setFilter, setQuery, reset, prefillForm }}>
      {children}
    </Ctx.Provider>
  );
}

export function useHomeState() {
  const v = useContext(Ctx);
  if (!v) throw new Error("useHomeState must be used inside HomeStateProvider");
  return v;
}

export function scrollToId(id: string) {
  const el = document.getElementById(id);
  if (!el) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  el.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
}
