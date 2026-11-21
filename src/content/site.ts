/**
 * Single source of truth for all homepage copy, prices and links.
 * Components must read from here — never hardcode text, prices or URLs.
 */
import jsonLdData from "./jsonld.json";
import batchData from "./batches.json";

export const jsonLd = jsonLdData;

/* ---------- Contact & config ---------- */
export const contact = {
  whatsappNumber: "917848942021",
  whatsappUrl: "https://wa.me/917848942021",
  whatsappLabel: "WhatsApp +91 78489 42021",
  email: "info@youronementor.com",
  emailUrl: "mailto:info@youronementor.com",
  hours: "Mon–Sat, 10 AM – 7 PM IST",
};

/** Values injected as window.TTM_CONFIG for /tracking.js. Leave "" to keep a feature off. */
export const trackingConfig = {
  LEAD_WEBHOOK_URL: "",
  META_PIXEL_ID: "",
  GA4_ID: "",
  WHATSAPP_NUMBER: contact.whatsappNumber,
};

export const links = {
  youtubePlaylist: "https://www.youtube.com/playlist?list=PL71i23QiQd9VSrHTuXQyiOlLsi8NnGbSp",
  linkedin: "https://www.linkedin.com/in/anshuman-behuria-946860130",
  blog: "blog/index.html",
  digitalProducts: "digital-products",
  privacy: "privacy.html",
  terms: "terms.html",
  refund: "refund.html",
  fonts:
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap",
  razorpayCheckout: "https://checkout.razorpay.com/v1/checkout.js",
};

/** wa.me link with the same encoding as the legacy site (parentheses escaped too). */
export function whatsappLink(text: string): string {
  const enc = encodeURIComponent(text).replace(/\(/g, "%28").replace(/\)/g, "%29");
  return `${contact.whatsappUrl}?text=${enc}`;
}

/* ---------- Meta ---------- */
export const meta = {
  siteUrl: "https://youronementor.com",
  title: "theTechMentor — SAP MM, EWM & S/4HANA Courses Online | Live & Self-Paced",
  description:
    "theTechMentor is an online SAP academy. Learn SAP MM, EWM and S/4HANA with live weekday & weekend batches, 24/7 recorded courses, real practice servers and placement support.",
  canonical: "https://youronementor.com/",
  icon: "/images/logo-mark.svg",
  themeColor: "#1d4ed8",
  og: {
    type: "website" as const,
    url: "https://youronementor.com/",
    title: "theTechMentor — SAP MM, EWM & S/4HANA Courses",
    description: "Live and self-paced SAP courses with practice servers, real projects and placement support.",
    image: "https://youronementor.com/images/og-cover.png",
    imageWidth: 1200,
    imageHeight: 630,
    locale: "en_IN",
    siteName: "theTechMentor",
  },
  twitter: {
    card: "summary_large_image" as const,
    title: "theTechMentor — SAP MM, EWM & S/4HANA Courses",
    description: "Live and self-paced SAP courses with practice servers and placement support.",
    image: "https://youronementor.com/images/og-cover.png",
  },
};

/* ---------- Brand ---------- */
export const brand = {
  logo: "/images/logo-mark.svg",
  homeLabel: "theTechMentor home",
  pre: "the",
  bold: "Tech",
  post: "Mentor",
  name: "theTechMentor",
};

export const skipLink = { label: "Skip to content", href: "#main" };

export const announce = {
  text: "New weekday & weekend live batches enrolling now — limited seats",
  link: { label: "Talk to a career advisor →", href: "#advisor" },
};

export const nav = {
  ariaLabel: "Main",
  searchPlaceholder: "Search SAP courses…",
  searchLabel: "Search courses",
  toggleLabel: "Open menu",
  links: [
    { label: "Courses", href: "#courses" },
    { label: "Digital Products", href: links.digitalProducts },
    { label: "Career paths", href: "#paths" },
    { label: "Blog", href: links.blog },
  ],
  cta: { label: "Free counselling", href: "#enroll-form" },
};

/* ---------- Hero ---------- */
export const hero = {
  eyebrow: "SAP S/4HANA Academy · Online",
  titleLine1: "Learn SAP from practitioners.",
  titleHighlight: "Get job-ready",
  titleRest: " in 90 days.",
  lead:
    "Recorded and live mentored courses in SAP MM, SD, FICO, ABAP, BASIS, EWM, TM and end-to-end Logistics on S/4HANA — with practice servers, project scenarios, interview preparation and placement support.",
  cta: { label: "Explore courses", href: "#courses" },
  popularLabel: "Popular:",
  popular: [
    { label: "SAP MM", href: "#mm-recorded" },
    { label: "SAP FICO", href: "#fico-recorded" },
    { label: "SAP ABAP", href: "#abap-recorded" },
    { label: "SAP EWM", href: "#ewm-recorded" },
    { label: "Live batches", href: "#live", jump: "live" },
  ] as { label: string; href: string; jump?: string }[],
  proof: [
    { strong: "1,000+", text: " learners trained" },
    { strong: "12+ yrs", text: " SAP project experience" },
    { strong: "Live", text: " S/4HANA practice server" },
  ],
};

/* ---------- Hero batch finder (per-module WhatsApp groups) ---------- */
export type BatchModule = {
  id: string;
  name: string;
  aliases: string[];
  startDate: string;
  time: string;
  mode: string;
  whatsappLink: string;
};
export type BatchData = { defaultWhatsappLink: string; sheetCsvUrl: string; modules: BatchModule[] };

/** Edit src/content/batches.json (or set sheetCsvUrl to a published Google Sheet CSV with the same columns). */
export const batches: BatchData = batchData;

export const batchFinder = {
  title: "Upcoming live batches",
  searchLabel: "Search module",
  searchPlaceholder: "Search module (MM, SD, FICO…)",
  upcomingCount: 6,
  debounceMs: 150,
  deepLinkParam: "module",
  joinLabel: (name: string) => `Join ${name} WhatsApp — Free Demo & Timings`,
  startsToday: "Starts today",
  startsIn: (days: number) => `Starts in ${days} day${days === 1 ? "" : "s"}`,
  comingSoon: "Next batch date coming soon",
  noMatch: "Module not listed — join our general group",
  noMatchButton: "Join general WhatsApp group",
  noUpcoming: "New batch dates coming soon — join our general group",
  generalId: "general",
  generalName: "General",
  trackEvent: "whatsapp_batch_click",
  dateLocale: "en-IN",
};

export const strip = {
  title: "Our learners have moved into SAP roles at",
  companies: ["Accenture", "Capgemini", "Infosys", "Wipro"],
};

/* ---------- Courses ---------- */
export type CourseFormat = "recorded" | "live";
export const formatLabels: Record<CourseFormat, string> = {
  recorded: "Recorded Session",
  live: "Live Mentored Session",
};

/** Prices in INR per format and course. */
export const prices: Record<string, Record<string, number>> = {
  "Recorded Session": { "SAP MM": 4999, "SAP SD": 4999, "SAP FICO": 4999, "SAP ABAP": 4999, "SAP BASIS": 4999, "SAP EWM": 6999, "SAP TM": 6999, "SAP Logistics": 6999 },
  "Live Mentored Session": { "SAP MM": 29999, "SAP SD": 29999, "SAP ABAP": 29999, "SAP FICO": 34999, "SAP BASIS": 34999, "SAP EWM": 34999, "SAP TM": 34999, "SAP Logistics": 34999 },
};
export const inr = (n: number) => "₹" + n.toLocaleString("en-IN");
export const priceFor = (course: string, format: string) => prices[format]?.[course] ?? null;

type Module = {
  key: string;
  short: string;
  name: string;
  cats: string;
  tags: string;
  skills: string;
  hours: string;
  recordedBadge?: string;
};

const modules: Module[] = [
  { key: "mm", short: "SAP MM", name: "SAP MM (Materials Management)", cats: "functional supply", tags: "materials management procurement purchasing p2p migo miro obyc split valuation inventory sap mm", skills: "Procure-to-Pay (P2P), MIGO, MIRO, OBYC, split valuation, FI/SD integration", hours: "35+ hours HD video" },
  { key: "sd", short: "SAP SD", name: "SAP SD (Sales & Distribution)", cats: "functional supply", tags: "sales distribution o2c order to cash pricing condition technique billing vkoa credit sap sd", skills: "Order-to-Cash (O2C), pricing procedure, condition technique, billing, VKOA, credit management", hours: "35+ hours HD video" },
  { key: "fico", short: "SAP FICO", name: "SAP FICO (Finance & Controlling)", cats: "functional", tags: "finance controlling fi co acdoca universal journal general ledger gl ap ar asset accounting cost center profit center sap fico", skills: "Universal Journal (ACDOCA), General Ledger, AP/AR, Asset Accounting, cost center & profit center accounting", hours: "40+ hours HD video" },
  { key: "abap", short: "SAP ABAP", name: "SAP ABAP (Advanced Business Application Programming)", cats: "technical", tags: "abap developer programming hana cds amdp odata fiori enhancements badi reports smartforms technical sap abap", skills: "ABAP on HANA, CDS views, AMDP, OData services, enhancements, reports & SmartForms", hours: "40+ hours HD video" },
  { key: "basis", short: "SAP BASIS", name: "SAP BASIS (System Administration)", cats: "technical", tags: "basis administration admin hana database security roles stms transport kernel upgrade technical sap basis", skills: "S/4HANA architecture, HANA DB administration, user & role security, transport management (STMS), kernel upgrades", hours: "35+ hours HD video" },
  { key: "ewm", short: "SAP EWM", name: "SAP EWM (Extended Warehouse Management)", cats: "functional supply", tags: "extended warehouse management ewm inbound outbound wave rf slotting posc losc yard sap ewm", skills: "Inbound/outbound processing, wave management, RF framework, slotting, POSC/LOSC, yard management", hours: "40+ hours HD video", recordedBadge: "Specialized" },
  { key: "tm", short: "SAP TM", name: "SAP TM (Transportation Management)", cats: "functional supply", tags: "transportation management tm freight order carrier selection charge calculation shipper lsp logistics sap tm", skills: "Freight order management, carrier selection, charge calculation, shipper/LSP scenarios, S/4HANA embedded TM", hours: "40+ hours HD video", recordedBadge: "Specialized" },
  { key: "logistics", short: "SAP Logistics", name: "SAP Logistics (End-to-End Supply Chain)", cats: "supply functional", tags: "logistics supply chain end to end mm sd ewm tm integrated procurement fulfilment warehouse sap logistics", skills: "Integrated MM + SD + EWM + TM workflows across procurement, order fulfilment and warehouse execution", hours: "45+ hours HD video", recordedBadge: "Complete Suite" },
];

export type Course = {
  id: string;
  format: CourseFormat;
  cats: string;
  tags: string;
  image: string;
  short: string;
  name: string;
  formatLabel: string;
  formatTag: string;
  badge?: string;
  skills: string;
  meta: string[];
  feat: string;
  price: string;
  priceNote: string;
  enrollHref: string;
};

const formatDetails = {
  recorded: {
    tag: "Recorded",
    meta: (m: Module) => [m.hours, "Lifetime access", "Certificate"],
    feat: "Configuration workbook · T-code cheat sheets · 24/7 access",
    priceNote: "one-time",
  },
  live: {
    tag: "Live · Weekday & Weekend",
    meta: () => ["Weekday & weekend batches", "6-month S/4HANA server", "EMI available"],
    feat: "24-hr recordings · Capstone project · Resume & LinkedIn review · Mock interviews",
    priceNote: "EMI available",
  },
};

function buildCourses(format: CourseFormat): Course[] {
  const d = formatDetails[format];
  const label = formatLabels[format];
  return modules.map((m) => ({
    id: `${m.key}-${format}`,
    format,
    cats: m.cats,
    tags: `${m.tags} ${format}`,
    image: `/images/courses/${m.key}.svg`,
    short: m.short,
    name: m.name,
    formatLabel: label,
    formatTag: d.tag,
    badge: format === "recorded" ? m.recordedBadge : undefined,
    skills: m.skills,
    meta: d.meta(m),
    feat: d.feat,
    price: inr(priceFor(m.short, label) ?? 0),
    priceNote: d.priceNote,
    enrollHref: whatsappLink(`I want to enroll in ${m.name} — ${label}`),
  }));
}

export const catalog = {
  eyebrow: "Course catalog",
  title: "Explore SAP S/4HANA courses",
  sub: "8 SAP modules, each available as 24/7 recorded classes or live mentored weekday & weekend batches.",
  filtersLabel: "Filter courses",
  filters: [
    { key: "all", label: "All" },
    { key: "recorded", label: "Recorded Sessions" },
    { key: "live", label: "Live Mentored" },
    { key: "functional", label: "Functional" },
    { key: "technical", label: "Technical" },
    { key: "supply", label: "Supply Chain" },
  ],
  providerPrefix: "theTechMentor · ",
  skillsLabel: "Skills:",
  enrollLabel: "Enroll now",
  advisorLabel: "Ask an advisor",
  advisorHref: "#enroll-form",
  noResults: "No course matches that search.",
  resetLabel: "Show all courses",
  sections: [
    {
      id: "recorded" as CourseFormat,
      title: "Recorded Sessions — Self-Paced Mastery",
      sub: "Learn on your own schedule with HD recorded classes, configuration workbooks, and lifetime access.",
      price: "₹4,999 core modules · ₹6,999 EWM, TM & Logistics",
      courses: buildCourses("recorded"),
    },
    {
      id: "live" as CourseFormat,
      title: "Live Mentored Sessions — Weekday & Weekend Batches",
      sub: "Instructor-led live classes in weekday and weekend batches, with 24/7 S/4HANA practice server access, real-time project scenarios, and mock interviews.",
      price: "₹29,999 MM, SD, ABAP · ₹34,999 FICO, BASIS, EWM, TM & Logistics",
      courses: buildCourses("live"),
    },
  ],
};

/** Next live batch start (shown as "Starts {date}" for Live Mentored Sessions). */
export const liveBatch = { startDate: "2026-11-28", startLabel: "28 Nov 2026", startsPrefix: "Starts " };

export const filterKeys = ["recorded", "live", "functional", "technical", "supply"];

/* ---------- Stats / Why ---------- */
export const stats = [
  { value: "1,000+", label: "Learners trained" },
  { value: "12+ yrs", label: "SAP implementation experience" },
  { value: "20+", label: "Full-cycle S/4HANA projects" },
  { value: "24/7", label: "Practice server access" },
];

export const why = {
  eyebrow: "Why theTechMentor",
  title: "Built for real SAP jobs, not just certificates",
  items: [
    { icon: "🖥️", title: "Live S/4HANA servers", text: "Practise every configuration and transaction yourself on a real system — not just slides." },
    { icon: "🏗️", title: "Project-based learning", text: "Implementation and support scenarios, ticket resolution and a capstone project you can talk about in interviews." },
    { icon: "👨‍🏫", title: "Taught by practitioners", text: "Mentors who have delivered MM and EWM implementations across manufacturing, retail and 3PL." },
    { icon: "🎯", title: "Interview preparation", text: "Mock interviews, scenario questions and resume reviews for consultant and analyst roles." },
    { icon: "📅", title: "Weekday & weekend batches", text: "Choose a live batch that fits your job — weekday or weekend — with recordings within 24 hours. Recorded courses are available 24/7." },
    { icon: "🤝", title: "Placement support", text: "Resume and LinkedIn optimisation, referrals and interview guidance. We support you — we don't promise jobs." },
  ],
};

/* ---------- Career paths ---------- */
export const paths = {
  eyebrow: "Career paths",
  title: "Pick the role you want. We'll map the route.",
  items: [
    { tag: "For logistics & procurement professionals", title: "SAP MM Consultant", steps: ["SAP basics & MM master data", "Procure-to-pay on S/4HANA", "Inventory, valuation & OBYC", "Projects + interview prep"], cta: { label: "View MM courses", href: "#mm-live" }, featured: false },
    { tag: "For warehouse & supply chain roles", title: "SAP EWM Consultant", steps: ["Warehouse structure & master data", "Inbound, outbound & waves", "RF framework & automation", "Embedded EWM capstone"], cta: { label: "View EWM courses", href: "#ewm-live" }, featured: true },
    { tag: "For IT support & career switchers", title: "SAP Logistics Consultant (MM + EWM)", steps: ["MM foundation", "EWM on top of MM", "End-to-end integration", "Placement support"], cta: { label: "View Logistics course", href: "#logistics-live" }, featured: false },
  ],
};

/* ---------- Curriculum ---------- */
export const curriculum = {
  eyebrow: "Curriculum",
  title: "What you'll master",
  sub: "A week-by-week plan from fundamentals to a capstone project. Every live batch includes recordings and practice server access.",
  tabs: [
    {
      key: "mm",
      label: "SAP MM",
      weeks: [
        ["Week 1", "SAP overview, organisational structure, MM master data"],
        ["Week 2", "Procurement cycle: requisition, RFQ, quotation, PO"],
        ["Week 3", "Goods receipt, invoice verification, account determination"],
        ["Week 4", "Inventory management, reservations, transfer postings"],
        ["Week 5", "Special procurement: subcontracting, consignment"],
        ["Week 6", "Integration, reporting and capstone implementation project"],
      ],
    },
    {
      key: "ewm",
      label: "SAP EWM",
      weeks: [
        ["Week 1–2", "EWM architecture, warehouse structure, master data"],
        ["Week 3", "Inbound: ASN, goods receipt, putaway strategies"],
        ["Week 4", "Outbound: waves, picking, packing, goods issue"],
        ["Week 5", "Internal processes: replenishment, rearrangement, physical inventory"],
        ["Week 6", "RF devices, production supply, quality inspection"],
        ["Week 7–8", "TM integration, monitoring and capstone warehouse project"],
      ],
    },
  ],
};

/* ---------- Formats ---------- */
export const formats = {
  eyebrow: "Learning formats",
  title: "Choose how you want to learn",
  items: [
    {
      title: "Recorded Sessions",
      price: "Starting at ₹4,999",
      split: "₹4,999 core modules | ₹6,999 EWM, TM & Logistics",
      points: ["35–45+ hours of HD recorded classes", "Configuration workbook & T-code cheat sheets", "Lifetime access — learn at your pace", "Certificate of completion", "24/7 access, any device"],
      cta: { label: "Browse recorded courses", href: "#recorded", jump: "recorded" },
      featured: false,
      ribbon: "",
    },
    {
      title: "Live Mentored Sessions",
      price: "Starting at ₹29,999",
      split: "₹29,999 MM, SD, ABAP | ₹34,999 FICO, BASIS, EWM, TM & Logistics",
      points: ["Live classes in weekday or weekend batches + recordings within 24 hours", "6 months S/4HANA practice server access", "Capstone implementation project", "Resume & LinkedIn review + mock interviews", "EMI available"],
      cta: { label: "See live batches", href: "#live", jump: "live" },
      featured: true,
      ribbon: "Most popular",
    },
  ],
};

/* ---------- Outcomes ---------- */
export const outcomes = {
  eyebrow: "Learner outcomes",
  title: "Career transitions our learners made",
  beforeLabel: "Before",
  afterLabel: "After",
  arrow: "→",
  items: [
    { company: "Accenture", before: "Mechanical Engineer", after: "SAP MM Consultant", quote: "“The S/4HANA sandbox practice and P2P scenarios made all the difference in my interviews.”" },
    { company: "Capgemini", before: "Warehouse Executive", after: "SAP EWM Analyst", quote: "“Embedded EWM and the RF framework sessions were exactly what interviewers asked about.”" },
    { company: "Wipro", before: "L1 IT Support", after: "SAP MM/EWM Consultant", quote: "“The resume rewrite and mock interviews were crucial for my switch to functional consulting.”" },
    { company: "Infosys", before: "Supply Chain Trainee", after: "Associate SAP Consultant", quote: "“Project documentation and hands-on inventory configuration helped me clear my first attempt.”" },
  ],
  fineprint: "Individual results vary. We provide placement support, not job guarantees.",
};

/* ---------- Mentor ---------- */
export const mentor = {
  photo: "/images/anshuman-behuria.jpg",
  photoAlt: "Anshuman Behuria, lead SAP mentor at theTechMentor",
  eyebrow: "Meet your lead mentor",
  greeting: "Hello, I'm",
  firstName: "Anshuman",
  lastName: "Behuria",
  name: "Anshuman Behuria",
  roleLead: "Lead SAP",
  roleFocus: "MM & EWM Mentor",
  role: "Lead SAP MM & EWM Mentor, theTechMentor",
  bio: "Anshuman has delivered SAP MM and EWM implementations across manufacturing, retail and 3PL — from greenfield S/4HANA rollouts to brownfield migrations — and has trained 1,000+ learners through theTechMentor and corporate batches.",
  /** Same bio, split so key phrases can be highlighted. */
  bioParts: [
    { text: "Anshuman has delivered " },
    { text: "SAP MM and EWM implementations", hl: true },
    { text: " across manufacturing, retail and 3PL — from greenfield S/4HANA rollouts to brownfield migrations — and has trained " },
    { text: "1,000+ learners", hl: true },
    { text: " through theTechMentor and corporate batches." },
  ] as { text: string; hl?: boolean }[],
  stats: [
    { value: "12+ yrs", label: "SAP experience" },
    { value: "1,000+", label: "Learners trained" },
    { value: "20+", label: "Implementations" },
  ],
  ticks: ["SAP certified — MM & EWM (S/4HANA)", "20+ full-cycle implementation projects", "6,900+ LinkedIn followers"],
  cta: { label: "View LinkedIn profile ↗", href: links.linkedin },
};

/* ---------- Blog ---------- */
export const blog = {
  eyebrow: "Free learning hub",
  title: "Free SAP guides & interview prep",
  sub: "New in-depth articles every day, plus a free 40+ lesson video playlist.",
  playlistCta: { label: "▶ Free video playlist", href: links.youtubePlaylist },
  allCta: { label: "All articles", href: links.blog },
  byPrefix: "By ",
  author: "Anshuman Behuria",
  minRead: " min read",
  readLabel: "Read article & join Q&A →",
  posts: [
    { slug: "sap-s4hana-system-architecture-basis-beginners", badge: "SAP BASIS TUTORIAL", tone: "teal", title: "SAP S/4HANA System Architecture Explained for BASIS Beginners", minutes: 10, date: "2026-11-15", dateLabel: "Nov 15, 2026" },
    { slug: "sap-sd-organisational-structure-s4hana-guide", badge: "SAP SD TUTORIAL", tone: "blue", title: "Mastering SAP SD Organisational Structure in S/4HANA for Logistics Consultants", minutes: 13, date: "2026-11-15", dateLabel: "Nov 15, 2026" },
    { slug: "abap-on-hana-code-pushdown-examples", badge: "SAP ABAP TUTORIAL", tone: "teal", title: "Mastering ABAP on HANA: Code Pushdown Techniques with Practical Examples", minutes: 11, date: "2026-11-14", dateLabel: "Nov 14, 2026" },
    { slug: "sap-ewm-warehouse-structure-storage-types-sections-bins", badge: "SAP EWM TUTORIAL", tone: "teal", title: "Mastering the SAP EWM Warehouse Structure: Storage Types, Sections, and Bins", minutes: 13, date: "2026-11-14", dateLabel: "Nov 14, 2026" },
    { slug: "sap-fico-organisational-structure-s4hana-guide", badge: "SAP FICO TUTORIAL", tone: "blue", title: "Mastering SAP FICO Organisational Structure in S/4HANA: Company Code, Controlling Area, and Chart of Accounts", minutes: 13, date: "2026-11-13", dateLabel: "Nov 13, 2026" },
    { slug: "material-master-views-s4hana-field-by-field-guide", badge: "SAP MM TUTORIAL", tone: "teal", title: "Mastering Material Master Views in S/4HANA: A Field-by-Field Deep Dive for MM & EWM Consultants", minutes: 10, date: "2026-11-13", dateLabel: "Nov 13, 2026" },
    { slug: "sap-mm-organisational-structure-s4hana", badge: "SAP MM TUTORIAL", tone: "teal", title: "Mastering SAP MM Organisational Structure in S/4HANA: Company Code, Plant, Storage Location, & Purchasing Org", minutes: 12, date: "2026-11-12", dateLabel: "Nov 12, 2026" },
    { slug: "sap-ewm-yard-management-tu-dock-door-check-in-guide", badge: "SAP EWM TUTORIAL", tone: "teal", title: "SAP EWM Yard Management: Transportation Unit, Dock Door, and Check-In Guide", minutes: 12, date: "2026-11-11", dateLabel: "Nov 11, 2026" },
    { slug: "sap-mm-subcontracting-process-s4hana-special-stock-o", badge: "SAP MM TUTORIAL", tone: "teal", title: "Mastering the SAP MM Subcontracting Process in S/4HANA: Special Stock 'O' Lifecycle", minutes: 14, date: "2026-11-08", dateLabel: "Nov 08, 2026" },
    { slug: "sap-ewm-slotting-rearrangement-optimization", badge: "SAP EWM TUTORIAL", tone: "teal", title: "SAP EWM Slotting and Rearrangement: Master Warehouse Optimization", minutes: 9, date: "2026-11-08", dateLabel: "Nov 08, 2026" },
    { slug: "sap-mm-batch-management-s4hana-configuration", badge: "SAP MM TUTORIAL", tone: "teal", title: "SAP MM Batch Management and Batch Determination in S/4HANA: A Masterclass", minutes: 11, date: "2026-11-07", dateLabel: "Nov 07, 2026" },
    { slug: "sap-s4hana-o2c-process-fi-vkoa", badge: "SAP SD TUTORIAL", tone: "blue", title: "SAP S/4HANA Order-to-Cash (O2C) Process Flow: Deep Dive into FI Integration & VKOA", minutes: 14, date: "2026-11-07", dateLabel: "Nov 07, 2026" },
  ],
};

/* ---------- Advisor / lead form ---------- */
export const advisor = {
  eyebrow: "Free career counselling",
  title: "Not sure which course is right for you?",
  sub: "Answer three quick questions and get a free 15-minute call with a theTechMentor career advisor. We'll recommend the right course, batch and budget for your background.",
  ticks: ["Personal learning roadmap", "Batch dates, fees and EMI options", "Instant access to our free video library"],
  contactWhatsapp: `💬 ${contact.whatsappLabel}`,
  contactEmail: `✉️ ${contact.email}`,
  form: {
    title: "Book your free counselling call",
    courseLabel: "Course *",
    coursePlaceholder: "Select course",
    courseOptions: ["SAP MM", "SAP SD", "SAP FICO", "SAP ABAP", "SAP BASIS", "SAP EWM", "SAP TM", "SAP Logistics", "Not sure yet"],
    formatLabel: "Format *",
    formatPlaceholder: "Select format",
    formatOptions: ["Recorded Session", "Live Mentored Session", "Not sure yet"],
    liveNote: " · EMI available",
    recordedNote: " · one-time, lifetime access",
    nameLabel: "Full name *",
    namePlaceholder: "Your name",
    phoneLabel: "Phone / WhatsApp *",
    phonePlaceholder: "+91 98765 43210",
    submit: "Get my free roadmap",
    fineprint: `We reply within 4 working hours · ${contact.hours}`,
    defaultProgram: "Free counselling call",
    defaultName: "Applicant",
  },
  success: {
    title: "🎉 Candidate Pre-Qualified!",
    text: (name: string) =>
      `Congratulations ${name}! Based on your experience and commitment, your application is approved for a 15-minute Strategy Call with Anshuman Behuria.`,
    cta: {
      label: "Confirm Strategy Call Slot on WhatsApp ↗",
      href: whatsappLink("Hi Anshuman, my application is approved. I want to schedule my 15-min strategy call."),
    },
    unlockLabel: "Curriculum Playlist Unlocked:",
    unlockLink: { label: "Access 40+ Module Video Library ↗", href: links.youtubePlaylist },
  },
};

/* ---------- FAQ ---------- */
export const faq = {
  eyebrow: "FAQ",
  title: "Frequently asked questions",
  items: [
    { q: "Do I need prior SAP experience?", a: "No. A basic understanding of ERP or supply chain helps, but we start from fundamentals. IT and logistics professionals with 0–2 years of SAP exposure do well in our batches." },
    { q: "Which SAP version do you teach?", a: "SAP S/4HANA, with a focus on embedded EWM and modern MM processes. We point out ECC differences where relevant." },
    { q: "Are classes live or recorded?", a: "Both. Live mentored courses run in weekday and weekend batches, with recordings within 24 hours. Recorded courses are available 24/7 with lifetime access, on any device." },
    { q: "Do you provide placement assistance?", a: "Yes — resume review, LinkedIn optimisation, referral network access and mock interviews. Placement is strongly supported but not guaranteed." },
    { q: "Will I get a certificate?", a: "Yes, a theTechMentor certificate of completion. It is not an official SAP SE certification; we guide you on SAP's own certification exams if you want one." },
    { q: "Can I pay in instalments?", a: "Yes. EMI and corporate billing are available for live batches and mentorship — ask your advisor after booking a counselling call." },
    {
      q: "What is your refund policy?",
      a: "Our courses are digital products, so all sales are final and no refunds are offered once you enrol. Please watch the free playlist or book a free counselling call before buying. Details are in our ",
      link: { label: "refund policy", href: links.refund },
      after: ".",
    },
  ] as { q: string; a: string; link?: { label: string; href: string }; after?: string }[],
};

/* ---------- Closing CTA ---------- */
export const ctaBand = {
  title: "Start your SAP career with theTechMentor",
  text: "Join the next weekday or weekend batch, or start a recorded course today.",
  primary: { label: "Explore courses", href: "#courses" },
  secondary: { label: "Free counselling", href: "#advisor" },
};

/* ---------- Footer ---------- */
export const footer = {
  tagline: "Online SAP S/4HANA academy for logistics, procurement and warehouse careers.",
  columns: [
    {
      title: "Courses",
      links: [
        { label: "Recorded Sessions", href: "#recorded", jump: "recorded" },
        { label: "Live Mentored Sessions", href: "#live", jump: "live" },
        { label: "Functional", href: "#courses", jump: "functional" },
        { label: "Technical", href: "#courses", jump: "technical" },
        { label: "Supply Chain", href: "#courses", jump: "supply" },
      ],
    },
    {
      title: "Resources",
      links: [
        { label: "Digital Products", href: links.digitalProducts },
        { label: "Blog", href: links.blog },
        { label: "Free videos", href: links.youtubePlaylist, external: true },
        { label: "FAQ", href: "#faq" },
        { label: "Free counselling", href: "#advisor" },
      ],
    },
    {
      title: "Contact",
      links: [
        { label: contact.email, href: contact.emailUrl },
        { label: contact.whatsappLabel, href: contact.whatsappUrl, external: true },
        { label: contact.hours },
      ],
    },
    {
      title: "Legal",
      links: [
        { label: "Privacy policy", href: links.privacy },
        { label: "Terms", href: links.terms },
        { label: "Refunds", href: links.refund },
      ],
    },
  ] as { title: string; links: { label: string; href?: string; jump?: string; external?: boolean }[] }[],
  copyright: "© 2026 theTechMentor. SAP and S/4HANA are trademarks of SAP SE; theTechMentor is not affiliated with SAP SE.",
  wordmark: "/images/footer-wordmark.webp?v=3",
};

export const stickyBar = {
  primary: { label: "Explore courses", href: "#courses" },
  secondary: { label: "Free counselling", href: "#enroll-form" },
};
