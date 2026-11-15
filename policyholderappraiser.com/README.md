# policyholderappraiser.com

Static marketing site for Policyholder Appraiser, the insurance appraisal and
umpire practice of Rise Public Adjusting LLC. Plain HTML, one stylesheet, one
script, a small PHP form handler. Hosted on Hostinger shared hosting
(account `u401386392`, website `policyholderappraiser.com`).

## Layout

| Path | What it is |
| --- | --- |
| `public/` | The generated site. This is what gets uploaded. |
| `build.py` | Generator: shared layout, page templates, JSON-LD |
| `siteconfig.py` | Business facts (phone, license, email, nav) |
| `content/services.py` | Seven service pages |
| `content/guides.py` | Four long-form guides (2027 Texas rules, demand letter, etc.) |
| `content/faq.py` | FAQ entries (homepage, /faq/, FAQPage schema) |
| `content/legal.py` | Privacy policy and terms |
| `src/` | Static files copied into `public/` as-is: CSS, JS, images, `contact.php`, `.htaccess`, icons |
| `make_assets.py` | Regenerates the logo SVG, favicons and OG image into `src/` |
| `validate.py` | Post-build checks (run after every build) |
| `deploy.sh` | Uploads `public/` to Hostinger over the File Browser TUS endpoint |

## Rebuilding and deploying

```sh
python3 build.py
python3 validate.py
./deploy.sh        # needs PHA_FB_URL / PHA_FB_AUTH / PHA_FB_REST, see the script header
```

No dependencies beyond the Python standard library (Pillow and ImageMagick only
for `make_assets.py`).

## Contact form

`public/contact.php` emails each submission and appends a copy to
`../form-log/` (outside `public_html`). The recipient defaults to
`info@policyholderappraiser.com`; override it by creating
`/home/u401386392/domains/policyholderappraiser.com/form-config.php` with:

```php
<?php const FORM_TO = 'you@example.com';
```

Create the `info@` and `forms@` mailboxes (or forwarders) in hPanel so the
From address is deliverable and SPF passes.

## Pages (21 indexable)

- `/` home
- `/services/` + 7 service pages (residential, commercial, hail/roof, hurricane/wind, water, fire, umpire)
- `/appraisal-process/`
- `/texas-appraisal-rules/` (SB 458, 28 TAC §§5.9800-5.9806, compliance date March 1, 2027)
- `/guides/` + 3 guides
- `/faq/`, `/about/`, `/service-areas/`, `/contact/`
- `/privacy-policy/`, `/terms-of-use/`
- `/thank-you/` and `/404.html` are noindex

## Facts to verify before launch

- Fee language: the site says fees are flat or hourly and never a percentage of the award.
- Conflict policy: the site says we decline appraiser appointments on claims where Rise Public Adjusting was the public adjuster.
- Hours: Mon-Sat 8:00 am - 7:00 pm.
- Rule citations were taken from TDI's adopted order for 28 TAC §§5.9800-5.9806 (compliance date March 1, 2027).
