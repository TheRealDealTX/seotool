# smokedamage.com — static rebuild + PHP lead/admin layer

Live on Hostinger Agency website **`qpuHSMS5T`** (smokedamage.com, since 2026-09-28).
The previous WordPress site (`1Sz13eGkC`) was kept intact on its temporary
domain darkgrey-pheasant-550019.hostingersite.com as a rollback; content snapshot
in `backup/wordpress-2026-09-28/`.

## Build & deploy
```sh
python3 images.py      # only when src/img/ changes (needs Pillow)
python3 build.py       # -> public/ (site) + private/ (admin manifest)
python3 validate.py    # must report 0 errors
export SD_FB_URL=… SD_FB_AUTH=… SD_FB_REST=…   # Hostinger agency-hosting_files_generate-upload-url
./deploy.sh            # then agency-hosting_cache_clear-website
```

## Layout
| Path | What |
|---|---|
| `content/pages`, `locations`, `blog`, `events`, `history`, `case-studies` | CMS collections (Markdown-lite; see `CONTENT-SPEC.md`) |
| `content/keyword-queue.csv`, `automation-status.json` | Blog keyword queue, automation status shown in admin |
| `siteconfig.py` | Site settings + compliance info (company, TDI license, licensed address, phone, popup, GA4/GSC/Bing IDs) |
| `build.py`, `home.py`, `tools.py`, `mdlite.py` | Generator: layout, schema, homepage, calculators |
| `assets/` | CSS, JS (site, scope calculator, contents calculator), fonts, images |
| `src/php/` | `index.php` front controller (redirects, 404), `api/lead.php` (claim form), `api/settings.php`, `admin/` |
| `research/` | `compliance.md` (verified TDI / Ins. Code 4102 / 28 TAC), `keywords.md` |
| `AUTOMATION.md` | Weekly event-scan and article runbook used by the scheduled routines |

## Server-side data
Private data lives in `.h5g/sd-private/` beside `public_html` (outside the web
root — this host ignores .htaccess): leads, uploads, `settings.json`,
`redirects.json`, `requests.json`, `admin.json`. Deploys never overwrite it.

## Admin — https://smokedamage.com/admin/
Leads (with private document downloads + CSV export), blog queue, keyword queue
(CSV import), event scans, location pages, SEO metadata change requests,
redirect manager, runtime settings (lead recipient, popup, SMTP).

PHP `mail()` is not available on this platform: enter the info@smokedamage.com
mailbox password under Settings → Email delivery (smtp.hostinger.com:465) and
use "Send test email". Leads are always stored in the admin regardless.

## Known limits
- www/http variants of static pages are served directly (the platform serves
  files without PHP); canonical tags point to https://smokedamage.com.
- Semrush connector currently has no API units; keyword work uses the CSV queue.
- Case studies and testimonials render only when real, approved entries exist.
