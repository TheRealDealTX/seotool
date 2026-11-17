# Biweekly article playbook — txinsuranceappraiser.com

This is the procedure the scheduled routine follows every two weeks. A human can follow it too.
Everything lives in the repo **TheRealDealTX/seotool**, folder `txinsuranceappraiser/`, branch
`claude/sleepy-newton-foy0fs`. The live site is the Hostinger website **txinsuranceappraiser.com**
(account `u401386392`). It is a custom PHP site: a post is a single JSON file in
`content/posts/`, which automatically appears on `/blog/`, in the sitemap and at `/<slug>/`.

## 0. Should this run publish?

- Read `_dev/content-calendar.json`. Find the most recent `published` date.
- If it was **less than 13 days ago, stop** and report "not due yet". This keeps a strict 14-day rhythm
  even though the schedule fires weekly.
- Otherwise take the **first topic with `"status": "queued"`**.
- If no queued topics remain, add 6 new topics first, using the rules in §7, then continue.

## 1. Set up

```bash
cd txinsuranceappraiser
php -S 127.0.0.1:8090 _dev/router.php &    # local preview, needed by the validator
```

Read 2–3 existing posts in `content/posts/` to match tone and structure, and `BLOG_SPEC` rules below.

## 2. Write the article (content/posts/<slug>.json)

**Length & keywords**
- `body_html` **2,000–2,400 words**: count with `re.sub('<[^>]+>',' ',body).split()`.
- Primary keyword in: `seo_title` (start), `h1`, `meta_description`, the first `<p class="lead">`, at least two H2s
  and about once per 150–200 words overall. Work **every** secondary keyword from the calendar entry in at least once,
  naturally (H2s and FAQs are good places). Never stuff awkward phrases — rewrite until it reads naturally.
- `seo_title` 45–60 chars · `meta_description` **120–145 chars** · `excerpt` 150–200 chars.

**Structure**
- Start with `<p class="lead">`: a 40–60 word direct answer (featured-snippet style).
- 8–11 `<h2 id="kebab-id">` sections, with `<h3>` where useful. At least one `<ul>`/`<ol>` and one `<table>` with `<thead>`.
- Include a Texas-specific section: Texas weather, Texas law (Tex. Ins. Code ch. 541, 542, 542A) or Texas cities.
- One `<div class="callout"><strong>Tip:</strong> …</div>` and one closing `<div class="callout callout-cta">…</div>`
  that links to `/contact-us/` or `/services/appraisal/` and mentions (254) 421-5412.
- 6–10 internal links using exact existing URLs: related posts (`ls content/posts`), the relevant service page,
  a relevant `/tools/...` page and, where natural, 1–2 `/areas/<city>-insurance-appraiser/` pages. Never link the post to itself.
- At most 2 external links, only authoritative sources (tdi.texas.gov, statutes.capitol.texas.gov, weather.gov,
  noaa.gov, fema.gov), each with `target="_blank" rel="noopener"`.
- Mention "TX Insurance Appraiser" 1–3 times. No `<h1>` in the body, no FAQ section in the body, no "Conclusion" heading.
- Allowed tags: p, h2, h3, ul, ol, li, strong, em, a, table, thead, tbody, tr, th, td, blockquote, div (callouts),
  figure, img, figcaption, span (photo credit), br.
- Add one line of general information / not legal advice wherever legal rights come up.

**Accuracy (non-negotiable)**
- No invented statistics, quotes, testimonials, client stories or case results. Label dollar examples as illustrative.
- Texas law references only when accurate and hedged ("generally", "most policies", "check your policy"):
  ch. 542 Prompt Payment (acknowledge within 15 days; accept/reject within 15 business days of receiving items, up to 45
  with notice; pay within 5 business days; +15 days in declared weather catastrophes), ch. 542A (61-day pre-suit notice for
  weather claims), *State Farm Lloyds v. Johnson* (2009), *Barbara Technologies* and *Ortiz v. State Farm Lloyds* (2019).
- Business facts: TX Insurance Appraiser (TX Insurance Appraisals LLC), (254) 421-5412, info@txinsuranceappraiser.com.
  Appraiser: Joseph Dittman, Texas-licensed public adjuster; Rise Public Adjusting LLC, TDI license #3356839. On an
  appraisal he is the policyholder's appraiser (or umpire), not their public adjuster or attorney. Not a law firm.
- Never promise or "guarantee" outcomes.

**JSON fields**
```
slug, seo_title, meta_description, h1, primary_keyword, secondary_keywords[], category (one of: Appraisal Process,
Roof Claims, Commercial Claims, Insurance Basics, Estimating & Technology, Texas Weather & Claims), excerpt,
published ("YYYY-MM-DDT09:00:00+00:00", today), updated ("YYYY-MM-DD", today), image (featured file name),
image_alt, image_credit (HTML credit line for the featured photo), key_takeaways[4-5], body_html, faqs[5] ({q,a}; 40–80 words each)
```
Build the JSON with a Python script and `json.dump(..., ensure_ascii=False, indent=1)`, never by hand.

## 3. Photos: 3 real, royalty-free photos per article (featured + 2 inline)

Use `_dev/fetch_image.py`. It queries Openverse for **CC0, public domain or CC BY** photos only, all of
which allow commercial use, and skips Flickr, whose image host blocks this network.

```bash
python3 _dev/fetch_image.py search "hail damage roof" "texas storm" "insurance adjuster"
python3 _dev/fetch_image.py get <id> <slug>-<short-name> "<alt text>" "<caption sentence>"
```
`get` saves `assets/img/blog/<stem>.webp` and prints JSON with a ready `<figure>` that includes the required credit.

- **Look at every downloaded image before using it** (open the .webp file with the Read tool). Titles are often
  misleading, and a "damaged roof" result can turn out to be a mushroom. Reject anything irrelevant, low quality,
  showing identifiable private people as the subject, war damage, or branding. Delete rejected files.
- Prefer Texas or US storm, roof, home, inspection and claim scenes. Never use AI-generated images or images from
  sites that are not CC0, public domain or CC BY.
- Photo 1 is the featured image (`image`, `image_alt`, `image_credit`, where the credit is the `<span class="credit">` content).
  Photos 2 and 3 go inside `body_html` as the printed `<figure>` blocks, placed after relevant sections.
- Captions must describe what the photo actually shows.
- If Wikimedia rate-limits downloads (429), wait a minute and retry, or pick another candidate.

## 4. Cross-link

Add one contextual link **to** the new post from 1–2 closely related existing posts, inside their `body_html`
(one sentence, e.g. "For more, see our guide to …"). Prefer the post that currently ranks for the cluster,
per the calendar `evidence`, so Google sees the new dedicated page.

## 5. Validate

```bash
python3 _dev/validate.py          # must print ALL CHECKS PASSED
```
Also confirm `curl -s 127.0.0.1:8090/<slug>/` returns 200 and the word count, meta length and image count meet §2–3.

## 6. Publish

1. Get upload credentials: Hostinger API `hosting_files_generate-upload-url` with
   `{"username": "u401386392", "domain": "txinsuranceappraiser.com"}`.
2. Upload only the new and changed files:
   ```bash
   export TX_FB_URL=… TX_FB_AUTH=… TX_FB_REST=…
   _dev/deploy_files.sh content/posts/<slug>.json assets/img/blog/<photo1>.webp assets/img/blog/<photo2>.webp \
       assets/img/blog/<photo3>.webp content/posts/<cross-linked-post>.json
   ```
3. Verify on the server with Hostinger `hosting_files_website-content`, e.g. path `content/posts/<slug>.json`.
   Also try `curl https://txinsuranceappraiser.com/<slug>/`; the sandbox network sometimes cannot reach the domain,
   which is fine if the server file check passes.
4. In `_dev/content-calendar.json`, set the topic's `status` to `"published"` and `"published": "YYYY-MM-DD"`.
5. Commit everything (post JSON, images, calendar, cross-link edits) to branch `claude/sleepy-newton-foy0fs` and push.
   If the push is rejected, fetch and merge that branch, then push again. Never force-push.
6. Report: title, URL, word count, primary keyword, secondary keywords used, the 3 photo credits, files uploaded.

## 7. Adding new topics when the queue runs low

Rules: pick clusters where (a) the site already gets Search Console impressions or the Semrush export shows the site ranking
20+, (b) keyword difficulty is about 25 or lower, (c) no existing post already targets the same primary query, so there is
no cannibalisation, and (d) the topic fits a Texas property-insurance appraisal firm. The original data files are no longer
available in a fresh session, so reuse the `evidence` style. Good sources of new angles: Texas cities with area pages,
claim types (wind, water, freeze, fire, smoke, theft), claim process steps, and policy terms (ACV, RCV, O&P, matching, ordinance & law).
If Semrush or Search Console tools are connected and have credits, use them to confirm volume and KD.
