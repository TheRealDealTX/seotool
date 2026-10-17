# stormclaims.org

Referral partner portal for Rise Public Adjusting. Not an SEO site: a single
landing page that embeds the Google Apps Script document-upload tool, plus a
full-page `/upload/` route for sharing a direct link.

| Path | What it is |
| --- | --- |
| `index.html` | Landing page: how it works, embedded upload tool, what to send, contact |
| `upload/index.html` | Full-page embed of the upload tool (`noindex`) |
| `assets/site.css` | The only stylesheet; palette and type match the upload tool |
| `.htaccess` | 404 page and www → apex redirect |
| `deploy.sh` | Uploads this folder to the Hostinger website (see header comment) |

The upload tool itself is the Apps Script web app at the URL stored as
`APPS_SCRIPT_URL` in `../siteconfig.py`. Its form, fields and file handling
live in Apps Script, not here.

Hosted on Hostinger Web hosting, account `u401386392`, order `64270646`,
addon domain `stormclaims.org` (created 2026-10-17).
