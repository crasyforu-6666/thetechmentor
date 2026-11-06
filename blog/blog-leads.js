/* Blog lead capture: in-article opt-in forms -> Google Sheet webhook + ad tracking. */
(function () {
  "use strict";
  var PLAYLIST = "https://www.youtube.com/playlist?list=PL71i23QiQd9VSrHTuXQyiOlLsi8NnGbSp";
  var cfg = window.TTM_CONFIG || {};
  var wa = cfg.WHATSAPP_NUMBER || "917848942021";

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  document.querySelectorAll(".ttm-optin-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var d = new FormData(form);
      var name = String(d.get("name") || "").trim();
      var source = form.getAttribute("data-source") || "blog";
      if (window.ttmSend) {
        window.ttmSend({
          type: "lead",
          name: name,
          phone: String(d.get("phone") || ""),
          email: String(d.get("email") || ""),
          status: "Blog opt-in (free kit)",
          program: source
        });
      }
      if (window.ttmTrack) window.ttmTrack("lead", { content_name: source, lead_status: "blog_optin" });

      var msg = "Hi Anshuman, I'm " + name + ". Please send me the free SAP MM/EWM kit (from " + document.title + ").";
      var done = form.parentNode.querySelector(".ttm-optin-done");
      form.hidden = true;
      if (done) {
        done.hidden = false;
        done.innerHTML =
          "<p>Thanks " + esc(name) + "! Here's your free course playlist:</p>" +
          '<p><a class="btn btn-primary" href="' + PLAYLIST + '" target="_blank" rel="noopener">Watch the free SAP playlist</a></p>' +
          '<p><a class="btn btn-outline" href="https://wa.me/' + wa + "?text=" + encodeURIComponent(msg) +
          '" target="_blank" rel="noopener">Get the interview kit on WhatsApp</a></p>';
      }
    });
  });

  // Reading progress bar
  var bar = document.getElementById("reading-progress-bar");
  if (bar) {
    window.addEventListener("scroll", function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    }, { passive: true });
  }
})();
