(function () {
  "use strict";

  const RAZORPAY_URL = "https://razorpay.me/@anshumanbehuria";
  const YOUTUBE_PLAYLIST = "https://www.youtube.com/playlist?list=PL71i23QiQd9VSrHTuXQyiOlLsi8NnGbSp";

  document.querySelectorAll(".razorpay-link").forEach((link) => {
    link.href = RAZORPAY_URL;
  });

  const playlistYoutubeLink = document.getElementById("playlist-youtube-link");
  if (playlistYoutubeLink && playlistYoutubeLink.getAttribute("href") === "#") {
    playlistYoutubeLink.href = YOUTUBE_PLAYLIST;
  }

  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });

    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  const tabs = document.querySelectorAll(".tab");
  const panels = {
    mm: document.getElementById("panel-mm"),
    ewm: document.getElementById("panel-ewm"),
  };

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.dataset.tab;
      tabs.forEach((t) => {
        t.classList.toggle("active", t === tab);
        t.setAttribute("aria-selected", String(t === tab));
      });
      Object.entries(panels).forEach(([key, panel]) => {
        if (!panel) return;
        const active = key === target;
        panel.classList.toggle("active", active);
        panel.hidden = !active;
      });
    });
  });

  const formatTabs = document.querySelectorAll(".format-tab");
  const pricingLive = document.getElementById("pricing-live");
  const pricingSelf = document.getElementById("pricing-self");

  formatTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const isLive = tab.dataset.format === "live";
      formatTabs.forEach((t) => {
        const active = t === tab;
        t.classList.toggle("active", active);
        t.setAttribute("aria-selected", String(active));
      });
      if (pricingLive) {
        pricingLive.hidden = !isLive;
        pricingLive.classList.toggle("active", isLive);
      }
      if (pricingSelf) {
        pricingSelf.hidden = isLive;
        pricingSelf.classList.toggle("active", !isLive);
      }
    });
  });

  const track = document.getElementById("slides-track");
  const slides = track ? [...track.querySelectorAll(".info-slide")] : [];
  const prevBtn = document.querySelector(".slide-prev");
  const nextBtn = document.querySelector(".slide-next");
  const currentEl = document.getElementById("slide-current");
  const totalEl = document.getElementById("slide-total");
  const dotsContainer = document.getElementById("slide-dots");
  let slideIndex = 0;

  if (totalEl) totalEl.textContent = String(slides.length);

  function goToSlide(index) {
    if (!slides.length) return;
    slideIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      slide.hidden = i !== slideIndex;
    });
    if (currentEl) currentEl.textContent = String(slideIndex + 1);
    dotsContainer?.querySelectorAll("button").forEach((dot, i) => {
      dot.classList.toggle("active", i === slideIndex);
      dot.setAttribute("aria-selected", String(i === slideIndex));
    });
  }

  if (slides.length) {
    goToSlide(0);
  }

  if (dotsContainer && slides.length) {
    slides.forEach((_, i) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.setAttribute("role", "tab");
      dot.setAttribute("aria-label", `Slide ${i + 1}`);
      if (i === 0) dot.classList.add("active");
      dot.addEventListener("click", () => goToSlide(i));
      dotsContainer.appendChild(dot);
    });
  }

  prevBtn?.addEventListener("click", () => goToSlide(slideIndex - 1));
  nextBtn?.addEventListener("click", () => goToSlide(slideIndex + 1));

  const funnelSteps = document.querySelectorAll(".funnel-step");
  const learnSection = document.getElementById("learn");
  const videoSection = document.getElementById("course-video");
  const enrollSection = document.getElementById("enroll");

  function setFunnelStep(step) {
    funnelSteps.forEach((el) => {
      el.classList.toggle("active", el.dataset.step === String(step));
    });
  }

  function updateFunnelFromScroll() {
    const mid = window.innerHeight * 0.4;
    const sections = [
      { el: enrollSection, step: 3 },
      { el: videoSection, step: 2 },
      { el: learnSection, step: 1 },
    ];
    for (const { el, step } of sections) {
      if (!el) continue;
      const rect = el.getBoundingClientRect();
      if (rect.top < mid && rect.bottom > mid) {
        setFunnelStep(step);
        return;
      }
    }
  }

  if (funnelSteps.length) {
    updateFunnelFromScroll();
    let funnelTicking = false;
    window.addEventListener(
      "scroll",
      () => {
        if (funnelTicking) return;
        funnelTicking = true;
        window.requestAnimationFrame(() => {
          updateFunnelFromScroll();
          funnelTicking = false;
        });
      },
      { passive: true }
    );
  }

  const courseSelect = document.getElementById("course");
  const sourceSelect = document.getElementById("source");

  document.querySelectorAll("[data-course]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const value = btn.getAttribute("data-course");
      if (courseSelect && value) courseSelect.value = value;
    });
  });

  const params = new URLSearchParams(window.location.search);
  if (sourceSelect) {
    const utm = params.get("utm_source") || params.get("source");
    if (utm && /meta|facebook|instagram|fb|ig/i.test(utm)) {
      sourceSelect.value = "Meta Ads";
    }
  }

  const form = document.getElementById("enroll-form");
  const successMsg = document.getElementById("form-success");

  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      const data = Object.fromEntries(new FormData(form));
      console.log("Enrollment request:", data);
      form.reset();
      if (successMsg) {
        successMsg.hidden = false;
        window.setTimeout(() => {
          successMsg.hidden = true;
        }, 8000);
      }
    });
  }

  const header = document.querySelector(".header");
  if (header) {
    let scrollTicking = false;
    const updateHeader = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 20);
      scrollTicking = false;
    };
    updateHeader();
    window.addEventListener(
      "scroll",
      () => {
        if (scrollTicking) return;
        scrollTicking = true;
        window.requestAnimationFrame(updateHeader);
      },
      { passive: true }
    );
  }

  function blogFilter(cat, btn) {
    document.querySelectorAll(".blog-tab").forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    if (btn) {
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
    }

    document.querySelectorAll("#blog-grid .blog-card").forEach((card) => {
      if (cat === "all" || card.dataset.cat === cat) {
        card.style.display = "flex";
      } else {
        card.style.display = "none";
      }
    });
  }

  document.querySelector(".blog-tabs")?.addEventListener("click", (event) => {
    const btn = event.target.closest(".blog-tab");
    if (!btn) return;
    blogFilter(btn.dataset.blogCat || "all", btn);
  });

  window.blogFilter = blogFilter;

  /* ==========================================================================
     High-Ticket Funnel & Pre-Qualification Screening Logic
     ========================================================================== */

  // VSL Play Button
  const vslPlayBtn = document.getElementById("vsl-play-btn");
  const vslPoster = document.getElementById("vsl-poster");
  const vslWrapper = document.getElementById("vsl-video-wrapper");

  if (vslPlayBtn && vslPoster && vslWrapper) {
    vslPlayBtn.addEventListener("click", () => {
      vslPoster.hidden = true;
      vslWrapper.hidden = false;
    });
  }

  // Screening Modal logic
  const modalBackdrop = document.getElementById("screening-modal-backdrop");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalProgramLabel = document.getElementById("modal-selected-program");
  const modalForm = document.getElementById("modal-screening-form");
  const modalResult = document.getElementById("modal-routing-result");

  function openScreeningModal(programName) {
    if (!modalBackdrop) return;
    if (modalProgramLabel) {
      modalProgramLabel.textContent = programName || "Strategy Call (15-Min)";
    }
    if (modalForm) {
      modalForm.reset();
      modalForm.hidden = false;
    }
    if (modalResult) {
      modalResult.hidden = true;
      modalResult.innerHTML = "";
    }
    modalBackdrop.hidden = false;
  }

  function closeScreeningModal() {
    if (modalBackdrop) {
      modalBackdrop.hidden = true;
    }
  }

  document.querySelectorAll(".open-screening-modal").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const program = btn.getAttribute("data-program") || "Strategy Call (15-Min)";
      openScreeningModal(program);
    });
  });

  modalCloseBtn?.addEventListener("click", closeScreeningModal);

  modalBackdrop?.addEventListener("click", (e) => {
    if (e.target === modalBackdrop) {
      closeScreeningModal();
    }
  });

  // Pre-qualification Routing Form Handler (Shared for page form & modal form)
  function handleScreeningSubmit(e, formEl, outputEl) {
    e.preventDefault();
    if (!formEl.checkValidity()) {
      formEl.reportValidity();
      return;
    }

    const formData = new FormData(formEl);
    const budget = formData.get("budget");
    const name = formData.get("name") || "Applicant";

    console.log("Pre-qualification submission:", Object.fromEntries(formData));

    formEl.hidden = true;
    outputEl.hidden = false;

    if (budget === "Yes") {
      outputEl.innerHTML = `
        <div class="routing-card routing-success">
          <h4>🎉 Candidate Pre-Qualified!</h4>
          <p>Congratulations ${name}! Based on your experience and commitment, your application is approved for a 15-minute Strategy Call with Anshuman Behuria.</p>
          <a href="https://wa.me/918895077943?text=Hi%20Anshuman,%20my%20application%20is%20approved.%20I%20want%20to%20schedule%20my%2015-min%20strategy%20call." target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-block">Confirm Strategy Call Slot on WhatsApp ↗</a>
          <p style="margin-top: 0.75rem; font-size: 0.85rem;">🔓 <strong>Curriculum Playlist Unlocked:</strong> <a href="https://www.youtube.com/playlist?list=PL71i23QiQd9VSrHTuXQyiOlLsi8NnGbSp" target="_blank" rel="noopener noreferrer" style="color: #3db8f5; text-decoration: underline;">Access 40+ Module Video Library ↗</a></p>
        </div>
      `;
    } else {
      outputEl.innerHTML = `
        <div class="routing-card routing-redirect">
          <h4>Notice: Self-Paced Track Recommended</h4>
          <p>Thank you for your response, ${name}! Live 1-on-1 strategy call slots are reserved for candidates ready to invest in live mentorship. Based on your budget readiness, our ₹4,999 Self-Paced Bundle is the best fit for your journey.</p>
          <a href="${RAZORPAY_URL}" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-block razorpay-link">Enroll in Self-Paced Track (₹4,999) ↗</a>
          <p style="margin-top: 0.75rem; font-size: 0.85rem;">🔓 <strong>Free Video Access:</strong> <a href="https://www.youtube.com/playlist?list=PL71i23QiQd9VSrHTuXQyiOlLsi8NnGbSp" target="_blank" rel="noopener noreferrer" style="color: #3db8f5; text-decoration: underline;">Watch Free Video Playlist on YouTube ↗</a></p>
        </div>
      `;
    }
  }

  const pageForm = document.getElementById("enroll-form");
  const pageOutput = document.getElementById("screening-routing-output");

  pageForm?.addEventListener("submit", (e) => {
    if (pageOutput) {
      handleScreeningSubmit(e, pageForm, pageOutput);
    }
  });

  modalForm?.addEventListener("submit", (e) => {
    if (modalResult) {
      handleScreeningSubmit(e, modalForm, modalResult);
    }
  });
})();
