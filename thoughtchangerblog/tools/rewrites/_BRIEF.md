# Rewrite brief — Thought Changer blog posts

You are rewriting under-performing posts on thoughtchangerblog.com (a reflective personal-growth blog: mindset, meaning of phrases, quotes, intentional living). The URL slug stays the same forever; only the article changes.

Inputs (all under /home/user/seotool/thoughtchangerblog):
- `tools/rewrite-briefs.json` — slug → [primary keyword, new H1 title]
- `public/content/posts/<slug>.html` — the CURRENT (old) article body. Read it for themes and any personal story worth keeping, then overwrite it.
- `public/content/posts.json` — metadata for every post (find yours by slug; note its current `image` — the featured image stays the same, so the article should still fit that image's subject: the filename describes it).
- `tools/rewrites/_site-index.txt` — every post URL + title, for internal links.
- A strong KEPT example of house style: `public/content/posts/life-is-fleeting-5-ways-to-slow-it-down.html`.

## Deliverables per slug
1. Overwrite `public/content/posts/<slug>.html` with the new body (HTML fragment).
2. Write `tools/rewrites/<slug>.json`:
```json
{"title": "<H1, from the brief, may tweak slightly>",
 "seo_title": "<≤ 60 chars, keyword near the front> - Thought Changer",
 "description": "<meta description 140–158 chars, includes the keyword, inviting>",
 "categories": ["General"] or ["General","Mindset"] or ["General","Quotes"] (Quotes only if the article is quote-centric),
 "products": [{"title":"…","by":"Author or brand","blurb":"one line why it helps (≤ 90 chars)","q":"Amazon search string: exact title + author"} x3],
 "faq": [{"q":"…?","a":"1–3 plain sentences"} x 6]}
```

## Body rules
- 1,500–2,100 words. No H1 (the template prints it). No featured image.
- Allowed tags: p, h2, h3, ul, ol, li, strong, em, blockquote, a, `<figure class="table-wrap"><table>…</table></figure>` (one comparison/summary table is welcome when it genuinely helps).
- Every h2 and h3 gets an id: `id="h-"` + lowercase heading, non-alphanumerics → single hyphens (e.g. `<h2 id="h-what-boundaries-really-mean">`).
- Primary keyword in the first 100 words, in at least one H2, and used naturally 4–8 times total. Use related phrasing/semantic variants too. Answer the searcher's core question early (a crisp 2–3 sentence definition/answer right after the intro helps featured snippets).
- Structure: short intro (hook, 2–4 short paragraphs) → meaning/definition → 4–7 substantive sections (practical steps, examples, reflection prompts, common mistakes) → a short closing section → then exactly:
  `<!--tc:products-->` on its own line, then `<h2 id="h-faqs">FAQs</h2>` and `<!--tc:faq-->` on their own lines, at the very end. (The template renders the product cards and FAQ accordion from the JSON.)
- 2–4 internal links to genuinely related posts from `_site-index.txt` using root-relative hrefs like `<a href="/life-is-a-river/">…</a>`. Optionally 1 external link to an authoritative source (Wikipedia, Merriam-Webster, APA, Greater Good Science Center, etc.) with `target="_blank" rel="noopener"`. Do not invent URLs.
- Voice: warm, reflective, first-person-plural/second-person with occasional first-person ("I"), short punchy lines mixed with fuller paragraphs — match the kept example. Practical, specific, human. No fake statistics, invented studies, invented quotes, or misattributed quotes; quote only well-known, correctly attributed lines. No medical/clinical claims.
- Avoid AI clichés: delve, tapestry, embark, navigate the complexities, in today's fast-paced world, unlock, game-changer, testament, realm, "it's important to note", "in conclusion".
- Products: real, well-known books (or a journal/tool) clearly relevant to the topic, that you are confident exist on Amazon under that title/author. Don't repeat the same three books across posts you write; vary them.
- Use straight HTML entities only where needed; UTF-8 curly quotes/em dashes are fine.

When finished, reply with one line per slug: slug — final title — word count. Do not edit any other file.
