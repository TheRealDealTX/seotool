# Pre-rebuild audit (2026-09-29)

## rodeotexas.org (WordPress on Hostinger)

Stack: WordPress + Elementor Pro, The Events Calendar (+ Event Aggregator), Rank Math, LiteSpeed
Cache, Google Site Kit (GA4 `G-BYZKZGNG2D`, Google tag `GT-MRQHZ43M`), Search Console file
`googlecccfbf2f7e9e5ae4.html`. Navigation: Schedule (home), Quick Search (`/rodeos/`), Past Events,
About, Blog, Contact.

| Content | Count | Decision |
| --- | --- | --- |
| Articles (`/{slug}/`) | 21 (1,300–2,000 words each, April–June 2026) | **Kept at identical URLs**, with SEO titles/descriptions, featured images and categories. |
| Pages: About, Contact, Privacy, Blog, Past Events, Home | 6 | Rebuilt; About/Contact copy kept; Privacy policy updated to be accurate (it claimed no cookies/tracking while GA was installed). |
| Categories `/category/general/`, `/category/how-to/` | 2 (+ unused "History") | Kept. |
| Events `/rodeos/{slug}/` | 365 | See below. |

Event data problems found: **no upcoming events** (latest ended 2026-09-21); **no venue, address,
organizer or price on any event**; many **outside Texas** (Fargo ND, Cave Creek AZ, Florida,
Alberta…); **201 events share the same wrong "official site"** (banderaprorodeo.org).

Migration of events:
* **184 events** identifiable as Texas rodeos (e.g. Rodeo Austin, Mesquite, San Angelo, Gladewater,
  Pecos) keep their URL as an **archived, noindex** page labelled “details not re-verified”, with the
  city from the event name and the real official link only where it wasn't the bogus one.
* **181 non-Texas/unidentifiable events** and WordPress-only URLs (feeds, sitemaps, `/events/`,
  `/rodeos/list/`, …) → **301** (199 redirects, `app/data/redirects.json`).
* `/wp-admin`, `/wp-login.php`, `/xmlrpc.php`, `/wp-json` → **410 Gone**.
* `/wp-content/uploads/` is **kept** (article images).

## prorodeo.com/schedule?circuitId=7 (reference)

Not accessible to automated tools: every request (page and robots.txt) returns **HTTP 403 from
Incapsula bot protection**. Its interface and data could therefore not be inspected, and it was not
copied. The new design is original and follows the brief (search, date/region/association/type
filters, weekend/month shortcuts, list/calendar/map views, event detail pages).
