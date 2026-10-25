# Network build status

Scheduled agents read this file first and append to it last. Keep entries short and dated.

## Fixed facts

- Program start (week 1 Monday): 2026-11-02. Week N = Monday of 2026-11-02 plus 7*(N-1) days.
- Branch: `claude/wonderful-clarke-j4ygbp`. All network work is committed and pushed here.
- Calendar: `network/content_calendar_q1.csv`. Link schedule: `network/link_schedule_q1.csv`. Rules: `network/NETWORK_PLAN.md`.
- Money sites (primary): huttoroofs.com, templeroofs.com, kyleroofs.com, copperascoveroofs.com. Optional extra targets, same owner, already hosted on Hostinger: austinsroofing.com, claimroofleak.com, stormclaims.org, houstonpublicadjusting.com, publicadjustersdallas.com. Use them only from the storm-damage and insurance-claim posts.
- Hosting: all nine domains are LIVE on the Hostinger Agency Plan (platform h5g, php-fpm, server 72.60.128.114, account username u914589053, order 1008744732). DNS resolves and every domain returns HTTPS 200 (checked 2026-10-25). Each already serves a static HTML site with its own template and angle (see table). Do not rebuild from scratch: mirror the live site into `network/sites/<domain>/live/` first, keep its template, palette and persona, and extend it.
- Deploy method (Hostinger connector, agency-hosting group): `agency-hosting_files_generate-upload-url` with the site's website_uid returns url, auth_key, rest_auth_key; upload each file with the TUS protocol via curl (POST then PATCH, headers X-Auth, X-Auth-Rest, Tus-Resumable: 1.0.0) to `public_html/<path>?override=true`. Verify by fetching the page over HTTPS. Never use `agency-hosting_files_import-website-from-archive` (it overwrites the whole site).
- Footprint warning: all nine sit on one IP shared with about 240 other sites on the same account, and all use Google Fonts. Accept for now; the plan's hosting-split advice stands if rankings stall.
- Angle mismatches to resolve (see log): comeicavoliamerenda.com is live as an earring/piercing guide although its real links are food-blog links; agadecor.com is live as Chicago wedding and event decor while the calendar assumed home decor; fraserandmorris.com is live as London garden design while the calendar assumed interiors. michellewhitephoto.com is live under the real photographer's name, which the plan says to avoid.
- Link timing: weeks 1 to 4 publish with no network links. Weeks 5 to 6 add Tier 2 to Tier 1 links. Money-site links start week 7. Strip the `network_link_out` value from any post published before its allowed week and add it in a later edit.

## Per-domain state

| Domain | Tier | Agency website_uid | Live title (2026-10-25) | DNS live | Disavow uploaded | Last week built | Last week deployed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hatetolovethesplit.com | 1 | JpvYWffmb | Hate to Love the Split: A Minneapolis Split-Level DIY Blog | yes | no | 0 | 0 |
| agadecor.com | 1 | DlnCdXsX9 | Wedding & Event Decor in Chicago, AGA Decor | yes | no | 0 | 0 |
| ohmtoherminediy.com | 1 | WSPEsjCDT | Oh, Mother Mine DIY: Easy DIY Home Decor & Crafts for Moms | yes | no | 0 | 0 |
| fraserandmorris.com | 1 | haI1jJ1FP | Garden Design London, Fraser & Morris Garden Designers | yes | no | 0 | 0 |
| rjbledlcdtvservicecentre.com | 1b | DZbtKzYiX | LED LCD TV Service Centre Kolkata, RJB TV Repair | yes | no | 0 | 0 |
| asmith.photography | 2 | xpKP4rrWT | asmith.photography, Los Angeles Photography Journal | yes | no | 0 | 0 |
| michellewhitephoto.com | 2 | TgdLuLxCB | Michelle White Photography, Salt Lake City Photographer | yes | no | 0 | 0 |
| comeicavoliamerenda.com | 2 | jlj9tGHeI | Come i Cavoli a Merenda: Earring Sizes & Piercing Guide | yes | no | 0 | 0 |
| findsforfitness.com | 2 | kAOBwY0ha | Finds For Fitness: Workouts, Weight Loss, Skin Care & Gear | yes | no | 0 | 0 |

## Log

- 2026-10-25: plan, calendar and link schedule committed. Scheduled tasks created: one-shot setup, weekly posts, monthly review.
- 2026-10-25: corrected hosting facts. All nine sites are live on the Agency Plan with existing templates. Setup task re-pointed to mirror and extend the live sites. Calendar rows for agadecor.com (event decor), fraserandmorris.com (garden design) and comeicavoliamerenda.com (live angle is piercing; recommended to revert to food) need re-targeting by the setup task; until then those rows are marked needs-retarget.
