# Custom Southern Co. — content spec (for writers)

Site: https://customsouthernco.com — "Custom Southern Co." A Southern vintage-finds and
repurposed-decor blog: antique history & collecting, thrift/junk flips, seasonal farmhouse
DIY, and old-fashioned home know-how. Voice: warm, friendly, practical, a little Southern
("y'all" sparingly, max once per post), first-person plural ("we"). US spelling.
Byline is always "The Custom Southern Co. Team" — never invent a named person, never
claim personal anecdotes as verifiable facts (light "we like to…" is fine).
Contact email: info@customsouthernco.com (only if needed).

## Output format
Each writer creates ONE Python module `customsouthernco/content/posts_<x>.py` that
defines `POSTS = [ {...}, ... ]`. Plain Python literals only, stdlib only. Use
triple-quoted strings for HTML. Each dict:

    {
      "slug": "history-of-prince-albert-tins",   # EXACT slug given, no slashes
      "title": "…",            # H1, <= 70 chars, contains primary keyword
      "seo_title": "…",        # <title>, <= 60 chars, contains keyword (site name appended automatically, don't add it)
      "description": "…",      # meta description 140-158 chars, contains keyword
      "keyword": "…",          # primary keyword (lowercase)
      "category": "…",         # one of: vintage-finds, diy-repurpose, seasonal, southern-home
      "date": "2026-10-01",    # YYYY-MM-DD, any date 2026-08-01..2026-10-16
      "image": "albert-tin",   # hero image key from the IMAGE KEYS list below
      "image_alt": "…",        # descriptive alt text
      "excerpt": "…",          # 1-2 sentence card teaser (<= 160 chars)
      "time": "45 minutes",    # DIY posts only: project time; omit key for non-DIY
      "difficulty": "Easy",    # DIY posts only: Easy | Moderate; omit for non-DIY
      "cost": "$10–$20",       # DIY posts only; omit for non-DIY
      "supplies": ["…", "…"],  # DIY posts only: list of strings
      "steps": [("Step name", "One-to-three sentence instruction."), ...],  # DIY posts only, 4-9 steps -> rendered as a numbered HowTo + HowTo schema
      "body": """<p>…</p><h2>…</h2>…""",   # main article HTML (see rules)
      "faq": [("Question?", "Answer 2-4 sentences."), ...],   # 3-6 items
      "related": ["slug-a", "slug-b", "slug-c"],   # 3 slugs from the MASTER LIST
    }

## Body HTML rules
- Allowed tags: p, h2, h3, ul, ol, li, strong, em, a, blockquote, table/thead/tbody/tr/th/td.
  No h1, no inline styles, no classes except those listed here, no scripts.
- Optional callout: `<div class="tip"><strong>Tip:</strong> …</div>` (max 2 per post).
- Optional inline image: a line exactly `{{img:KEY|Caption text}}` on its own (max 2 per
  post, KEY from the image list, different from the hero).
- Optional interactive tool embed: a line exactly `{{tool:NAME}}` on its own, only where noted.
  NAMES: `tin-dater` (Prince Albert tin dating helper), `jar-dater` (Ball jar logo age
  finder), `detergent` (laundry detergent batch & cost calculator), `project-finder`.
- For DIY posts DO NOT write the supplies list or numbered steps in the body — they are
  rendered from `supplies`/`steps` automatically, after the body's intro. The body for a DIY
  post should cover: intro (why this project), "Finding the right piece"/sourcing tips, the
  design/styling ideas, variations, care/safety notes. Write `{{howto}}` on its own line
  where the supplies+steps block should appear (usually after the first 2-3 paragraphs).
- Internal links: 3-6 per post, href="/slug/" for posts in the MASTER LIST, "/tools/<name>/"
  for tools (/tools/prince-albert-tin-dater/, /tools/ball-jar-age-finder/,
  /tools/laundry-detergent-calculator/, /tools/diy-project-finder/), "/blog/", "/contact/".
  No external links.
- Length: DIY posts 900-1300 words of body; history/guide posts 1300-2000 words;
  the Prince Albert flagship 2200-2800 words.
- Use the primary keyword in the first paragraph and in at least one H2. Natural language,
  no keyword stuffing. Use 4-8 H2s.
- Accuracy: only state historical facts you are confident about; hedge dates with
  "around", "by the early 1900s", etc. Never invent prices as fact — give ranges with
  "typically" and note condition drives value. No medical/legal claims.
- Safety notes where relevant (borax/washing soda handling, lead paint on old pieces,
  rusty metal, glass, electrical rewiring of light globes, open flames near decor).

## Escape rules
Content is inserted as raw HTML. Use `&amp;` for literal ampersands in body HTML.
Use straight ASCII apostrophes or typographic ones, either is fine. Make sure the module
imports cleanly: `python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" FILE`.

## IMAGE KEYS (hero/inline)
hero, about, flea-market, antiques-shop, estate-sale, albert-tin, tobacco-tins,
red-barn, barn-winter, mason-jars, jars-shelf, laundry, soap-bar, folded-towels,
tinsel-tree, xmas-ornaments, snowman, doorknobs, barnwood, barnwood-tree, pie, bread,
old-photos, flag, spice-tins, cutting-board, yardstick, pumpkins, jello-mold, cloche,
succulents, valentine, old-books, sheet-music, old-window, light-globe, tiered-tray,
rusty-metal, chalk-paint, porch, kitchen-vintage

## MASTER LIST (slug — primary keyword — category — writer)
### Existing pages being rebuilt (keep slugs EXACTLY)
history-of-prince-albert-tins — prince albert in a can — vintage-finds — A  (flagship; embed {{tool:tin-dater}}; cover: what it is, 1907 R.J. Reynolds launch, named for Prince Albert/Edward VII, crimp cut, the "do you have Prince Albert in a can?" prank call joke, tin designs by era, how to date a tin, tin values, cigarette/pocket tins, where to find, repurposing ideas, is it still made (hedge))
how-to-make-laundry-detergent-with-3-ingredients — diy laundry detergent 3 ingredients — southern-home — A (DIY; embed {{tool:detergent}}; washing soda, borax, grated bar soap; HE notes; safety)
pie-bird — pie bird — vintage-finds — A (what a pie bird is, history (pie funnels, UK origins, ceramic birds), how to use, collecting tips, reproductions)
history-of-the-red-barn — why are barns red — vintage-finds — A
the-christmas-barn-sale-trail — christmas barn sale — seasonal — A (general guide to holiday barn/junk sales; do not invent a real named event's dates)
lets-go-pickin-for-antiques — antique picking tips — vintage-finds — A
what-vintage-jars-to-look-for — vintage jars to look for — vintage-finds — A (embed {{tool:jar-dater}})
how-to-clean-old-jars — how to clean old jars — vintage-finds — A
how-to-make-a-faux-tinsel-tree — diy tinsel tree — seasonal — B (DIY)
diy-spindle-snowman-ornament — spindle snowman — seasonal — B (DIY)
quick-vintage-door-knob-tree — door knob christmas tree — seasonal — B (DIY)
easy-christmas-spindle-ornaments — spindle ornaments — seasonal — B (DIY)
simple-barn-wood-christmas-trees — barn wood christmas trees — seasonal — B (DIY)
easy-pumpkin-funnel-diy — funnel pumpkin — seasonal — B (DIY)
vintage-jello-mold-pumpkin-diy — jello mold pumpkin — seasonal — B (DIY)
rustic-cloche-diy-for-spring — diy cloche — seasonal — B (DIY)
upcycled-vintage-cutting-board-for-spring — spring cutting board decor — seasonal — B (DIY)
succulent-dustpan-decor — dustpan planter — diy-repurpose — B (DIY)
easy-vintage-valentine-banner — vintage valentine banner — seasonal — C (DIY)
easy-valentine-book-decor-diy — valentine book decor — seasonal — C (DIY)
rustic-patriotic-decor-diy — rustic patriotic decor — seasonal — C (DIY)
how-to-make-faux-bread — faux bread — diy-repurpose — C (DIY, decorative fake bread loaves for farmhouse kitchens)
easy-vintage-photo-shelf-sitter — vintage photo holder — diy-repurpose — C (DIY)
easy-vintage-spice-tin-diy — vintage spice tin — diy-repurpose — C (DIY)
easy-ball-jar-decor-diy — ball jar decor — diy-repurpose — C (DIY; embed {{tool:jar-dater}} is optional)
repurposed-yardstick-decor-project — yardstick decor — diy-repurpose — C (DIY)
easy-vintage-cutting-board-decor — cutting board decor — diy-repurpose — D (DIY)
old-window-decoupage-mirror — old window mirror — diy-repurpose — D (DIY)
how-to-repurpose-antique-light-globes — antique light globes — diy-repurpose — D (DIY; ideas: cloches, planters, pendant swaps, terrariums; electrical safety)
easy-hymn-tea-stain-diy — tea stained hymn pages — diy-repurpose — D (DIY)
rustic-tiered-tray-diy — diy tiered tray — diy-repurpose — D (DIY)
### New blog posts
how-to-date-ball-mason-jars — how to date ball mason jars — vintage-finds — E (embed {{tool:jar-dater}})
vintage-tobacco-tin-values — vintage tobacco tin value — vintage-finds — E (link to Prince Albert post & tool)
how-to-remove-rust-from-vintage-metal — how to remove rust from vintage metal — southern-home — E
estate-sale-shopping-tips — estate sale tips — vintage-finds — E
how-to-spot-reproduction-antiques — how to spot reproduction antiques — vintage-finds — E
homemade-fabric-softener — homemade fabric softener — southern-home — E (DIY; link to detergent post+calculator)
how-to-distress-furniture-with-chalk-paint — how to distress furniture — diy-repurpose — E (DIY)
southern-front-porch-decor-ideas — front porch decor ideas — southern-home — E
