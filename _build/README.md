# sbarates.com build tools

The site is static HTML served from the repo root. This folder holds the
generator for pages rebuilt from old-URL exports, plus checks. It is blocked
from the web by `.htaccess` (`RewriteRule ^_build(/|$) - [F,L]`) and doesn't
need to be uploaded.

```bash
python3 _build/build.py      # render pages from content/*.json, refresh hubs, sitemaps, CTAs
python3 _build/validate.py   # links, titles, descriptions, H1, canonical, CTA on every directory page
```

| File | Purpose |
| --- | --- |
| `shell.py` | Page shell copied from the live templates, rate data (prime, 7(a) caps, 504 rate), lender-match CTA |
| `build.py` | Renders lenders, industries, blog posts, `/get-matched/`; rebuilds hub lists and sitemaps; injects the CTA site-wide |
| `content/lenders_*.json` | 53 lender profiles (slug, about, known_for, programs, FAQs) |
| `content/industries_*.json` | 43 industry guides (NAICS, who qualifies, programs, uses, amounts, FAQs) |
| `content/blog.json` | SBA eligibility and SBA loan documentation posts |

## Monthly rate update

1. Edit `PRIME`, `PRIME_DATE` and `RATE_504_25` in `shell.py`.
2. Update the hand-written rate pages (`index.html`, `sba-loan-rates/`, `sba-504-loan-rates/`, `sba-loan-calculator/`) and the inline `window.SBA_RATES` on existing pages, or regenerate them.
3. Run `build.py` and `validate.py`, then upload the changed files.

## Lender match / affiliate

Every lender, industry, hub, rates and blog page has a "Get matched with an SBA lender"
block linking to `/get-matched/?from=<page>&state=..&industry=..`. The tool
(`assets/match.js`) is client-side only: it shows the rate cap, the program that
fits, directory lenders in the state, and a button to the SBA's free Lender Match.

To add a paid partner, fill in `PARTNER` at the top of `assets/match.js`
(name, URL with your tracking ID, one-line blurb). It is shown first and
labelled as sponsored. GA4 events: `lender_match_cta`, `lender_match_submit`,
`lender_match_click`.

## Deploying

The Hostinger account (u401386392, sbarates.com is an addon domain) refuses API
file uploads and has no GitHub integration connected, so deploys go through
`release/site.zip`: the server clones this branch into a subfolder, then
"Deploy static site archive" replaces the site with the zip's contents.
Rebuild the zip after every change:

    git ls-files | grep -v -e '^_build/' -e '^release/' | zip -q -@ release/site.zip
