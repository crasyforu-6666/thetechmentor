# Switching on lead capture, payment alerts and tracking

All three are configured in `site-config.js`. Until a value is filled in, that feature is simply off.

## 1. Leads & payments → Google Sheet + email (≈10 minutes, free)

1. Create a new Google Sheet (e.g. "YourOneMentor Leads") while signed in to the Google account you want alerts on.
2. In the sheet: **Extensions → Apps Script**.
3. Delete the sample code, paste in everything from `integrations/google-apps-script.gs`, and change `NOTIFY_EMAIL` if needed. Save.
4. Click **Deploy → New deployment** → type **Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Click **Deploy**, approve the permissions, and copy the **Web app URL** (ends in `/exec`).
6. Paste it into `site-config.js` as `LEAD_WEBHOOK_URL`, then redeploy the site.
7. Test: submit the strategy-call form on the live site. A row should appear in the **Leads** tab and an email should arrive within a minute.

Payments appear in a **Sales** tab. These rows come from the buyer's browser, so treat them as alerts.
Always confirm money against the Razorpay dashboard. Razorpay also emails you each payment.

## 2. Meta Pixel

Meta Events Manager → Data sources → your Pixel → copy the numeric ID → `META_PIXEL_ID`.
Events sent: `PageView`, `Lead` (form submit), `InitiateCheckout` (checkout opened), `Purchase` (payment success, with value in INR).
In Ads Manager, set your campaigns to optimise for **Leads** or **Purchases**.

## 3. Google Analytics 4

analytics.google.com → Admin → Data streams → Web → copy the `G-…` ID → `GA4_ID`.
The same events are sent as `lead`, `begin_checkout` and `purchase`.

## Ad links

Point Meta ads at `https://youronementor.com/?utm_source=meta&utm_campaign=<name>`.
UTM values are saved with every lead so you can see which campaign produced it.
