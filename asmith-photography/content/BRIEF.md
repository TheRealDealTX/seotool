# Content brief: asmith.photography journal pages

asmith.photography used to be the portfolio of Los Angeles photographer Aaron Smith
(skate, footwear, lifestyle, editorial). The domain expired and is being relaunched as an
**independent photography journal** about commercial, editorial, skate and sport photography in
Los Angeles. It is NOT Aaron Smith's site and must never pretend to be.

Each old URL is rebuilt as a journal article on the subject its slug names (see plan.json:
[slug, category, focus keyword, angle]).

## Hard rules
1. Never claim this site, its writers, or "we" photographed any named brand, person or publication.
   Never write "our campaign for Nike", "when we shot Shaun White" etc. Write about the *craft* of
   that kind of shoot: how such work is approached, lit, planned, edited.
2. Never invent facts about real people or brands: no fake quotes, dates, collaborations,
   awards, or numbers. Only use widely known, uncontroversial facts (e.g. "Kilian Martin is a
   Spanish freestyle skateboarder"). When unsure, stay general.
3. Do not mention Aaron Smith at all. Do not mention the domain's history.
4. Don't use brand names as if endorsed. Use them as subject context ("a Vans-style skate shoe shoot").
5. US English. Concrete, specific, practical: real LA places (Venice, Silver Lake, Arts District,
   LA River, Griffith Park, Carson's VELO Sports Center, Westwood, Downtown's Broadway, etc.), real
   gear and techniques (fisheye, strobes, panning at 1/30s, polarizers, Portra 400). No fluff, no
   "in today's fast-paced world", no "elevate", "unleash", "delve", "tapestry", "game-changer".
6. Focus keyword appears naturally in title, h1, description, dek and the first section's first
   paragraph, plus 1–2 more times in the body. Don't stuff it.

## Output: one JSON file per page at content/pages/<slug>.json
{
  "slug": "nike-sb",
  "title": "≤ 60 chars, include the focus keyword, no site name (added automatically)",
  "description": "140–158 chars, includes the keyword, specific",
  "h1": "Headline with the keyword, ≤ 70 chars",
  "dek": "One or two sentence standfirst, ≤ 230 chars",
  "sections": [ {"h2": "…", "paras": ["…", "…"]} ],
  "notes_title": "e.g. Shot list / Kit list / On set",
  "notes": ["4–6 short practical bullets, ≤ 120 chars each"],
  "pull_quote": "One memorable original sentence (not attributed to any real person), ≤ 140 chars",
  "image_queries": ["2–3 short Creative Commons image search queries for a generic, brand-free hero image, e.g. 'skateboarder kickflip', 'skate shoes'"],
  "related": ["3 other slugs from plan.json that genuinely relate"]
}
- 4 or 5 sections, 2–3 paragraphs each; total body 600–850 words.
- Plain text only (no HTML, no markdown). Use ’ and — sparingly; straight quotes OK.
- Validate each file parses as JSON: python3 -c "import json;json.load(open('FILE'))"
