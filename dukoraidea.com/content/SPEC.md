# Content spec — dukoraidea.com rebuild

Dukora Idea ("Dukora") is a DIY lighting & decor ideas site: fairy lights, string
lights, LED strip lights, smart bulbs/controllers and the decor around them
(garlands, fake ivy). The original 2021 site was a small Shopify store with a blog.
The rebuild is a content site: the old product URLs become in-depth **light
guides** (buying + styling + how-to), and the old blog posts are rewritten and
expanded. We do NOT sell anything: no prices, no "add to cart", no "our product",
no fake reviews, no invented statistics, no claims of testing labs. Voice:
warm, practical, a maker-friend who has strung a lot of lights. US English.
Second person. Short paragraphs. Concrete numbers only where they are general
knowledge (e.g. 2×AA ≈ 2,000–2,500 mAh, LED strips are commonly 5 V / 12 V / 24 V,
IP65 = splash-proof, IP67/68 = submersible) and phrase them as typical ranges.

Contact email: info@dukoraidea.com (only if natural; never a phone number or address).

## File format

Each content file is a Python module (stdlib only) that defines a list. Bodies are
HTML strings in triple-quoted **raw** strings (`r"""..."""`). Do not use `{`/`}` in
body text except the tokens below. Must import cleanly: verify with
`python3 -c "import importlib.util,sys; s=importlib.util.spec_from_file_location('m','FILE'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(len(m.POSTS))"`
(or `PRODUCTS`).

### Blog post dict (list name `POSTS`)
```python
dict(
    slug="create-your-mason-jar-fairy-lights-in-5-minutes",   # EXACT slug given
    title="Create Your Mason Jar Fairy Lights in 5 Minutes",  # H1, ≤ 70 chars
    meta_title="Mason Jar Fairy Lights: 5-Minute DIY Guide",   # ≤ 60 chars, contains keyword; " | Dukora Idea" is appended by the build if it fits
    description="...",          # meta description 140–158 chars, contains keyword
    keyword="mason jar fairy lights",
    category="DIY Projects",    # one of: "DIY Projects", "Decor Ideas", "Smart Lighting", "Guides", "Events & Holidays"
    image="mason-jar-fairy-lights",   # hero image name from the image list (no extension)
    image_alt="...",
    published="2021-03-14",     # given below
    updated="2026-10-17",
    excerpt="...",              # 1–2 sentences for cards, ≤ 180 chars
    body=r"""<p>...</p> ...""",
    faq=[("Question?", "Answer in 1–3 sentences."), ...],   # 3–5 items, plain text (no HTML)
    related=["slug-a", "slug-b", "slug-c"],   # 3 other blog slugs from the list below
    products=["outdoor-fairy-lights", "battery-operated-fairy-lights"],  # 1–3 product guide slugs from the list below
)
```

### Product guide dict (list name `PRODUCTS`)
```python
dict(
    slug="outdoor-fairy-lights",          # EXACT slug given
    name="Outdoor Fairy Lights",          # short card name
    title="Outdoor Fairy Lights: Battery-Operated, Waterproof & Timer Guide",  # H1 ≤ 75 chars
    meta_title="...",                     # ≤ 60 chars, contains keyword
    description="...",                    # 140–158 chars, contains keyword
    keyword="outdoor fairy lights",
    collection="fairy-lights",            # "fairy-lights" | "smart-lights" | "decor"
    image="garden-string-lights-night",
    image_alt="...",
    gallery=["patio-string-lights", "outdoor-cafe-lights"],   # 2 more image names
    tagline="...",                        # one sentence under the H1
    highlights=["Battery or solar packs", "8-mode + 6h timer", "IP65+ for rain", "Copper or PVC wire"],  # 4 items, ≤ 28 chars each
    specs=[("Power", "2–3×AA or USB; solar for gardens"), ...],  # 6–8 "what to look for" rows (label, recommendation)
    body=r"""...""",                      # the guide, see below
    faq=[(q, a), ...],                    # 4–6
    related_posts=["slug", "slug", "slug"],   # 3 blog slugs
    related_products=["slug", "slug", "slug"],# 3 other product slugs
    updated="2026-10-17",
)
```

## Body HTML rules
- Start with an intro `<p>` (2–3 short paragraphs), then `<h2>` sections (5–8), `<h3>` inside as needed. Never an `<h1>`.
- Keyword in the first paragraph and in at least one `<h2>`; use natural variants of the secondary keywords listed for your page.
- Allowed elements: p, h2, h3, ul, ol, li, strong, em, a, table/thead/tbody/tr/th/td, blockquote, and the components below.
- Components:
  - Tip box: `<div class="callout"><strong>Tip:</strong> text</div>`; warning: `<div class="callout callout--warn"><strong>Safety:</strong> text</div>`
  - Step list: `<ol class="steps"><li><h3>Step title</h3><p>text</p></li>...</ol>`
  - Materials/checklist: `<ul class="checklist"><li>...</li></ul>`
  - Table: wrap in `<div class="table-wrap"><table>...</table></div>`
  - Image figure (use 1–3 per post, different from the hero image): `{{fig:IMAGE_NAME|alt text|caption}}` on its own line
  - Interactive tool embed (only where listed for your page, once): `{{tool:battery}}` (fairy-light battery-life calculator), `{{tool:strip}}` (LED strip length/power-supply calculator), `{{tool:color}}` (color-temperature & mood picker), `{{tool:patio}}` (patio string-light planner). Introduce the tool in the sentence before it.
- Internal links: 4–8 per page, root-relative, no trailing slash, e.g. `<a href="/products/outdoor-fairy-lights">outdoor fairy lights</a>`, `<a href="/blogs/blog/smart-bulbs">smart bulbs</a>`. Tools hub: `/pages/light-tools`. Contact: `/pages/contact`. Only link to URLs in the lists below.
- Length: blog posts 1,100–1,600 words of body; product guides 900–1,300 words.
- No external links. No emoji. No brand names of real products/stores except generic platforms (Alexa, Google Home, Apple HomeKit, Wi-Fi, Bluetooth, Zigbee, Matter are fine).
- No "In conclusion". End with a short wrap-up section that points to a related guide or tool.

## Images (name — orientation — subject)
backyard-lounge-lights L backyard lounge with string lights and floor cushions at night
blue-led-night-lights P blue neon "hello there" sign glowing on a bed
christmas-garland-lights P green garland wound with fairy lights on an old stone wall
christmas-tree-lights P close-up of christmas tree with warm lights and ornament
copper-wire-fairy-lights-terrarium L geometric glass terrarium wrapped in copper-wire fairy lights
cozy-fairy-lights L feet in cozy socks wrapped in warm white fairy lights
fairy-light-photo-wall L person looking at a wall of photos clipped to fairy lights
gaming-rgb-setup L gaming desk with RGB lighting in a dark room
garden-string-lights-night L garden patio with string lights through trees at night
globe-string-lights L colorful globe (ball) string lights on a table
glowing-jar-hands P hands holding a glowing jar of lights
hands-holding-fairy-lights P hands holding a bundle of warm fairy lights, bokeh
holiday-ornaments-lights P holiday ornaments and fairy lights on a knit blanket
ivy-brick-wall L green ivy leaves growing over a brick wall
ivy-leaves-wall L dense ivy leaves covering a wall
jar-fairy-lights-twilight P glass jar of fairy lights at twilight, crescent moon
mason-jar-fairy-lights P clear mason jar with fairy lights at night, crescent moon
outdoor-cafe-lights P outdoor cafe seating at night with warm lights and palms
outdoor-wedding-setup P long outdoor wedding tables with string lights overhead
party-string-lights L people dancing under string lights at night
patio-string-lights P restaurant patio with festoon string lights and greenery
rainbow-light-bulb P light bulb on a rainbow-striped background
red-led-strip-ceiling L red LED strip glowing along a ceiling edge in a dark room
rgb-ball-string-lights P multicolor ball string lights close-up
smart-bulbs-phone L smart bulbs and smartphone on an orange background
smart-home-bulbs L smart bulbs glowing pink with a smartphone
starlight-dream-bottle L glass bottle of lights with a "dreams" note in its neck
warm-bedroom-lighting P cozy bedroom with warm lamp light and macrame
wedding-reception-lights L outdoor wedding reception at night under lights
wedding-table-garden L long wedding table set on a lawn under string lights

## All URLs (link only to these)
Home `/` · Tools `/pages/light-tools` · About `/pages/about-us` · Contact `/pages/contact`
Collections: `/collections/fairy-lights`, `/collections/smart-lights`, `/collections/all`
Blog index `/blogs/blog`

Product guides (slug — primary keyword — secondary keywords):
- outdoor-fairy-lights — fairy lights / outdoor fairy lights — battery operated fairy lights, fairy lights with timer, battery powered fairy lights, outdoor battery christmas lights, battery operated hanging lights, connectable outdoor fairy lights, white outdoor fairy lights — tool: battery
- battery-operated-fairy-lights — battery operated fairy lights — starry string lights, mini string lights battery operated, micro fairy lights, led micro light string, star fairy lights battery operated, battery operated fairy lights wedding — tool: battery
- wifi-smart-led-strip-lights — smart led strip lights — led strip lights, wifi led light strip, smart led strip lights app, outdoor/waterproof led strip lights, bedroom lights with remote — tool: strip
- smart-led-light-bulbs — smart led light bulbs — google home color changing light bulbs, smart color bulbs, alexa light bulbs — tool: color
- led-controller — wifi led controller — led controller alexa, wifi led controller google home, led strip controller wifi, smart wireless led controller, rgb controller — tool: strip
- outdoor-string-lights — waterproof fairy lights — waterproof outdoor fairy lights, copper wire fairy lights, waterproof battery operated string lights, underwater fairy lights, waterproof garden fairy lights — tool: patio
- garland-fairy-string-light — battery operated garland — pre lit garland battery operated, christmas garland with battery operated lights, fairy light garland, cordless garland with lights — tool: battery
- fake-ivy-leaves — fake ivy leaves — fake vines room decor, fake ivy room decor, fake ivy wall decor, hanging fake vines (pairing vines with fairy lights) — no tool
- string-lights — firefly string lights — firefly lights copper wire, battery operated flower fairy lights, fireflies in mason jar battery operated — tool: battery
- fairy-lights — silver wire fairy lights — silver wire micro fairy lights, micro LED wire lights, USB fairy lights — tool: battery
- indoor-fairy-lights — indoor fairy lights — mini lights, fairy lights for bedroom, plug-in vs USB fairy lights — tool: color

Blog posts (slug — published — keyword — notes):
- create-your-mason-jar-fairy-lights-in-5-minutes — 2020-11-20 — mason jar fairy lights — secondary: fairy lights in a jar, diy mason jar fairy lights, how to put fairy lights in a jar, how to hide a fairy light battery pack, solar mason jar fairy lights, mason jar fairy lights centerpiece, fairy light jar craft, how to make a fairy lamp. THE most important page (it ranked #2–#10). Title exactly "Create Your Mason Jar Fairy Lights in 5 Minutes". Steps, materials, 5+ variations, battery-pack hiding tricks. tool: battery
- how-to-make-diy-fairy-lights-to-decorate-your-home — 2020-12-08 — how to make diy fairy lights — secondary: fairy lights headboard, fairy lights around mirror, fairy lights above bed, how to make your own fairy lights, decorate a room with fairy lights, copper wire lights
- best-strip-lights-for-diy-project — 2021-01-19 — best strip lights for diy projects — secondary: diy waterproof led lights, IP ratings, LED density, 12V vs 24V, COB vs SMD. tool: strip
- beautiful-diy-fairy-light-decor-ideas — 2021-02-02 — fairy light decoration ideas — secondary: fairy light room ideas, fairy lights all year round
- gorgeous-fairy-lights-for-your-bedroom-decor-event-or-party — 2021-02-23 — fairy lights for bedroom, events and parties — secondary: party lights, western party lights, event lighting
- 9-innovative-ways-to-use-fairy-lihgts-in-you-diy-porject — 2021-03-10 — ways to use fairy lights in diy projects — (slug keeps the original typo; title: "9 Innovative Ways to Use Fairy Lights in Your DIY Project") secondary: diy fairy light wall
- strip-lights-sofa — 2021-04-06 — led lights under couch — secondary: sofa with lights under it, smart strip lights sofa, motion sensor. tool: strip
- give-your-child-a-dream-of-starry-sky-with-fairy-lights-super-simple-starlight-bottle-diy — 2021-05-11 — starlight bottle diy — secondary: dream fairy lights, fairy lights in a bottle, kids night light DIY (child safety: battery compartments screwed shut, adult supervision). Title: "Give Your Child a Dream of a Starry Sky: Super-Simple Starlight Bottle DIY"
- most-significant-wedding-celebration-motif-patterns — 2021-06-15 — wedding motifs — secondary: wedding motif patterns, wedding lighting ideas, fairy light wedding decor. Title: "The Most Significant Wedding Celebration Motifs (and How to Light Them)"
- smart-bulbs — 2021-07-20 — smart bulbs — secondary: smart bulb vs incandescent, google home color changing bulbs, music sync smart bulbs, how smart bulbs work, Wi-Fi vs Zigbee vs Bluetooth vs Matter. tool: color
- how-to-connect-alexa-to-led-strip-lights — 2026-08-04 — how to connect alexa to led lights — secondary: alexa led strip lights, google home led strip, 2.4 GHz wifi troubleshooting
- how-long-do-battery-fairy-lights-last — 2026-08-18 — how long do battery fairy lights last — secondary: fairy light battery life, rechargeable vs alkaline, timer modes. tool: battery
- how-to-hang-outdoor-string-lights — 2026-09-01 — how to hang outdoor string lights — secondary: patio string light ideas, without nails, guide wire, poles. tool: patio
- how-to-cut-and-connect-led-strip-lights — 2026-09-15 — how to cut led strip lights — secondary: connect led strip lights, solderless connectors, corners. tool: strip
- christmas-fairy-light-ideas — 2026-09-29 — christmas fairy light ideas — secondary: battery operated christmas lights, garland with lights, indoor christmas decor
- led-strip-light-colors-meaning — 2026-10-06 — led light colors meaning — secondary: best led color for sleep, best led color for studying, color temperature kelvin, mood lighting. tool: color
- fairy-lights-vs-string-lights — 2026-10-13 — fairy lights vs string lights — secondary: difference, which to choose, micro LED, festoon, globe lights
