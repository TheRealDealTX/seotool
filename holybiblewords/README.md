# holybiblewords.com — Bible web app

A PHP + vanilla-JS Bible app that replaces the WordPress site at
[holybiblewords.com](https://holybiblewords.com). Three versions:

| URL prefix | Version | Text source | Coverage |
| --- | --- | --- | --- |
| `/ta/` | King James Version (KJV) | eBible.org `eng-kjv` (public domain) | complete, 31,102 verses |
| `/ml/` | Ang Biblia, 2011 (Cebuano) | the verses published on the old WordPress site | Genesis – 2 Kings, 10,026 verses |
| `/ceb/` | Biblica® Open Ang Pulong sa Dios™ (Cebuano, "APSD") | eBible.org `cebocb` (CC BY-SA 4.0), used unchanged | complete |

Verses a version doesn't have are filled from the next version in its chain, with a
badge naming the source: **AB → APSD → KJV**, **APSD → KJV**. Ang Pulong sa Dios
sometimes joins verses (e.g. 1 Cronicas 8:14–16). Those show as one range, and the
joined verse URLs (`/ceb/1chronicles/8/15/`) 301 to the start of the range.

The URL format of the old site is kept exactly: `/{ta|ml}/`, `/{ver}/{book}/`,
`/{ver}/{book}/{chapter}/`, `/{ver}/{book}/{chapter}/{verse}/` with the same book
slugs (`genesis`, `1kings`, `songofsongs`, …). WordPress's duplicate slugs
(`/ml/genesis/13-2/7-2/`) 301 to the clean URL, and the old sitemaps, feeds, `?s=`
search and `wp-*` paths redirect to their new equivalents.

## Ang Biblia, 2011 — licensing

Ang Biblia, 2011 is © Philippine Bible Society. Without permission it may only be
quoted up to 500 verses. The site carries only what the old site already published,
and verses that are missing show Ang Pulong sa Dios in their place, clearly
labelled, with `noindex` on pages that have no Ang Biblia text. To add the rest, get the licensed
text from PBS (translations@bible.org.ph), drop it into `sources/ml-licensed/`
(format in that folder's README) and rebuild. Nothing else needs changing.

## Ang Pulong sa Dios — license terms

CC BY-SA 4.0 from Biblica: free to publish (ads included), on condition that the text
and its title stay unchanged and the copyright notice is shown. The notice is in
`VERSIONS["ceb"]` in `tools/build_data.py`. It appears in the footer of every page, under
each chapter and verse that uses it, and on `/ceb/`. Don't edit the text. If it ever
is changed, the license requires publishing a list of the changes.

## Features

- **Seamless version switching.** The KJV / AB / APSD toggle in the header keeps you on the same
  book, chapter and verse, at the same scroll position, without a page reload.
- **Navigation.** A book → chapter → verse picker (filter by name or type `John 3:16`),
  prev/next chapter, swipe left/right on phones, ← → keys, and a search box that
  understands references in English and Cebuano (`jn 3:16`, `Juan 3 16`, `1 cor 13`).
- **Verse of the Day.** Changes automatically at local midnight. The same verse shows in
  both versions, and you can share it or make an image of it. There's an archive of the
  past week at `/verse-of-the-day/`.
- **Verse actions.** Tap a verse to highlight it (4 colors), bookmark it, add a note, copy,
  share, make a 1080×1080 image, compare versions, or listen. Highlights are tied to the
  verse, not the version, so they carry across.
- **Side-by-side view** of two versions (choose which in Reading settings), **listen** (text-to-speech), and **full-text
  search** with OT/NT filters and "exact phrase" support.
- **Bible in a Year** reading plan with progress, plus a *Mark as read* button on chapters.
- **Saved**: bookmarks, highlights, notes and history. All of it stays on the device, in localStorage.
- **Reading settings**: theme (auto, light, sepia, dark), text size, serif/sans, line
  spacing, verse-per-line or paragraph layout, verse numbers on/off.
- **PWA**: installable, works offline. Visited pages are cached, and `/app/` downloads a
  whole version for offline reading.
- **SEO**: server-rendered pages, canonical + hreflang between versions, breadcrumbs
  and Quotation JSON-LD, per-book XML sitemaps at `/sitemap_index.xml`.
- Google Analytics, AdSense (`ads.txt` included) and the Amazon affiliate links are kept.
  Ads are not loaded inside the native apps.

## Layout

| Path | What it is |
| --- | --- |
| `public/` | **The deploy root** (upload this to `public_html`) |
| `public/index.php` | Front controller: routing, redirects |
| `public/lib/` | PHP: data access + reference parser + search (`bible.php`), page chrome (`layout.php`), pages, JSON API, sitemaps. Blocked from direct access by `.htaccess` |
| `public/data/` | Generated Bible data: `books.json`, `versions.json`, `votd.json`, `{ta,ml,ceb}/{book}.json`, `{ta,ml,ceb}/search.tsv` |
| `public/assets/` | `css/app.css`, `js/app.js` (the whole client app), icons |
| `public/sw.js`, `manifest.webmanifest` | Service worker and PWA manifest |
| `tools/build_data.py` | Builds `public/data/` from the sources |
| `tools/build_content.py` | Builds blog posts and the privacy policy from the WordPress export |
| `sources/` | WordPress exports (Ang Biblia verses, posts, pages). Keep them: they're the only copy of the old site's content |
| `mobile/` | Android + iOS apps (Capacitor) |

JSON API (used by the app, cacheable): `/api/chapter/{ver}/{book}/{ch}`,
`/api/votd?date=YYYY-MM-DD`, `/api/search?v=&q=&t=ot|nt&offset=`, `/api/ref?q=`.

## Develop

```sh
python3 tools/build_data.py        # downloads the KJV and Ang Pulong sa Dios on first run
python3 tools/build_content.py
php -S localhost:8080 -t public tools/dev-router.php
```

Needs PHP ≥ 8.1. There's no build step for CSS or JS. After you change `app.css` or `app.js`, bump
`ASSET_VER` in `public/lib/bible.php` and the matching `?v=` / cache names in `public/sw.js`.

## Going live (replacing WordPress)

1. **Back up the WordPress site** (files and database) in hPanel.
2. Empty `public_html`, or move the WordPress files aside, so `wp-login.php`, `wp-admin/` etc. are gone.
3. Upload the *contents* of `public/` to `public_html` (`./deploy.sh`, or hPanel File Manager).
   PHP 8.1+ is required (the site runs 8.2 today).
4. Clear the Hostinger/LiteSpeed cache and check `/`, `/ta/john/3/16/`, `/ml/genesis/1/`,
   `/sitemap_index.xml`.
5. In Google Search Console, submit `https://holybiblewords.com/sitemap_index.xml`.

Routing works with `.htaccess` (Apache/LiteSpeed). It also works on hosts that ignore
`.htaccess` and send unknown paths to `index.php`, because there is no `index.html`.

## Mobile apps (Android & iOS)

`mobile/` is a [Capacitor](https://capacitorjs.com) project whose app loads
`https://holybiblewords.com`. The website stays the single thing you host and
update, and app users get changes instantly. The app adds: native share sheet,
a daily "Verse of the Day" reminder (Reading settings → Daily verse reminder),
the Android back button, a status bar that follows the theme, a splash screen, and
an offline error page.

```sh
cd mobile
npm install
npx cap sync
npx cap open android   # Android Studio → Build → Generate Signed Bundle (AAB) for Google Play
npx cap open ios       # Xcode (macOS) → set your Team → Product → Archive for the App Store
npm run assets         # regenerate icons/splash from mobile/resources/ if you change them
```

- App id: `com.holybiblewords.app`. Change it in `capacitor.config.json` before the first store upload if you want a different one.
- iOS: `WKAppBoundDomains` is set to `holybiblewords.com`, which lets the service worker (offline reading) run inside the app.
- Apple reviews "website in an app" submissions strictly (guideline 4.2). The native share
  sheet, notifications and offline reading help here; describe them in the review notes.
- Optional deep links (tapping a holybiblewords.com link opens the app): add
  `/.well-known/assetlinks.json` (Android, needs your signing-key SHA-256) and
  `/.well-known/apple-app-site-association` (iOS, needs your Team ID) to `public/`,
  then enable the associated domains in Android Studio and Xcode.
