/**
 * Admin Dashboard Controller & RBAC Management Engine
 * theTechMentor (youronementor.com)
 */
(function () {
  "use strict";

  // Storage Keys
  const SALES_KEY = "ttm_admin_sales";
  const TRAFFIC_KEY = "ttm_admin_traffic";
  const COURSES_KEY = "ttm_admin_courses";
  const BLOGS_KEY = "ttm_admin_custom_blogs";
  const LEADS_KEY = "ttm_admin_leads";

  // Check RBAC Route Guard
  if (!window.TTM_AUTH || !window.TTM_AUTH.enforceRouteGuard({ allowedRoles: ["admin", "super_admin"] })) {
    return;
  }

  const currentUser = window.TTM_AUTH.getCurrentUser();

  // Initialize Default Courses
  const defaultCourses = [
    { id: "mm-self-paced", name: "SAP MM Materials Management (Self-Paced)", category: "Self-Paced", price: 4999, originalPrice: 9999, status: "Active", hours: "35+ Hours" },
    { id: "ewm-self-paced", name: "SAP EWM Extended Warehouse (Self-Paced)", category: "Self-Paced", price: 6999, originalPrice: 12999, status: "Active", hours: "40+ Hours" },
    { id: "bundle-self-paced", name: "MM + EWM Complete Self-Paced Bundle", category: "Self-Paced", price: 10999, originalPrice: 18999, status: "Active", hours: "70+ Hours" },
    { id: "mm-live-batch", name: "SAP MM S/4HANA Weekend Live Batch", category: "Live Batch", price: 24999, originalPrice: 35000, status: "Active", hours: "10-12 Weeks" },
    { id: "ewm-live-batch", name: "SAP EWM S/4HANA Weekend Live Batch", category: "Live Batch", price: 29999, originalPrice: 40000, status: "Active", hours: "10-12 Weeks" },
    { id: "bundle-live-batch", name: "SAP MM + EWM Complete Live Combo", category: "Live Batch", price: 43999, originalPrice: 55000, status: "Active", hours: "20 Weeks" },
    { id: "mentorship-placement", name: "1-on-1 Placement Mentorship & Career Switch", category: "Mentorship", price: 25000, originalPrice: 35000, status: "Active", hours: "Personalized" }
  ];

  const defaultSales = [
    { id: "pay_R8z2kd91", date: "2026-08-16 14:15", name: "Rahul Sharma", email: "rahul.sharma88@gmail.com", phone: "+91 98234 11200", course: "MM + EWM Complete Self-Paced Bundle", amount: 10999, status: "Paid", method: "UPI (Razorpay)" },
    { id: "pay_K72jd002", date: "2026-08-15 19:40", name: "Vikas Patel", email: "vikas.patel@tcs.com", phone: "+91 97120 44589", course: "SAP EWM Extended Warehouse (Self-Paced)", amount: 6999, status: "Paid", method: "Card (Razorpay)" },
    { id: "pay_M98xc411", date: "2026-08-14 11:20", name: "Ananya Mishra", email: "ananya.mishra@accenture.com", phone: "+91 99341 88721", course: "SAP MM S/4HANA Weekend Live Batch", amount: 24999, status: "Paid", method: "NetBanking (Razorpay)" }
  ];

  const defaultLeads = [
    { id: "lead_01", date: "2026-08-16 12:45", name: "Pooja Hegde", email: "pooja.hegde@wipro.com", phone: "9876543210", module: "SAP MM Live", experience: "2-5 Years", budget: "Yes", status: "Qualified" },
    { id: "lead_02", date: "2026-08-15 18:20", name: "Suresh Reddy", email: "suresh.reddy@gmail.com", phone: "9123456780", module: "1-on-1 Mentorship", experience: "Logistics Pro", budget: "Yes", status: "Qualified" }
  ];

  function getSales() {
    const raw = localStorage.getItem(SALES_KEY);
    return raw ? JSON.parse(raw) : defaultSales;
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
    return raw ? JSON.parse(raw) : { totalVisits: 1480, uniqueVisitors: 920, checkoutClicks: 142, leadsSubmitted: 38, todayVisits: 84 };
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

  // Render Stats & Sales
  function renderOverview() {
    const sales = getSales();
    const traffic = getTraffic();
    const leads = getLeads();

    const totalRevenue = sales.reduce((acc, s) => acc + (s.amount || 0), 0);
    const totalEnrollments = sales.length;
    const conversionRate = traffic.totalVisits ? ((totalEnrollments / traffic.totalVisits) * 100).toFixed(1) : "3.2";

    const revEl = document.getElementById("kpi-revenue");
    const enrollEl = document.getElementById("kpi-enrollments");
    const visitsEl = document.getElementById("kpi-visits");
    const convEl = document.getElementById("kpi-conversion");

    if (revEl) revEl.textContent = `₹${totalRevenue.toLocaleString("en-IN")}`;
    if (enrollEl) enrollEl.textContent = `${totalEnrollments} Students`;
    if (visitsEl) visitsEl.textContent = `${traffic.totalVisits.toLocaleString("en-IN")}`;
    if (convEl) convEl.textContent = `${conversionRate}%`;

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

    const leadsTable = document.getElementById("leads-tbody");
    if (leadsTable) {
      leadsTable.innerHTML = leads.map(l => {
        const cleanPhone = (l.phone || "").replace(/[^0-9]/g, "");
        const waLink = `https://wa.me/91${cleanPhone}?text=Hi%20${encodeURIComponent(l.name)},%20this%20is%20Anshuman%20from%20theTechMentor.`;
        return `
          <tr>
            <td><strong>${l.name}</strong><br><small style="color:var(--admin-muted);">${l.email}</small></td>
            <td>${l.phone}</td>
            <td>${l.module}</td>
            <td>${l.experience}</td>
            <td>
              <span class="status-pill ${l.budget === 'Yes' ? 'status-qualified' : 'status-browsing'}">
                ${l.budget === 'Yes' ? '✅ Qualified' : 'Browsing'}
              </span>
            </td>
            <td>
              <a href="${waLink}" target="_blank" class="action-btn action-btn-green">WhatsApp ↗</a>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  // Render User Management & Teacher Approvals
  function renderUsersAndTeachers() {
    const users = window.TTM_AUTH.getUsers();

    // Render Users Table
    const usersTable = document.getElementById("users-tbody");
    if (usersTable) {
      usersTable.innerHTML = users.map((u, i) => `
        <tr>
          <td><strong>${u.name}</strong><br><small style="color:var(--admin-muted);">${u.email}</small></td>
          <td>
            <span class="status-pill status-${u.role}">${u.role.toUpperCase()}</span>
          </td>
          <td>
            <span class="status-pill status-${u.status}">${u.status.toUpperCase()}</span>
          </td>
          <td>${u.created_at ? u.created_at.split('T')[0] : '-'}</td>
          <td>
            ${u.status === 'active' ? `
              <button type="button" class="action-btn" style="color:#ef4444; border-color:#ef4444;" onclick="window.toggleUserStatus('${u.id}', 'suspended')">Suspend</button>
            ` : `
              <button type="button" class="action-btn action-btn-green" onclick="window.toggleUserStatus('${u.id}', 'active')">Reactivate</button>
            `}
          </td>
        </tr>
      `).join('');
    }

    // Render Pending Teacher Applications
    const pendingTeachers = users.filter(u => u.role === 'teacher' && u.status === 'pending');
    const teacherTable = document.getElementById("pending-teachers-tbody");
    if (teacherTable) {
      if (pendingTeachers.length === 0) {
        teacherTable.innerHTML = `<tr><td colspan="5" style="color:var(--admin-muted); text-align:center;">No pending instructor applications.</td></tr>`;
      } else {
        teacherTable.innerHTML = pendingTeachers.map(t => `
          <tr>
            <td><strong>${t.name}</strong><br><small style="color:var(--admin-muted);">${t.email}</small></td>
            <td>${t.phone || '-'}</td>
            <td>${t.specialization || 'SAP Instructor'}</td>
            <td>${t.created_at ? t.created_at.split('T')[0] : '-'}</td>
            <td>
              <button type="button" class="action-btn action-btn-green" onclick="window.approveTeacher('${t.id}')">Approve &amp; Activate</button>
              <button type="button" class="action-btn" style="color:#ef4444; margin-left:0.3rem;" onclick="window.rejectTeacher('${t.id}')">Reject</button>
            </td>
          </tr>
        `).join('');
      }
    }
  }

  window.toggleUserStatus = function(userId, newStatus) {
    const users = window.TTM_AUTH.getUsers();
    const u = users.find(x => x.id === userId);
    if (u) {
      u.status = newStatus;
      window.TTM_AUTH.saveUsers(users);
      window.TTM_AUTH.logAudit(currentUser.id, currentUser.email, `USER_${newStatus.toUpperCase()}`, "user", userId, "SUCCESS", { targetUser: u.email });
      alert(`User account ${u.email} is now ${newStatus.toUpperCase()}.`);
      renderUsersAndTeachers();
    }
  };

  window.approveTeacher = function(teacherId) {
    const users = window.TTM_AUTH.getUsers();
    const t = users.find(x => x.id === teacherId);
    if (t) {
      t.status = "active";
      window.TTM_AUTH.saveUsers(users);
      window.TTM_AUTH.logAudit(currentUser.id, currentUser.email, "TEACHER_APPROVED", "teacher", teacherId, "SUCCESS", { teacherEmail: t.email });
      alert(`🎉 Instructor ${t.name} has been approved and activated!`);
      renderUsersAndTeachers();
    }
  };

  window.rejectTeacher = function(teacherId) {
    if (confirm("Are you sure you want to reject this instructor application?")) {
      const users = window.TTM_AUTH.getUsers();
      const filtered = users.filter(x => x.id !== teacherId);
      window.TTM_AUTH.saveUsers(filtered);
      window.TTM_AUTH.logAudit(currentUser.id, currentUser.email, "TEACHER_REJECTED", "teacher", teacherId, "SUCCESS", {});
      alert("Application rejected.");
      renderUsersAndTeachers();
    }
  };

  // Render Courses
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
          <button type="button" class="action-btn action-btn-green" onclick="window.saveCoursePrice(${index})">Save Price</button>
        </td>
      </tr>
    `).join('');
  }

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
    window.TTM_AUTH.logAudit(currentUser.id, currentUser.email, "COURSE_PRICE_UPDATED", "course", courses[index].id, "SUCCESS", { newPrice });
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

  // Render Audit Logs
  function renderAuditLogs() {
    const logs = JSON.parse(localStorage.getItem("ttm_audit_logs") || "[]");
    const tbody = document.getElementById("audit-logs-tbody");
    if (!tbody) return;

    if (logs.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="color:var(--admin-muted); text-align:center;">No audit logs recorded yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = logs.slice(0, 25).map(l => `
      <tr>
        <td><small>${l.timestamp ? l.timestamp.replace('T', ' ').substring(0, 19) : '-'}</small></td>
        <td><code>${l.action}</code></td>
        <td><strong>${l.user_email}</strong></td>
        <td><span class="status-pill status-${l.status === 'SUCCESS' ? 'paid' : 'browsing'}">${l.status}</span></td>
        <td><small style="color:var(--admin-muted);">${JSON.stringify(l.metadata || {})}</small></td>
      </tr>
    `).join('');
  }

  // Setup Blog CMS
  function setupBlogCMS() {
    const form = document.getElementById("admin-new-blog-form");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const title = document.getElementById("blog-input-title").value.trim();
      const category = document.getElementById("blog-input-category").value;
      const readTime = document.getElementById("blog-input-time").value.trim();
      const excerpt = document.getElementById("blog-input-excerpt").value.trim();
      const imageUrl = document.getElementById("blog-input-image") ? document.getElementById("blog-input-image").value.trim() : "";
      const content = document.getElementById("blog-input-content").value.trim();

      const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
      const newPost = {
        id: "post_" + Date.now(),
        title: title,
        slug: slug,
        category: category,
        readTime: readTime || "8 min read",
        excerpt: excerpt,
        imageUrl: imageUrl || "https://youronementor.com/images/og-cover.svg",
        content: content,
        date: new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
      };

      const customBlogs = JSON.parse(localStorage.getItem(BLOGS_KEY) || "[]");
      customBlogs.unshift(newPost);
      localStorage.setItem(BLOGS_KEY, JSON.stringify(customBlogs));
      window.TTM_AUTH.logAudit(currentUser.id, currentUser.email, "BLOG_PUBLISHED", "blog", newPost.id, "SUCCESS", { title });

      alert(`🎉 Blog article "${title}" published successfully!`);
      form.reset();
      renderCustomBlogs();
    });
  }

  window.insertImageHelper = function() {
    const imgUrl = prompt("Enter the Direct Image URL (or path like ../images/your-screenshot.png):", "https://youronementor.com/images/og-cover.svg");
    if (!imgUrl) return;
    const altText = prompt("Enter Image Description / Caption:", "SAP Configuration Screenshot") || "Article Image";
    const textarea = document.getElementById("blog-input-content");
    if (textarea) {
      const markdownTag = `\n\n![${altText}](${imgUrl})\n\n`;
      textarea.value += markdownTag;
      textarea.focus();
    }
  };

  function renderCustomBlogs() {
    const list = document.getElementById("admin-custom-blogs-list");
    if (!list) return;
    const customBlogs = JSON.parse(localStorage.getItem(BLOGS_KEY) || "[]");
    if (customBlogs.length === 0) {
      list.innerHTML = `<p style="color:var(--admin-muted); font-size:0.9rem;">No custom articles published yet.</p>`;
      return;
    }
    list.innerHTML = customBlogs.map((b, i) => `
      <div class="card-panel" style="margin-bottom:1rem; padding:1.25rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
          <div style="display:flex; gap:1rem; align-items:flex-start;">
            ${b.imageUrl ? `<img src="${b.imageUrl}" alt="${b.title}" style="width:80px; height:60px; object-fit:cover; border-radius:6px; border:1px solid var(--admin-border);" />` : ''}
            <div>
              <span class="status-pill status-qualified">${b.category}</span>
              <h4 style="color:#fff; font-size:1.1rem; margin:0.4rem 0;">${b.title}</h4>
              <p style="color:var(--admin-muted); font-size:0.85rem;">${b.date} · ${b.readTime}</p>
            </div>
          </div>
          <button type="button" class="action-btn" style="color:#ef4444;" onclick="window.deleteCustomBlog(${i})">Delete</button>
        </div>
      </div>
    `).join('');
  }

  window.deleteCustomBlog = function(index) {
    if (confirm("Delete this article?")) {
      const customBlogs = JSON.parse(localStorage.getItem(BLOGS_KEY) || "[]");
      customBlogs.splice(index, 1);
      localStorage.setItem(BLOGS_KEY, JSON.stringify(customBlogs));
      renderCustomBlogs();
    }
  };

  document.addEventListener("DOMContentLoaded", () => {
    // Show logged-in admin identity
    const adminEmailEl = document.getElementById("admin-user-email");
    if (adminEmailEl) adminEmailEl.textContent = currentUser.email;

    setupNavigation();
    renderOverview();
    renderUsersAndTeachers();
    renderCourses();
    renderAuditLogs();
    setupBlogCMS();
    renderCustomBlogs();

    // Logout
    document.getElementById("admin-logout-btn")?.addEventListener("click", () => {
      window.TTM_AUTH.logout();
      window.location.href = "../login/index.html";
    });
  });
})();
