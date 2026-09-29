# Administrator guide

Sign in at **https://rodeotexas.org/admin/**. Sessions end after 2 hours idle or 12 hours total;
5 wrong passwords lock the account for 15 minutes. Change your password under **Account**.

## Weekly routine (10–15 minutes, Monday after 7 AM Central)

1. **Dashboard** — check the last import is *success*. A red box lists failing sources (their
   events were left unchanged). You also get an e-mail when a source fails.
2. **Review queue** — work through open items:
   * **Event submissions** → *Create event from this submission…* opens a prefilled event form.
     Verify every detail against the official source, then publish. Or *Reject*.
   * **Correction reports** → check the evidence, edit the event, *Mark resolved*.
   * **Import conflicts** → a source disagrees with a value you edited (or with another source):
     *Apply incoming value* or *Keep current value*.
   * **Possible duplicates / unclear location** → link to the matching event ID, create a draft,
     or ignore.
   * **Incomplete imported events** → open the draft, fill what is missing *from the official
     source*, publish.
   * **Contact messages** → reply by e-mail (the sender's address is shown), then resolve.
3. **Links & missing info** — press *Check links now*; fix broken links; fill gaps only from
   official sources.

## Events

* **Events** → search/filter; tick several and *Publish / Unpublish / Archive*.
* **Publishing states:** *Draft* (hidden), *Published*, *Archived* (page stays reachable for old
  links but is hidden from search engines). Past events stay published and move to *Past events*
  automatically; archive only if a page is wrong or unwanted.
* **Status:** *Scheduled*, *Postponed*, *Canceled* (+ public status note). Upcoming / Happening now /
  Completed are calculated from the dates in the venue's time zone.
* **Show times:** one per line, venue local time: `2026-10-03 19:30` or `2026-10-03 7:30pm-9:30pm | Slack`.
  El Paso-area venues are automatically in Mountain Time.
* **Ticket links** appear publicly only after you tick *I checked this ticket link…*.
* **Verification:** tick *I verified these details… today* to update “Last verified”.
* **Related competitions:** enter another event's ID in *Group with related event* (e.g. link the
  breakaway to the main rodeo).
* **Import protection:** fields you change are locked against imports. Tick *unlock* to let the
  source update a field again.
* **Changing a URL slug** creates a 301 redirect automatically.
* **Never invent information.** Leave a field empty if the organizer hasn't published it; the site
  shows “Not listed”.

## Venues

Venue name, address, map position, region, time zone, and default parking/accessibility text
(used by every event at that venue unless the event overrides it). Editing a venue protects it from
automatic updates. *Locate up to 25 now* fills missing map positions via OpenStreetMap.

## Sources & imports

* **Sources** — each source's access status, health, and recent records (with skip reasons).
  *Run this source now* runs just that source. CSV sources have *Upload & import*.
* Only enable automation for sources whose terms allow it. Record permission e-mails in *Access notes*.
* **Import history** — every run with statistics and full log (filter warnings/errors).
* **Run import now** (Dashboard) runs all enabled sources with the same safety rules as cron. If
  cron is already running you'll see “Another import is already running”.

## Articles

**Articles** → edit title, URL slug, SEO title, meta description, excerpt, HTML content, featured
image path and categories. Old article images live under `/wp-content/uploads/…`. New images:
upload in hPanel File Manager to `public_html/assets/img/articles/` (WebP, ≤ 1600 px wide) and use
`/assets/img/articles/name.webp`.

## Other

* **Redirects** — add 301s for any URL you retire; the hit counter shows which are still used.
* **Associations** — labels shown on events; add new sanctioning bodies here.
* **Account** — change password, add another administrator.
* **Forgotten password** — over SSH: `php app/bin/create-admin.php --email=you@… ` (resets it).

## Site-wide code (analytics, pixels, verification tags)

Edit `public_html/includes/head.php` (block *SITE-WIDE HEAD CODE*) in hPanel File Manager. It
appears on every public page and never in the admin area.
