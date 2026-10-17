# collinhughesweddings.com — expired-domain rebuild

Static rebuild of a Minneapolis–St. Paul wedding photography site. `python3 build.py`
writes everything into `public/`; `./deploy.sh` uploads `public/` to Hostinger.

- **Hosting:** Hostinger Agency Growth, website UID `uaSy8Q59R`, live at
  https://collinhughesweddings.com (http and www 301 to it).
- **Checks:** `python3 build.py && python3 validate.py` — titles ≤60 chars, descriptions
  110–160, one H1, heading order, canonicals, OG/Twitter tags, valid JSON-LD, alt text and
  dimensions on every image, no broken internal links, Google tag (G-3FFZD336L6) in every
  `<head>`, favicon set, GSC verification file and sitemap.
- **SEO extras:** 1200×630 JPG share images (`assets/og/`), image sitemap, WebPage /
  BreadcrumbList / FAQPage / BlogPosting / LocalBusiness schema, favicon + web manifest
  (`src/icons/`), GSC file `googlecccfbf2f7e9e5ae4.html`.
- **Preserved URLs:** `/` (all ~3,800 backlinks; "collin hughes" rankings),
  `/wedding-chrisjasmine/` and `/maddy-ben-surrey-uk/` (old ranking pages).
  `index.php` 301s legacy WordPress paths (feed, category, wp-*) and returns real 404s.
- **Pages:** home, about, weddings, two wedding stories, collections + FAQ,
  destination weddings, contact, privacy, 404.
- **Images:** royalty-free Unsplash photos, converted to WebP in `src/img/`.
- **Contact form:** posts to `send.php`, which emails info@collinhughesweddings.com
  with PHP `mail()`. Mail for that address only arrives once the domain's email is set up.
- No `index.html` on purpose: the host would serve it for every unknown URL.
