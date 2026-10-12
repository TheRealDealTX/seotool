# Article content spec — comeicavoliamerenda.com

The site: **Come i Cavoli a Merenda** — an independent earring & ear-piercing guide.
The name is an Italian idiom ("like cabbages at snack time" = something charmingly out
of place). Brand voice: warm, knowledgeable, a little playful, celebrates
mismatched/curated ears. US English. Second person ("you"). No fluff, no filler intros
("In today's world..."), no "In conclusion". Short paragraphs (2–4 sentences).

Each category module is a Python file `content/<module>.py` that defines:

```python
ARTICLES = [
  dict(
    slug="5mm-earrings-actual-size",          # given to you — do not change
    category="guides",                         # given
    keyword="5mm earrings actual size",        # primary keyword (given)
    title="5mm Earrings Actual Size: See Every Stud Size to Scale",  # <=60 chars, contains keyword (or close variant)
    description="...",                         # 140–158 chars, contains keyword, compelling
    h1="...",                                  # contains keyword; may differ from title
    image="diamond-studs",                     # given (or None)
    image_alt="...",                           # describe the actual photo (see image list), work in keyword naturally if honest
    quick=["...", "...", "..."],               # 3–4 short bullet answers for a "Quick answer" box (plain text, may use <strong>)
    body="""<h2>...</h2><p>...</p> ...""",   # HTML, 750–1100 words
    faqs=[("Question?", "Answer in 1–3 sentences."), ...],  # exactly 4
    related=["slug-a", "slug-b", "slug-c"],    # 3 slugs from the master list below
  ),
  ...
]
```

Body HTML rules:
- Use only: `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>`, `<li>`, `<strong>`, `<em>`, `<a href="/slug/">`,
  `<table class="tbl"><thead>…</thead><tbody>…</tbody></table>`,
  `<div class="callout"><p>…</p></div>` (a tip/aside, max 2 per article).
- No `<h1>`, no images, no inline styles, no scripts, no external links.
- Start with a `<p>` (no heading first). 4–7 `<h2>` sections.
- Include 2–4 contextual internal links to other slugs from the master list (href="/slug/").
- Use the primary keyword in the first paragraph and in at least one `<h2>`, naturally.
- At least one table or list where it genuinely helps.
- Python: use triple-quoted strings; make sure the file imports nothing and is valid Python
  (run `python3 -c "import ast,sys;ast.parse(open(sys.argv[1]).read())" content/<module>.py`).
  Avoid `"""` inside body text. Apostrophes are fine inside triple quotes.

Accuracy rules (important):
- Celebrity / pop-culture pages: only state facts you are confident are true and widely
  documented. Never invent quotes, dates, prices or interviews. When unsure, hedge
  ("is often photographed with…", "fans point to…") or leave it out. Focus on the *style*
  and how readers can get the look — that's the useful part.
- Brand pages (Coach, Nike, Chanel, etc.): we are an independent guide, not affiliated.
  No current prices, no claims about current stock. Talk about signature styles, how to
  spot fakes in general terms, materials, care, and alternatives. Never claim a brand
  sells something you aren't sure it sells (e.g. say "Nike-themed" / "swoosh earrings" are
  mostly fan-made / third-party).
- Piercing / health topics: practical, cautious; recommend a professional (APP-member)
  piercer and implant-grade titanium / 14k+ solid gold for fresh piercings; mention seeing
  a doctor for signs of infection. Healing times as typical ranges.
- Metric facts must be right: 1 mm = 0.03937 in; gauge table: 20g=0.8mm, 18g=1.0mm,
  16g=1.2mm, 14g=1.6mm, 12g=2mm, 10g=2.5mm, 8g=3mm(3.2), 6g=4mm, 4g=5mm, 2g=6mm,
  0g=8mm, 00g=10mm, 7/16"=11mm, 1/2"=12.7mm, 9/16"=14mm, 5/8"=16mm, 3/4"=19mm, 7/8"=22mm, 1"=25mm.
  Standard lobe earrings are usually 20g or 18g. US penny = 19.05 mm, US dime = 17.91 mm,
  pencil eraser ≈ 6–7 mm, credit card = 85.6 × 53.98 mm.

Images available (key → what the photo shows):
- hoops-book: chunky gold double hoop earrings resting on an open book
- ear-hoop: close-up of a woman's ear with a small gold hoop, fingers touching neck
- ear-huggie-dark: profile of an ear with a textured gold huggie hoop, black background
- ear-stack: ear with a curated stack — small studs and a thin gold hoop in the lobe
- diamond-hoops: two gold eternity hoops set with round diamonds on white
- portrait-gold: woman in profile wearing chunky gold earring and gold chain
- dangle-chains: long delicate gold chain drop earrings hanging, soft background
- sapphire-drops: ornate blue-stone and crystal drop earrings on a green monstera leaf
- diamond-studs: pair of round diamond halo stud earrings on white
- ear-touch: woman tucking hair behind ear, small silver hoop visible
- jhumka: gold Indian temple jewelry set with ruby-studded jhumka-style earrings and necklace
- twist-hoops: twisted gold hoop earrings on white pebbles, dramatic shadows
- twist-hoops-2: chunky twisted gold hoops on stones with dried grass
- flower-studs: two gold flower-shaped crystal stud earrings on dark background
- rose-drops: rose-gold crystal pear drop earrings on white
- blue-hearts: blue crystal heart dangle earrings on gold hooks on white fabric
- jewel-box: jewelry box with rings and small gold ball stud earrings
- display-tray: black-and-white shot of crystal earrings in a compartment display tray
- trays: assorted earrings and pearls arranged in small trays and boxes

MASTER SLUG LIST (for related + internal links):
guides: 5mm-earrings-actual-size, 8mm-earrings-actual-size, what-gauge-are-regular-earrings,
  ear-gauge-size-chart, why-do-my-earrings-smell, types-of-earring-backs, earring-types,
  earring-holder-target, self-piercing-earrings, earrings-in-spanish, kids-clip-on-earrings
piercings: triple-forward-helix-earrings, helix-earrings, rook-earrings, tragus-piercing-earrings,
  dermal-earring, double-lobe-piercing-earrings, behind-the-ear-earrings, cute-cartilage-earrings
celebrity: jason-aldean-earrings, barry-bonds-earring, janet-jackson-key-earring,
  harry-styles-earring, david-bowie-earrings, harrison-ford-earring, felicity-smoak-earrings,
  kylie-jenner-ear-piercings, why-does-mr-clean-have-an-earring
pop culture: fairy-tail-earrings, skyrim-earrings, potara-earrings, dirigible-plum-earrings, eevee-earrings
style: coach-earrings, nike-earrings, chanel-earrings, 80s-earrings, jhumka-earrings, ebay-earrings,
  guys-with-earrings, jordan-earrings-for-guys, dangling-cross-earrings-for-mens
Also linkable tools: /earring-size-tool/ (interactive actual-size viewer + gauge converter).
