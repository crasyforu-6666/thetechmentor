"use client";

import { useEffect, useState } from "react";
import { advisor, inr, priceFor } from "@/content/site";
import { useHomeState } from "./HomeState";

declare global {
  interface Window {
    ttmSend?: (payload: Record<string, string>) => void;
    ttmTrack?: (event: string, params: Record<string, string>) => void;
  }
}

const f = advisor.form;

export default function LeadForm() {
  const { prefill } = useHomeState();
  const [course, setCourse] = useState("");
  const [format, setFormat] = useState("");
  const [doneName, setDoneName] = useState<string | null>(null);

  useEffect(() => {
    if (prefill.n === 0) return;
    setCourse(prefill.course);
    setFormat(prefill.format);
  }, [prefill]);

  const price = priceFor(course, format);

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    const data = new FormData(form);
    const name = String(data.get("name") || f.defaultName);
    const phone = String(data.get("phone") || "");
    const program = course && format ? `${course} — ${format}` : f.defaultProgram;

    try {
      const leads = JSON.parse(localStorage.getItem("ttm_admin_leads") || "[]");
      leads.unshift({
        id: "lead_" + Date.now().toString(36),
        date: new Date().toISOString().replace("T", " ").substring(0, 16),
        name,
        email: "",
        phone,
        module: course,
        experience: "Experienced Professional",
        status: "New",
      });
      localStorage.setItem("ttm_admin_leads", JSON.stringify(leads));
    } catch (err) {
      console.error(err);
    }
    window.ttmSend?.({ type: "lead", name, email: "", phone, role: "", timeline: "", status: "New", program });
    window.ttmTrack?.("lead", { content_name: program, lead_status: "new" });
    setDoneName(name);
  }

  return (
    <div className="form-card">
      <form className="enroll-form screening-form" id="enroll-form" noValidate onSubmit={onSubmit} hidden={doneName !== null}>
        <h3>{f.title}</h3>
        <div className="form-row form-2">
          <div>
            <label htmlFor="app-course">{f.courseLabel}</label>
            <select id="app-course" name="course" required value={course} onChange={(e) => setCourse(e.target.value)}>
              <option value="">{f.coursePlaceholder}</option>
              {f.courseOptions.map((o) => (
                <option key={o} value={o}>
                  {o}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="app-format">{f.formatLabel}</label>
            <select id="app-format" name="format" required value={format} onChange={(e) => setFormat(e.target.value)}>
              <option value="">{f.formatPlaceholder}</option>
              {f.formatOptions.map((o) => (
                <option key={o} value={o}>
                  {o}
                </option>
              ))}
            </select>
          </div>
        </div>
        <p className="price-line" id="app-price-line" hidden={!price}>
          {price ? (
            <>
              <strong>
                {course} — {format}:
              </strong>{" "}
              {inr(price)}
              {format === "Live Mentored Session" ? f.liveNote : f.recordedNote}
            </>
          ) : null}
        </p>
        <div className="form-row">
          <label htmlFor="name">{f.nameLabel}</label>
          <input type="text" id="name" name="name" required placeholder={f.namePlaceholder} autoComplete="name" />
        </div>
        <div className="form-row">
          <label htmlFor="phone">{f.phoneLabel}</label>
          <input type="tel" id="phone" name="phone" required placeholder={f.phonePlaceholder} autoComplete="tel" />
        </div>
        <button type="submit" className="btn btn-primary btn-block">
          {f.submit}
        </button>
        <p className="fineprint">{f.fineprint}</p>
      </form>
      <div className="screening-routing-output" id="screening-routing-output" hidden={doneName === null}>
        {doneName !== null && (
          <div className="routing-card routing-success">
            <h4>{advisor.success.title}</h4>
            <p>{advisor.success.text(doneName)}</p>
            <a href={advisor.success.cta.href} target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-block">
              {advisor.success.cta.label}
            </a>
            <p style={{ marginTop: "0.75rem", fontSize: "0.85rem" }}>
              🔓 <strong>{advisor.success.unlockLabel}</strong>{" "}
              <a
                href={advisor.success.unlockLink.href}
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: "#3db8f5", textDecoration: "underline" }}
              >
                {advisor.success.unlockLink.label}
              </a>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
