/* /digital-products — filters, practice-server price matrix, unlock/order modal, preview drawer.
   Data comes from <script id="dp-data"> (built from data/digital-products.json).
   Phase 2 hook: replace loadData() with a fetch to the Admin/API endpoint. */
(function () {
  "use strict";

  function loadData() {
    var el = document.getElementById("dp-data");
    return el ? JSON.parse(el.textContent) : null;
  }
  var DATA = loadData();
  if (!DATA) return;
  var SRV = DATA.server;
  var cfg = window.TTM_CONFIG || {};
  var WA = cfg.WHATSAPP_NUMBER || "917848942021";

  var $ = function (id) { return document.getElementById(id); };
  var inr = function (n) { return "₹" + Number(n).toLocaleString("en-IN"); };
  var esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  };
  var productById = {};
  DATA.products.forEach(function (p) { productById[p.id] = p; });
  var catLabel = {};
  DATA.categories.forEach(function (c) { catLabel[c.id] = c.label; });

  /* ---------------- Practice server price matrix ---------------- */
  function moduleById(id) { return SRV.modules.filter(function (m) { return m.id === id; })[0]; }
  function durationById(id) { return SRV.durations.filter(function (d) { return d.id === id; })[0]; }
  function serverQuote() {
    var mod = moduleById($("dp-module").value);
    var dur = durationById($("dp-duration").value);
    var table = SRV.pricing[mod.tier];
    var price = table[dur.id];
    var monthly = table["1m"] * dur.months;
    var save = dur.months > 1 ? Math.round((1 - price / monthly) * 100) : 0;
    return { module: mod, duration: dur, price: price, monthlyTotal: monthly, save: save };
  }
  function renderServer() {
    var q = serverQuote();
    $("dp-price").textContent = inr(q.price);
    $("dp-was").textContent = q.save > 0 ? inr(q.monthlyTotal) : "";
    $("dp-price-meta").textContent = q.duration.label + " · " + inr(Math.round(q.price / q.duration.months)) + " per month";
    var badge = $("dp-save");
    badge.hidden = !q.save;
    badge.textContent = q.save ? "You save " + q.save + "%" : "";
    $("dp-included").innerHTML =
      "<li><strong>" + esc(q.module.label) + "</strong> system access</li>" +
      "<li>" + esc(q.duration.label) + " · 24/7 availability</li>" +
      "<li>" + (q.module.tier === "specialized" ? "Specialised configuration &amp; scenario data" : "Pre-configured master data &amp; best-practice content") + "</li>" +
      "<li>Credentials within 2 hours on WhatsApp &amp; email</li>";
    // keep dropdown savings honest for the selected module's tier
    var table = SRV.pricing[q.module.tier];
    Array.prototype.forEach.call($("dp-duration").options, function (opt) {
      var d = durationById(opt.value);
      var s = d.months > 1 ? Math.round((1 - table[d.id] / (table["1m"] * d.months)) * 100) : 0;
      var tag = d.months === 3 ? "Popular" : d.months === 6 ? "Best Value" : "";
      opt.textContent = d.label + (tag ? " — " + tag + " — Save " + s + "%" : "");
    });
  }
  $("dp-module").addEventListener("change", renderServer);
  $("dp-duration").addEventListener("change", renderServer);
  renderServer();

  /* ---------------- Filters ---------------- */
  var current = "all";
  var cards = Array.prototype.slice.call(document.querySelectorAll(".dp-card"));
  var server = document.querySelector(".dp-server");
  function applyFilter() {
    var freeOnly = $("dp-free-only").checked;
    var shown = 0;
    cards.forEach(function (c) {
      var ok = (current === "all" || c.dataset.category === current) && (!freeOnly || c.dataset.free === "true");
      c.hidden = !ok;
      if (ok) shown++;
    });
    var showServer = (current === "all" || current === "servers") && !freeOnly;
    server.hidden = !showServer;
    if (showServer) shown++;
    $("dp-empty").hidden = shown > 0;
    document.querySelectorAll("[data-dp-filter]").forEach(function (b) { b.classList.toggle("active", b.dataset.dpFilter === current); });
  }
  document.querySelectorAll("[data-dp-filter]").forEach(function (b) {
    b.addEventListener("click", function () { current = b.dataset.dpFilter; applyFilter(); });
  });
  $("dp-free-only").addEventListener("change", applyFilter);
  // deep links: /digital-products#servers, #free, #resumes, #interview, #notes
  var hash = (location.hash || "").slice(1);
  if (hash === "free") $("dp-free-only").checked = true;
  else if (["servers", "resumes", "interview", "notes"].indexOf(hash) !== -1) current = hash;
  applyFilter();

  /* ---------------- Modals ---------------- */
  var modal = $("dp-modal"), drawer = $("dp-preview");
  var active = null; // { kind: 'free'|'buy'|'server', product?, quote? }
  var lastFocus = null;

  function open(el) { lastFocus = document.activeElement; el.hidden = false; document.body.style.overflow = "hidden"; var f = el.querySelector("input, select, button:not([data-dp-close])"); if (f) f.focus(); }
  function close(el) { el.hidden = true; document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
  [modal, drawer].forEach(function (el) {
    el.addEventListener("click", function (e) { if (e.target === el || e.target.closest("[data-dp-close]")) close(el); });
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { if (!modal.hidden) close(modal); if (!drawer.hidden) close(drawer); } });

  function openOrder(kind, product) {
    active = { kind: kind, product: product || null, quote: kind === "server" ? serverQuote() : null };
    $("dp-form").hidden = false; $("dp-form").reset();
    $("dp-modal-done").hidden = true; $("dp-modal-body").hidden = false;
    var sum = $("dp-modal-summary");
    if (kind === "free") {
      $("dp-modal-kind").textContent = "Free download";
      $("dp-modal-title").textContent = product.title;
      sum.innerHTML = '<div class="dp-line"><span>' + esc(catLabel[product.category]) + " · " + esc(product.format) + '</span><strong class="dp-free-text">FREE</strong></div>';
      $("dp-submit").textContent = "Unlock free PDF";
      $("dp-fineprint").textContent = "We'll also send the PDF to your WhatsApp. No spam — unsubscribe anytime.";
    } else if (kind === "buy") {
      $("dp-modal-kind").textContent = "Order summary";
      $("dp-modal-title").textContent = product.title;
      sum.innerHTML = '<div class="dp-line"><span>' + esc(catLabel[product.category]) + " · " + esc(product.format) + " · " + product.pages + ' pages</span><strong>' + inr(product.price) + '</strong></div>' +
        '<div class="dp-line dp-total"><span>Total</span><strong>' + inr(product.price) + "</strong></div>";
      $("dp-submit").textContent = "Proceed to pay " + inr(product.price);
      $("dp-fineprint").innerHTML = 'Secure checkout via Razorpay · Digital product — all sales final, <a href="refund.html" target="_blank">no refunds</a>.';
    } else {
      var q = active.quote;
      $("dp-modal-kind").textContent = "Order summary";
      $("dp-modal-title").textContent = SRV.title;
      sum.innerHTML = '<div class="dp-line"><span>Module</span><strong>' + esc(q.module.label) + "</strong></div>" +
        '<div class="dp-line"><span>Duration</span><strong>' + esc(q.duration.label) + "</strong></div>" +
        (q.save ? '<div class="dp-line"><span>Saving vs monthly</span><strong class="dp-free-text">' + q.save + "% (" + inr(q.monthlyTotal - q.price) + ")</strong></div>" : "") +
        '<div class="dp-line dp-total"><span>Total</span><strong>' + inr(q.price) + "</strong></div>";
      $("dp-submit").textContent = "Proceed to pay " + inr(q.price);
      $("dp-fineprint").innerHTML = 'Credentials within 2 hours on WhatsApp &amp; email · Digital product — all sales final, <a href="refund.html" target="_blank">no refunds</a>.';
    }
    open(modal);
  }

  function itemName() {
    if (active.kind === "server") return SRV.title + " — " + active.quote.module.label + " — " + active.quote.duration.label;
    return active.product.title;
  }

  $("dp-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var form = e.target;
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var user = { name: form.name.value.trim(), email: form.email.value.trim(), phone: form.phone.value.trim() };
    var amount = active.kind === "server" ? active.quote.price : (active.product ? active.product.price : 0);
    var lead = {
      type: "lead", name: user.name, email: user.email, phone: user.phone,
      program: "Digital: " + itemName(), amount: amount,
      status: active.kind === "free" ? "Free PDF unlocked" : "Digital checkout started"
    };
    if (window.ttmSend) window.ttmSend(lead);
    if (window.ttmTrack) window.ttmTrack("lead", { content_name: itemName(), value: amount || undefined });

    if (active.kind === "free") { showFreeDelivery(user); return; }
    close(modal);
    if (typeof window.payWithRazorpay === "function") {
      window.payWithRazorpay(amount, itemName(), user);
    } else {
      window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent("Hi, I'd like to buy: " + itemName() + " (" + inr(amount) + ")"), "_blank");
    }
  });

  function showFreeDelivery(user) {
    var p = active.product;
    var waMsg = "Hi theTechMentor, I'm " + user.name + ". Please send me the free PDF: " + p.title;
    var waLink = "https://wa.me/" + WA + "?text=" + encodeURIComponent(waMsg);
    var html;
    if (p.file) {
      html = '<div class="dp-done"><div class="dp-done-ic">✅</div><h3>Your PDF is ready</h3>' +
        "<p>Thanks " + esc(user.name) + "! Your download should start automatically.</p>" +
        '<a class="btn btn-primary btn-block" href="' + esc(p.file) + '" download id="dp-dl">Download PDF</a>' +
        '<a class="btn btn-ghost btn-block" href="index.html#courses">Explore SAP courses</a></div>';
    } else {
      html = '<div class="dp-done"><div class="dp-done-ic">📩</div><h3>You\'re on the list</h3>' +
        "<p>Thanks " + esc(user.name) + "! We're sending <strong>" + esc(p.title) + "</strong> to your WhatsApp and email shortly.</p>" +
        '<a class="btn btn-primary btn-block" href="' + waLink + '" target="_blank" rel="noopener">Get it now on WhatsApp</a></div>';
    }
    $("dp-modal-body").hidden = true;
    var done = $("dp-modal-done");
    done.innerHTML = html; done.hidden = false;
    var dl = $("dp-dl");
    if (dl) setTimeout(function () { dl.click(); }, 300);
  }

  /* ---------------- Preview drawer ---------------- */
  function openPreview(p) {
    $("dp-preview-title").textContent = p.title;
    $("dp-preview-meta").textContent = catLabel[p.category] + " · " + p.format + " · " + p.pages + " pages · " + (p.price ? inr(p.price) : "FREE");
    $("dp-preview-list").innerHTML = p.preview.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");
    $("dp-preview-cta").innerHTML = '<button type="button" class="btn btn-primary btn-block" data-dp-from-preview="' + esc(p.id) + '">' +
      (p.price ? "Buy now — " + inr(p.price) : "Download free PDF") + "</button>";
    open(drawer);
  }

  /* ---------------- Click routing ---------------- */
  document.addEventListener("click", function (e) {
    var fromPreview = e.target.closest("[data-dp-from-preview]");
    if (fromPreview) {
      var pp = productById[fromPreview.getAttribute("data-dp-from-preview")];
      close(drawer); openOrder(pp.price ? "buy" : "free", pp); return;
    }
    var btn = e.target.closest("[data-dp-action]");
    if (!btn) return;
    var action = btn.getAttribute("data-dp-action");
    if (action === "server") { openOrder("server"); return; }
    var card = btn.closest(".dp-card");
    var p = card && productById[card.dataset.id];
    if (!p) return;
    if (action === "preview") openPreview(p);
    else openOrder(action === "free" ? "free" : "buy", p);
  });
})();
