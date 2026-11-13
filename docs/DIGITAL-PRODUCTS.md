# Digital Products storefront (Phase 1) — integration notes for Phase 2

## Files
| File | Role |
|---|---|
| `data/digital-products.json` | Single source of truth: server modules, durations, price matrix, highlights, PDF products (id, category, title, price, summary, format, pages, file, preview). |
| `scripts/build_digital_products.py` | Renders `digital-products.html` from the JSON (static cards for SEO + embedded JSON for the script). Re-run after any data change. |
| `digital-products.html` | Generated page (do not hand-edit). Served at `/digital-products` via `vercel.json` rewrite. |
| `digital-products.js` | Filters + Free Only toggle, server price matrix, unlock/order modal, preview drawer, lead capture, Razorpay hand-off. `loadData()` is the hook to swap for an API call. |
| `site.css` (section "Digital products") | `dp-*` styles on top of the site design system. |
| `downloads/` | Deliverable files. Set a product's `file` to a path here to enable instant download. |

## Data contract
- Price of a server order = `server.pricing[module.tier][duration.id]`.
- `price: 0` ⇒ FREE (lead-gated). `file: null` ⇒ lead captured, delivery by WhatsApp/email.

## Events sent today (via `tracking.js` → Google Sheet webhook / Meta / GA4)
- Free unlock: `{type:"lead", status:"Free PDF unlocked", program:"Digital: <title>", amount:0, name, email, phone}`
- Paid / server checkout start: `{type:"lead", status:"Digital checkout started", program:"Digital: <item>", amount}`
- Payment success (from `script.js`): `{type:"sale", program, amount, payment_id}` → `thank-you.html`

## Phase 2 checklist
1. Products/prices CRUD in Admin Panel writing the same schema (or an API returning it).
2. Razorpay webhook (server-side) → order record → automatic delivery: signed PDF link / server credentials e-mail + WhatsApp.
3. Student dashboard "My purchases" listing orders by email/phone.
