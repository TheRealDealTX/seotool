# Daily news runbook — renternews.net

The daily routine follows this file. A human can follow it too.

**Goal:** publish 2–4 new, original, verified renter/apartment news stories
on renternews.net each day, then rebuild and deploy the site. Quality beats
quantity: if there is no solid, verifiable news, publish fewer (or none) and
say so in the summary. Never invent facts to fill a quota.

## 0. Setup

```sh
git fetch origin claude/confident-franklin-p8wwcx
git checkout claude/confident-franklin-p8wwcx   # create it from origin if needed
git pull origin claude/confident-franklin-p8wwcx
cd renternews
```

All work happens on that branch, in `renternews/`. Pillow must be importable
(`python3 -c "import PIL"`; `pip install pillow` if not).

## 1. Know what's already published

List every existing slug, title, city and date so you don't duplicate a story:

```sh
python3 -c "import build; [print(a['dt'].date(), a['category'], a.get('city'), a['title']) for a in build.load_articles()[:60]]"
```

A follow-up on an existing story is fine only with substantial new facts
(cause determined, charges filed, a ruling) — give it a new slug and link the
earlier article in the body.

## 2. Research (WebSearch / WebFetch)

Look for US news from the **last 48 hours**, in this priority order:

1. **Apartment / multifamily fires** and building emergencies (collapses,
   CO leaks, floods, mass displacements, condemned buildings) — the site's
   core beat. Prefer incidents with displaced residents. Spread cities and states.
2. **Rent and market data** — new national/metro rent reports, vacancy, CPI shelter.
3. **Tenant rights and housing policy** — new state/city laws taking effect,
   court rulings, eviction rules, rent caps, HUD/voucher changes, enforcement.

Use local TV/newspapers, fire-department and city statements, Red Cross
posts, court documents and government data. Each story needs **at least 2
independent sources**, opened and read (not just search snippets).

## 3. Write

Hard rules:

- **Original wording.** Summarize facts in your own words and add renter-focused
  context (what it means for tenants, what displaced residents should do,
  safety takeaways). Never copy or closely paraphrase source text. At most one
  short quote per article, attributed.
- **Every fact verified** against a source you read: names, numbers, dates,
  addresses, causes. If sources disagree, say so or leave it out. Do not name
  victims who haven't been publicly identified. Never state a fire cause before
  officials do.
- 600–1000 words, neutral newsroom tone, US spelling.
- `title` ≤ 70 chars; `description` 140–160 chars; slug short and keyword-led,
  no dates, unique.
- `body_html` uses only `p h2 h3 ul ol li strong em a blockquote`; no `<h1>`,
  images or inline styles. Typical sections: what happened, who was affected,
  response and aid, cause/investigation, what this means for renters.

Save today's stories as one file, `content/articles/YYYY-MM-DD.json` (a list):

```json
[{
  "slug": "kebab-case-slug",
  "title": "Headline",
  "description": "140–160 character meta description",
  "category": "fire | safety | rent-prices | housing-policy | tenant-rights | guides",
  "date": "YYYY-MM-DD",
  "city": "City, ST",
  "tags": ["3-6 short tags"],
  "key_points": ["three one-sentence takeaways"],
  "body_html": "<p>…</p><h2>…</h2>…",
  "sources": [{"name": "Publisher or agency", "url": "https://…"}]
}]
```

`city` is optional (use `null` for national stories); when set, it puts the
story on the fire map. `date` is the publication date (today).

## 4. Check

```sh
python3 tools/overlap_check.py content/articles/YYYY-MM-DD.json   # must exit 0; reword anything flagged
python3 tools/geocode.py      # adds map coordinates for new cities; add any MISS by hand to content/geo.json
python3 build.py              # also draws cover images for the new articles
python3 validate.py           # must print OK
```

Re-read each new article once more for accuracy against its sources before deploying.

## 5. Commit and push

```sh
git add -A . && git commit -m "renternews: daily news YYYY-MM-DD (N stories)" && git push origin claude/confident-franklin-p8wwcx
```

## 6. Deploy

1. Hostinger API `hosting_files_generate-upload-url` with
   `{"username": "u401386392", "domain": "renternews.net"}`.
2. `RN_FB_URL=<url> RN_FB_AUTH=<auth_key> RN_FB_REST=<rest_auth_key> ./deploy.sh`
   (never print or commit these values) — must end `failed=0`.
3. Hostinger API `hosting_cache_clear-website` with the same username/domain.
4. Verify with curl: each new `https://renternews.net/news/<slug>/` returns
   200, the homepage lists the newest headline, and `news-sitemap.xml`
   contains the new URLs.

Never touch the WordPress backup at
`/home/u401386392/domains/renternews.net/renternews-wordpress-backup-2026-10-06/`,
and never delete files on the server.

## 7. Report

Finish with a short summary: the stories published (title + live URL),
anything you skipped and why, and any facts that were uncertain or where
sources disagreed.
