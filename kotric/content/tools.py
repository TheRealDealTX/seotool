"""Interactive craft tools. The logic lives in assets/js/site.js."""

ICONS = {
    "ruler": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4z"/><path d="m7.5 10.5 2 2M10.5 7.5l2 2M13.5 4.5l2 2M4.5 13.5l2 2"/></svg>',
    "blanket": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="5" width="14" height="14" rx="1"/><path d="M5 9H2M5 13H2M5 17H2M19 9h3M19 13h3M19 17h3M9 5V2M13 5V2M9 22v-3M13 22v-3"/></svg>',
    "swap": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4 3 8l4 4"/><path d="M3 8h14"/><path d="m17 20 4-4-4-4"/><path d="M21 16H7"/></svg>',
    "quiz": '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg>',
}

TOOLS = [
    {"slug": "fabric-yardage-calculator", "short": "Fabric Yardage Calculator", "icon": "ruler",
     "title": "Fabric Yardage Calculator",
     "seo": "Fabric Yardage Calculator: How Much Fabric to Buy",
     "desc": "Free fabric yardage calculator: enter piece size, quantity, seam allowance and bolt width to see how many yards or meters to buy, with a cutting layout.",
     "blurb": "Find out exactly how much fabric to buy for any number of pieces, with a live cutting layout."},
    {"slug": "fleece-tie-blanket-calculator", "short": "Fleece Blanket Calculator", "icon": "blanket",
     "title": "Fleece Tie Blanket Calculator",
     "seo": "Fleece Tie Blanket Calculator: Size & Yardage",
     "desc": "How much fleece you need for a no-sew tie blanket in baby, lap, throw, twin or custom sizes, plus cut sizes, corner squares and number of knots.",
     "blurb": "Fleece yardage, cut size, corner squares and knot count for any tie blanket."},
    {"slug": "sewing-unit-converter", "short": "Sewing Unit Converter", "icon": "swap",
     "title": "Sewing Unit Converter",
     "seo": "Sewing Converter: cm to Inches & Fractions | Kotric",
     "desc": "Convert sewing measurements between inches, fractions, centimeters, millimeters, yards and meters — and see the nearest standard seam allowance.",
     "blurb": "Convert cm, mm, yards and meters to inches with sewing-friendly fractions."},
    {"slug": "no-sew-method-quiz", "short": "No-Sew Method Quiz", "icon": "quiz",
     "title": "Which No-Sew Method Should I Use?",
     "seo": "No-Sew Method Quiz: Glue, Fusible Web or Knots?",
     "desc": "Answer four quick questions and find the best no-sew way to join fabric for your project: fabric glue, fusible web, hem tape, hot glue or knots.",
     "blurb": "Four questions to find the right bond: glue, fusible web, hem tape or knots."},
]


def tool_card(t, cls="tool-card reveal"):
    return (f'<a class="{cls}" href="/tools/{t["slug"]}/"><span class="ico">{ICONS[t["icon"]]}</span>'
            f'<h3>{t["short"]}</h3><p>{t["blurb"]}</p><span class="go">Open tool →</span></a>')


def _yardage():
    return '''<div class="calc reveal" id="yardage-calc">
  <div class="fields">
    <div class="seg" role="group" aria-label="Units"><button type="button" data-u="in" aria-pressed="true">Inches</button><button type="button" data-u="cm" aria-pressed="false">Centimeters</button></div>
    <div class="field-row">
      <div class="field"><label for="y-w">Piece width (<span class="u">in</span>)</label><input id="y-w" type="number" min="0" step="0.25" value="18" inputmode="decimal"></div>
      <div class="field"><label for="y-l">Piece length (<span class="u">in</span>)</label><input id="y-l" type="number" min="0" step="0.25" value="18" inputmode="decimal"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="y-q">How many pieces?</label><input id="y-q" type="number" min="1" step="1" value="4" inputmode="numeric"></div>
      <div class="field"><label for="y-sa">Seam allowance (<span class="u">in</span>)</label><input id="y-sa" type="number" min="0" step="0.125" value="0.5" inputmode="decimal"><div class="hint">Added to every side.</div></div>
    </div>
    <div class="field"><label for="y-fw">Fabric width</label>
      <select id="y-fw"><option value="44">44–45" (quilting cotton)</option><option value="54">54" (home décor, some linen)</option><option value="60">58–60" (fleece, knits, apparel)</option><option value="108">108" (wide backing)</option></select></div>
    <div class="field"><label for="y-sh">Allow for shrinkage</label>
      <select id="y-sh"><option value="0">None (polyester, fleece, prewashed)</option><option value="3" selected>3% (most cottons)</option><option value="5">5% (linen, denim)</option><option value="8">8% (flannel, rayon)</option></select></div>
  </div>
  <div class="result" id="y-out" aria-live="polite"></div>
</div>'''


def _tie():
    return '''<div class="calc reveal" id="tie-calc">
  <div class="fields">
    <div class="field"><label for="t-size">Blanket size</label>
      <select id="t-size"><option value="baby">Baby — 36" × 36"</option><option value="lap">Lap — 45" × 55"</option><option value="throw" selected>Throw — 50" × 60"</option><option value="twin">Twin — 60" × 84"</option><option value="custom">Custom size…</option></select></div>
    <div class="field-row" id="t-custom">
      <div class="field"><label for="t-w">Finished width (in)</label><input id="t-w" type="number" min="10" value="50" inputmode="decimal"></div>
      <div class="field"><label for="t-l">Finished length (in)</label><input id="t-l" type="number" min="10" value="60" inputmode="decimal"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="t-f">Fringe length (in)</label><input id="t-f" type="number" min="2" max="8" step="0.5" value="4" inputmode="decimal"><div class="hint">4" is classic; 3" for baby blankets.</div></div>
      <div class="field"><label for="t-s">Fringe strip width (in)</label><input id="t-s" type="number" min="0.5" max="3" step="0.25" value="1" inputmode="decimal"></div>
    </div>
  </div>
  <div class="result" id="t-out" aria-live="polite"></div>
</div>'''


def _unit():
    return '''<div class="calc reveal" id="unit-calc">
  <div class="fields">
    <div class="field"><label for="u-v">Measurement</label><input id="u-v" type="number" step="any" value="1.5" inputmode="decimal"></div>
    <div class="field"><label for="u-from">Unit</label>
      <select id="u-from"><option value="cm" selected>Centimeters (cm)</option><option value="mm">Millimeters (mm)</option><option value="in">Inches (in)</option><option value="ft">Feet (ft)</option><option value="yd">Yards (yd)</option><option value="m">Meters (m)</option></select></div>
    <p class="hint" style="font-size:.9rem;color:var(--muted)">Results round to the nearest ⅛", the smallest mark on most sewing rulers.</p>
  </div>
  <div class="result" id="u-out" aria-live="polite"></div>
</div>'''


def _quiz():
    q = [
        ("Will the finished project be washed?", [("Yes, often", "glue:2,fuse:2,knot:2"), ("Occasionally", "glue:2,fuse:1,tape:1,knot:1"), ("Never — it's décor", "hot:3,glue:1")]),
        ("What fabric are you using?", [("Fleece or T-shirt jersey", "knot:4"), ("Cotton or linen", "glue:2,fuse:2,tape:1"), ("Felt", "glue:2,hot:2"), ("Heavy: denim, canvas, upholstery", "glue:2,tape:2")]),
        ("What are you joining?", [("A hem or straight edge", "tape:3,glue:1"), ("A shape or appliqué on top of fabric", "fuse:3,glue:1"), ("Two whole layers together", "knot:2,fuse:1,glue:1"), ("Fabric to another material (wood, glass, a frame)", "hot:3")]),
        ("What matters most?", [("Speed", "hot:2,tape:1"), ("Soft and flexible", "knot:2,glue:1"), ("A crisp, flat finish", "fuse:2,tape:1"), ("Maximum strength", "glue:2,knot:1")]),
    ]
    res = {
        "glue": ("Permanent fabric glue", "Flexible and washable once cured. Apply a thin bead, press and weigh down, and wait 24–72 hours before washing."),
        "fuse": ("Fusible web", "Paper-backed fusible web gives crisp, flat appliqué and bonded layers. Press — don't slide — the iron, using a pressing cloth."),
        "tape": ("Iron-on hem tape", "The fastest way to hem curtains, trousers and straight edges. Choose a heavy-duty tape for thick fabrics."),
        "hot": ("Hot glue", "Instant and strong on décor that never gets washed: wreaths, frames, wrapped jars and headbands."),
        "knot": ("Knots and ties", "Fleece and jersey don't fray, so cut fringe and knot the layers. Soft, washable and endlessly sturdy."),
    }
    steps = ""
    for i, (question, opts) in enumerate(q):
        o = "".join(f'<button type="button" class="opt" data-s="{s}">{t}</button>' for t, s in opts)
        steps += f'<div class="qstep"><p class="eyebrow">Question {i + 1} of {len(q)}</p><h3>{question}</h3><div class="opts">{o}</div></div>'
    out = "".join(f'<div class="qres" data-r="{k}"><p class="eyebrow">Your best match</p><h3>{n}</h3><p>{d}</p></div>' for k, (n, d) in res.items())
    steps += (f'<div class="qstep">{out}<p>Read the full comparison in <a href="/fabric-glue-vs-fusible-web/">fabric glue vs fusible web vs hem tape</a>, '
              f'or put it to work with the <a href="/no-sew-fabric-craft-projects/">41 no-sew projects</a>.</p>'
              f'<button type="button" class="btn btn-ghost q-again">Take it again</button></div>')
    return f'<div class="quiz reveal" id="nosew-quiz"><div class="qbar"><i></i></div>{steps}</div>'


GUIDES = {
    "fabric-yardage-calculator": ("How the calculator works", """
<p>The calculator adds your seam allowance to every side of each piece, then works out how many pieces fit across the usable width of the fabric (the bolt width minus about an inch for selvedges). It tries the pieces both ways round and picks the layout that uses the least length, then rounds up to the nearest ⅛ yard — the smallest cut most fabric stores will make.</p>
<h3>Tips for buying fabric</h3>
<ul><li>Directional prints and plaids need extra for matching — add 10–15%.</li><li>Buy everything for a project from the same bolt; dye lots vary.</li><li>Add shrinkage if you'll <a href="/how-to-prewash-fabric/">prewash</a> natural fibers.</li><li>Pattern pieces that are cut "on the fold" count as one piece twice as wide.</li></ul>
<h3>Common yardages</h3>
<table><thead><tr><th>Project</th><th>Typical fabric</th></tr></thead><tbody><tr><td>18" pillow cover (envelope back)</td><td>⅝ yd of 44" fabric</td></tr><tr><td>Simple tote bag</td><td>¾ yd outer + ¾ yd lining</td></tr><tr><td>Set of 4 napkins (18")</td><td>1 ¼ yd of 44" fabric</td></tr><tr><td>Apron</td><td>1 yd</td></tr><tr><td>Throw quilt backing (50" × 65")</td><td>3 ¾ yd of 44" or 1 ⅞ yd of 108"</td></tr></tbody></table>"""),
    "fleece-tie-blanket-calculator": ("How to use your numbers", """
<p>Fleece is 58–60" wide, so any blanket wider than about 50" with 4" fringe on both sides needs to be cut with the length running across the bolt, or pieced. Buy the same length of each fleece for the top and backing layers.</p>
<p>Follow the full <a href="/how-to-make-a-no-sew-fleece-blanket/">no-sew fleece blanket tutorial</a> for cutting and knotting, or see blanket #1 in our <a href="/4no-sew-diy-fabric-projects/">four weekend no-sew projects</a>.</p>
<h3>Fringe tips</h3><ul><li>Cut through both layers at once so the strips line up.</li><li>Shorter fringe (3") suits baby blankets and is quicker to tie.</li><li>Narrower strips look neater but mean more knots.</li></ul>"""),
    "sewing-unit-converter": ("Seam allowances at a glance", """
<table><thead><tr><th>Seam allowance</th><th>Metric</th><th>Used for</th></tr></thead><tbody>
<tr><td>¼"</td><td>6 mm</td><td>Quilting, patchwork</td></tr><tr><td>⅜"</td><td>1 cm</td><td>Many indie and European garment patterns</td></tr>
<tr><td>½"</td><td>1.3 cm</td><td>Bags, home décor, many tutorials</td></tr><tr><td>⅝"</td><td>1.5 cm</td><td>Big 4 commercial garment patterns</td></tr></tbody></table>
<p>Need to know how much fabric that pattern takes? Try the <a href="/tools/fabric-yardage-calculator/">fabric yardage calculator</a>.</p>"""),
    "no-sew-method-quiz": ("The five no-sew methods", """
<p>Every no-sew project relies on one of five ways to join fabric: permanent fabric glue, fusible web, iron-on hem tape, hot glue, or knots and ties. Each suits a different fabric and use — our <a href="/fabric-glue-vs-fusible-web/">full comparison</a> explains strength, washability and flexibility side by side.</p>"""),
}


def build_tools(ctx):
    page, crumbs_fn, esc = ctx["page"], ctx["breadcrumbs"], ctx["esc"]
    SITE = ctx["SITE"]
    widgets = {"fabric-yardage-calculator": _yardage, "fleece-tie-blanket-calculator": _tie,
               "sewing-unit-converter": _unit, "no-sew-method-quiz": _quiz}
    # Hub
    crumbs, crumb_ld = crumbs_fn([("Home", "/"), ("Craft Tools", "/tools/")])
    cards = "".join(tool_card(t) for t in TOOLS)
    body = f'''<section class="page-hero"><div class="wrap">{crumbs}<span class="eyebrow">Free &amp; interactive</span><h1>Craft &amp; Sewing Tools</h1>
<p class="lead" style="max-width:640px">Skip the mental math. These free tools work out fabric yardage, fleece blanket sizes and sewing conversions, and help you pick the right no-sew method — right in your browser.</p></div></section>
<section class="section" style="padding-top:10px"><div class="wrap"><div class="tool-grid">{cards}</div></div></section>'''
    yield "/tools/", page("/tools/", "Free Sewing & Fabric Craft Calculators | Kotric",
                          "Free interactive sewing tools: fabric yardage calculator, fleece tie blanket calculator, sewing unit converter and a no-sew method quiz.",
                          body, [crumb_ld], og_img="scissors-and-thread")
    for t in TOOLS:
        path = f'/tools/{t["slug"]}/'
        crumbs, crumb_ld = crumbs_fn([("Home", "/"), ("Craft Tools", "/tools/"), (t["title"], path)])
        gh, gb = GUIDES[t["slug"]]
        others = "".join(tool_card(o) for o in TOOLS if o is not t)
        body = f'''<section class="page-hero"><div class="wrap">{crumbs}<span class="eyebrow">Free tool</span><h1>{esc(t["title"])}</h1>
<p class="lead" style="max-width:680px">{esc(t["desc"])}</p></div></section>
<section class="section" style="padding-top:10px"><div class="wrap">{widgets[t["slug"]]()}</div></section>
<section class="section section-alt"><div class="wrap"><div class="prose" style="margin:0 auto"><h2 id="guide">{gh}</h2>{gb}</div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><span class="eyebrow">More tools</span><h2>Other free craft tools</h2></div><div class="tool-grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">{others}</div></div></section>'''
        app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"], "url": SITE + path,
                  "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "description": t["desc"],
                  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        yield path, page(path, t["seo"], t["desc"], body, [app_ld, crumb_ld], og_img="scissors-and-thread")
