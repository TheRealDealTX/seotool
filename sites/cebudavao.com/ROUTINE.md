# Every-other-day news routine — runbook

A scheduled Claude Code session follows these steps to publish fresh, original
news coverage on cebudavao.com. Humans can run the same steps by hand.

Repo: `TheRealDealTX/seotool`, branch `claude/confident-davinci-ae6cyn`,
project folder `sites/cebudavao.com/`. Live site: Hostinger Agency website UID
`gLBQLhLT2` (cebudavao.com).

## 1. Get the code

```sh
git fetch origin claude/confident-davinci-ae6cyn
git checkout -B claude/confident-davinci-ae6cyn origin/claude/confident-davinci-ae6cyn
cd sites/cebudavao.com
pip install -q pillow 2>/dev/null || true
```

## 2. Find the news (web search)

Search for news from the **last 48 hours** about, in priority order:
Cebu (city/province, Mactan), Davao (city/region, Samal), other Visayas &
Mindanao, and nationally significant Philippine news that affects readers
(weather/typhoons, transport, travel rules, prices, big sports results,
entertainment). Good sources: SunStar, Philippine News Agency (pna.gov.ph),
Inquirer, Philstar/The Freeman, GMA, ABS-CBN, Rappler, Manila Bulletin,
CNN Philippines successors, MindaNews, PAGASA, DOT, LGU official pages.

Pick **2 or 3 stories** that:
- are confirmed by **at least two independent reputable sources** (or one
  official/government source);
- are useful to Cebu/Davao readers or travellers;
- are not already covered — check `content/posts/` (grep titles, keywords and
  paths) and skip duplicates. A genuinely new development of an old story is fine.

Skip: crime stories naming private individuals, unconfirmed rumours, gossip,
partisan political opinion, anything you cannot verify.

## 3. Write each article

Follow `content/CONTENT_GUIDE.md` exactly, plus these news rules:

- File `content/posts/<slug>.md`; `path: /news/<slug>/` for news (use
  `/travel/…`, `/sports/…`, `/entertainment/…`, `/food/…` when that fits
  better). Slug: short, keyword-led, no dates unless essential.
- Front matter must include `date:` and `updated:` = today (YYYY-MM-DD,
  Philippine date), `category:` (`news`, `travel`, `sports`, `entertainment`,
  `money`, `tech`, `food`, `culture`, `lifestyle`), `places:`, `keyword:`,
  `description:` (140–158 chars), `excerpt:`, `image:` (an existing key in
  `data/photos.json` — pick the most relevant; never invent a key) and
  `image_alt:` describing *that photo*.
- 500–900 words. Original wording — summarise and explain, never copy
  sentences from sources. Lead with what happened, where, when; then why it
  matters for Cebu/Davao readers; then what to do / what happens next.
- Every factual claim must come from the sources. No invented quotes, numbers,
  names or dates. Attribute ("according to PAGASA…", "SunStar reported…").
- End the body with `## Sources` — a bullet list of 2–4 links to the articles
  you used (`[Publisher: headline](url)`) — then
  `## Frequently Asked Questions` with 3 short Q&As.
- 2–4 internal links to relevant existing pages (see `content/briefs/ALL_PATHS.md`,
  `/weather/`, `/tools/…`, `/cebu/`, `/davao/`, `/news/`).

## 4. Build and check

```sh
python3 build.py && python3 validate.py
```

Fix every error before going further. Never deploy a failing build.

## 5. Deploy

1. Hostinger connector: `agency-hosting_files_generate-upload-url` with
   `website_uid: gLBQLhLT2` → export `CD_FB_URL` (the `url`), `CD_FB_AUTH`
   (`auth_key`), `CD_FB_REST` (`rest_auth_key`). Never commit these.
2. `./deploy.sh` (uploads the whole `public/`; ~2 minutes). Must end with
   `failed=0`.
3. Hostinger connector: `agency-hosting_cache_clear-website` with
   `website_uid: gLBQLhLT2`.
4. Verify: `curl -s -o /dev/null -w "%{http_code}"` on `https://cebudavao.com/`,
   each new article URL and `/feed/` → all 200; the homepage HTML contains the
   new titles.

## 6. Commit and push

```sh
git add -A
git commit -m "cebudavao.com: news update YYYY-MM-DD — <short titles>"
git push origin claude/confident-davinci-ae6cyn
```

## 7. If something goes wrong

- No story meets the bar → publish nothing; report that and stop. Quality over
  quantity.
- Build/validate/deploy failure you cannot fix → do not deploy; leave the live
  site as it is, push nothing broken, and report the error.
- Never delete or overwrite existing posts, never touch other websites on the
  Hostinger account, never change DNS/domains.
