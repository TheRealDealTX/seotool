# deniedtheclaim.com — Denied the Claim

Attorney lead-generation and information site for **The Lawgical Firm, P.A.**
(Florida property insurance claims). It is a Florida homeowner's step-by-step guide
for when the property insurer denied the claim. It covers reading the denial letter,
common denial reasons and getting the claim documents. It also compares appraisal,
DFS mediation, a Civil Remedy Notice and a lawsuit, and covers deadlines and when
to call a lawyer. Phone (407) 433-4131. Firm details live in `FIRM` in `build.py`.
The attorney-advertising footer, CTA band, sidebar and lead form all render from it.

Hosting: Hostinger Cloud addon website, canonical origin `https://deniedtheclaim.com`
(`STAGING = False`, so pages are indexable).

## Keyword targets (one per page)

| Path | Primary keyword |
| --- | --- |
| `/` | denied the claim (exact match; `validate.py` requires 6–10 visible lowercase uses) |
| `/insurance-denied-my-claim-florida/` | insurance denied my claim Florida |
| `/denial-letter-explained/` | denial letter explained |
| `/wear-and-tear-denial/` | wear and tear denial |
| `/late-notice-claim-denial/` | late notice claim denial |
| `/how-to-appeal-a-denied-homeowners-insurance-claim-florida/` | how to appeal a denied homeowners insurance claim Florida |
| `/denied-hurricane-claim/` | denied hurricane claim |
| `/denied-water-damage-claim/` | denied water damage claim |
| `/free-case-review/`, `/about-the-firm/`, `/disclaimer/`, `/privacy-policy/`, `/sitemap/`, `404.html` | site pages |

Guide pages carry "Last reviewed: October 2026" and Article + FAQPage schema.
The FAQPage schema is generated from each page's `<details class="faq">` blocks.
Guides cite Florida Statutes, so re-check the legal content when the statutes change.

## Design

The look is a "legal notebook":

- Colors: off-white paper (`#f6f2e9`), ink black (`#17140f`) and one red-orange accent (`#c4381a`).
- Type: Fraunces for headlines, Public Sans for body text and IBM Plex Mono for labels and citations.
- Home page: a ruled-paper hero with a red margin line, a sample denial letter "exhibit" with a DENIED stamp, a black strip of key deadlines, and nine large outlined step numbers.
- Tables are styled like ledgers. Guide pages have a sticky table of contents.
- A small vanilla-JS deadline worksheet works out the general s. 627.70132 and s. 95.11(2)(e) dates from a date of loss.

## Layout

| Path | What it is |
| --- | --- |
| `src/pages/*.html` | Page bodies; the first line is a JSON header (path, title, description, crumb, article, group) |
| `src/static/` | Copied verbatim: CSS, JS, favicon.svg, logo, `index.php`, `.htaccess`, `api/` |
| `src/static/index.php` | Front controller: serves `home.html` for `/`, redirects www and http to the https apex, and returns a real 404 for unknown URLs |
| `src/static/api/lead.php` | Free case review form. Appends leads to `public_html/data/leads.php`, which returns 404 on the web. If `public_html/data/lead-config.php` exists on the server, it also emails each lead. Never commit that file; its format is in the `lead.php` header |
| `build.py` | Wraps pages in the layout and writes `public/`, plus sitemap.xml and robots.txt |
| `validate.py` | Checks one H1 per page, unique title, description and canonical, canonical URLs, internal links and anchors, no `href="#"`, JSON-LD types, disclosures, restricted advertising words, guide word counts, and homepage keyword placement and count |

## Build & deploy

```sh
python3 build.py && python3 validate.py && ../deploy-cloud.sh deniedtheclaim
```
