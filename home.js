/* Homepage course catalog: filter chips, search and quick jumps. */
(function () {
  "use strict";
  var courses = Array.prototype.slice.call(document.querySelectorAll("#catalog .course"));
  if (!courses.length) return;
  var chips = document.querySelectorAll(".filters .chip");
  var noResults = document.getElementById("no-results");
  var searchInputs = [document.getElementById("course-search"), document.getElementById("hero-search")].filter(Boolean);

  function apply(filter, query) {
    var q = (query || "").trim().toLowerCase();
    var shown = 0;
    courses.forEach(function (c) {
      var types = (c.getAttribute("data-type") || "").split(" ");
      var text = (c.getAttribute("data-tags") + " " + c.textContent).toLowerCase();
      var okType = filter === "all" || types.indexOf(filter) !== -1;
      var okQuery = !q || q.split(/\s+/).every(function (w) { return text.indexOf(w) !== -1; });
      c.hidden = !(okType && okQuery);
      if (!c.hidden) shown++;
    });
    if (noResults) noResults.hidden = shown > 0;
    chips.forEach(function (ch) { ch.classList.toggle("active", ch.getAttribute("data-filter") === filter); });
  }

  var state = { filter: "all", query: "" };
  function run() { apply(state.filter, state.query); }
  function goToCatalog() {
    var el = document.getElementById("courses");
    if (el) el.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }

  chips.forEach(function (ch) {
    ch.addEventListener("click", function () { state.filter = ch.getAttribute("data-filter"); run(); });
  });

  searchInputs.forEach(function (inp) {
    inp.addEventListener("input", function () {
      state.query = inp.value;
      searchInputs.forEach(function (o) { if (o !== inp) o.value = inp.value; });
      run();
    });
    inp.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); goToCatalog(); }
    });
  });
  var heroBtn = document.getElementById("hero-search-btn");
  if (heroBtn) heroBtn.addEventListener("click", goToCatalog);

  function setQuery(q) {
    state.query = q; state.filter = "all";
    searchInputs.forEach(function (o) { o.value = q; });
    run();
  }

  // "Popular" pills and data-jump links (career paths, footer)
  var jumpMap = { mm: ["all", "sap mm"], ewm: ["all", "ewm"], self: ["self", ""], live: ["live", ""], career: ["career", ""], combo: ["all", "combo"] };
  document.querySelectorAll(".popular button[data-q], [data-jump]").forEach(function (el) {
    el.addEventListener("click", function () {
      var key = el.getAttribute("data-q") || el.getAttribute("data-jump");
      var m = jumpMap[key] || ["all", key];
      state.filter = m[0]; state.query = m[1];
      searchInputs.forEach(function (o) { o.value = m[1]; });
      run();
      if (el.tagName === "BUTTON") goToCatalog();
    });
  });

  document.querySelectorAll("[data-reset]").forEach(function (b) {
    b.addEventListener("click", function () { setQuery(""); });
  });
})();
