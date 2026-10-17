"""Homepage, pillar pages, hubs and legal pages. build_pages yields (path, html, sitemap_priority|None)."""
import json
import re

from content.projects import PROJECTS
from content.tools import TOOLS, tool_card


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def home(c):
    pic, posts, esc = c["pic"], c["posts"], c["esc"]
    cats = "".join(
        f'<a class="cat-tile reveal d{i % 4}" href="/category/{s}/">{pic(v[2], v[0])}<div class="in"><h3>{v[0]}</h3><p>{v[1]}</p></div></a>'
        for i, (s, v) in enumerate(c["CATEGORIES"].items()))
    latest = c["post_card"](posts[0], feature=True) + "".join(c["post_card"](p) for p in posts[1:5])
    tools = "".join(tool_card(t) for t in TOOLS)
    ideas = [
        {"time": "quick", "skill": "nosew", "mood": "home", "title": "Knotted pillow cover", "label": "20 min", "text": "Wrap a pillow in fabric and tie a big decorative knot — swap it every season.", "url": "/4no-sew-diy-fabric-projects/#pillow", "img": "/assets/img/linen-pillow.jpg"},
        {"time": "quick", "skill": "nosew", "mood": "gift", "title": "Furoshiki fabric gift wrap", "label": "5 min", "text": "A fabric square and one clever knot — the wrapping becomes part of the gift.", "url": "/no-sew-fabric-craft-projects/#project-25", "img": "/assets/img/colorful-fabrics.jpg"},
        {"time": "quick", "skill": "nosew", "mood": "kids", "title": "T-shirt superhero cape", "label": "10 min", "text": "One old T-shirt, a felt emblem and a very happy small person.", "url": "/no-sew-fabric-craft-projects/#project-15", "img": "/assets/img/cozy-craft-flatlay.jpg"},
        {"time": "hour", "skill": "nosew", "mood": "home", "title": "Fabric-wrapped storage bins", "label": "45 min", "text": "Turn delivery boxes into pretty shelf storage with fabric and Mod Podge.", "url": "/4no-sew-diy-fabric-projects/#bins", "img": "/assets/img/felt-fabric-stack.jpg"},
        {"time": "hour", "skill": "nosew", "mood": "gift", "title": "Felt coasters set", "label": "20–30 min", "text": "Patterned cotton on thick wool felt, trimmed with pinking shears.", "url": "/no-sew-fabric-craft-projects/#project-9", "img": "/assets/img/plaid-patchwork.jpg"},
        {"time": "hour", "skill": "nosew", "mood": "kids", "title": "Felt-board story set", "label": "1 hr", "text": "Felt sticks to felt — cut characters and scenery for endless storytelling.", "url": "/no-sew-fabric-craft-projects/#project-39", "img": "/assets/img/felt-fabric-stack.jpg"},
        {"time": "weekend", "skill": "nosew", "mood": "home", "title": "No-sew fleece tie blanket", "label": "2 hrs", "text": "Two fleece layers, a fringe and a lot of knots — the classic cozy make.", "url": "/how-to-make-a-no-sew-fleece-blanket/", "img": "/assets/img/folded-blankets.jpg"},
        {"time": "weekend", "skill": "nosew", "mood": "gift", "title": "No-sew diaper changing pad", "label": "30–45 min", "text": "Laminated cotton bonded to flannel — a baby-shower favorite.", "url": "/no-sew-fabric-craft-projects/#project-18", "img": "/assets/img/linen-swatches.jpg"},
        {"time": "weekend", "skill": "nosew", "mood": "kids", "title": "Fleece car seat poncho", "label": "45 min–1 hr", "text": "Keeps little ones warm in the car without a bulky coat under the straps.", "url": "/no-sew-fabric-craft-projects/#project-17", "img": "/assets/img/folded-blankets.jpg"},
        {"time": "quick", "skill": "hand", "mood": "home", "title": "Sew on a button properly", "label": "5 min", "text": "Learn the thread shank and your buttons will never pop off again.", "url": "/how-to-sew-a-button/", "img": "/assets/img/buttons.jpg"},
        {"time": "hour", "skill": "hand", "mood": "gift", "title": "Lavender sachets", "label": "30 min", "text": "Two squares, a slip stitch and dried lavender — practice your hand stitches.", "url": "/hand-sewing-stitches-for-beginners/", "img": "/assets/img/thimble-and-spools.jpg"},
        {"time": "weekend", "skill": "hand", "mood": "kids", "title": "Visible-mend denim patches", "label": "1–2 hrs", "text": "Turn worn knees into a feature with sashiko-style running stitch.", "url": "/upcycle-old-jeans/", "img": "/assets/img/embroidered-denim-pocket.jpg"},
        {"time": "quick", "skill": "machine", "mood": "gift", "title": "Scrunchies from scraps", "label": "15 min", "text": "A strip of fabric, some elastic and one seam.", "url": "/fabric-scrap-projects/", "img": "/assets/img/colorful-fabrics.jpg"},
        {"time": "hour", "skill": "machine", "mood": "home", "title": "Patchwork pillow cover", "label": "1 hr", "text": "Sixteen 5\" squares and an envelope back.", "url": "/fabric-scrap-projects/", "img": "/assets/img/plaid-patchwork.jpg"},
        {"time": "weekend", "skill": "machine", "mood": "gift", "title": "Jean-leg tote bag", "label": "1–2 hrs", "text": "Old jeans become the toughest tote you'll ever own.", "url": "/upcycle-old-jeans/", "img": "/assets/img/old-jeans.jpg"},
        {"time": "hour", "skill": "machine", "mood": "kids", "title": "Kids' bucket hat", "label": "1 hr", "text": "Denim or cotton scraps make a sturdy, sunny-day hat.", "url": "/upcycle-old-jeans/", "img": "/assets/img/sewing-machine-orange-felt.jpg"},
    ]
    body = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow reveal">Fabric crafts · DIY projects · Sewing</span>
      <h1 class="reveal d1">Make something lovely with fabric — <span class="hl">no sewing<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M2 12 C 60 2, 120 18, 180 8 S 270 4, 298 12"/></svg></span> required.</h1>
      <p class="lead reveal d2">Kotric is a home for easy fabric craft ideas, no-sew projects, beginner sewing tutorials and organizing tips. Grab your scraps — let's make something today.</p>
      <div class="hero-ctas reveal d3">
        <a class="btn btn-primary" href="/no-sew-fabric-craft-projects/">See 41 no-sew projects <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
        <a class="btn btn-ghost" href="#picker">Find a project for me</a>
      </div>
      <div class="hero-stats reveal d3">
        <div><b data-count="41">41</b>no-sew projects</div>
        <div><b data-count="{len(posts)}">{len(posts)}</b>step-by-step guides</div>
        <div><b data-count="{len(TOOLS)}">{len(TOOLS)}</b>free craft tools</div>
      </div>
    </div>
    <div class="collage" aria-hidden="true">
      <svg class="spool-badge" viewBox="0 0 130 130"><defs><path id="circ" d="M65,65 m-50,0 a50,50 0 1,1 100,0 a50,50 0 1,1 -100,0"/></defs><text><textPath href="#circ">DIY • SEW • CRAFT • CREATE • </textPath></text></svg>
      <span class="spool-core">K</span>
      <figure class="c1">{pic("sewing-machine-orange-felt", "", eager=True)}</figure>
      <figure class="c2">{pic("colorful-fabrics", "")}</figure>
      <figure class="c3">{pic("pincushion-and-thread", "")}</figure>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track"><span>No-sew projects</span><span>Fabric scraps</span><span>Fleece blankets</span><span>Upcycled denim</span><span>Sewing hacks</span><span>Stash organization</span><span>Felt crafts</span><span>Gift ideas</span><span>No-sew projects</span><span>Fabric scraps</span><span>Fleece blankets</span><span>Upcycled denim</span><span>Sewing hacks</span><span>Stash organization</span><span>Felt crafts</span><span>Gift ideas</span></div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Browse by craft</span><h2>What do you feel like making?</h2><p class="lead">Four corners of the craft room, each packed with ideas you can start today.</p></div>
    <div class="cat-grid">{cats}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div class="split-media reveal">{pic("scissors-and-thread", "Fabric scissors, thread and flowers on an open book")}<div class="sticker">41<br>no-sew<br>ideas</div></div>
    <div class="reveal d1">
      <span class="eyebrow">Reader favorite</span>
      <h2>41 amazing no-sew DIY fabric projects</h2>
      <p class="lead">Our most-loved guide: blankets, pillow covers, bags, gifts and décor made with knots, glue and fusible tape — not a single stitch.</p>
      <ul class="checklist"><li>Filter by kids, home décor, gifts or quick makes</li><li>Tick off each project you make — we'll remember your progress</li><li>Materials and time for every idea</li></ul>
      <a class="btn btn-primary" href="/no-sew-fabric-craft-projects/">Explore all 41 projects</a>
    </div>
  </div>
</section>

<section class="section" id="picker-section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Interactive</span><h2>Not sure what to make? Let's pick together.</h2><p class="lead">Tell us how much time you have and how you like to work — we'll suggest a project.</p></div>
    <div class="picker reveal" id="picker">
      <div class="picker-q" data-k="time"><span>How much time do you have?</span><div class="chips"><button type="button" class="chip" data-v="quick" aria-pressed="false">Under 20 minutes</button><button type="button" class="chip" data-v="hour" aria-pressed="true">About an hour</button><button type="button" class="chip" data-v="weekend" aria-pressed="false">A lazy weekend</button></div></div>
      <div class="picker-q" data-k="skill"><span>How do you want to work?</span><div class="chips"><button type="button" class="chip" data-v="nosew" aria-pressed="true">No sewing at all</button><button type="button" class="chip" data-v="hand" aria-pressed="false">A little hand stitching</button><button type="button" class="chip" data-v="machine" aria-pressed="false">Sewing machine</button></div></div>
      <div class="picker-q" data-k="mood"><span>Who's it for?</span><div class="chips"><button type="button" class="chip" data-v="home" aria-pressed="true">My home</button><button type="button" class="chip" data-v="gift" aria-pressed="false">A gift</button><button type="button" class="chip" data-v="kids" aria-pressed="false">The kids</button></div></div>
      <div class="picker-result" aria-live="polite"></div>
      <script type="application/json" id="picker-data">{json.dumps(ideas)}</script>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">From the blog</span><h2>Fresh tutorials &amp; ideas</h2></div>
    <div class="post-grid">{latest}</div>
    <p class="center" style="margin-top:40px"><a class="btn btn-ghost" href="/blog/">Read all articles</a></p>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Free craft tools</span><h2>Skip the mental math</h2><p style="opacity:.8">Calculators and helpers that answer the questions every crafter asks.</p></div>
    <div class="tool-grid">{tools}</div>
  </div>
</section>

<section class="section">
  <div class="wrap split rev">
    <div class="split-media reveal">{pic("home-cushions", "A sofa styled with soft handmade cushions")}<div class="sticker">Weekend<br>projects</div></div>
    <div class="reveal d1">
      <span class="eyebrow">Step by step</span>
      <h2>4 no-sew DIY fabric projects to finish this weekend</h2>
      <p class="lead">Detailed tutorials for a fleece tie blanket, a knotted pillow cover, a T-shirt tote bag and fabric-wrapped storage bins — with checklists you can tick off as you go.</p>
      <a class="btn btn-primary" href="/4no-sew-diy-fabric-projects/">Start a weekend project</a>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="cta-band reveal">
      <div><h2>Made something from Kotric?</h2><p>We love seeing your projects — and we read every question. Send a photo or ask us anything about fabric, sewing or no-sew crafts.</p></div>
      <div><a class="btn" href="mailto:{c["EMAIL"]}">Email {c["EMAIL"]}</a></div>
    </div>
  </div>
</section>'''
    ws = {"@context": "https://schema.org", "@graph": [
        dict(c["ORG"], sameAs=[]),
        {"@type": "WebSite", "@id": c["SITE"] + "/#website", "url": c["SITE"] + "/", "name": "Kotric",
         "description": "Fabric crafts, DIY projects and sewing tutorials", "publisher": {"@id": c["SITE"] + "/#org"}}]}
    return c["page"]("/", "Kotric | Fabric Crafts, No-Sew DIY Projects & Sewing Tutorials",
                     "Easy fabric craft ideas, 41 no-sew DIY projects, beginner sewing tutorials, organizing tips and free craft calculators. Make something lovely with fabric today.",
                     body, [ws], og_img="sewing-machine-orange-felt")


def projects_page(c):
    pic, esc = c["pic"], c["esc"]
    path = "/no-sew-fabric-craft-projects/"
    title = "41 Amazing No-Sew DIY Fabric Projects"
    crumbs, crumb_ld = c["breadcrumbs"]([("Home", "/"), ("Fabric Crafts", "/category/fabric-crafts/"), (title, path)])
    items = ""
    for i, (name, t, lvl, tags, text, mats, link, img) in enumerate(PROJECTS, 1):
        more = f' <a href="{link}">Step-by-step guide →</a>' if link else ""
        im = f'<div class="proj-img">{pic(img, name)}</div>' if img else ""
        items += f'''<div class="proj reveal" id="project-{i}" data-tags="{tags} {lvl.lower()}">
  {im}<div class="num">{i:02d}</div>
  <div><h3>{esc(name)}</h3><div class="facts"><span>⏱ {t}</span><span class="lvl-{lvl.lower()}">{lvl}</span><span>🧵 {esc(mats)}</span></div>
  <p>{esc(text)}{more}</p>
  <label class="made"><input type="checkbox"> I made this!</label></div>
</div>'''
    chips = [("all", "All 41"), ("quick", "Under 20 min"), ("kids", "For kids"), ("decor", "Home décor"), ("gift", "Gifts"),
             ("fleece", "Fleece"), ("tshirt", "T-shirt"), ("felt", "Felt"), ("wearable", "Wearable"), ("made", "✓ Made it")]
    chip_html = "".join(f'<button type="button" class="chip" data-v="{v}" aria-pressed="{"true" if v == "all" else "false"}">{l}</button>' for v, l in chips)
    fq_list = [
        ("What is the easiest no-sew fabric project?", "A knotted pillow cover or furoshiki gift wrap — both take minutes and need only a square of fabric. For a bigger project, the fleece tie blanket is the classic first make."),
        ("What can I use instead of sewing fabric?", "Permanent fabric glue, fusible web, iron-on hem tape, hot glue (for décor only) and knots. Fleece, felt and T-shirt jersey don't fray, which makes them ideal for no-sew projects."),
        ("Are no-sew projects washable?", "Projects made with knots, permanent fabric glue or fusible web can be washed once the adhesive has cured. Hot glue is not washable, so keep it for décor."),
        ("What fabric is best for no-sew crafts?", "Fleece, felt, T-shirt jersey and medium-weight cotton. Non-fraying fabrics are easiest because their cut edges don't need finishing."),
    ]
    fq, fq_ld = c["faq_html"](fq_list)
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs}
    <span class="eyebrow">No needle, no thread</span>
    <h1 class="reveal">41 Amazing No-Sew DIY Fabric Projects</h1>
    <p class="lead reveal d1" style="max-width:760px">No sewing machine? No problem. These no-sew fabric craft projects use knots, fabric glue, fusible web and a little creativity to make blankets, pillow covers, bags, gifts, kids' crafts and home décor. Filter the list, search it, and tick off the projects you've made.</p>
    <div class="post-meta reveal d2"><span>By the Kotric Team</span><span>Updated {c["fmt_date"](c["BUILD_DATE"])}</span><span>12 min read</span></div>
    <div class="hero-img reveal d2">{pic("colorful-fabrics", "Bright cotton and silk fabrics ready for no-sew projects", eager=True)}</div>
  </div>
</section>
<section class="section" style="padding-top:24px">
  <div class="wrap">
    <div class="prose" style="max-width:860px;margin:0 auto 34px">
      <h2 id="before-you-start">Before you start: the no-sew toolkit</h2>
      <p>Almost every project below uses some combination of these supplies. Pick up the basics once and you'll be ready for dozens of makes:</p>
      <ul class="supplies"><li>Sharp fabric scissors &amp; pinking shears</li><li>Permanent fabric glue</li><li>Fusible web &amp; iron-on hem tape</li><li>Hot glue gun (décor only)</li><li>Mod Podge &amp; a foam brush</li><li>An iron and pressing cloth</li></ul>
      <p>Not sure which bond to use? Read <a href="/fabric-glue-vs-fusible-web/">fabric glue vs fusible web vs hem tape</a> or take the <a href="/tools/no-sew-method-quiz/">no-sew method quiz</a>. For step-by-step photos of four of these projects, see our <a href="/4no-sew-diy-fabric-projects/">weekend no-sew tutorials</a>.</p>
    </div>
    <div class="proj-toolbar">
      <div class="row">
        <div class="chips" id="proj-filter" role="group" aria-label="Filter projects">{chip_html}</div>
      </div>
      <div class="row" style="margin-top:10px">
        <input class="proj-search" id="proj-q" type="search" placeholder="Search projects (e.g. pillow, felt, gift)…" aria-label="Search projects">
        <div class="proj-progress"><span class="bar"><i id="proj-bar"></i></span><span id="proj-prog">0 / {len(PROJECTS)} made</span></div>
      </div>
    </div>
    <div class="proj-list" id="proj-list" style="max-width:860px;margin:0 auto">{items}</div>
    <p class="empty-note">No projects match — try another filter or search term.</p>
    <div class="prose" style="max-width:860px;margin:50px auto 0">
      <h2 id="tips">Tips for no-sew success</h2>
      <ul>
        <li><strong>Choose non-fraying fabrics</strong> — fleece, felt and jersey — when edges will show.</li>
        <li><strong>Let glue cure fully</strong> before washing: usually 24–72 hours.</li>
        <li><strong>Press, don't slide</strong> the iron when using fusible web.</li>
        <li><strong>Prewash cottons</strong> for anything washable, so they don't shrink away from the bond later. See <a href="/how-to-prewash-fabric/">should you prewash fabric?</a></li>
        <li><strong>Save your scraps</strong> — half of these projects need only small pieces. Our <a href="/fabric-scrap-projects/">fabric scrap projects</a> list has 25 more ideas.</li>
      </ul>
      {fq}
    </div>
  </div>
</section>
<section class="section section-dark">
  <div class="wrap"><div class="section-head"><span class="eyebrow">Plan your project</span><h2>Free tools for no-sew makers</h2></div><div class="tool-grid">{"".join(tool_card(t) for t in TOOLS)}</div></div>
</section>'''
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": title, "numberOfItems": len(PROJECTS),
          "itemListElement": [{"@type": "ListItem", "position": i, "name": p[0], "url": f'{c["SITE"]}{path}#project-{i}'} for i, p in enumerate(PROJECTS, 1)]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": title,
           "description": "41 no-sew DIY fabric projects using knots, fabric glue and fusible web.",
           "image": c["SITE"] + c["img_url"]("colorful-fabrics"), "dateModified": c["BUILD_DATE"], "datePublished": "2023-01-10",
           "author": {"@type": "Organization", "name": "The Kotric Team"}, "publisher": c["ORG"], "mainEntityOfPage": c["SITE"] + path}
    return c["page"](path, "41 Amazing No-Sew DIY Fabric Projects (Easy Ideas) | Kotric",
                     "41 easy no-sew DIY fabric projects: fleece tie blankets, knotted pillow covers, T-shirt bags, felt crafts, gifts and home décor made without a needle and thread.",
                     body, [art, il, crumb_ld, fq_ld], og_img="colorful-fabrics", og_type="article", progress=False)


FOUR = [
    ("blanket", "1. No-sew fleece tie blanket", "folded-blankets", "Two hours · Easy · Great for gifts",
     "The classic. Two layers of fleece knotted together around the edges make a warm, washable blanket for any size bed or sofa.",
     ["2 coordinating fleece pieces (2 yd each for a 50\" × 60\" throw)", "Fabric scissors or rotary cutter", "Cutting mat and ruler", "4\" cardboard square template"],
     ["Lay the backing fleece face-down and the top face-up, edges aligned.", "Trim off the selvedges and square up both layers together.", "Cut a 4\" square out of every corner, through both layers.",
      "Cut 1\"-wide, 4\"-deep fringe strips along every side.", "Double-knot each top strip to the backing strip beneath it.", "Tie the corners last and shake the blanket out."],
     'Use the <a href="/tools/fleece-tie-blanket-calculator/">fleece blanket calculator</a> for other sizes, or read the <a href="/how-to-make-a-no-sew-fleece-blanket/">full fleece blanket guide</a> for knot variations.'),
    ("pillow", "2. Knotted no-sew pillow cover", "linen-pillow", "20 minutes · Easy · Renter-friendly décor",
     "A square of fabric wrapped around a pillow form and tied at the front, like a Japanese furoshiki. Change it with the seasons in seconds.",
     ["Pillow form (16–18\")", "Fabric square 2½× the pillow width (about 1 yd for an 18\" pillow)", "Scissors", "Optional: fabric glue or a safety pin"],
     ["Lay the fabric face-down and place the pillow diagonally in the center.", "Fold the bottom corner up over the pillow and tuck the point under.", "Fold the top corner down over the pillow.",
      "Bring the left and right corners to the front and tie them in a square knot.", "Tuck the tails into the knot or spread them into a bow.", "Secure the knot with a hidden safety pin if it will be used a lot."],
     'Lighter cottons and linens knot best. Bulky upholstery fabric makes a lumpy knot — save it for the <a href="/no-sew-fabric-craft-projects/">fleece and felt projects</a>.'),
    ("tote", "3. T-shirt tote bag", "cozy-craft-flatlay", "15 minutes · Easy · Upcycle",
     "Turn an old T-shirt into a washable shopping bag. The fringe knotted along the bottom closes the bag — no sewing at all.",
     ["An old T-shirt (thicker cotton is sturdier)", "Sharp scissors", "A bowl to trace the neckline", "Washable marker"],
     ["Turn the shirt inside out and lay it flat.", "Cut off both sleeves just inside the seam — these become the handles.", "Trace a bowl around the neckline and cut it out to make the bag opening.",
      "Cut 3\"-deep fringe strips, 1\" wide, through both layers along the bottom hem.", "Knot each front strip to the back strip below it, then knot neighboring pairs together to close the gaps.", "Turn the bag right side out so the knots are hidden inside."],
     'Want more ways to use old clothes? See <a href="/upcycle-old-jeans/">17 ways to upcycle old jeans</a>.'),
    ("bins", "4. Fabric-wrapped storage bins", "felt-fabric-stack", "45 minutes · Easy · Organization",
     "Cardboard delivery boxes become pretty, matching shelf storage with fabric and a little Mod Podge or spray adhesive.",
     ["Sturdy cardboard box", "Fabric (fat quarter for a small box, ½ yd for a large one)", "Mod Podge or spray adhesive and a foam brush", "Scissors and a craft knife"],
     ["Cut the flaps off the box (or fold them inside for extra strength).", "Cut fabric to wrap around the box with 2\" extra at the top and bottom.", "Brush adhesive on one side at a time and smooth the fabric on, working out bubbles.",
      "Fold the bottom fabric under like wrapping a gift and glue it down.", "Fold the top 2\" over the rim and glue it to the inside.", "Line the bottom with a cardboard insert covered in matching fabric."],
     'Pair your new bins with our guide to <a href="/organize-fabric-stash/">organizing a fabric stash</a>.'),
]


def four_page(c):
    pic, esc = c["pic"], c["esc"]
    path = "/4no-sew-diy-fabric-projects/"
    crumbs, crumb_ld = c["breadcrumbs"]([("Home", "/"), ("DIY Projects", "/category/diy-projects/"), ("4 No-Sew DIY Fabric Projects", path)])
    jump = "".join(f'<a class="tool-card reveal" href="#{k}"><h3>{esc(t)}</h3><p>{esc(m)}</p><span class="go">Jump to tutorial ↓</span></a>' for k, t, _, m, *_ in FOUR)
    secs = ""
    howtos = []
    for k, t, img, meta, intro, sup, steps, tip in FOUR:
        sl = "".join(f"<li>{esc(s)}</li>" for s in sup)
        st = "".join(f"<li>{esc(s)}</li>" for s in steps)
        secs += f'''<h2 id="{k}">{esc(t)}</h2>
<p class="eyebrow">{esc(meta)}</p>
<figure>{pic(img, t.split(". ", 1)[1])}</figure>
<p>{esc(intro)}</p>
<h3>You'll need</h3><ul class="supplies">{sl}</ul>
<h3>Steps</h3><ol class="steps">{st}</ol>
<p class="steps-hint">Tap each step to tick it off — progress saves on this device.</p>
<div class="tip"><p>{tip}</p></div>'''
        howtos.append({"@context": "https://schema.org", "@type": "HowTo", "name": t.split(". ", 1)[1],
                       "supply": [{"@type": "HowToSupply", "name": s} for s in sup],
                       "step": [{"@type": "HowToStep", "position": i, "text": s} for i, s in enumerate(steps, 1)],
                       "image": c["SITE"] + c["img_url"](img)})
    body = f'''<section class="page-hero">
  <div class="wrap">
    {crumbs}
    <span class="eyebrow">Weekend tutorials</span>
    <h1 class="reveal">4 No-Sew DIY Fabric Projects You Can Finish This Weekend</h1>
    <p class="lead reveal d1" style="max-width:760px">Four genuinely useful no-sew fabric projects, each explained step by step: a cozy fleece tie blanket, a knotted pillow cover, a T-shirt tote bag and fabric-wrapped storage bins. All you need is fabric, scissors and an afternoon.</p>
    <div class="post-meta reveal d2"><span>By the Kotric Team</span><span>Updated {c["fmt_date"](c["BUILD_DATE"])}</span><span>10 min read</span></div>
  </div>
</section>
<section class="section" style="padding-top:10px"><div class="wrap"><div class="tool-grid">{jump}</div></div></section>
<section class="section" style="padding-top:0">
  <div class="wrap article-layout">
    <article class="prose">
      <p>These four projects were chosen because they're useful every day, use inexpensive materials and teach the main no-sew techniques: <strong>knotting</strong>, <strong>wrapping</strong> and <strong>gluing</strong>. Once you've made them, you'll be ready for any of our <a href="/no-sew-fabric-craft-projects/">41 no-sew fabric projects</a>.</p>
      {secs}
      <h2 id="next">What to make next</h2>
      <p>Loved working without a needle? Browse the full list of <a href="/no-sew-fabric-craft-projects/">41 amazing no-sew DIY fabric projects</a>, try our <a href="/fabric-scrap-projects/">fabric scrap ideas</a>, or learn a few <a href="/hand-sewing-stitches-for-beginners/">basic hand stitches</a> to open up even more projects.</p>
    </article>
    <aside>
      <nav class="toc" aria-label="On this page"><h4>Tutorials</h4><ol>{"".join(f'<li><a href="#{k}">{esc(t.split(". ", 1)[1])}</a></li>' for k, t, *_ in FOUR)}<li><a href="#next">What to make next</a></li></ol></nav>
      <div class="side-card"><h4>Which bond should I use?</h4><p>Glue, fusible web, hem tape or knots — find out in four questions.</p><a class="btn btn-primary" href="/tools/no-sew-method-quiz/">Take the quiz</a></div>
    </aside>
  </div>
</section>'''
    art = {"@context": "https://schema.org", "@type": "Article", "headline": "4 No-Sew DIY Fabric Projects You Can Finish This Weekend",
           "image": c["SITE"] + c["img_url"]("folded-blankets"), "dateModified": c["BUILD_DATE"], "datePublished": "2023-01-10",
           "author": {"@type": "Organization", "name": "The Kotric Team"}, "publisher": c["ORG"], "mainEntityOfPage": c["SITE"] + path}
    return c["page"](path, "4 No-Sew DIY Fabric Projects: Easy Step-by-Step Tutorials | Kotric",
                     "Four easy no-sew DIY fabric projects with step-by-step instructions: a fleece tie blanket, knotted pillow cover, T-shirt tote bag and fabric-wrapped storage bins.",
                     body, [art, crumb_ld] + howtos, og_img="folded-blankets", og_type="article", progress=True)


def blog_index(c):
    crumbs, crumb_ld = c["breadcrumbs"]([("Home", "/"), ("Blog", "/blog/")])
    chips = '<button type="button" class="chip" data-v="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" class="chip" data-v="{s}" aria-pressed="false">{v[0]}</button>' for s, v in c["CATEGORIES"].items())
    cards = "".join(c["post_card"](p) for p in c["posts"])
    body = f'''<section class="page-hero"><div class="wrap">{crumbs}<span class="eyebrow">The Kotric blog</span><h1>Fabric Craft &amp; Sewing Blog</h1>
<p class="lead" style="max-width:680px">Tutorials, project ideas, sewing tips and organizing guides — written for real people with real scrap bins.</p></div></section>
<section class="section" style="padding-top:10px"><div class="wrap">
<div class="filter-bar chips" id="blog-filter" role="group" aria-label="Filter by category">{chips}</div>
<div class="post-grid">
<a class="post-card reveal" href="/no-sew-fabric-craft-projects/" data-cat="fabric-crafts"><div class="pic">{c["pic"]("colorful-fabrics", "Colorful fabrics")}<span class="tag">Fabric Crafts</span></div><div class="body"><h3>41 Amazing No-Sew DIY Fabric Projects</h3><p>Our most popular guide — blankets, bags, gifts and décor without a stitch.</p><div class="meta"><span>12 min read</span></div></div></a>
<a class="post-card reveal" href="/4no-sew-diy-fabric-projects/" data-cat="diy-projects"><div class="pic">{c["pic"]("home-cushions", "Handmade cushions on a sofa")}<span class="tag">DIY Projects</span></div><div class="body"><h3>4 No-Sew DIY Fabric Projects for the Weekend</h3><p>Step-by-step tutorials with tick-off checklists.</p><div class="meta"><span>10 min read</span></div></div></a>
{cards}</div></div></section>'''
    return c["page"]("/blog/", "Fabric Craft, DIY & Sewing Blog | Kotric",
                     "Fabric craft tutorials, no-sew DIY projects, beginner sewing guides and organizing tips from the Kotric blog.",
                     body, [crumb_ld], og_img="thread-bobbins")


def category(c, slug):
    name, blurb, img = c["CATEGORIES"][slug]
    path = f"/category/{slug}/"
    crumbs, crumb_ld = c["breadcrumbs"]([("Home", "/"), ("Blog", "/blog/"), (name, path)])
    ps = [p for p in c["posts"] if p["cat"] == slug]
    extra = ""
    if slug == "fabric-crafts":
        extra = f'<a class="post-card feature reveal" href="/no-sew-fabric-craft-projects/"><div class="pic">{c["pic"]("colorful-fabrics", "Colorful fabrics")}<span class="tag">Reader favorite</span></div><div class="body"><h3>41 Amazing No-Sew DIY Fabric Projects</h3><p>Blankets, pillow covers, bags, gifts and décor made with knots, glue and fusible web.</p><div class="meta"><span>12 min read</span></div></div></a>'
    if slug == "diy-projects":
        extra = f'<a class="post-card feature reveal" href="/4no-sew-diy-fabric-projects/"><div class="pic">{c["pic"]("home-cushions", "Handmade cushions")}<span class="tag">Step by step</span></div><div class="body"><h3>4 No-Sew DIY Fabric Projects You Can Finish This Weekend</h3><p>Fleece blanket, knotted pillow, T-shirt tote and fabric-wrapped bins.</p><div class="meta"><span>10 min read</span></div></div></a>'
    cards = "".join(c["post_card"](p) for p in ps)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs}<span class="eyebrow">Category</span><h1>{name}</h1><p class="lead" style="max-width:640px">{blurb}</p>
<div class="hero-img">{c["pic"](img, name, eager=True)}</div></div></section>
<section class="section" style="padding-top:10px"><div class="wrap"><div class="post-grid">{extra}{cards}</div></div></section>'''
    return c["page"](path, f"{name}: Tutorials & Ideas | Kotric", f"{blurb} Browse every {name.lower()} article on Kotric.", body, [crumb_ld], og_img=img)


def simple(c, path, title, seo, desc, inner, img=None):
    crumbs, crumb_ld = c["breadcrumbs"]([("Home", "/"), (title, path)])
    hero = f'<div class="hero-img">{c["pic"](img, title, eager=True)}</div>' if img else ""
    body = f'''<section class="page-hero"><div class="wrap">{crumbs}<h1>{title}</h1>{hero}</div></section>
<section class="section" style="padding-top:10px"><div class="wrap"><div class="prose" style="margin:0 auto">{inner}</div></div></section>'''
    return c["page"](path, seo, desc, body, [crumb_ld], og_img=img or "sewing-machine-orange-felt")


def about(c):
    inner = f'''<p class="lead">Kotric is an independent craft blog about <strong>fabric crafts, DIY projects and sewing</strong>. We believe anyone can make something useful and beautiful with fabric — with or without a sewing machine.</p>
<h2 id="what-we-cover">What we cover</h2>
<ul><li><strong>No-sew fabric crafts</strong> — projects made with knots, fabric glue and fusible web, like our <a href="/no-sew-fabric-craft-projects/">41 no-sew DIY fabric projects</a>.</li>
<li><strong>DIY projects</strong> for the home, kids and gifts.</li>
<li><strong>Sewing tutorials</strong> and hacks for beginners.</li>
<li><strong>Organization</strong> — taming the fabric stash and setting up a craft space that works.</li></ul>
<h2 id="how-we-write">How we write our guides</h2>
<p>Every tutorial is written to be followed, not just admired. We list materials and realistic times, explain <em>why</em> a step matters, and point out the mistakes we've made ourselves. When we recommend a technique — like using a denim needle or prewashing flannel — it's because it works.</p>
<h2 id="tools">Free tools</h2>
<p>We built a set of <a href="/tools/">free craft tools</a> to answer the questions we kept asking ourselves: how much fabric do I need, how big should this fleece blanket be, and what is 1.5 cm in inches?</p>
<h2 id="say-hello">Say hello</h2>
<p>Questions, corrections, project photos or collaboration ideas are always welcome. Email us at <a href="mailto:{c["EMAIL"]}">{c["EMAIL"]}</a> or use the <a href="/contact/">contact form</a>.</p>'''
    return simple(c, "/about/", "About Kotric", "About Kotric | Fabric Crafts, DIY Projects & Sewing",
                  "Kotric is an independent blog sharing easy fabric crafts, no-sew DIY projects, sewing tutorials, organizing tips and free craft tools.", inner, "spools-on-wood")


def contact(c):
    path = "/contact/"
    crumbs, crumb_ld = c["breadcrumbs"]([("Home", "/"), ("Contact", path)])
    body = f'''<section class="page-hero"><div class="wrap">{crumbs}<span class="eyebrow">Get in touch</span><h1>Contact Kotric</h1>
<p class="lead" style="max-width:640px">Have a question about a project, a craft you'd like us to cover, or a photo of something you made? We'd love to hear from you.</p></div></section>
<section class="section" style="padding-top:10px"><div class="wrap split" style="align-items:start">
<div class="calc" style="grid-template-columns:1fr">
<form class="form" id="contact-form" action="/contact.php" method="post">
  <div class="field-row"><div class="field"><label for="cf-name">Name</label><input id="cf-name" name="name" required autocomplete="name"></div>
  <div class="field"><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" required autocomplete="email"></div></div>
  <div class="field"><label for="cf-topic">Topic</label><select id="cf-topic" name="topic"><option>Project question</option><option>Article suggestion</option><option>Share my project</option><option>Correction</option><option>Collaboration</option><option>Something else</option></select></div>
  <div class="field"><label for="cf-msg">Message</label><textarea id="cf-msg" name="message" required></textarea></div>
  <div class="hp" aria-hidden="true"><label for="cf-web">Website</label><input id="cf-web" name="website" tabindex="-1" autocomplete="off"></div>
  <button class="btn btn-primary" type="submit">Send message</button>
  <div class="notice" id="contact-note" role="status"></div>
</form></div>
<div><h2>Prefer email?</h2><p>Write to us directly at <a href="mailto:{c["EMAIL"]}"><strong>{c["EMAIL"]}</strong></a>. We read every message and usually reply within two working days.</p>
<ul class="checklist"><li>Include a photo if you're asking about a project</li><li>Tell us which article you're following</li><li>We can't offer paid sewing or alteration services</li></ul>
<figure style="margin:24px 0 0">{c["pic"]("thread-bobbins", "Colorful thread bobbins")}</figure></div>
</div></section>'''
    return c["page"](path, "Contact Kotric | Email info@kotric.com", "Contact the Kotric team with project questions, article ideas or photos of your makes. Email info@kotric.com.",
                     body, [crumb_ld], og_img="thread-bobbins")


def legal(c):
    e = c["EMAIL"]
    privacy = f'''<p><em>Last updated: {c["fmt_date"](c["BUILD_DATE"])}</em></p>
<p>This policy explains what information kotric.com ("Kotric", "we") collects and how we use it.</p>
<h2 id="info">Information we collect</h2>
<ul><li><strong>Messages you send us.</strong> If you use the contact form or email us, we receive your name, email address and message, and use them only to reply.</li>
<li><strong>Server logs.</strong> Our host automatically records standard technical data such as IP address, browser type and pages requested, for security and performance.</li>
<li><strong>Data stored on your device.</strong> Our interactive features (for example, the "I made this" checkboxes and tutorial step checklists) save your progress in your browser's local storage. This data never leaves your device and you can clear it at any time in your browser settings.</li></ul>
<h2 id="cookies">Cookies</h2>
<p>Kotric does not set advertising or tracking cookies. Fonts are loaded from Google Fonts, which may log your IP address as described in Google's privacy policy.</p>
<h2 id="sharing">Sharing</h2><p>We do not sell or rent personal information. We share it only where required by law.</p>
<h2 id="rights">Your rights</h2><p>You can ask us to access, correct or delete personal information you've sent us by emailing <a href="mailto:{e}">{e}</a>.</p>
<h2 id="children">Children</h2><p>Kotric is intended for a general audience and does not knowingly collect information from children under 13.</p>
<h2 id="changes">Changes</h2><p>We may update this policy from time to time; the date above shows the latest revision.</p>'''
    terms = f'''<p><em>Last updated: {c["fmt_date"](c["BUILD_DATE"])}</em></p>
<h2 id="use">Use of this site</h2><p>The content on kotric.com is provided for personal, non-commercial use. You may share links to our pages and make the projects for yourself or as gifts.</p>
<h2 id="content">Content</h2><p>Text, graphics and tools on this site are owned by Kotric unless otherwise stated. Please don't republish full articles without permission; a short quote with a link back is welcome.</p>
<h2 id="safety">Safety</h2><p>Crafting involves sharp tools, hot irons and glue guns. Follow manufacturer instructions, supervise children and use your own judgment. Projects for babies and pets should be checked for loose parts and used under supervision.</p>
<h2 id="tools">Calculators</h2><p>Our calculators give estimates. Always check measurements against your pattern and buy a little extra fabric.</p>
<h2 id="liability">Limitation of liability</h2><p>Kotric is not liable for any loss or damage arising from the use of this site or its content.</p>
<h2 id="contact">Contact</h2><p>Questions about these terms: <a href="mailto:{e}">{e}</a>.</p>'''
    disclaimer = f'''<p>The information on Kotric is for general educational and entertainment purposes. We test our methods and write them carefully, but results vary with materials, tools and skill.</p>
<h2 id="products">Product mentions</h2><p>When we mention a type of product (for example fabric glue or fusible web), it's because we find it useful. If we ever include affiliate links, they will be clearly disclosed on the page, and they never change what we recommend.</p>
<h2 id="safety">Safety</h2><p>Always follow the safety instructions for irons, glue guns, blades and adhesives. Do not use small parts, ribbons or loose fringe in items intended for unsupervised infants.</p>
<h2 id="contact">Questions</h2><p>Email <a href="mailto:{e}">{e}</a>.</p>'''
    yield "/privacy-policy/", simple(c, "/privacy-policy/", "Privacy Policy", "Privacy Policy | Kotric", "How Kotric collects, uses and protects your information.", privacy), "0.2"
    yield "/terms-of-use/", simple(c, "/terms-of-use/", "Terms of Use", "Terms of Use | Kotric", "The terms for using kotric.com, its content and free craft tools.", terms), "0.2"
    yield "/disclaimer/", simple(c, "/disclaimer/", "Disclaimer", "Disclaimer | Kotric", "Kotric's content, product-mention and safety disclaimer.", disclaimer), "0.2"


def sitemap_page(c):
    li = lambda items: "".join(f'<li><a href="{u}">{c["esc"](t)}</a></li>' for u, t in items)
    main = [("/", "Home"), ("/no-sew-fabric-craft-projects/", "41 Amazing No-Sew DIY Fabric Projects"), ("/4no-sew-diy-fabric-projects/", "4 No-Sew DIY Fabric Projects"),
            ("/blog/", "Blog"), ("/tools/", "Craft Tools"), ("/about/", "About"), ("/contact/", "Contact")]
    cats = [(f"/category/{s}/", v[0]) for s, v in c["CATEGORIES"].items()]
    posts = [(f'/{p["slug"]}/', p["title"]) for p in c["posts"]]
    tools = [(f'/tools/{t["slug"]}/', t["title"]) for t in TOOLS]
    legal_l = [("/privacy-policy/", "Privacy Policy"), ("/terms-of-use/", "Terms of Use"), ("/disclaimer/", "Disclaimer")]
    inner = f'<h2 id="pages">Pages</h2><ul>{li(main)}</ul><h2 id="categories">Categories</h2><ul>{li(cats)}</ul><h2 id="articles">Articles</h2><ul>{li(posts)}</ul><h2 id="tools">Tools</h2><ul>{li(tools)}</ul><h2 id="legal">Legal</h2><ul>{li(legal_l)}</ul>'
    return simple(c, "/sitemap/", "Sitemap", "Sitemap | Kotric", "Every page on Kotric: projects, articles, categories and free craft tools.", inner)


def not_found(c):
    body = f'''<section class="page-hero" style="padding:80px 0"><div class="wrap center"><span class="eyebrow">Error 404</span><h1>Oops — this page came unstitched.</h1>
<p class="lead" style="max-width:560px;margin:0 auto 28px">The page you're looking for has moved or no longer exists. Try one of these instead:</p>
<p><a class="btn btn-primary" href="/no-sew-fabric-craft-projects/">41 no-sew projects</a> <a class="btn btn-ghost" href="/blog/">Browse the blog</a></p></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="post-grid">{"".join(c["post_card"](p) for p in c["posts"][:3])}</div></div></section>'''
    return c["page"]("/404.html", "Page Not Found | Kotric", "This page could not be found.", body, robots="noindex, follow")


def build_pages(c):
    yield "/", home(c), "1.0"
    yield "/no-sew-fabric-craft-projects/", projects_page(c), "0.9"
    yield "/4no-sew-diy-fabric-projects/", four_page(c), "0.9"
    yield "/blog/", blog_index(c), "0.8"
    for s in c["CATEGORIES"]:
        yield f"/category/{s}/", category(c, s), "0.6"
    yield "/about/", about(c), "0.5"
    yield "/contact/", contact(c), "0.5"
    yield from legal(c)
    yield "/sitemap/", sitemap_page(c), "0.3"
    yield "/404.html", not_found(c), None
