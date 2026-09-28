# converseroofer.com

Text files of the live site (Hostinger Agency website `9Rd2MxlgI`, document
root `public_html`). Images are on the server only.

## Clean URLs

The H5G host is nginx: it serves real files directly, ignores `.htaccess`, and
sends unknown paths to `index.php` - but only when no root `index.html` exists
(otherwise it answers every unknown path with the homepage as a 200). So:

- The homepage is `home.html`; `index.php` serves it at `/`.
- Pages live in `_pages/*.php` (HTML behind a one-line `ROUTER` guard) so
  `/about.html` no longer exists as a file. `index.php` serves `/about` from
  `_pages/about.php` and 301s `/about.html` and `/about/` to `/about`.
- `blog/`, `areas/` and `storms/` keep their `index.html` and stay `/blog/` etc.
- Anything else gets `404.html` with a real 404.

To add a page `foo`: create `_pages/foo.php` starting with
`<?php defined('ROUTER') or exit; ?>`, link it as `foo` (no `.html`), and add
`https://converseroofer.com/foo` to `sitemap.xml`. Upload with the File
Browser TUS endpoint from `agency-hosting_generateUploadURLV1`, then clear the
cache (`agency-hosting_clearWebsiteCacheV1`).
