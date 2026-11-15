"use client";

import { useState } from "react";
import { curriculum } from "@/content/site";

export default function CurriculumTabs() {
  const [active, setActive] = useState(curriculum.tabs[0].key);
  return (
    <div className="wrap two-col">
      <div>
        <p className="eyebrow">{curriculum.eyebrow}</p>
        <h2>{curriculum.title}</h2>
        <p className="sub">{curriculum.sub}</p>
        <div className="tabs" role="tablist">
          {curriculum.tabs.map((t) => (
            <button
              key={t.key}
              className={`tab${active === t.key ? " active" : ""}`}
              role="tab"
              aria-selected={active === t.key}
              aria-controls={`panel-${t.key}`}
              onClick={() => setActive(t.key)}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>
      <div>
        {curriculum.tabs.map((t) => (
          <div
            key={t.key}
            className={`tab-panel${active === t.key ? " active" : ""}`}
            id={`panel-${t.key}`}
            role="tabpanel"
            hidden={active !== t.key}
          >
            <ol className="weeks">
              {t.weeks.map(([w, text]) => (
                <li key={w}>
                  <span>{w}</span>
                  {text}
                </li>
              ))}
            </ol>
          </div>
        ))}
      </div>
    </div>
  );
}
