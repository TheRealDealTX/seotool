# collinhughesweddings.com — expired-domain rebuild

Static rebuild of a Minneapolis–St. Paul wedding photography site. `python3 build.py`
writes everything into `public/`; `./deploy.sh` uploads `public/` to Hostinger.

- **Hosting:** Hostinger Agency Growth, website UID `uaSy8Q59R`, temporary domain
  https://wheat-squid-242818.hostingersite.com. When the domain is ready, link
  `collinhughesweddings.com` to the website (`agency-hosting_domains_change-website`).
  Canonicals, sitemap and schema already point at https://collinhughesweddings.com.
- **Preserved URLs:** `/` (all ~3,800 backlinks; "collin hughes" rankings),
  `/wedding-chrisjasmine/` and `/maddy-ben-surrey-uk/` (old ranking pages).
  `index.php` 301s legacy WordPress paths (feed, category, wp-*) and returns real 404s.
- **Pages:** home, about, weddings, two wedding stories, collections + FAQ,
  destination weddings, contact, privacy, 404.
- **Images:** royalty-free Unsplash photos, converted to WebP in `src/img/`.
- **Contact form:** posts to `send.php`, which emails info@collinhughesweddings.com
  with PHP `mail()`. Mail for that address only arrives once the domain's email is set up.
- No `index.html` on purpose: the host would serve it for every unknown URL.
