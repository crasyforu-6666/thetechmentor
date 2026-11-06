# theTechMentor: growth & automation plan (Nov 2026 → 2027)

Goal: a site that finds learners on its own (SEO + ads), captures every lead,
follows up automatically, sells courses without manual work, and delivers them
on our own Graphy/Teachable-style platform by early 2027.

---

## 1. What is automated now

| System | Status | Notes |
|---|---|---|
| Blog: 3 articles/day | ✅ built (Gemini free key for new posts, Claude Pro token for rewrites) | 9:00 AM and 8:00 PM IST new articles; 2:30 PM IST rewrites one old thin post (17 queued). Writes with Claude, rejects anything under 1,500 words or with filler, adds FAQ + Article schema, internal links and a lead form. Without the key it publishes nothing (old template posts hurt rankings). |
| Editorial rules | ✅ | Reads `AGENTS.md` from the repo root if present, plus built-in standards in `scripts/ai_writer.py`. |
| Deploy | ✅ | Vercel deploys every push to `main`. |
| Sitemap / robots | ✅ | Rebuilt on every run; thin pages are `noindex` and left out until rewritten. |
| Lead capture | ✅ code, needs Google Sheet link | Homepage form, blog opt-in on every post, payments → Google Sheet + email alert. |
| Ad tracking | ✅ code, needs IDs | Meta Pixel + GA4 events: Lead, InitiateCheckout, Purchase. |

Running cost: ₹0 with the free Gemini key + Claude Pro token (paid ANTHROPIC_API_KEY optional).

---

## 2. Ranking plan

**On-site (done or automated)**
- Every new article: 1,500–2,500 words, real T-codes/config steps, FAQ schema, internal links.
- Old thin posts: hidden from Google now, rewritten one per day.
- Titles ≤ 60 chars, descriptions ≤ 155, PNG share image, structured data on all posts.

**You need to do (one time)**
1. **Google Search Console**: verify youronementor.com (DNS TXT record in your domain panel), submit `https://youronementor.com/sitemap.xml`.
2. **Bing Webmaster Tools**: import from Search Console (2 minutes).
3. **Google Business Profile**: "theTechMentor – SAP Training", service area India.
4. **Links that build authority** (biggest ranking factor we can't automate):
   - Your YouTube channel: link the site in the channel header and in every video description.
   - LinkedIn (6,900+ followers): post each new article with your own 3-line take; link the site in your profile.
   - Listings: UrbanPro, Sulekha, Justdial, Shiksha, Quora answers on SAP MM/EWM questions linking to the matching article.
   - Ask 5–10 past students to post their success story on LinkedIn mentioning the site.
5. **Pick one brand**: "theTechMentor" or "YourOneMentor", and use it everywhere.

**Next site work (I can build)**
- City/landing pages: "SAP MM training in Bangalore / Pune / Hyderabad / Chennai / online".
- Course pages per program (`/courses/sap-mm`, `/courses/sap-ewm`) with Course schema and curriculum.
- Real student testimonials page with LinkedIn links (replace unverifiable salary claims).

---

## 3. Lead strategy: turning traffic into money

**Funnel**

```
Google / YouTube / LinkedIn / Meta ads
        ↓
Blog article or homepage
        ↓  (free kit opt-in or strategy-call form)
Lead in Google Sheet + instant email to you
        ↓
WhatsApp follow-up sequence (automated)
        ↓
Free 15-min call (qualified) or self-paced checkout (budget-limited)
        ↓
Razorpay → thank-you page → course access
        ↓
Upsell: self-paced → live batch (₹5,000 credit) → 1-on-1
```

**Improvements, in order of impact**
1. **Connect the Google Sheet** (`integrations/README.md`). Until then, form leads don't reach you.
2. **WhatsApp automation** (biggest win for Indian buyers): WhatsApp Business API via
   Interakt / AiSensy / WATI (~₹2–3k/month). Sequence for every new lead:
   - Minute 0: welcome + playlist link
   - Day 1: "Top 30 MM interview questions" PDF
   - Day 3: student success story
   - Day 5: next live batch date + seats left
   - Day 7: EMI offer / self-paced discount, valid 48 hours
   I can connect the Google Sheet to it so this runs with zero manual work.
3. **Lead magnet PDF**: a real 15–20 page "SAP MM Interview Kit" (I can draft it from your posts). Replaces "playlist only" and doubles opt-in rates.
4. **Weekly free live webinar** ("SAP MM career in 90 days", Saturday 11 AM): the best converter for ₹25k live batches. Auto-registration + reminders via WhatsApp.
5. **Pricing ladder**:
   - ₹499 weekend workshop or interview kit (turns leads into buyers, pays for ads)
   - ₹4,999–10,999 self-paced
   - ₹24,999 live batch (show EMI: "from ₹2,200/month")
   - raise 1-on-1 to ₹45,000–60,000 with limited seats
6. **Retargeting**: once the Pixel is live, run a small ₹300–500/day Meta retargeting campaign to blog readers and form-starters.
7. **Referral**: ₹1,000 cashback for each student who refers a paying student.

---

## 4. Our own course platform (Graphy/Teachable-style), target Feb–Mar 2027

**Why**: lower fees than Graphy (which takes a cut and limits branding), own the student data, and scale with more trainers.

**Architecture** (works on the current Vercel hosting):

| Piece | Choice | Why |
|---|---|---|
| Logins & database | **Supabase** (Postgres + Auth: email OTP, Google) | Free tier to start, India-friendly, secure row-level permissions |
| Video hosting | **Bunny Stream** | ~₹1/GB, token-protected URLs, India CDN, anti-download |
| Payments | **Razorpay Orders API + webhook** (Vercel serverless function, signature verified) | Payment → automatic enrolment; no manual access |
| Emails | Resend or Brevo | Receipts, access emails |
| WhatsApp | Interakt/AiSensy API | Same provider as lead follow-up |

**Roles & features**
- **Student**: my courses, video player with progress, notes/workbooks download, quizzes, certificate PDF, community link, server-access details.
- **Trainer**: upload lessons, see their batch, answer Q&A, mark attendance for live classes.
- **Admin (you)**: sales, leads, students, coupons/discounts, batches, trainer approvals, revenue dashboard, refunds.
- **Public**: course catalog pages (SEO), checkout, coupon codes, EMI.

**Phases**
1. **Weeks 1–2**: Supabase + login, course catalog, Razorpay webhook → enrolment, student dashboard with Bunny videos.
2. **Weeks 3–4**: admin dashboard (sales/leads/students), coupons, certificates, progress tracking.
3. **Weeks 5–6**: trainer panel, quizzes, live-batch scheduling with Zoom links, WhatsApp/email automations.
4. **Then**: migrate existing students, test with 1 batch, open publicly.

---

## 5. What I need from you

| # | Item | Why | How |
|---|---|---|---|
| 1 | **Anthropic API key** saved as GitHub secret `ANTHROPIC_API_KEY` | Turns on the 3×/day blog | console.anthropic.com → API keys → create; GitHub repo → Settings → Secrets and variables → Actions → New repository secret |
| 2 | **AGENTS.md** (your existing blog instructions, on your Mac in the site folder) | Writer follows your rules | Send it to me or commit it to the repo root |
| 3 | **Google Sheet web-app link** | Leads & sales reach you | `integrations/README.md` |
| 4 | **Meta Pixel ID + GA4 ID** | Ad optimisation & analytics | Paste in chat; I'll add them |
| 5 | **Search Console verification** | Indexing & ranking data | Add the DNS TXT record Google gives you |
| 6 | **Decision on the course platform** | Build vs use Graphy | If building: create a Supabase project and Bunny Stream account and share access when we start |
| 7 | **Real testimonials** (name, role, company, LinkedIn, photo with consent) | Trust + legal safety | 5–10 students |
| 8 | **Next live batch date** | Shown on site & in follow-ups | Date + seats |
| 9 | **WhatsApp API provider choice** | Automated follow-up | Interakt / AiSensy / WATI account |
