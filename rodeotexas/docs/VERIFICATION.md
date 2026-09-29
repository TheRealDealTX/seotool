# Verification results (2026-09-29)

Environment: local PHP 8.4 + MariaDB 10.11 (code targets the Hostinger server's PHP 8.2), Chromium via Playwright,
live source feeds for the import. Production deployment status is at the end.

## Automated integration tests — `tests/run.php`: **101 passed, 0 failed**

| Area | What was proven |
| --- | --- |
| Texas-only | TX state / Texas ZIP accepted; Oklahoma venue skipped; no-location record skipped or sent to review, never guessed |
| Time zones | El Paso & Hudspeth → Mountain Time (by county or ZIP); 7:30 PM El Paso = 01:30Z; Central after DST end = UTC−6; `.ics` uses correct UTC; labels show MDT/CDT |
| Status | upcoming / happening now / completed from venue-local dates; canceled & postponed override |
| Shortcuts | “This weekend” (Tue → Fri–Sun; Sat → Sat–Sun), “This month” |
| First import | 4 Texas events created & published, 1 out-of-state skipped, 1 non-rodeo filtered, 1 no-location skipped |
| Repeat import | identical data → 0 new, 7 unchanged, no duplicate source records (idempotent) |
| Manual corrections | admin-edited title stays; one import-conflict review item, not duplicated on re-run |
| Source changes | rescheduled dates applied + logged; explicit “CANCELED:” sets canceled; new event added; youth level detected |
| Disappearing events | removed from feed → still scheduled & published |
| Cross-source duplicates | same rodeo from an iCal feed matched to the existing event, not duplicated |
| Distinct competitions | breakaway kept separate from the rodeo and grouped with it |
| JSON-LD adapter | Event imported; `EventPostponed` → postponed; offer URL stored but not shown until verified |
| Failures | HTTP 500 source and non-JSON source → run “partial”, errors logged, failure counters incremented, **existing events byte-identical** |
| Overlap | second run while locked → refused, nothing changed |
| CSV fallback | Texas row imported, Oklahoma row skipped, bad row reported; “7:30 pm” parsed; re-upload → no changes |
| Search/filters | name, city, venue, exact ZIP, ZIP-area fallback, literal `%`/`_`, association, level, type, date overlap, hostile values ignored, drafts hidden |
| Forms | honeypot, too-fast, tampered token, cross-form token, per-IP rate limit |
| Auth | password hashed (bcrypt), short passwords rejected, lockout after 5 failures |

## End-to-end HTTP tests — `tests/http.php`: **53 passed, 0 failed**

All public pages 200; titles/descriptions/canonicals/OG tags; analytics tag on public pages and **absent from admin**;
`/includes` and `/pages` blocked; 404 for unknown URLs; **all 21 articles at original URLs; all 199 retired URLs 301 to the
right target; all 184 Texas legacy URLs kept (noindex)**; valid Event JSON-LD with Texas address; date shows year; source and
last-verified shown; `.ics` download; favorites API; reflected-XSS attempt escaped; forged form token rejected; honeypot
discarded; valid contact message stored; admin requires login; admin CSP + noindex; session cookie HttpOnly + SameSite=Strict
(+ Secure on HTTPS); login and logged-in POSTs without CSRF token → 400; cross-origin POST → 400.

## Browser checks (Playwright, Chromium)

* Desktop 1280 px and phone 390 px screenshots reviewed: home, directory, calendar (month grid on desktop, agenda list on
  phone), map, event page, mobile menu, admin dashboard and editor. Found & fixed: calendar columns stretched by long titles;
  mobile weekday header; admin button font.
* Map view: Leaflet from cdnjs with SRI + OpenStreetMap tiles → 3 venue markers, list under the map, no JS errors.
* Full flow: visitor submits an event on a phone → thank-you page; invalid ZIP (Oklahoma) → 6 field errors; favorites
  saved and shown on /favorites/; admin opens the submission, creates the prefilled event, adds a show time and publishes →
  public search finds it (“starts 7:30 PM CDT”).
* Admin: every page loads without PHP warnings or JS errors under the strict CSP.

## Live import (real sources, local DB)

`140 fetched, 4 new (3 published, 1 held for review), 136 filtered, 0 errors; 5/5 sources OK` — PBR Rattler Days
(Dickies Arena, Oct 2–4 2026), Fort Worth Stock Show & Rodeo (Jan 15–Feb 6 2027), Brazos Valley Fair and Rodeo (Bryan,
Oct 23–25 2026); Stephenville “Rodeo Heritage” held for review (no link in the feed). Second run: 140 unchanged.

## Installer (simulated Hostinger directory with a fake WordPress)

check → backup (DB dump + WordPress files moved, uploads & Search Console file kept) → extract → migrate → seed → admin →
import → cleanup (package + installer deleted); wrong token → 404; config.php written 0600 outside the web root.

## Production

* Database `u401386392_rodeo` created on Hostinger (via API).
* **Files not yet deployed:** the Hostinger file-upload API returns 404 for this account (tested for rodeotexas.org and the
  main domain), and a remote-download installer variant was not used for security reasons. The live site is still the
  original WordPress. See docs/DEPLOYMENT.md §7 for the File Manager upload steps.
