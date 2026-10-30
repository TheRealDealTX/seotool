# tinyhomesblueprint.com — plan store

The PHP site (`site/`, deployed to `public_html`) plus the generator that turns each
plan's room layout into a complete, downloadable plan set, and the Stripe checkout that
sells it.

| Path | What it is |
| --- | --- |
| `site/` | The website. `index.php` routes every URL through `inc/config.php` (`$ROUTES`). |
| `site/inc/plans.php` | The plan catalog: specs, copy and room geometry for every plan. |
| `site/inc/store.php` | Stripe Checkout, order records, download links, delivery email. |
| `site/pages/plan.php` | Plan page: buy box, drawing previews, 3D viewer, cost estimate, materials. |
| `site/pages/order/` | `/order/checkout/`, `/order/complete/`, `/order/download/`, `/order/lookup/`, `/order/webhook/` |
| `site/assets/plans/<slug>/` | Generated public previews (watermarked SVGs, `model.json`, renders). |
| `site/inc/plan-sets.json` | Generated estimate, materials summary and file list for each plan page. |
| `generator/` | Python + Node plan-set generator (below). |
| `dist/plan-files/` | Generated paid downloads (not committed; uploaded outside the web root). |
| `deploy.sh` | Uploads `site/` to `public_html/` and the zips to `thb-plan-files/`. |
| `dev-router.php` | Local preview router. |

## Shared code

The generator, 3D viewer, `plan-page.js`, `store.php`, `mailer.php`, `plan-svg.php` and the
webhook are shared with `../cowboytinyhomes/`. Site-specific settings live in
`generator/profile.json` (brand, overhangs, climate features, slab, cover notes, README text) and
`site/inc/config.php` (`STORE_PREFIX`, `ORDER_PREFIX`, `plan_url()`). After editing a shared file in
either site run `../sync-shared.sh <from> <to>`; `../sync-shared.sh --check` reports drift.

Shared features this site picked up: full second floors (`'upper'` rooms with a `STAIR`),
breezeway / dogtrot plans, front, rear and side porches, half baths, walk-in closets, park-model
chassis, room-by-room heat pump sizing, and fixes for interior walls drawn past the exterior
face, gable walls showing through roofs, gooseneck windows above the eave and 3D stills
cropping porches.

## What a buyer gets

One zip per plan:

- **Construction drawing set** (24 x 36 in. PDF, 10–11 sheets): cover with project data,
  code and load notes and a 3D rendering; floor plan with dimensions and door, window and
  room-finish schedules; loft plan; four exterior elevations; building section with wall,
  roof and floor assemblies; foundation (or trailer) plan; roof framing plan with header
  schedule; electrical plan with legend, panel schedule and NEC load calculation; plumbing
  plan (hot, cold, drain-waste-vent) with fixture schedule; materials list; cost estimate.
- **CAD**: DXF (R12, inches, full scale) with every plan view, elevations and the section on
  separate layers (walls, doors, glazing, fixtures, dimensions, electrical, plumbing).
- **Materials list** and **cost estimate** as CSV.
- **3D model** (OBJ + MTL) and **PNG images** (3D views, plans, elevations).
- README with the license (one home) and the professional-review notice.

## How the generator works

```
python3 generator/build.py                 # all plans (about 2 minutes)
python3 generator/build.py plan-12-2429    # one or more plans
```

Needs PHP 8, Python 3 with `reportlab` and `Pillow`, Node with `playwright` and Chromium.

1. `export-plans.php` dumps `$PLANS` as JSON.
2. `thb_model.py` derives the buildable model from the room rectangles: interior and exterior
   walls, the entry and interior doors (every enclosed room is connected back to the living
   areas), windows with egress windows in sleeping rooms, kitchen / bath / laundry fixtures,
   electrical devices (NEC receptacle spacing, GFCI locations, switches, lighting, smoke/CO
   alarms, panel, mini-split), circuits and the service load, and plumbing supply and DWV runs.
3. `thb_qty.py` takes off materials (framing, sheathing, roofing, insulation, drywall, wire by
   circuit run, PEX and PVC by pipe run, concrete...) at 2026 US average prices, then builds the
   estimate (labor by trade, overhead, permits, contingency; owner-built and contractor).
4. `thb_mesh.py` builds the 3D model; `thb_views.py` / `thb_sheets.py` draw every view once
   against three backends in `thb_draw.py` (PDF, SVG previews, DXF).
5. `render.js` renders the 3D stills and PNGs with headless Chromium using the site's own viewer.

To add a plan: add it to `site/inc/plans.php` with `rooms` (and `loft`, `porch`, `roof_type`),
run the build, deploy. A room labeled `PORCH` is an inset porch (not heated area).

Everything generated is planning documentation. The cover, the README and the terms tell the
buyer to have structure, electrical and plumbing reviewed, and stamped where required, by
licensed professionals.

## Checkout setup (one time)

1. In the Stripe dashboard copy the **secret key** (`sk_live_...`).
2. Add a webhook endpoint `https://tinyhomesblueprint.com/order/webhook/` for the events
   `checkout.session.completed`, `checkout.session.async_payment_succeeded` and
   `charge.refunded`; copy its **signing secret** (`whsec_...`).
3. Add both to `thb-secrets.php`, which sits one level above `public_html`
   (`/home/u401386392/domains/tinyhomesblueprint.com/thb-secrets.php`) next to the SMTP keys:

   ```php
   <?php return [
       'smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
       'smtp_user' => 'contact@tinyhomesblueprint.com', 'smtp_pass' => '...',
       'stripe_secret' => 'sk_live_...',
       'stripe_webhook_secret' => 'whsec_...',
   ];
   ```

4. Upload the zips (`./deploy.sh --files`) to `thb-plan-files/`.

Until a Stripe key is present (or if a plan's zip is missing) the plan page falls back to
the original "Order this plan" contact form, so the site never shows a broken checkout.
Test first with `sk_test_...` keys and the card `4242 4242 4242 4242`.

Orders are JSON files in `thb-data/orders/` (also above the web root) with a CSV sales log in
`thb-data/orders.csv`. Each sale emails the buyer their link and emails `contact@` a notice.
A full refund in Stripe turns the download link off. Buyers can get fresh links at
`/order/lookup/`.

## Local preview

```
php -S localhost:8000 -t site dev-router.php
```

Set `THB_PRIVATE_DIR` to a folder holding a test `thb-secrets.php` and `thb-plan-files/` to
exercise checkout locally (`stripe_api_base` in the secrets can point at a mock API).
