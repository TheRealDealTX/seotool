# cowboytinyhomes.com — Texas tiny home builder + house plan store

The PHP site (`site/`, deployed to `public_html`) for Cowboy Tiny Homes, a Texas design-build
company, with a catalog of 25 Texas house plans that are sold as instant downloads and lead
into build consultations. The plan generator, 3D viewer and store engine are shared with
`../tinyhomesblueprint/` (see "Shared code" below).

| Path | What it is |
| --- | --- |
| `site/index.php` | Front controller. Routes come from `inc/pages.php` (`PAGES`), which adds one route per plan and the `/order/` pages. |
| `site/inc/config.php` | Business details, nav, store settings (`STORE_PREFIX`, `PLAN_CREDIT`), Texas cost table (`TX_REGIONS`), `plan_url()`. |
| `site/inc/plans.php` | The plan catalog: specs, copy and room geometry (main floor, second floor, lofts, porches). |
| `site/inc/plan-ui.php` | Plan cards, catalog grid, "plans you can buy" strips, Texas regulation and build notes. |
| `site/inc/store.php`, `mailer.php` | Stripe Checkout, order records, download links, delivery email (shared). |
| `site/pages/plan.php` | Plan page: buy box, build call to action, drawing previews, 3D viewer, Texas notes, cost estimate, materials. |
| `site/pages/gonzales-modern-living.php` | The original featured design: keeps its URL, H1 and story and uses the plan template. |
| `site/pages/home-designs.php` | `/home-designs/`: the filterable catalog (`/home-designs/#adu` opens a filter). |
| `site/pages/order/` | `/order/checkout/`, `complete/`, `download/`, `lookup/`, `webhook/` (noindex, not in the sitemap). |
| `site/pages/terms-of-sale.php` | License, delivery, refunds, build credit and the professional-review notice. |
| `site/assets/plans/<slug>/` | Generated public previews: watermarked SVGs, `model.json`, 3D renders. |
| `site/inc/plan-sets.json` | Generated estimate, materials summary, HVAC sizing and file list for each plan page. |
| `generator/` | Plan-set generator (shared code) plus `profile.json` (this site's brand, Texas climate, slab, notes and cost regions). |
| `dist/plan-files/` | Generated paid downloads (not committed; uploaded outside the web root). |
| `tests/e2e_store.py` | End-to-end purchase test against a fake Stripe API (`tests/mock_stripe.py`). |
| `validate.php` | Catalog checks: room tiling, stairs, square footage in the copy, routes, Texas cost table. |
| `deploy.sh` | Uploads `site/` to `public_html/` and the zips to `cth-plan-files/`. |

## The catalog

| Category | Plans |
| --- | --- |
| Small homes (400–1,800 sq ft) | Comal Cottage, Bandera, Gonzales Modern Living (two-story), Pedernales, Llano Dogtrot, Lockhart Farmhouse, Fredericksburg, Brazos, Mesquite |
| ADUs & casitas | Alamo Heights Casita, King William Casita, Mueller ADU, Bluebonnet Granny Flat (accessible), Bishop Arts ADU (two-story), Magnolia Guest House |
| Park models (ANSI A119.5) | Guadalupe, Medina, Frio (loft) |
| Tiny homes on wheels | Maverick (20 ft), Wrangler (26 ft), Rodeo (30 ft gooseneck), Big Bend (36 ft gooseneck) |
| Studios & offices | Hill Country Studio, Ranch Office, Pool House Studio |

Prices run $295–$1,495. Gonzales Modern Living stays at $1,000 and at `/gonzales-modern-living/`;
the other plans live at `/home-designs/<slug>/`.

## What makes the plans Texas plans

All of this comes from `generator/profile.json` and shows up on the drawings, the plan pages and the estimate:

- **Climate (IECC zones 2–3):** radiant-barrier roof deck, R-38 attic / R-30 cathedral, R-21 walls,
  windows SHGC 0.25 max., 18 in. overhangs, covered porches, ceiling fans in living rooms,
  bedrooms and on porches, and ductless heat pumps sized room by room (22 BTU/sq ft) with a schedule on E1.0.
- **Expansive clay:** stiffened slab with 12 x 24 in. grade beams and interior beams at 15 ft,
  select fill, termite pre-treatment, and a "final design from a geotechnical report" note.
- **Wind:** 115 mph inland design wind with uplift connectors; the cover, the plan pages and the
  FAQs flag the Gulf Coast windborne-debris region and TDI windstorm certification. No snow load.
- **Regulation:** cover-sheet notes are picked by plan type: IRC with local amendments (cities)
  and no residential code in many counties; ADU rules by city; park models as RVs under
  ANSI A119.5; tiny homes on wheels under TxDMV trailer, size and weight rules. All link the
  existing Texas tiny house laws guide.
- **Costs:** every estimate has totals for Austin, Dallas, Houston, Fort Worth, San Antonio and
  rural Texas (factors against 2026 US averages). The same table (`TX_REGIONS`) drives the plan-page
  estimate and the cost calculator at `/tools/tiny-home-cost-calculator/`. The factors are planning
  estimates; adjust them in both places if your own bids say otherwise.

## Builder tie-in

Every plan page has a "Have Cowboy Tiny Homes build it" section and a build-quote link in the
buy box, both prefilled into the contact form. The plan price is credited toward a build contract
signed within 12 months (`PLAN_CREDIT` in `config.php`; repeated in the order email, the success
page and the terms of sale). Service and city pages show matching plans.

## Generating the plan sets

```
python3 generator/build.py                 # all 25 plans (about 3 minutes)
python3 generator/build.py bandera         # one or more plans
php validate.php
```

Needs PHP 8, Python 3 with `reportlab` and `Pillow`, Node with `playwright` and Chromium. Each zip
holds the 24 x 36 PDF set (10–13 sheets; two-story plans get second-floor plan, electrical and
plumbing sheets), a DXF, CSVs, an OBJ model, PNG images and a README with the license and the
review notice. Everything generated is planning documentation: the cover sheet, README and terms
tell buyers to have the set reviewed — and sealed where their jurisdiction requires — by a
Texas-licensed engineer or architect.

## Checkout setup (one time)

Same Stripe account as tinyhomesblueprint.com, with its own webhook:

1. Stripe dashboard → Developers → Webhooks → add `https://cowboytinyhomes.com/order/webhook/` for
   `checkout.session.completed`, `checkout.session.async_payment_succeeded` and `charge.refunded`;
   copy its signing secret (`whsec_...`). The secret key (`sk_live_...`) is the same as the other site's.
2. Create `cth-secrets.php` one level above `public_html`
   (`/home/u401386392/domains/cowboytinyhomes.com/cth-secrets.php`):

   ```php
   <?php return [
       'stripe_secret' => 'sk_live_...',
       'stripe_webhook_secret' => 'whsec_...',
       // 'stripe_tax' => true,   // optional: let Stripe Tax add Texas sales tax (set up Stripe Tax first)
   ];
   ```

   Store emails use the contact form's existing SMTP login in `public_html/inc/secrets.php`
   unless you add `smtp_host` / `smtp_port` / `smtp_user` / `smtp_pass` here.
3. Upload the zips: `./deploy.sh --files` (to `cth-plan-files/`).

Until a Stripe key is present (or a plan's zip is missing) the plan page shows "Order this plan",
which opens the contact form prefilled with the plan, so the site never shows a broken checkout.
Orders are JSON files in `cth-data/orders/` with a CSV log in `cth-data/orders.csv`; the buyer
and `contact@` are emailed on each sale; a full refund turns the link off; `/order/lookup/` re-sends links.
Order numbers start `CTH-` so they never collide with tinyhomesblueprint (`THB-`) in the shared Stripe account.

**Sales tax:** Texas generally taxes digital products, which likely includes downloaded plans
(6.25% state plus up to 2% local). Check with your CPA; if you decide to collect it, set up Stripe
Tax in the dashboard and add `'stripe_tax' => true`. It is off by default.

## Testing

```
python3 tests/e2e_store.py site /tmp/cth-e2e
```

Runs the whole flow against the fake Stripe API: fallback without keys, checkout parameters, signed
webhook, duplicate webhooks, success page, download, wrong token, success page before the
webhook, lookup with CSRF, refund, bad signature, a 100%-off order and the Stripe Tax switch.

## Local preview

```
php -S localhost:8000 -t site dev-router.php
```

## Shared code

`../sync-shared.sh` lists the files both plan-store sites share (generator `.py`/`.js`, the 3D
viewer, `plan-page.js`, `store.php`, `mailer.php`, `plan-svg.php`, the webhook). Edit them in either
site, then run `./sync-shared.sh <from> <to>`; `./sync-shared.sh --check` reports drift. Site-specific
behavior goes in `generator/profile.json` and `site/inc/config.php`, never in the shared files.

## Baseline and secrets

The first commit under `cowboytinyhomes/` is the untouched live `public_html` (Oct 30, 2026),
minus `inc/secrets.php` (SMTP login), `.private/` and `wordpress-backup-2026-10-28/` (contains
`wp-config.php`). Those stay on the server only and are git-ignored.
