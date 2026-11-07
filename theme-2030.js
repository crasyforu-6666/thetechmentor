/* 2030 theme: gentle fade-up of cards and section headers as they scroll into view. */
(function () {
  "use strict";
  if (!("IntersectionObserver" in window)) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var targets = document.querySelectorAll(
    ".section-header, .nurture-header, .course-card, .pricing-card, .feature-card, .testimonial, " +
    ".outcome-card, .sp-card, .blog-card, .faq-item, .instructor-grid > *, .final-cta .container"
  );
  if (!targets.length) return;
  document.documentElement.classList.add("t-anim");

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("t-in");
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

  targets.forEach(function (el, i) {
    el.classList.add("t-reveal");
    // stagger siblings slightly
    var idx = Array.prototype.indexOf.call(el.parentNode.children, el);
    el.style.transitionDelay = Math.min(idx, 5) * 70 + "ms";
    io.observe(el);
  });

})();
