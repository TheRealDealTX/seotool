# External services, costs and open dependencies

| Service | Used for | Cost | Account / key |
| --- | --- | --- | --- |
| Hostinger Cloud Enterprise (existing plan) | Hosting, MySQL, cron, SSL, e-mail sending, daily backups | Already paid (existing subscription) | existing |
| OpenStreetMap tiles (`tile.openstreetmap.org`) + Leaflet 1.9.4 via cdnjs | Map view and event mini-maps | Free; subject to the [OSM tile usage policy](https://operations.osmfoundation.org/policies/tiles/) (attribution shown; fine for this traffic level). If traffic grows a lot, switch `map.tile_url` to a commercial tile provider (e.g. MapTiler/Stadia free tiers, then paid). | none |
| OpenStreetMap Nominatim | Turning venue addresses into map positions (only for new venues; results cached) | Free; max 1 request/second, identified User-Agent (built in) | none |
| Google Maps (links only) | “Get directions” button opens Google Maps | Free (a plain link, no API) | none |
| Google Analytics 4 | Analytics (tag carried over) | Free | existing GA property |
| cdnjs (Cloudflare) | Serves Leaflet with Subresource Integrity | Free | none |

No paid service is required. Fonts are self-hosted (Zilla Slab, SIL Open Font License).

## Unresolved dependencies

1. **PRORODEO / PRCA data** — requires permission or a data agreement from PRCA; until then
   enter PRCA rodeos manually/CSV from organizers' own announcements.
2. **Houston Livestock Show and Rodeo** and **Cowtown Coliseum** — feeds exist but their terms
   forbid automated collection; ask for written permission (then enable the pre-configured sources).
3. **Association schedules** (IPRA, UPRA, CPRA, THSRA, TYRA, AJRA…) — no feeds; request
   spreadsheets or add by hand.
4. **Coverage** — automated sources currently yield only a handful of upcoming rodeos; most listings
   will come from submissions, CSV imports and editor entry until more organizers share feeds.
5. **E-mail deliverability** — alerts are sent with PHP `mail()` from `no-reply@rodeotexas.org`.
   Creating that mailbox/alias in hPanel (with SPF/DKIM enabled for the domain) improves delivery to Gmail.
