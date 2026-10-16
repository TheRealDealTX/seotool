# RelationAdvisor post content spec

Each post is one JSON file: `relationadvisor/content/posts/<slug>.json` (UTF-8, valid JSON).

```json
{
  "slug": "how-to-show-love",
  "title": "How to Show Love: 25 Ways Your Actions Say It Best",
  "h1": "How to Show Love: 25 Ways Your Actions Say It Best",
  "description": "Meta description, 140-158 characters, includes the primary keyword naturally.",
  "keyword": "how to show love",
  "excerpt": "One or two sentences (max ~180 chars) used on cards and listings.",
  "intro": "<p>Opening paragraph(s) — hook + what the reader will get. 80-150 words.</p>",
  "body": "<h2>...</h2><p>...</p> ... (main article HTML)",
  "takeaways": ["3-5 short key takeaways, plain text"],
  "faq": [{"q": "Question?", "a": "Plain-text answer, 40-80 words."}]
}
```

Rules

- `title` <= 62 characters, contains the primary keyword (usually the slug phrase). `h1` may be the same or slightly longer.
- Write **fresh, original** copy. The archived originals are given only for topic, angle and outline — never copy their sentences. Fix their grammar/odd phrasing (e.g. "Does he likes me" → the keyword can stay in the slug, but write correct English).
- Length: guide-style posts 1,300-1,900 words in `intro`+`body`. List posts (pickup lines, questions, captions, paragraphs, quotes, texts) must actually deliver a generous list — 60-120 items for lines/questions/captions, 25-40 for paragraphs/letters — grouped under H2 subheadings, plus a short how-to-use section.
- Warm, modern, practical, inclusive voice; second person. American English. No fluff intros ("In today's world…"), no "As an AI". Respect consent and healthy relationships: if an old topic is manipulative or sketchy (e.g. "how to make a guy jealous", "how to get her on the bed", "how to catch your girlfriend cheating", "how to handle husband/wife"), keep the keyword/slug but reframe toward honest, respectful, consent-based advice.
- Abuse/safety topics: include the US National Domestic Violence Hotline (1-800-799-7233, text START to 88788, thehotline.org) in a `tip` callout. Mental-health-heavy topics may mention talking to a licensed therapist. Do not give medical/legal claims.
- No fabricated statistics, studies, quotes from named experts or fake testimonials. Generic, well-known ideas (e.g. Gottman's "bids for connection", the five love languages) are fine if described accurately and briefly.
- No year in titles (the originals said "2019" — drop it).

Allowed HTML in `intro` / `body` (nothing else — no inline styles, no classes except those listed, no images, no scripts):

- `h2`, `h3`, `p`, `ul`, `ol`, `li`, `strong`, `em`, `blockquote`, `a`
- `<div class="tip"><strong>Tip:</strong> …</div>` — a highlighted callout (use 1-3 per post)
- `<ol class="lines">…</ol>` — for numbered lists of lines/questions/captions (styled as cards). Use plain `<ul>`/`<ol>` for normal lists.
- `<div class="note-card"><p>…</p></div>` — for a paragraph/letter/message the reader can copy (paragraph posts, love letters).
- Internal links: `<a href="/other-slug/">anchor</a>` — 3-6 per post, only to slugs that exist in `relationadvisor/content/plan.json`. Category links `/category/<cat>/` are allowed.
- Every `h2` should be a useful, specific heading (they form the table of contents). 5-10 H2s per post.
- Don't repeat the H1 in the body. Don't add a "Conclusion" H2 titled literally "Conclusion" — use something like "The bottom line" or a specific phrase.

FAQ: 3-4 questions people really search ("People also ask" style), answers in plain text.
