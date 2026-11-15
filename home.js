/* Homepage: course catalog filters/search, and counselling form pre-fill. */
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
  var inputs = [document.getElementById("course-search")].filter(Boolean);
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
  document.querySelectorAll('.popular a[href^="#"]:not([data-jump])').forEach(function (a) {
    a.addEventListener("click", function () { state.filter = "all"; setQuery(""); run(); });
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
    course.addEventListener("change", update);
    format.addEventListener("change", update);
    return { course: course, format: format, update: update };
  }
  var app = wire("app");

  /* ---------- "Ask an advisor" links pre-fill the counselling form ---------- */
  document.querySelectorAll('a[href="#enroll-form"][data-course]').forEach(function (a) {
    a.addEventListener("click", function () {
      if (!app) return;
      app.course.value = a.getAttribute("data-course") || "";
      app.format.value = a.getAttribute("data-format") || "";
      app.update();
    });
  });
})();
