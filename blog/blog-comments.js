/**
 * Interactive Community Q&A and Commenting Engine for theTechMentor Blog
 */
(function () {
  "use strict";

  // Reading progress bar updater
  window.addEventListener("scroll", () => {
    const bar = document.getElementById("reading-progress-bar");
    if (!bar) return;
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    bar.style.width = scrolled + "%";
  });

  const getArticleSlug = () => {
    const path = window.location.pathname.replace(/\/$/, "");
    const parts = path.split("/");
    return parts[parts.length - 1] || "general-article";
  };

  const getStorageKey = (slug) => `ttm_comments_${slug}`;

  // Default seed questions/comments for active feel
  const defaultSeeds = {
    "top-30-sap-mm-interview-questions-2026.html": [
      {
        id: "c1",
        author: "Vikram Rajput",
        role: "student",
        text: "Question #14 on OBYC automatic account determination was asked word-for-word in my recent interview with Capgemini! The Valuation Class breakdown helped me clear round 2.",
        time: "3 days ago",
        upvotes: 14,
        replies: [
          {
            id: "r1",
            author: "Anshuman Behuria",
            role: "instructor",
            text: "Congratulations Vikram! OBYC is hands down the #1 filter question interviewers use to distinguish real consultants from theoretical candidates. Best of luck for your final partner round!",
            time: "2 days ago",
            upvotes: 8
          }
        ]
      },
      {
        id: "c2",
        author: "Siddharth Verma",
        role: "student",
        text: "Sir, what is the best way to explain the difference between Split Valuation and Batch Management when an interviewer asks how to track procurement costs per consignment?",
        time: "1 day ago",
        upvotes: 6,
        replies: [
          {
            id: "r2",
            author: "Anshuman Behuria",
            role: "instructor",
            text: "Great question Siddharth! Key distinction: Split Valuation values the same material differently (e.g. In-house vs External, New vs Refurbished) at the valuation area level. Batch Management tracks homogeneous production/procurement lots for expiry/properties. I've covered a dedicated 20-min deep dive on this in Module 4 of the Self-Paced MM Track!",
            time: "18 hours ago",
            upvotes: 5
          }
        ]
      }
    ],
    "configure-purchase-order-cycle-s4hana.html": [
      {
        id: "c1",
        author: "Pooja Hegde",
        role: "student",
        text: "The diagram of the 3-Way Match (PO -> MIGO Movement 101 -> MIRO) made the GR/IR clearing process so clear. Thank you!",
        time: "4 days ago",
        upvotes: 11,
        replies: [
          {
            id: "r1",
            author: "Anshuman Behuria",
            role: "instructor",
            text: "Glad it helped, Pooja! Make sure you practice posting an invoice price variance in MIRO to see how PRD accounts get triggered.",
            time: "3 days ago",
            upvotes: 4
          }
        ]
      }
    ],
    "sap-mm-vs-ewm-career-guide.html": [
      {
        id: "c1",
        author: "Arjun K.",
        role: "student",
        text: "I currently have 2 years of MM support experience. Is it better to transition to EWM or master S/4HANA Sourcing first?",
        time: "2 days ago",
        upvotes: 9,
        replies: [
          {
            id: "r1",
            author: "Anshuman Behuria",
            role: "instructor",
            text: "Arjun, with 2 years of MM under your belt, learning EWM will make you an indispensable end-to-end logistics consultant. Most Tier-1 MNCs are desperately looking for dual MM+EWM profiles for warehouse digital transformations.",
            time: "1 day ago",
            upvotes: 7
          }
        ]
      }
    ]
  };

  function loadComments(slug) {
    const raw = localStorage.getItem(getStorageKey(slug));
    if (raw) {
      try {
        return JSON.parse(raw);
      } catch (e) {
        console.error(e);
      }
    }
    return defaultSeeds[slug] || [
      {
        id: "default_seed",
        author: "Rajesh Nair",
        role: "student",
        text: "Very practical explanation! Really appreciate the step-by-step breakdown and configuration tips.",
        time: "2 days ago",
        upvotes: 5,
        replies: [
          {
            id: "rep_inst",
            author: "Anshuman Behuria",
            role: "instructor",
            text: "Thanks Rajesh! Feel free to ask any specific configuration or real-time project doubts right here.",
            time: "1 day ago",
            upvotes: 3
          }
        ]
      }
    ];
  }

  function saveComments(slug, comments) {
    localStorage.setItem(getStorageKey(slug), JSON.stringify(comments));
  }

  function renderComments(containerId, comments, slug) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const countBadge = document.getElementById("comments-count");
    if (countBadge) {
      let total = comments.length;
      comments.forEach(c => total += (c.replies ? c.replies.length : 0));
      countBadge.textContent = `${total} Discussions`;
    }

    if (comments.length === 0) {
      container.innerHTML = `<div style="text-align:center; padding: 2rem; color: var(--blog-muted);">No questions or comments yet. Be the first to ask! 🚀</div>`;
      return;
    }

    container.innerHTML = comments.map(c => `
      <div class="comment-item" id="comment-${c.id}">
        <div class="comment-item-header">
          <div class="comment-user-wrap">
            <div class="user-avatar ${c.role === 'instructor' ? 'instructor-avatar' : ''}">
              ${c.role === 'instructor' ? 'AB' : (c.author.substring(0, 2).toUpperCase())}
            </div>
            <div class="user-meta">
              <strong>
                ${escapeHtml(c.author)}
                ${c.role === 'instructor' ? '<span class="instructor-badge-tag">Instructor</span>' : ''}
              </strong>
              <div class="comment-time">${c.time}</div>
            </div>
          </div>
        </div>
        <div class="comment-body">${escapeHtml(c.text)}</div>
        <div class="comment-actions">
          <button type="button" class="comment-vote-btn" onclick="window.upvoteComment('${slug}', '${c.id}')">
            ▲ Helpful (${c.upvotes || 0})
          </button>
          <button type="button" class="reply-btn" onclick="window.toggleReplyBox('${c.id}')">
            Reply / Answer
          </button>
        </div>

        <!-- Inline Reply Input Box (Hidden by default) -->
        <div id="reply-box-${c.id}" class="reply-input-box" style="display:none;">
          <input type="text" id="reply-name-${c.id}" class="comment-input" placeholder="Your Name" style="margin-bottom:0.5rem;" />
          <textarea id="reply-text-${c.id}" class="comment-textarea" placeholder="Write your reply or follow-up question..."></textarea>
          <div style="display:flex; justify-content:flex-end; gap:0.5rem;">
            <button type="button" class="btn btn-sm" style="background:#334155;" onclick="window.toggleReplyBox('${c.id}')">Cancel</button>
            <button type="button" class="comment-submit-btn" style="padding:0.4rem 1rem;" onclick="window.submitReply('${slug}', '${c.id}')">Post Reply</button>
          </div>
        </div>

        ${c.replies && c.replies.length > 0 ? `
          <div class="replies-container">
            ${c.replies.map(r => `
              <div class="reply-item">
                <div class="comment-item-header">
                  <div class="comment-user-wrap">
                    <div class="user-avatar ${r.role === 'instructor' ? 'instructor-avatar' : ''}">
                      ${r.role === 'instructor' ? 'AB' : (r.author.substring(0, 2).toUpperCase())}
                    </div>
                    <div class="user-meta">
                      <strong>
                        ${escapeHtml(r.author)}
                        ${r.role === 'instructor' ? '<span class="instructor-badge-tag">Instructor</span>' : ''}
                      </strong>
                      <div class="comment-time">${r.time}</div>
                    </div>
                  </div>
                </div>
                <div class="comment-body">${escapeHtml(r.text)}</div>
              </div>
            `).join('')}
          </div>
        ` : ''}
      </div>
    `).join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Global methods
  window.upvoteComment = function (slug, commentId) {
    const comments = loadComments(slug);
    const item = comments.find(c => c.id === commentId);
    if (item) {
      item.upvotes = (item.upvotes || 0) + 1;
      saveComments(slug, comments);
      renderComments("comments-list-container", comments, slug);
    }
  };

  window.toggleReplyBox = function (commentId) {
    const box = document.getElementById(`reply-box-${commentId}`);
    if (box) {
      box.style.display = box.style.display === "none" ? "block" : "none";
    }
  };

  window.submitReply = function (slug, commentId) {
    const nameEl = document.getElementById(`reply-name-${commentId}`);
    const textEl = document.getElementById(`reply-text-${commentId}`);
    if (!nameEl || !textEl) return;

    const name = nameEl.value.trim();
    const text = textEl.value.trim();
    if (!name || !text) {
      alert("Please enter your name and reply message.");
      return;
    }

    const comments = loadComments(slug);
    const item = comments.find(c => c.id === commentId);
    if (item) {
      if (!item.replies) item.replies = [];
      const isInstructor = name.toLowerCase().includes("anshuman") || name.toLowerCase().includes("instructor");
      item.replies.push({
        id: "r_" + Date.now(),
        author: name,
        role: isInstructor ? "instructor" : "student",
        text: text,
        time: "Just now",
        upvotes: 0
      });
      saveComments(slug, comments);
      renderComments("comments-list-container", comments, slug);
    }
  };

  window.initBlogComments = function () {
    const slug = getArticleSlug();
    const comments = loadComments(slug);
    renderComments("comments-list-container", comments, slug);

    const form = document.getElementById("new-comment-form");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        const nameInput = document.getElementById("commenter-name");
        const emailInput = document.getElementById("commenter-email");
        const textInput = document.getElementById("commenter-message");

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const text = textInput.value.trim();

        if (!name || !text) {
          alert("Please fill in your name and question/comment.");
          return;
        }

        const isInstructor = name.toLowerCase().includes("anshuman") || name.toLowerCase().includes("instructor");

        const newComment = {
          id: "c_" + Date.now(),
          author: name,
          email: email,
          role: isInstructor ? "instructor" : "student",
          text: text,
          time: "Just now",
          upvotes: 1,
          replies: []
        };

        const currentComments = loadComments(slug);
        currentComments.unshift(newComment);
        saveComments(slug, currentComments);
        renderComments("comments-list-container", currentComments, slug);

        textInput.value = "";
        alert("🎉 Your comment/question has been published!");
      });
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    window.initBlogComments();
  });
})();
