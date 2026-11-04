# Los Arcos Apartments & Townhomes: concept site

A static pitch site (plain HTML/CSS/JS, no framework, no server runtime) for Los Arcos Apartments & Townhomes, 11315 Fondren Rd, Houston, TX 77035.

**Live demo (temporary Hostinger domain):** https://darkblue-anteater-582827.hostingersite.com

## Build

```bash
pip install pillow        # only dependency (reads image sizes)
python3 build.py          # writes the finished site to ./dist
```

- `build.py` holds all page content, the property facts (`P`), floor plans (`PLANS`), FAQs, schema and the shared header and footer.
- `src/css/style.css` is the design system (tokens at the top: terracotta, sand, olive and night).
- `src/js/main.js` contains every interaction: menu, hero slider, filters, lightbox, forms, banner and placeholder links.
- `images.json` and `IMAGES.md` list every image and its source, plus a swap guide.

## Editing checklist before going live

- Search the source for `[confirm]`. Each marker flags an item to verify with management (amenities beyond the verified list, rents, beds and baths per plan, pet policy, lease terms, nearby places and drive times).
- Replace the placeholder URLs at the top of `build.py`: `APPLY_URL`, `PAY_URL`, `MAINT_URL`, `PORTAL_URL`. Social links are in `footer()`.
- Connect the forms to the leasing CRM or email service. See the `LEASING CRM / EMAIL HOOK` comment in `src/js/main.js`.
- Remove `<meta name="robots" content="noindex, nofollow">` from `page()` and replace `src/robots.txt` when moving to the real domain. Also remove the "Concept site" line from `footer()`.

## Adding new photos

Place a JPG anywhere and run:

```bash
python3 -c "from PIL import Image; im=Image.open('photo.jpg').convert('RGB'); [ (im if w==1600 else im.resize((w,round(im.height*w/im.width)))).save(f'src/img/KEY-{w}.webp',quality=62) for w in (1600,900,500)]"
```

## Deploy (Hostinger Agency plan)

Zip the contents of `dist/` (with `index.html` at the archive root) and upload the zip to the website's `.h5g/` directory with `agency-hosting_files_generate-upload-url`. Then run `agency-hosting_files_import-website-from-archive`.
