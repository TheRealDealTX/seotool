# Event sources & the import process

## Status of sources (researched 2026-09-29)

No single source covers every Texas rodeo, and **PRORODEO has no documented public API**: its
site returns HTTP 403 (Incapsula bot protection) to automated requests. We do not bypass that.
Every source below was checked for a machine-readable format, `robots.txt` and terms of use.

### Implemented automation (running weekly)

| Source | Adapter | Why it is allowed | Notes |
| --- | --- | --- | --- |
| Dickies Arena, Fort Worth | `tribe_rest` | Public WordPress Events Calendar API; robots.txt allows all; no terms-of-use page | Keeps rodeo/PBR/stock-show items only. Feed omits the address, so the arena's address is set in `default_venue`. Title codes such as “2026.10.2-4 ” are stripped; “FWSSR” is expanded. |
| Destination Bryan (Bryan–College Station CVB) | `jsonld` | schema.org Event data on public pages found through the public event sitemap; robots.txt allows; no automated-access restriction | Concerts held at a rodeo are excluded (`exclude_acts`). |
| Visit Stephenville | `ical` | Public CivicPlus iCalendar feed; path allowed by robots.txt | Mostly community events → rodeo keyword filter. Records without a location go to review. |
| Visit Mesquite | `tribe_rest` | Public API; robots.txt Crawl-delay 10 is honoured | Currently no rodeos listed; venues often blank → review. |
| Freeman Coliseum, San Antonio | `tribe_rest` | Public API; robots.txt disallows only /wp-admin/ | Currently no rodeos listed. |

### Awaiting access (manual CSV fallback works today)

| Source | Blocker | What to do |
| --- | --- | --- |
| PRORODEO / PRCA schedule | Bot protection (403); no public API; no published reuse licence | Ask PRCA for a data feed or written permission. Meanwhile enter events you're entitled to list by hand or CSV. |
| Houston Livestock Show and Rodeo | Working API, but terms of use forbid “data mining, robots, or similar data gathering” | Ask for written permission, then set the source to *active* + *enabled*. |
| Cowtown Coliseum / Stockyards Championship Rodeo | Operator terms (Legends Global) forbid systematic retrieval to build a directory | Ask for permission. |
| IPRA, THSRA and other associations | HTML/Wix pages only, no feed or licence | Request a spreadsheet; import as CSV. |
| rodeosusa.com, rodeo.guide (aggregators) | Terms forbid crawling/reuse | Use only to discover organizers by hand. |

Details and quotes from each terms page are in the `access_note` of each source (Admin → Sources).

## Adapters (`app/adapters/`)

Each adapter only **fetches and normalizes**; it never writes to the database.

| Adapter | Class | Config keys |
| --- | --- | --- |
| `tribe_rest` | `TribeRestAdapter` | `base_url`, `days_ahead`, `max_pages` |
| `ical` | `IcalAdapter` | `url`, `timezone` |
| `jsonld` | `JsonLdAdapter` | `urls` or `sitemap_url` + `url_pattern`, `max_pages`, `timezone` |
| `csv` | `CsvAdapter` | (file uploaded in the admin or `--file=`) |

Common keys: `require_keywords`, `exclude_keywords`, `exclude_acts`, `title_strip_regex`,
`title_replace`, `default_venue`, `unknown_location` (`skip`|`review`), `min_delay`.

**Adding a source:** Admin → Sources → *Add a source*, pick the adapter, paste the config JSON,
record what the site's terms say in *Access notes*, set access status *active*, save, press
*Run this source now*, check the import log, then tick *Run automatically every week*.
A new source type = one new class extending `RT\Adapters\Adapter` + one line in
`Importer::adapterFor()`.

## Import rules (`app/lib/Importer.php`)

1. **Scheduling:** cron at 12:00 and 13:00 UTC on Mondays; the script proceeds only at 07:00
   America/Chicago (DST-safe). Manual runs: Admin → Dashboard → *Run import now*, or CLI.
2. **No overlap:** an exclusive file lock; a second run exits with “Another import is already
   running” and changes nothing. A crashed run is marked *abandoned* on the next start.
3. **Source failure = no changes:** each source is fetched completely before anything is written.
   Network errors, HTTP 429/5xx are retried 3× with exponential backoff; if it still fails, the
   source is marked failed, the admin is e-mailed and its existing events are left untouched.
4. **Texas only:** a record is imported only if its venue state is Texas, or its ZIP is a Texas
   ZIP (75xxx–79xxx, 885xx). Other states are skipped. No location → skipped or sent to review
   (per source). Circuit membership is never used.
5. **Stable identity & idempotency:** `(source, source uid)` is unique; the normalized record is
   hashed, and an identical record is a no-op (only “last seen/verified” is updated).
6. **Cross-source duplicates:** a new record is compared with existing events whose dates overlap
   (±1 day): same normalized title *and* same city → linked to that event; same title with an
   unknown city, or several candidates → review queue.
7. **Distinct competitions are kept apart:** titles differing by a discriminator (breakaway,
   Xtreme Bulls, steer roping, barrels, youth, finals …) are never merged; if they share the base
   name, city and dates they are **grouped** and shown as “Related competitions”.
8. **Auto-publish** only complete records (Texas city, official/source link, sensible dates) from
   sources set to auto-publish; everything else is saved as a draft + review item.
9. **Updates:** the primary source updates dates, venue, links, prices, times, and status.
   Other sources only fill empty fields; disagreements become review items.
10. **Manual corrections win:** any field an admin edits is locked. Imports never overwrite it;
    a differing value creates one *import conflict* review item (deduplicated).
11. **Cancellations:** set only when the source says so explicitly (iCal `STATUS:CANCELLED`,
    schema.org `EventCancelled`/`EventPostponed`, or a “CANCELED:” / “POSTPONED:” title prefix).
    An event that disappears from a source is **never** canceled or deleted.
12. **Logs:** every run and message is stored (Admin → Import history) and summarized in
    `app/storage/logs/cron.log`.

## Manual CSV import

Template: `docs/csv-template.csv` (also downloadable in the admin). Required columns: `title`,
`start_date` (YYYY-MM-DD), and a Texas `city` + `state`/`postal_code`. Performances:
`2027-06-10 19:30; 2027-06-11 2:00 pm Matinee` (venue local time). Upload in Admin → Sources →
(CSV source) → *Upload & import*, or `php app/bin/import.php --source=manual-csv --file=events.csv`.
The same rules apply (Texas check, dedupe, locks). Re-uploading the same file changes nothing.
