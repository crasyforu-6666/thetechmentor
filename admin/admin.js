/**
 * Admin Dashboard Engine for theTechMentor (youronementor.com)
 */
(function () {
  "use strict";

  const ADMIN_PASS_KEY = "ttm_admin_pwd";
  const DEFAULT_PASS = "admin@youronementor2026";
  const SESSION_KEY = "ttm_admin_authenticated";

  // Storage Keys
  const SALES_KEY = "ttm_admin_sales";
  const TRAFFIC_KEY = "ttm_admin_traffic";
  const COURSES_KEY = "ttm_admin_courses";
  const BLOGS_KEY = "ttm_admin_custom_blogs";
  const LEADS_KEY = "ttm_admin_leads";

  // Initialize Default Courses
  const defaultCourses = [
    {
      id: "mm-self-paced",
      name: "SAP MM Materials Management (Self-Paced)",
      category: "Self-Paced",
      price: 4999,
      originalPrice: 9999,
      status: "Active",
      hours: "35+ Hours"
    },
    {
      id: "ewm-self-paced",
      name: "SAP EWM Extended Warehouse (Self-Paced)",
      category: "Self-Paced",
      price: 6999,
      originalPrice: 12999,
      status: "Active",
      hours: "40+ Hours"
    },
    {
      id: "bundle-self-paced",
      name: "MM + EWM Complete Self-Paced Bundle",
      category: "Self-Paced",
      price: 10999,
      originalPrice: 18999,
      status: "Active",
      hours: "70+ Hours"
    },
    {
      id: "mm-live-batch",
      name: "SAP MM S/4HANA Weekend Live Batch",
      category: "Live Batch",
      price: 24999,
      originalPrice: 35000,
      status: "Active",
      hours: "10-12 Weeks"
    },
    {
      id: "ewm-live-batch",
      name: "SAP EWM S/4HANA Weekend Live Batch",
      category: "Live Batch",
      price: 29999,
      originalPrice: 40000,
      status: "Active",
      hours: "10-12 Weeks"
    },
    {
      id: "bundle-live-batch",
      name: "SAP MM + EWM Complete Live Combo",
      category: "Live Batch",
      price: 43999,
      originalPrice: 55000,
      status: "Active",
      hours: "20 Weeks"
    },
    {
      id: "mentorship-placement",
      name: "1-on-1 Placement Mentorship & Career Switch",
      category: "Mentorship",
      price: 25000,
      originalPrice: 35000,
      status: "Active",
      hours: "Personalized"
    }
  ];

  // Default Seed Sales
  const defaultSales = [
    {
      id: "pay_R8z2kd91",
      date: "2026-08-16 14:15",
      name: "Rahul Sharma",
      email: "rahul.sharma88@gmail.com",
      phone: "+91 98234 11200",
      course: "MM + EWM Complete Self-Paced Bundle",
      amount: 10999,
      status: "Paid",
      method: "UPI (Razorpay)"
    },
    {
      id: "pay_K72jd002",
      date: "2026-08-15 19:40",
      name: "Vikas Patel",
      email: "vikas.patel@tcs.com",
      phone: "+91 97120 44589",
      course: "SAP EWM Extended Warehouse (Self-Paced)",
      amount: 6999,
      status: "Paid",
      method: "Card (Razorpay)"
    },
    {
      id: "pay_M98xc411",
      date: "2026-08-14 11:20",
      name: "Ananya Mishra",
      email: "ananya.mishra@accenture.com",
      phone: "+91 99341 88721",
      course: "SAP MM S/4HANA Weekend Live Batch",
      amount: 24999,
      status: "Paid",
      method: "NetBanking (Razorpay)"
    },
    {
      id: "pay_L41op992",
      date: "2026-08-13 16:50",
      name: "Deepak S.",
      email: "deepak.sundaram@gmail.com",
      phone: "+91 98401 22910",
      course: "SAP MM Materials Management (Self-Paced)",
      amount: 4999,
      status: "Paid",
      method: "UPI (Razorpay)"
    }
  ];

  // Default Seed Candidate Leads
  const defaultLeads = [
    {
      id: "lead_01",
      date: "2026-08-16 12:45",
      name: "Pooja Hegde",
      email: "pooja.hegde@wipro.com",
      phone: "9876543210",
      module: "SAP MM Live",
      experience: "2-5 Years (Looking to Switch to S/4HANA)",
      budget: "Yes",
      status: "Qualified"
    },
    {
      id: "lead_02",
      date: "2026-08-15 18:20",
      name: "Suresh Reddy",
      email: "suresh.reddy@gmail.com",
      phone: "9123456780",
      module: "1-on-1 Mentorship",
      experience: "Domain Logistics Professional",
      budget: "Yes",
      status: "Qualified"
    },
    {
      id: "lead_03",
      date: "2026-08-14 09:10",
      name: "Arun Kumar",
      email: "arun.k@gmail.com",
      phone: "9988776655",
      module: "SAP EWM Live",
      experience: "Fresher / College Graduate",
      budget: "No",
      status: "Self-Paced Redirected"
    }
  ];

  // Global Helpers
  function getStoredPassword() {
    return localStorage.getItem(ADMIN_PASS_KEY) || DEFAULT_PASS;
  }

  function getSales() {
    const raw = localStorage.getItem(SALES_KEY);
    return raw ? JSON.parse(raw) : defaultSales;
  }

  function saveSales(sales) {
    localStorage.setItem(SALES_KEY, JSON.stringify(sales));
  }

  function getCourses() {
    const raw = localStorage.getItem(COURSES_KEY);
    return raw ? JSON.parse(raw) : defaultCourses;
  }

  function saveCourses(courses) {
    localStorage.setItem(COURSES_KEY, JSON.stringify(courses));
  }

  function getLeads() {
    const raw = localStorage.getItem(LEADS_KEY);
    return raw ? JSON.parse(raw) : defaultLeads;
  }

  function getTraffic() {
    const raw = localStorage.getItem(TRAFFIC_KEY);
    if (raw) return JSON.parse(raw);
    return {
      totalVisits: 1480,
      uniqueVisitors: 920,
      checkoutClicks: 142,
      leadsSubmitted: 38,
      todayVisits: 84
    };
  }

  // Authentication logic
  function checkAuth() {
    const authOverlay = document.getElementById("login-modal");
    const isAuthed = sessionStorage.getItem(SESSION_KEY) === "true";
    if (isAuthed) {
      if (authOverlay) authOverlay.style.display = "none";
      initDashboard();
    } else {
      if (authOverlay) authOverlay.style.display = "flex";
    }
  }

  function login(pass) {
    if (pass === getStoredPassword()) {
      sessionStorage.setItem(SESSION_KEY, "true");
      checkAuth();
    } else {
      alert("❌ Incorrect Admin Password. Please try again.");
    }
  }

  function logout() {
    sessionStorage.removeItem(SESSION_KEY);
    window.location.reload();
  }

  // Navigation Tabs Switching
  function setupNavigation() {
    const navButtons = document.querySelectorAll(".nav-item-btn");
    const panes = document.querySelectorAll(".tab-pane");
    const pageTitle = document.getElementById("admin-page-title");

    navButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetTab = btn.dataset.tab;
        navButtons.forEach(b => b.classList.remove("active"));
        panes.forEach(p => p.classList.remove("active"));

        btn.classList.add("active");
        const activePane = document.getElementById(`tab-${targetTab}`);
        if (activePane) activePane.classList.add("active");

        if (pageTitle) {
          pageTitle.textContent = btn.innerText.trim();
        }
      });
    });
  }

  // Render Overview Stats & Sales
  function renderOverview() {
    const sales = getSales();
    const traffic = getTraffic();
    const leads = getLeads();

    const totalRevenue = sales.reduce((acc, s) => acc + (s.amount || 0), 0);
    const totalEnrollments = sales.length;
    const aov = totalEnrollments ? Math.round(totalRevenue / totalEnrollments) : 0;
    const conversionRate = traffic.totalVisits ? ((totalEnrollments / traffic.totalVisits) * 100).toFixed(1) : "3.2";

    // Update KPI UI
    const revEl = document.getElementById("kpi-revenue");
    const enrollEl = document.getElementById("kpi-enrollments");
    const visitsEl = document.getElementById("kpi-visits");
    const convEl = document.getElementById("kpi-conversion");

    if (revEl) revEl.textContent = `₹${totalRevenue.toLocaleString("en-IN")}`;
    if (enrollEl) enrollEl.textContent = `${totalEnrollments} Students`;
    if (visitsEl) visitsEl.textContent = `${traffic.totalVisits.toLocaleString("en-IN")}`;
    if (convEl) convEl.textContent = `${conversionRate}%`;

    // Render Recent Sales in Overview Table
    const recentTable = document.getElementById("recent-sales-tbody");
    if (recentTable) {
      recentTable.innerHTML = sales.slice(0, 5).map(s => `
        <tr>
          <td><strong>${s.name}</strong><br><small style="color:var(--admin-muted);">${s.email}</small></td>
          <td>${s.course}</td>
          <td><strong>₹${(s.amount || 0).toLocaleString("en-IN")}</strong></td>
          <td><span class="status-pill status-paid">${s.status}</span></td>
          <td>${s.date}</td>
        </tr>
      `).join('');
    }

    // Render Full Sales Table
    const fullSalesTable = document.getElementById("full-sales-tbody");
    if (fullSalesTable) {
      fullSalesTable.innerHTML = sales.map(s => `
        <tr>
          <td><code>${s.id}</code></td>
          <td><strong>${s.name}</strong></td>
          <td>${s.email}<br><small style="color:var(--admin-muted);">${s.phone || '-'}</small></td>
          <td>${s.course}</td>
          <td><strong>₹${(s.amount || 0).toLocaleString("en-IN")}</strong></td>
          <td>${s.method || 'Razorpay'}</td>
          <td><span class="status-pill status-paid">${s.status}</span></td>
          <td>${s.date}</td>
        </tr>
      `).join('');
    }

    // Render Leads Table
    const leadsTable = document.getElementById("leads-tbody");
    if (leadsTable) {
      leadsTable.innerHTML = leads.map(l => {
        const cleanPhone = (l.phone || "").replace(/[^0-9]/g, "");
        const waLink = `https://wa.me/91${cleanPhone}?text=Hi%20${encodeURIComponent(l.name)},%20this%20is%20Anshuman%20from%20theTechMentor.%20I%20reviewed%20your%20application%20for%20${encodeURIComponent(l.module)}!`;
        return `
          <tr>
            <td><strong>${l.name}</strong><br><small style="color:var(--admin-muted);">${l.email}</small></td>
            <td>${l.phone}</td>
            <td>${l.module}</td>
            <td>${l.experience}</td>
            <td>
              <span class="status-pill ${l.budget === 'Yes' ? 'status-qualified' : 'status-browsing'}">
                ${l.budget === 'Yes' ? '✅ Budget Ready' : 'Browsing'}
              </span>
            </td>
            <td>
              <a href="${waLink}" target="_blank" class="action-btn action-btn-green">
                WhatsApp ↗
              </a>
              <a href="tel:${cleanPhone}" class="action-btn" style="margin-left:0.3rem;">
                Call
              </a>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  // Render Course & Pricing Manager
  function renderCourses() {
    const courses = getCourses();
    const tbody = document.getElementById("courses-tbody");
    if (!tbody) return;

    tbody.innerHTML = courses.map((c, index) => `
      <tr>
        <td><strong>${c.name}</strong><br><small style="color:var(--admin-muted);">${c.category} · ${c.hours}</small></td>
        <td>
          <input type="number" id="course-price-${index}" class="admin-input" value="${c.price}" style="width:110px; display:inline-block;" />
        </td>
        <td>
          <input type="number" id="course-oldprice-${index}" class="admin-input" value="${c.originalPrice || c.price}" style="width:110px; display:inline-block;" />
        </td>
        <td><span class="status-pill status-paid">${c.status}</span></td>
        <td>
          <button type="button" class="action-btn action-btn-green" onclick="window.saveCoursePrice(${index})">
            Save Price
          </button>
        </td>
      </tr>
    `).join('');
  }

  // Global methods for pricing & actions
  window.saveCoursePrice = function (index) {
    const courses = getCourses();
    const newPrice = parseInt(document.getElementById(`course-price-${index}`).value, 10);
    const newOldPrice = parseInt(document.getElementById(`course-oldprice-${index}`).value, 10);

    if (isNaN(newPrice) || newPrice <= 0) {
      alert("Please enter a valid price amount.");
      return;
    }

    courses[index].price = newPrice;
    courses[index].originalPrice = newOldPrice;
    saveCourses(courses);
    alert(`🎉 Price for "${courses[index].name}" updated to ₹${newPrice.toLocaleString('en-IN')}!`);
    renderCourses();
  };

  window.exportSalesCSV = function () {
    const sales = getSales();
    let csv = "Transaction ID,Student Name,Email,Phone,Course,Amount,Payment Method,Status,Date\n";
    sales.forEach(s => {
      csv += `"${s.id}","${s.name}","${s.email}","${s.phone || ''}","${s.course}","${s.amount}","${s.method || 'Razorpay'}","${s.status}","${s.date}"\n`;
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `theTechMentor_Sales_${new Date().toISOString().split("T")[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Blog CMS Publisher
  function setupBlogCMS() {
    const form = document.getElementById("admin-new-blog-form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const title = document.getElementById("blog-input-title").value.trim();
      const category = document.getElementById("blog-input-category").value;
      const readTime = document.getElementById("blog-input-time").value.trim();
      const excerpt = document.getElementById("blog-input-excerpt").value.trim();
      const content = document.getElementById("blog-input-content").value.trim();

      if (!title || !content) {
        alert("Please provide at least a title and article content.");
        return;
      }

      const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
      const newPost = {
        id: "post_" + Date.now(),
        title: title,
        slug: slug,
        category: category,
        readTime: readTime || "8 min read",
        excerpt: excerpt,
        content: content,
        date: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
      };

      const customBlogs = JSON.parse(localStorage.getItem(BLOGS_KEY) || "[]");
      customBlogs.unshift(newPost);
      localStorage.setItem(BLOGS_KEY, JSON.stringify(customBlogs));

      alert(`🎉 Blog article "${title}" published successfully!`);
      form.reset();
      renderCustomBlogsList();
    });
  }

  function renderCustomBlogsList() {
    const listContainer = document.getElementById("admin-custom-blogs-list");
    if (!listContainer) return;
    const customBlogs = JSON.parse(localStorage.getItem(BLOGS_KEY) || "[]");

    if (customBlogs.length === 0) {
      listContainer.innerHTML = `<div style="color:var(--admin-muted); font-size:0.9rem;">No custom articles published yet. Use the form above to add your first post!</div>`;
      return;
    }

    listContainer.innerHTML = customBlogs.map((b, i) => `
      <div class="card-panel" style="margin-bottom:1rem; padding:1.25rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <span class="status-pill status-qualified" style="margin-bottom:0.4rem;">${b.category}</span>
            <h4 style="color:#fff; font-size:1.1rem; margin-bottom:0.3rem;">${b.title}</h4>
            <p style="color:var(--admin-muted); font-size:0.85rem;">${b.date} · ${b.readTime}</p>
          </div>
          <button type="button" class="action-btn" style="color:#ef4444; border-color:#ef4444;" onclick="window.deleteCustomBlog(${i})">Delete</button>
        </div>
      </div>
    `).join('');
  }

  window.deleteCustomBlog = function (index) {
    if (confirm("Are you sure you want to delete this article?")) {
      const customBlogs = JSON.parse(localStorage.getItem(BLOGS_KEY) || "[]");
      customBlogs.splice(index, 1);
      localStorage.setItem(BLOGS_KEY, JSON.stringify(customBlogs));
      renderCustomBlogsList();
    }
  };

  // Change Password
  function setupSettings() {
    const pwdForm = document.getElementById("change-password-form");
    if (!pwdForm) return;

    pwdForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const current = document.getElementById("curr-pwd").value;
      const newPwd = document.getElementById("new-pwd").value;

      if (current !== getStoredPassword()) {
        alert("Current password is incorrect.");
        return;
      }
      if (newPwd.length < 6) {
        alert("New password must be at least 6 characters.");
        return;
      }

      localStorage.setItem(ADMIN_PASS_KEY, newPwd);
      alert("✅ Admin Password updated successfully!");
      pwdForm.reset();
    });
  }

  function initDashboard() {
    setupNavigation();
    renderOverview();
    renderCourses();
    setupBlogCMS();
    renderCustomBlogsList();
    setupSettings();
  }

  // DOM Loaded Event Listener
  document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("admin-login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const pass = document.getElementById("admin-password-input").value;
        login(pass);
      });
    }

    const logoutBtn = document.getElementById("admin-logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", logout);
    }

    checkAuth();
  });
})();
