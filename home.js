/* Homepage: course catalog filters/search, and the enrol/advisor modal pre-fill. */
(function () {
  "use strict";

  /* ---------- Prices (single source on the page) ---------- */
  var PRICES = {
    "Recorded Session": { "SAP MM": 4999, "SAP SD": 4999, "SAP FICO": 4999, "SAP ABAP": 4999, "SAP BASIS": 4999, "SAP EWM": 6999, "SAP TM": 6999, "SAP Logistics": 6999 },
    "Live Mentored Session": { "SAP MM": 29999, "SAP SD": 29999, "SAP ABAP": 29999, "SAP FICO": 34999, "SAP BASIS": 34999, "SAP EWM": 34999, "SAP TM": 34999, "SAP Logistics": 34999 }
  };
  function inr(n) { return "₹" + Number(n).toLocaleString("en-IN"); }
  function priceFor(course, format) { return (PRICES[format] || {})[course] || null; }

  /* ---------- Catalog filtering ---------- */
  var courses = Array.prototype.slice.call(document.querySelectorAll("#courses .course"));
  var sections = Array.prototype.slice.call(document.querySelectorAll("#courses .cat-section"));
  var chips = document.querySelectorAll(".filters .chip");
  var noResults = document.getElementById("no-results");
  var inputs = [document.getElementById("course-search"), document.getElementById("hero-search")].filter(Boolean);
  var state = { filter: "all", query: "" };

  function run() {
    var q = state.query.trim().toLowerCase();
    var shown = 0;
    courses.forEach(function (c) {
      var fmt = c.getAttribute("data-format");
      var cats = (c.getAttribute("data-cats") || "").split(" ");
      var f = state.filter;
      var okFilter = f === "all" || f === fmt || cats.indexOf(f) !== -1;
      var text = (c.getAttribute("data-tags") + " " + c.textContent).toLowerCase();
      var okQuery = !q || q.split(/\s+/).every(function (w) { return text.indexOf(w) !== -1; });
      c.hidden = !(okFilter && okQuery);
      if (!c.hidden) shown++;
    });
    sections.forEach(function (sec) { sec.hidden = !sec.querySelector(".course:not([hidden])"); });
    if (noResults) noResults.hidden = shown > 0;
    chips.forEach(function (ch) { ch.classList.toggle("active", ch.getAttribute("data-filter") === state.filter); });
  }
  function scrollTo(id) {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }
  function setQuery(q) { state.query = q; inputs.forEach(function (o) { o.value = q; }); }

  chips.forEach(function (ch) {
    ch.addEventListener("click", function () { state.filter = ch.getAttribute("data-filter"); run(); });
  });
  inputs.forEach(function (inp) {
    inp.addEventListener("input", function () {
      state.query = inp.value;
      inputs.forEach(function (o) { if (o !== inp) o.value = inp.value; });
      run();
    });
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); scrollTo("courses"); } });
  });
  var heroBtn = document.getElementById("hero-search-btn");
  if (heroBtn) heroBtn.addEventListener("click", function () { scrollTo("courses"); });

  document.querySelectorAll(".popular button[data-q]").forEach(function (b) {
    b.addEventListener("click", function () { state.filter = "all"; setQuery(b.getAttribute("data-q")); run(); scrollTo("courses"); });
  });
  // data-jump: filter keys (recorded/live/functional/technical/supply) or a course keyword
  var FILTERS = ["recorded", "live", "functional", "technical", "supply"];
  document.querySelectorAll("[data-jump]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      var key = el.getAttribute("data-jump");
      if (FILTERS.indexOf(key) !== -1) { state.filter = key; setQuery(""); }
      else { state.filter = "all"; setQuery(key); }
      run();
      if (el.tagName === "BUTTON") scrollTo("courses");
      if (el.tagName === "A" && (key === "recorded" || key === "live")) { e.preventDefault(); scrollTo(key); }
    });
  });
  document.querySelectorAll("[data-reset]").forEach(function (b) {
    b.addEventListener("click", function () { state.filter = "all"; setQuery(""); run(); });
  });
  if (courses.length) run();

  /* ---------- Forms: course + format → price line ---------- */
  function wire(prefix) {
    var course = document.getElementById(prefix + "-course");
    var format = document.getElementById(prefix + "-format");
    var line = document.getElementById(prefix + "-price-line");
    if (!course || !format) return null;
    function update() {
      var p = priceFor(course.value, format.value);
      if (line) {
        line.hidden = !p;
        if (p) line.innerHTML = "<strong>" + course.value + " — " + format.value + ":</strong> " + inr(p) +
          (format.value === "Live Mentored Session" ? " · EMI available" : " · one-time, lifetime access");
      }
      return p;
    }
    course.addEventListener("change", function () { update(); if (prefix === "modal") syncModal(); });
    format.addEventListener("change", function () { update(); if (prefix === "modal") syncModal(); });
    return { course: course, format: format, update: update };
  }
  var modal = wire("modal");
  wire("app");

  /* ---------- Modal pre-fill (runs after script.js opens/resets the modal) ---------- */
  var label = document.getElementById("modal-selected-program");
  var payBtn = document.getElementById("modal-pay-btn");
  var payNote = document.getElementById("modal-pay-note");
  var title = document.getElementById("modal-title");
  var submit = document.getElementById("modal-submit");

  function syncModal() {
    if (!modal) return;
    var c = modal.course.value, f = modal.format.value, p = priceFor(c, f);
    if (label) label.textContent = (c && f) ? c + " — " + f + (p ? " (" + inr(p) + ")" : "") : "Free counselling (15 min)";
    if (payBtn) {
      payBtn.hidden = !p;
      payBtn.textContent = f === "Live Mentored Session" ? "Reserve your seat — pay " + inr(p || 0) : "Pay " + inr(p || 0) + " & start now";
    }
    if (payNote) payNote.hidden = !p;
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".open-screening-modal");
    if (!btn || !modal) return;
    var c = btn.getAttribute("data-course") || "";
    var f = btn.getAttribute("data-format") || "";
    modal.course.value = c;
    modal.format.value = f;
    modal.update();
    syncModal();
    var enrol = btn.getAttribute("data-action") === "enroll";
    if (title) title.textContent = enrol ? "Enrol in " + c : "Talk to a career advisor";
    if (submit) submit.textContent = enrol ? "Not ready to pay? Request a call back" : "Request a call back";
    if (submit) submit.className = enrol ? "btn btn-ghost btn-block" : "btn btn-primary btn-block";
  });

  if (payBtn) {
    payBtn.addEventListener("click", function () {
      var c = modal.course.value, f = modal.format.value, p = priceFor(c, f);
      if (!p || typeof window.payWithRazorpay !== "function") return;
      var v = function (id) { var el = document.getElementById(id); return el ? el.value : ""; };
      window.payWithRazorpay(p, c + " — " + f, { name: v("modal-name"), email: v("modal-email"), phone: v("modal-phone") });
    });
  }
})();
