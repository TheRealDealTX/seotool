# Network build status

Scheduled agents read this file first and append to it last. Keep entries short and dated.

## Fixed facts

- Program start (week 1 Monday): 2026-11-02. Week N = Monday of 2026-11-02 plus 7*(N-1) days.
- Branch: `claude/wonderful-clarke-j4ygbp`. All network work is committed and pushed here.
- Calendar: `network/content_calendar_q1.csv`. Link schedule: `network/link_schedule_q1.csv`. Rules: `network/NETWORK_PLAN.md`.
- Money sites (primary): huttoroofs.com, templeroofs.com, kyleroofs.com, copperascoveroofs.com. Optional extra targets, same owner, already hosted on Hostinger: austinsroofing.com, claimroofleak.com, stormclaims.org, houstonpublicadjusting.com, publicadjustersdallas.com. Use them only from the storm-damage and insurance-claim posts.
- Hosting: as of 2026-10-25 none of the nine network domains has a website on the Hostinger account (checked `hosting_websites_list`). Sites must be created there or elsewhere, and DNS pointed, before posts go live. Until a domain is live, its posts are built into `network/sites/<domain>/` in this repo and marked "built, not deployed".
- Link timing: weeks 1 to 4 publish with no network links. Weeks 5 to 6 add Tier 2 to Tier 1 links. Money-site links start week 7. Strip the `network_link_out` value from any post published before its allowed week and add it in a later edit.

## Per-domain state

| Domain | Tier | Persona | Template | Hosting | DNS live | Disavow uploaded | Last week built | Last week deployed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hatetolovethesplit.com | 1 | not set | not built | none | no | no | 0 | 0 |
| agadecor.com | 1 | not set | not built | none | no | no | 0 | 0 |
| ohmtoherminediy.com | 1 | not set | not built | none | no | no | 0 | 0 |
| fraserandmorris.com | 1 | not set | not built | none | no | no | 0 | 0 |
| rjbledlcdtvservicecentre.com | 1b | not set | not built | none | no | no | 0 | 0 |
| asmith.photography | 2 | not set | not built | none | no | no | 0 | 0 |
| michellewhitephoto.com | 2 | not set | not built | none | no | no | 0 | 0 |
| comeicavoliamerenda.com | 2 | not set | not built | none | no | no | 0 | 0 |
| findsforfitness.com | 2 | not set | not built | none | no | no | 0 | 0 |

## Log

- 2026-10-25: plan, calendar and link schedule committed. Scheduled tasks created: one-shot setup, weekly posts, monthly review.
