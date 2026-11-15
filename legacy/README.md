# SAP MM & EWM Course Landing Page

Marketing site for **live** and **self-paced** SAP MM & EWM training, with a Meta ads lead-nurture funnel (slides → video → enroll).

## Live site

**https://sap-mm-ewm-courses.vercel.app**

## Quick start (local)

```bash
cd ~/Desktop/sap-mm-ewm-courses
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080)

## Redeploy (Vercel)

```bash
cd ~/Desktop/sap-mm-ewm-courses
vercel deploy --prod
```

## Page flow (Meta ads)

1. **Hero** → Watch Free Preview
2. **#learn** — 6-slide information deck + YouTube overview + nurture video thumbnails
3. **#enroll** — Enrollment form (immediately after the video)
4. **#courses** — Live instructor-led programs
5. **#self-paced** — Self-paced pricing (₹9,999 – ₹18,999)
6. **#pricing** — Toggle live vs self-paced pricing

## YouTube playlist

Edit `script.js` and paste your playlist URL or ID:

```javascript
const YOUTUBE_PLAYLIST = "https://www.youtube.com/playlist?list=PLxxxxxxxx";
```

You can also use just the ID: `"PLxxxxxxxx"`.

## Meta ads URL

Point ads to:

```
https://yoursite.com/?utm_source=meta
```

The form auto-selects **Meta (Facebook / Instagram) Ads** as the source.

## Payments (Razorpay)

All **Pay with Razorpay** buttons link to:

[https://razorpay.me/@anshumanbehuria](https://razorpay.me/@anshumanbehuria)

To change the URL, edit `RAZORPAY_URL` in `script.js` (and `href` on `.razorpay-link` elements in `index.html`).

## Customize

| Item | Location |
|------|----------|
| Brand | Search "SAP Pro Academy" in `index.html` |
| Live prices | Course cards, `#pricing` live grid |
| Self-paced prices | `#self-paced`, `#pricing` self grid |
| Slide content | `.info-slide` articles in `#learn` |
| Contact | Footer |

## Files

- `index.html` — structure
- `styles.css` — dark + corporate light sections
- `script.js` — carousel, video, pricing tabs, form
