/*
 * Analytics + lead delivery helpers. Reads IDs from site-config.js.
 * Exposes:
 *   window.ttmTrack(eventName, params)  -> fires Meta Pixel + GA4 events (no-op if not configured)
 *   window.ttmSend(payload)             -> POSTs a lead/sale to LEAD_WEBHOOK_URL (no-op if not configured)
 *   window.ttmUtm()                     -> UTM params captured on landing
 */
(function () {
  "use strict";
  var cfg = window.TTM_CONFIG || {};

  // ---- Meta Pixel ----
  if (cfg.META_PIXEL_ID) {
    /* eslint-disable */
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    /* eslint-enable */
    window.fbq("init", cfg.META_PIXEL_ID);
    window.fbq("track", "PageView");
  }

  // ---- Google Analytics 4 ----
  if (cfg.GA4_ID) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(cfg.GA4_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", cfg.GA4_ID);
  }

  // ---- UTM capture (kept for the session so it survives in-page navigation) ----
  var UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid"];
  function readUtm() {
    var stored = {};
    try { stored = JSON.parse(sessionStorage.getItem("ttm_utm") || "{}"); } catch (e) {}
    var params = new URLSearchParams(window.location.search);
    var changed = false;
    UTM_KEYS.forEach(function (k) {
      if (params.get(k)) { stored[k] = params.get(k); changed = true; }
    });
    if (changed) { try { sessionStorage.setItem("ttm_utm", JSON.stringify(stored)); } catch (e) {} }
    return stored;
  }
  var utm = readUtm();
  window.ttmUtm = function () { return utm; };

  // Map our event names to Meta standard events / GA4 recommended events.
  var META_MAP = { lead: "Lead", begin_checkout: "InitiateCheckout", purchase: "Purchase", contact: "Contact" };

  window.ttmTrack = function (eventName, params) {
    params = params || {};
    try {
      if (window.fbq && META_MAP[eventName]) {
        var metaParams = {};
        if (params.value) { metaParams.value = params.value; metaParams.currency = "INR"; }
        if (params.content_name) metaParams.content_name = params.content_name;
        window.fbq("track", META_MAP[eventName], metaParams);
      }
      if (window.gtag) {
        var gaParams = Object.assign({}, params);
        if (params.value) gaParams.currency = "INR";
        window.gtag("event", eventName, gaParams);
      }
    } catch (e) { console.error(e); }
  };

  window.ttmSend = function (payload) {
    if (!cfg.LEAD_WEBHOOK_URL) return Promise.resolve(false);
    var body = JSON.stringify(Object.assign({
      page: window.location.href,
      submitted_at: new Date().toISOString(),
    }, utm, payload));
    // text/plain avoids a CORS preflight, which Google Apps Script doesn't answer.
    return fetch(cfg.LEAD_WEBHOOK_URL, {
      method: "POST",
      mode: "no-cors",
      keepalive: true,
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: body,
    }).then(function () { return true; }).catch(function (err) {
      console.error(err);
      try { return navigator.sendBeacon(cfg.LEAD_WEBHOOK_URL, body); } catch (e) { return false; }
    });
  };
})();
