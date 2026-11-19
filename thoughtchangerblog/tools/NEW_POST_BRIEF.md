# Weekly article brief — thoughtchangerblog.com

Everything happens in `/home/user/seotool/thoughtchangerblog` (git branch `claude/gallant-fermi-9ya39s`).

## 1. Pick and validate the keyword (Data for SEO)
Load the Data for SEO tools with ToolSearch ("Data_for_seo"). Large results are saved to a file; parse them
with `python3 -I` + json (fields: `keyword`, `keyword_info.search_volume`, `keyword_properties.keyword_difficulty`,
`search_intent_info.main_intent`). Location "United States", language "en".

1. Open `tools/content-calendar.json` and take the **first** entry with `"status": "pending"`.
2. Re-check it: `dataforseo_labs_google_keyword_overview` on the primary keyword plus 4–8 close variants
   (e.g. "X meaning", "what does X mean", "X quotes", "X definition"). Choose as primary the variant with the
   best volume among those with **KD ≤ 20** (realistic for this small site). Use the others as H2/H3 wording.
   * If KD is missing/0 for a variant, treat it as unknown, not easy.
   * Run `serp_organic_live_advanced` on the chosen primary. It is realistic if page 1 shows at least 3 results
     from small blogs, forums (Reddit/Quora), social (Facebook/Pinterest/TikTok) or thin pages. If page 1 is all
     major publishers/dictionaries, skip this entry (set `"status": "skipped"` with a note) and take the next.
   * Read "People also ask" and related searches from that SERP and answer them in the article/FAQ.
3. Record the final numbers in the entry (`keyword`, `vol`, `kd`, `serp`).
4. **Keep the queue full:** if fewer than 4 entries remain pending, research new ones:
   `dataforseo_labs_google_keyword_ideas` / `dataforseo_labs_google_related_keywords` seeded with this site's
   themes (meanings of phrases and idioms, mindset, quotes, Stoic/Latin sayings, symbolism, intentional living),
   filtered to volume ≥ 300 and KD ≤ 20, informational intent. Prefer topics that support an existing pillar post
   (they help it rank). Never target an existing post's exact primary keyword (check `public/content/posts.json`
   and the calendar). Append 4–6 entries in the same format (slug, keyword, vol, kd, title, supporting, angle,
   pillar, category, status "pending").
   Our own Search Console data (`tools/data/gsc-queries.json`) is a tiebreaker: themes that already earn
   impressions are worth doubling down on.

## 2. Write the article → `tools/drafts/<slug>.html`
* **2,000–2,600 words** of body text (FAQ not counted). No H1 (template prints it); no featured image in the body.
* Allowed tags: p, h2, h3, ul, ol, li, strong, em, blockquote, a, and `<figure class="table-wrap"><table>…</table></figure>`.
* Every h2/h3 has `id="h-…"` = lowercase heading, non-alphanumerics → single hyphens (apostrophes become hyphens: "you're" → `you-re`).
* SEO: primary keyword in the first 100 words, in the first H2 and one more H2, and used naturally 6–10 times;
  use the supporting queries as H2/H3 wording where natural. Give a crisp 2–3 sentence answer/definition right
  after the intro (featured-snippet bait). Include one genuinely useful table or checklist.
* Structure: hook intro (short paragraphs) → definition/answer → 6–9 substantive sections → short close →
  then exactly, on their own lines: `<!--tc:products-->`, `<h2 id="h-faqs">FAQs</h2>`, `<!--tc:faq-->`.
* Put **one `<!--tc:image-->` marker** on its own line roughly 35–45% into the article (between sections) — the
  inline photo is inserted there.
* **Interlinks:** link the pillar post at least twice (once in the first 300 words) and 3–5 other relevant posts,
  using root-relative hrefs (`<a href="/slug/">descriptive anchor</a>`). Only link slugs that exist in
  `public/content/posts.json`. At most 2 external links, to authoritative sources (Wikipedia, Merriam-Webster,
  Britannica, APA, Greater Good, Poetry Foundation…), with `target="_blank" rel="noopener"`.
* Voice: warm, reflective, practical — match `public/content/posts/life-is-fleeting-5-ways-to-slow-it-down.html`.
  Short punchy lines mixed with fuller paragraphs. Second person with occasional "I"/"we".
* Accuracy: no invented statistics, studies, or quotes. Quote only well-known, correctly attributed lines.
  No medical or legal claims. If unsure of a fact, leave it out.
* Avoid AI clichés: delve, tapestry, embark, navigate the complexities, in today's fast-paced world, unlock,
  game-changer, testament, realm, "it's important to note", "in conclusion".

## 3. Metadata → `tools/drafts/<slug>.json`
```json
{"slug": "...", "title": "<H1>", "seo_title": "<≤ 60 chars incl. keyword> - Thought Changer",
 "description": "<145–158 chars, keyword included, inviting>",
 "categories": ["General", "Mindset" | "Quotes"],
 "interlink_phrases": "keyword|close variant|another variant",
 "products": [{"title": "", "by": "", "blurb": "≤ 90 chars", "q": "Amazon search: exact title + author"} ×3],
 "faq": [{"q": "...?", "a": "1–3 plain sentences"} ×6–8],
 "featured": {"url": "<photo url>", "alt": "<descriptive alt incl. keyword naturally>"},
 "inline":   {"url": "<photo url>", "alt": "<descriptive alt>", "caption": "<short caption>"}}
```
Products: real, well-known books (or a journal) relevant to the topic that certainly exist on Amazon. Don't
reuse the pillar post's three books.

## 4. Photos (real, royalty-free, ≥ 2)
`python3 tools/find_photos.py "<search terms>"` — searches CC0 photos (WordPress Photo Directory via Openverse;
no attribution required). Choose two **different**, landscape, ≥ 1600px-wide real photographs that fit the topic
(featured = the strongest; inline = supports a mid-article section). Download one and look at it before choosing
if the title is ambiguous. Never use AI-generated, watermarked, or non-CC0/PD images.

## 5. Publish
```bash
python3 tools/add_post.py tools/drafts/<slug>.json      # prints FILES=...
php -S localhost:8080 -t public tools/dev-router.php &   # if not already running
python3 tools/validate.py                                # must end "0 errors"
```
Check the post renders (`curl -s localhost:8080/<slug>/`), the body word count is ≥ 2,000, and that auto-interlinks look sensible.

**First, deploy any backlog:** if `tools/content-calendar.json` has entries with `"status": "ready-to-deploy"`,
deploy their stored `files` lists (oldest first) together with today's files, then mark them `published`.

Deploy only the changed files with the Hostinger connector (load its tools with ToolSearch "Hostinger_Connector";
if the connector is not available in this session, skip the deploy: set the calendar entry to
`"status": "ready-to-deploy", "files": "<the FILES string>"`, commit and push, and report that the article is
written and committed but waiting for a deploy):
1. `hosting_files_generate-upload-url` (username `u401386392`, domain `thoughtchangerblog.com`) → url, auth_key, rest_auth_key.
2. `TC_FB_URL=<url> TC_FB_AUTH=<auth_key> TC_FB_REST=<rest_auth_key> FILES="<from add_post>" tools/deploy.sh production` → must report `fail=0`.
3. `hosting_cache_clear` (domain `thoughtchangerblog.com`).
4. Verify `https://thoughtchangerblog.com/<slug>/` returns 200 and appears in `https://thoughtchangerblog.com/post-sitemap.xml`.

## 6. Record
Set the calendar entry to `"status": "published", "published": "<YYYY-MM-DD>"`, commit
(`thoughtchangerblog: publish <slug>`) and push to `claude/gallant-fermi-9ya39s`.
