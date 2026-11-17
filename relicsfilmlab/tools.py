"""Shopper tools (/tools/*) and the Film & Batteries shop page (/collections/film).

All tools run client-side (src/tools.js) on data written to /assets/tools-data.json.
"""
import json, os, re, html
import catalog, content as C, prices as PR

# ---------------------------------------------------------------- film shop data
# (name, amazon query, format, iso, kind, looks, light, blurb, brand colour)
FILM_SHOP = [
    ("Kodak Gold 200", "Kodak Gold 200 35mm film", "35mm", 200, "colour", ["warm", "nostalgic"], ["bright"], "Warm, golden, forgiving — the classic sunny-day film.", "kodak"),
    ("Kodak UltraMax 400", "Kodak UltraMax 400 35mm film", "35mm", 400, "colour", ["warm", "punchy"], ["bright", "mixed"], "Affordable all-rounder that suits point-and-shoots.", "kodak"),
    ("Kodak Portra 400", "Kodak Portra 400 35mm film", "35mm", 400, "colour", ["natural", "portrait"], ["bright", "mixed"], "Beautiful skin tones and huge latitude; the wedding favourite.", "kodak"),
    ("Kodak Ektar 100", "Kodak Ektar 100 35mm", "35mm", 100, "colour", ["punchy", "landscape"], ["bright"], "The finest-grain colour negative; saturated landscapes.", "kodak"),
    ("CineStill 800T", "CineStill 800T 35mm", "35mm", 800, "colour", ["cinematic", "night"], ["low"], "Tungsten cinema film with glowing halation around lights.", "cinestill"),
    ("Ilford HP5 Plus 400", "Ilford HP5 Plus 35mm film", "35mm", 400, "bw", ["classic", "grainy"], ["bright", "mixed", "low"], "Flexible black & white that pushes to 1600 with ease.", "ilford"),
    ("Kodak Tri-X 400", "Kodak Tri-X 400 35mm film", "35mm", 400, "bw", ["classic", "contrast"], ["bright", "mixed", "low"], "The legendary photojournalism stock — gritty and contrasty.", "kodak"),
    ("Kodak Portra 400 (120)", "Kodak Portra 400 120 film", "120", 400, "colour", ["natural", "portrait"], ["bright", "mixed"], "Portra's famous tones on a big medium-format negative.", "kodak"),
    ("Kodak Ektar 100 (120)", "Kodak Ektar 100 120 film", "120", 100, "colour", ["punchy", "landscape"], ["bright"], "Ultra-fine grain colour for landscapes in 120.", "kodak"),
    ("Ilford HP5 Plus (120)", "Ilford HP5 Plus 120 film", "120", 400, "bw", ["classic", "grainy"], ["bright", "mixed", "low"], "Go-to black & white for TLRs and medium-format SLRs.", "ilford"),
    ("Polaroid 600 Color", "Polaroid 600 color film", "instant-600", 640, "colour", ["dreamy", "nostalgic"], ["bright", "mixed"], "For every 600-series Polaroid; battery built into the pack.", "polaroid"),
    ("Polaroid 600 B&W", "Polaroid 600 black and white film", "instant-600", 640, "bw", ["classic", "dreamy"], ["bright", "mixed"], "Monochrome instant prints for 600 cameras.", "polaroid"),
    ("Polaroid SX-70 Color", "Polaroid SX-70 color film", "instant-sx70", 160, "colour", ["dreamy", "nostalgic"], ["bright"], "Made for SX-70, OneStep Land and Pronto cameras.", "polaroid"),
    ("Polaroid SX-70 B&W", "Polaroid SX-70 black and white film", "instant-sx70", 160, "bw", ["classic", "dreamy"], ["bright"], "Black & white for SX-70-type cameras.", "polaroid"),
    ("Instax Wide (twin pack)", "Fujifilm Instax Wide film twin pack", "instant-wide", 800, "colour", ["natural"], ["bright", "mixed", "low"], "Crisp credit-card-wide prints for Instax Wide cameras.", "fuji"),
    ("Instax Wide Monochrome", "Instax Wide monochrome film", "instant-wide", 800, "bw", ["classic"], ["bright", "mixed", "low"], "Black & white Instax Wide.", "fuji"),
    ("Kodak Vision3 50D Super 8", "Kodak Vision3 50D Super 8 film", "super8", 50, "colour", ["cinematic", "natural"], ["bright"], "Daylight cinema stock with the finest grain.", "kodak"),
    ("Kodak Vision3 200T Super 8", "Kodak Vision3 200T Super 8 film", "super8", 200, "colour", ["cinematic", "natural"], ["mixed", "bright"], "The all-rounder; meters correctly in most vintage cameras.", "kodak"),
    ("Kodak Vision3 500T Super 8", "Kodak Vision3 500T Super 8", "super8", 500, "colour", ["cinematic", "night"], ["low", "mixed"], "Fast tungsten stock for receptions and night scenes.", "kodak"),
    ("Kodak Tri-X Super 8", "Kodak Tri-X Super 8 film", "super8", 200, "bw", ["classic", "contrast"], ["bright", "mixed"], "Black & white reversal — projects straight away.", "kodak"),
    ("Lomography 110 Color", "Lomography 110 color film", "110", 200, "colour", ["punchy", "nostalgic"], ["bright"], "Fresh film for 110 pocket cameras.", "lomo"),
    ("Kodak FunSaver (disposable)", "Kodak FunSaver disposable camera", "disposable", 800, "colour", ["warm", "punchy"], ["bright", "mixed"], "Single-use camera with flash, 27 exposures.", "kodak"),
    ("Fujifilm QuickSnap (disposable)", "Fujifilm QuickSnap disposable camera", "disposable", 400, "colour", ["natural"], ["bright", "mixed"], "Cooler-toned single-use camera with flash.", "fuji"),
    ("Ilford XP2 (disposable)", "Ilford XP2 single use camera", "disposable", 400, "bw", ["classic"], ["bright", "mixed"], "Black & white disposable any colour lab can develop.", "ilford"),
]
BATTERY_SHOP = [("LR44 / SR44", "LR44 batteries", "Most 1970s–80s SLR light meters (Pentax K1000, Nikon FM/FE, Minolta X-700)"),
                ("CR123A", "CR123A lithium batteries", "Many 1990s compacts (Olympus Stylus Epic, Contax T2)"),
                ("CR2", "CR2 lithium battery", "Compacts and autofocus SLRs (Contax T3, EOS Rebel XS)"),
                ("4LR44 / PX28 6V", "4LR44 6V battery", "Canon A-series SLRs (AE-1, AE-1 Program, A-1, AT-1)"),
                ("2CR5", "2CR5 lithium battery", "Early autofocus SLRs (original Canon EOS Rebel)"),
                ("PX625 / MR9 adapter", "PX625 battery adapter MR9", "1960s–70s meters designed for mercury cells (Canonet, Minolta SRT)")]
FORMAT_LABEL = {"35mm": "35mm film", "120": "120 medium format", "instant-600": "Polaroid 600", "instant-sx70": "Polaroid SX-70", "instant-wide": "Instax Wide",
                "super8": "Super 8", "110": "110 film", "disposable": "Disposable cameras"}

TOOLS = [
    ("camera-finder", "Film Camera Finder", "Which film camera should I buy? Answer four questions and get matched cameras you can buy today.", "Camera finder quiz"),
    ("exposure-calculator", "Exposure Calculator", "Sunny 16 and EV exposure calculator for film: get the right shutter speed and aperture for any light.", "Exposure calculator"),
    ("film-stock-finder", "Film Stock Finder", "Find the right film for your camera, light and look — 35mm, 120, Polaroid, Instax and Super 8.", "Film stock finder"),
    ("battery-finder", "Film Camera Battery Finder", "Look up which battery your film camera takes, with buy links for every type.", "Battery finder"),
    ("cost-per-shot-calculator", "Film Cost per Shot Calculator", "How much does each film photo cost? Compare 35mm, half-frame, 120, Polaroid, Instax and Super 8.", "Cost per shot"),
    ("depth-of-field-calculator", "Depth of Field Calculator", "Depth of field and hyperfocal distance calculator for 35mm, half-frame and medium format film cameras.", "Depth of field"),
    ("super-8-calculator", "Super 8 Runtime Calculator", "How long is a Super 8 cartridge? Work out runtime and how many cartridges you need.", "Super 8 calculator"),
]

def camera_traits(p):
    s = (p["spec"] + " " + p["name"]).lower()
    t = []
    if "autofocus" in s or "fixed focus" in s or "focus free" in s or p["cat"] == "instant": t.append("auto")
    if any(k in s for k in ("manual", "mechanical", "match-needle")) or (p["cat"] in ("slr", "mf") and "autofocus" not in s): t.append("manual")
    if any(k in s for k in ("aperture-priority", "shutter-priority", "program")): t.append("semi")
    if "zoom" in s: t.append("zoom")
    if re.search(r"f/1\.[0-9]", s): t.append("fast")
    if any(k in s for k in ("weatherproof", "waterproof", "underwater")): t.append("weather")
    if "selenium" in s or "no batteries" in s: t.append("nobatt")
    if p["cat"] in ("ps", "pocket") and "zoom" not in s: t.append("pocket")
    if p["cat"] == "ps" and ("clamshell" in s or "stylus" in s or "xa" in p["slug"]): t.append("pocket")
    if "rangefinder" in s: t.append("rangefinder")
    if "half-frame" in s: t.append("halfframe")
    return sorted(set(t))

def build_data(ctx):
    """JSON for the client-side tools."""
    build = ctx["build"]
    cams = []
    for i, p in enumerate(sorted(ctx["PRODUCTS"], key=ctx["rank_of"])):
        if p["cat"] not in ("ps", "slr", "instant", "mf", "movie", "pocket"):
            continue
        slug = p["slug"]
        exact = slug in build.SLUG_ASIN
        sim = build.SIMILAR.get(slug) if not exact else None
        a = (f"https://www.amazon.com/dp/{build.SLUG_ASIN[slug]['asin']}?tag={C.AMZ_TAG}" if exact else
             f"https://www.amazon.com/dp/{sim['asin']}?tag={C.AMZ_TAG}" if sim else build.amz(build.amz_query(p)))
        bat = C.BATTERIES.get(slug)
        _pr = PR.price_range(p)
        cams.append(dict(pr=PR.fmt(_pr) if _pr else "", s=slug, n=p["name"], c=p["cat"], sp=p["spec"], y=p["year"], i=ctx["img_path"](slug) or "", r=i, a=a,
                         ax=1 if exact else (2 if sim else 0), t=camera_traits(p),
                         b=("none" if bat == "none" else C.BATTERY_KIT[bat][0] if bat else ""), ba=(build.amz(C.BATTERY_KIT[bat][1]) if bat and bat != "none" else "")))
    films = [dict(n=n, f=f, fl=FORMAT_LABEL[f], iso=iso, k=k, lk=lk, li=li, d=d, br=br, a=build.amz(q), pr=PR.fmt(PR.FILM_PRICES[n]) if n in PR.FILM_PRICES else "", i=film_img(n) or "") for n, q, f, iso, k, lk, li, d, br in FILM_SHOP]
    bats = [dict(n=n, d=d, a=build.amz(q)) for n, q, d in BATTERY_SHOP]
    out = os.path.join(build.PUB, "assets", "tools-data.json")
    json.dump(dict(cams=cams, films=films, bats=bats), open(out, "w"), separators=(",", ":"))

FILM_IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "assets", "img", "film")

def film_key(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def film_img(name):
    k = film_key(name)
    return f"/assets/img/film/{k}.webp" if os.path.exists(os.path.join(FILM_IMG_DIR, k + ".webp")) else None

def film_card(f, amz_link, esc):
    n, q, fmt, iso, kind, looks, light, blurb, br = f
    im = film_img(n)
    box_cls = "fcard__box fcard__box--img" if im else "fcard__box"
    img_tag = f'<img src="{im}" alt="{esc(n)}" loading="lazy" width="400" height="400">' if im else ""
    return (f'<article class="fcard fcard--{br} reveal"><div class="{box_cls}">{img_tag}<span class="fcard__iso">{iso}</span><span class="fcard__fmt">{esc(FORMAT_LABEL[fmt])}</span>'
            f'<span class="fcard__name">{esc(n)}</span></div><div class="fcard__body"><p>{esc(blurb)}</p>'
            f'<div class="fcard__tags">' + "".join(f"<span>{esc(t)}</span>" for t in ([("B&W" if kind == "bw" else "Colour")] + looks[:2])) + "</div>"
            + (f'<div class="fcard__price">{PR.fmt(PR.FILM_PRICES[n])}<small>typical price</small></div>' if n in PR.FILM_PRICES else "")
            + amz_link("Buy on Amazon →", q, "btn btn--sm") + "</div></article>")

def build_film_page(ctx):
    write, crumbs, phero, site_img, esc, amz_link, faq_html, grid, P = (ctx[k] for k in ("write", "crumbs", "phero", "site_img", "esc", "amz_link", "faq_html", "grid", "PRODUCTS"))
    groups = [("35mm film", "35mm"), ("120 medium format film", "120"), ("Instant film", "instant"), ("Super 8 film", "super8"), ("110 film", "110"), ("Disposable cameras", "disposable")]
    secs = ""
    for title, key in groups:
        items = [f for f in FILM_SHOP if f[2] == key or f[2].startswith(key + "-")]
        secs += f'<section class="fshelf" id="{key}"><div class="head-row"><h2>{title}</h2></div><div class="fgrid">' + "".join(film_card(f, amz_link, esc) for f in items) + "</div></section>"
    def _bbox(n):
        im = film_img(n)
        return (f'<div class="fcard__box fcard__box--img"><img src="{im}" alt="{esc(n)} battery" loading="lazy" width="400" height="400">' if im else '<div class="fcard__box">')
    bats = "".join(f'<article class="fcard fcard--battery reveal">{_bbox(n)}<span class="fcard__fmt">Battery</span><span class="fcard__name">{esc(n)}</span></div>'
                   f'<div class="fcard__body"><p>{esc(d)}</p>' + (f'<div class="fcard__price">{PR.fmt(PR.FILM_PRICES[n])}<small>typical price</small></div>' if n in PR.FILM_PRICES else "") + f'{amz_link("Buy on Amazon →", q, "btn btn--sm")}</div></article>' for n, q, d in BATTERY_SHOP)
    secs += f'<section class="fshelf" id="batteries"><div class="head-row"><h2>Camera batteries</h2><a class="btn btn--ghost btn--sm" href="/tools/battery-finder">Which battery does my camera take?</a></div><div class="fgrid">{bats}</div></section>'
    jump = "".join(f'<a class="chip" href="#{k}">{t}</a>' for t, k in groups + [("Batteries", "batteries")])
    cr_h, cr_ld = crumbs([("/collections/all", "Shop"), (None, "Film &amp; Batteries")])
    fh, fld = faq_html([("What film should I buy first?", "Kodak Gold 200 for sunny days or Kodak UltraMax 400 for everything else — both are affordable and forgiving. For black & white, Ilford HP5 Plus."),
                        ("Which film does my Polaroid take?", "600-series cameras (Sun 600, OneStep 600, Impulse) take Polaroid 600 film; SX-70, OneStep Land and Pronto cameras take SX-70 film. Instax Wide cameras take Instax Wide film."),
                        ("How should I store film?", "Keep it cool and dry — the fridge is ideal. Let it warm to room temperature for an hour before loading."),
                        ("Not sure which film suits your shoot?", 'Try our <a href="/tools/film-stock-finder">film stock finder</a>.')])
    body = (phero("Film &amp; <em>batteries</em>", "Fresh film for every camera we sell — 35mm, 120, Polaroid, Instax, Super 8 and 110 — plus the batteries vintage cameras need. Every card links straight to the product on Amazon.", cr_h, site_img("film-rolls"))
            + f'<section class="section" style="padding-top:36px"><div class="wrap"><div class="toolbar">{jump}</div>{secs}'
            + f'<div class="prose mt"><h2>FAQ</h2>{fh}</div></div></section>')
    write("/collections/film", "Buy Film Online — 35mm, 120, Polaroid, Instax & Super 8 Film", "Shop film for vintage cameras: Kodak Portra, Gold, Ektar, Ilford HP5, CineStill, Polaroid 600 & SX-70, Instax Wide, Kodak Vision3 Super 8, 110 film and camera batteries.",
          body, schema=[cr_ld, fld], preload=site_img("film-rolls"))

# ---------------------------------------------------------------- tool pages
WIDGETS = {
"camera-finder": """
<form class="tool quiz" id="quiz">
 <fieldset><legend>1. What will you mostly shoot?</legend><div class="opts">
  <label><input type="radio" name="use" value="everyday" checked><span>Everyday &amp; travel</span></label>
  <label><input type="radio" name="use" value="party"><span>Parties &amp; events</span></label>
  <label><input type="radio" name="use" value="learn"><span>Learning photography</span></label>
  <label><input type="radio" name="use" value="quality"><span>Portraits &amp; landscapes</span></label>
  <label><input type="radio" name="use" value="movie"><span>Home movies</span></label></div></fieldset>
 <fieldset><legend>2. How hands-on do you want to be?</legend><div class="opts">
  <label><input type="radio" name="ctl" value="auto" checked><span>Point and shoot — fully automatic</span></label>
  <label><input type="radio" name="ctl" value="semi"><span>Some control</span></label>
  <label><input type="radio" name="ctl" value="manual"><span>Full manual</span></label></div></fieldset>
 <fieldset><legend>3. Which kind of photos?</legend><div class="opts">
  <label><input type="radio" name="fmt" value="any" checked><span>No preference</span></label>
  <label><input type="radio" name="fmt" value="35"><span>35mm negatives</span></label>
  <label><input type="radio" name="fmt" value="instant"><span>Instant prints</span></label>
  <label><input type="radio" name="fmt" value="mf"><span>Medium format (120)</span></label></div></fieldset>
 <fieldset><legend>4. Nice to have</legend><div class="opts">
  <label><input type="checkbox" name="want" value="pocket"><span>Fits in a pocket</span></label>
  <label><input type="checkbox" name="want" value="zoom"><span>Zoom lens</span></label>
  <label><input type="checkbox" name="want" value="fast"><span>Low-light lens</span></label>
  <label><input type="checkbox" name="want" value="weather"><span>Weatherproof</span></label>
  <label><input type="checkbox" name="want" value="nobatt"><span>No batteries needed</span></label></div></fieldset>
 <button class="btn" type="submit">Show my matches →</button>
</form>
<div id="quiz-out" class="tool-out" aria-live="polite"></div>""",
"exposure-calculator": """
<div class="tool calc" id="expo">
 <div class="row3">
  <label>Film speed (ISO)<select id="ex-iso"><option>25</option><option>50</option><option>100</option><option>160</option><option selected>200</option><option>400</option><option>800</option><option>1600</option><option>3200</option></select></label>
  <label>Light<select id="ex-ev">
   <option value="16">Bright sun on snow or sand</option><option value="15" selected>Bright sun, distinct shadows</option><option value="14">Hazy sun, soft shadows</option>
   <option value="13">Overcast, light</option><option value="12">Heavy overcast / open shade</option><option value="11">Sunset, golden hour</option>
   <option value="9">Just after sunset / bright interior</option><option value="8">Well-lit indoors</option><option value="7">Home interior at night</option>
   <option value="5">Night street lighting</option><option value="4">Candlelight</option></select></label>
  <label>Your aperture<select id="ex-f"><option>1.4</option><option>2</option><option>2.8</option><option>4</option><option>5.6</option><option selected>8</option><option>11</option><option>16</option><option>22</option></select></label>
 </div>
 <div class="result"><span>Use a shutter speed of</span><b id="ex-out">—</b><small id="ex-ev-out"></small></div>
 <h3>Equivalent exposures</h3><div class="pairs" id="ex-pairs"></div>
</div>""",
"film-stock-finder": """
<form class="tool quiz" id="fsf">
 <fieldset><legend>Your camera takes…</legend><div class="opts">
  <label><input type="radio" name="f" value="35mm" checked><span>35mm</span></label><label><input type="radio" name="f" value="120"><span>120</span></label>
  <label><input type="radio" name="f" value="instant-600"><span>Polaroid 600</span></label><label><input type="radio" name="f" value="instant-sx70"><span>Polaroid SX-70</span></label>
  <label><input type="radio" name="f" value="instant-wide"><span>Instax Wide</span></label><label><input type="radio" name="f" value="super8"><span>Super 8</span></label>
  <label><input type="radio" name="f" value="110"><span>110</span></label></div></fieldset>
 <fieldset><legend>Light you'll shoot in</legend><div class="opts">
  <label><input type="radio" name="li" value="bright" checked><span>Bright daylight</span></label><label><input type="radio" name="li" value="mixed"><span>A bit of everything</span></label>
  <label><input type="radio" name="li" value="low"><span>Indoors &amp; night</span></label></div></fieldset>
 <fieldset><legend>The look you want</legend><div class="opts">
  <label><input type="radio" name="lk" value="warm" checked><span>Warm &amp; nostalgic</span></label><label><input type="radio" name="lk" value="natural"><span>Natural skin tones</span></label>
  <label><input type="radio" name="lk" value="punchy"><span>Bold &amp; saturated</span></label><label><input type="radio" name="lk" value="cinematic"><span>Cinematic</span></label>
  <label><input type="radio" name="lk" value="bw"><span>Black &amp; white</span></label></div></fieldset>
</form>
<div id="fsf-out" class="tool-out" aria-live="polite"></div>""",
"battery-finder": """
<div class="tool" id="bat">
 <label class="bigsearch">Your camera<input id="bat-q" type="search" placeholder="e.g. Canon AE-1, Pentax K1000, Olympus Stylus…" autocomplete="off"></label>
 <div id="bat-out" class="tool-out" aria-live="polite"></div>
 <h3>Common film camera batteries</h3><div id="bat-all" class="batlist"></div>
</div>""",
"cost-per-shot-calculator": """
<div class="tool calc" id="cps">
 <div class="row3">
  <label>Format<select id="cps-fmt">
   <option value="36|14|15">35mm · 36 exposures</option><option value="24|10|15">35mm · 24 exposures</option><option value="72|14|18">Half-frame · 72 exposures</option>
   <option value="15|13|18">120 · 6×4.5 (15 shots)</option><option value="12|13|18">120 · 6×6 (12 shots)</option><option value="10|13|18">120 · 6×7 (10 shots)</option>
   <option value="8|21|0">Polaroid · 8 shots</option><option value="10|14|0">Instax Wide · 10 shots</option><option value="27|16|14">Disposable · 27 shots</option></select></label>
  <label>Film price per roll/pack ($)<input id="cps-film" type="number" min="0" step="0.5" value="14"></label>
  <label>Develop + scan per roll ($)<input id="cps-dev" type="number" min="0" step="0.5" value="15"></label>
 </div>
 <div class="result"><span>Each photo costs about</span><b id="cps-out">—</b><small id="cps-roll"></small></div>
 <p class="muted small">Prices are editable estimates — check the live price of your film on Amazon. Instant film needs no developing.</p>
 <div id="cps-shop"></div>
</div>""",
"depth-of-field-calculator": """
<div class="tool calc" id="dof">
 <div class="row3">
  <label>Format<select id="dof-fmt"><option value="0.03" selected>35mm</option><option value="0.02">Half-frame</option><option value="0.047">6×4.5</option><option value="0.053">6×6</option><option value="0.059">6×7</option></select></label>
  <label>Focal length (mm)<input id="dof-fl" type="number" min="8" max="600" value="50"></label>
  <label>Aperture (f/)<select id="dof-n"><option>1.4</option><option>1.8</option><option>2</option><option>2.8</option><option>4</option><option>5.6</option><option selected>8</option><option>11</option><option>16</option><option>22</option></select></label>
  <label>Subject distance<input id="dof-d" type="number" min="0.3" step="0.1" value="3"></label>
  <label>Units<select id="dof-u"><option value="m">metres</option><option value="ft">feet</option></select></label>
 </div>
 <div class="result result--grid"><div><span>Near limit</span><b id="dof-near">—</b></div><div><span>Far limit</span><b id="dof-far">—</b></div><div><span>Total depth</span><b id="dof-tot">—</b></div><div><span>Hyperfocal</span><b id="dof-h">—</b></div></div>
 <div class="dofbar"><i id="dof-bar"></i><em id="dof-subj"></em></div>
</div>""",
"super-8-calculator": """
<div class="tool calc" id="s8">
 <div class="row3">
  <label>Frame rate<select id="s8-fps"><option value="18">18 fps</option><option value="24" selected>24 fps</option></select></label>
  <label>Cartridges (50 ft)<input id="s8-n" type="number" min="1" max="100" value="3"></label>
  <label>…or minutes you need<input id="s8-min" type="number" min="0" step="0.5" placeholder="e.g. 10"></label>
 </div>
 <div class="result result--grid"><div><span>Runtime</span><b id="s8-run">—</b></div><div><span>Per cartridge</span><b id="s8-per">—</b></div><div><span>Cartridges needed</span><b id="s8-need">—</b></div></div>
 <div id="s8-shop"></div>
</div>""",
}

PROSE = {
"camera-finder": ("""<h2>How the camera finder works</h2><p>We score every camera in our catalogue against your answers — what you shoot, how much control you want, the format and the features you care about — then favour cameras that people search for most and that are actually available on Amazon right now. Each result links to our full buying guide and straight to the listing.</p>
<h3>Quick advice</h3><ul><li><strong>Total beginner?</strong> A good compact like the <a href="/products/olympus-stylus">Olympus Stylus Epic</a> or <a href="/products/olympus-trip-35">Trip 35</a> gets you great results with zero settings.</li><li><strong>Want to learn?</strong> A manual SLR such as the <a href="/products/pentax-k-1000-with-50mm-lens-1">Pentax K1000</a> or <a href="/products/canon-ae-1">Canon AE-1</a> teaches exposure properly.</li><li><strong>Want prints in your hand?</strong> Go <a href="/collections/polaroid-cameras">instant</a>.</li></ul>""",
  [("What is the best film camera for beginners?", "For fully automatic shooting, a quality 35mm point-and-shoot such as the Olympus Stylus Epic. To learn manual exposure, a simple SLR like the Pentax K1000 or Canon AE-1 Program."),
   ("Are vintage film cameras reliable?", "Well-made models from Canon, Nikon, Olympus, Minolta and Pentax often work perfectly decades later. Check the light seals, shutter and lens when your camera arrives — every product page lists what to inspect.")]),
"exposure-calculator": ("""<h2>How to use the exposure calculator</h2><p>Pick your film speed, the light you're in and the aperture you want. The calculator works out the shutter speed using exposure value (EV), then lists every equivalent aperture/shutter pair so you can trade depth of field for motion blur.</p>
<h3>The Sunny 16 rule</h3><p>In bright sun, at f/16, use a shutter speed of 1 / your ISO. With ISO 400 film that's f/16 at 1/500 (or 1/400). Every step darker on the light scale opens up one stop: f/11 for hazy sun, f/8 for overcast, f/5.6 for heavy overcast, f/4 for open shade.</p>
<h3>Tips</h3><ul><li>Colour negative film forgives over-exposure — when in doubt, give it more light.</li><li>Slide film and instant film need accurate exposure.</li><li>Below 1/30 s, use a tripod or brace yourself.</li></ul>""",
  [("What is the Sunny 16 rule?", "On a sunny day, set the aperture to f/16 and the shutter speed to the reciprocal of your film speed — e.g. 1/100 s for ISO 100 film."),
   ("Do I need a light meter for film?", "Many vintage cameras have a built-in meter. If yours doesn't (or the meter is dead), this calculator, the Sunny 16 rule or a phone light-meter app will get you close; a handheld meter is the most accurate.")]),
"film-stock-finder": ("""<h2>Choosing film</h2><p>Three things decide which film to load: your camera's format, how much light you'll have, and the look you're after. Faster film (higher ISO) copes with dim light but shows more grain; slower film is finer and more saturated but needs bright conditions.</p>
<table><tr><th>ISO</th><th>Best for</th></tr><tr><td>50–100</td><td>Bright sun, landscapes, tripod work</td></tr><tr><td>200</td><td>Sunny days, holidays</td></tr><tr><td>400</td><td>The all-rounder — indoors and out</td></tr><tr><td>800+</td><td>Night, concerts, interiors</td></tr></table>""",
  [("What film speed should I buy?", "ISO 400 is the safest all-rounder. Choose 100–200 for bright sunny days and 800 or higher for indoors and night."),
   ("Colour or black & white?", "Colour negative is the easiest to get developed anywhere. Black & white is cheap to develop at home and very forgiving.")]),
"battery-finder": ("""<h2>Film camera batteries explained</h2><p>Most vintage SLRs only need a battery for the light meter — the shutter works without it. Many 1990s point-and-shoots need a lithium battery for everything. Here are the common types:</p><ul>
<li><strong>LR44 / SR44</strong> — tiny button cells for 1970s–80s SLR meters. Silver-oxide (SR44) gives the most stable readings.</li><li><strong>4LR44 / PX28</strong> — the 6V stack used by Canon's A-series SLRs.</li>
<li><strong>CR123A and CR2</strong> — lithium cells for 90s compacts and autofocus SLRs.</li><li><strong>PX625 mercury cells</strong> — discontinued; use an MR9 adapter or a 1.35V zinc-air cell.</li></ul>""",
  [("Does my film camera work without a battery?", "Fully mechanical cameras (Pentax K1000, Nikon FM, Canon FTb) fire at every shutter speed without one — only the meter needs power. Electronic cameras and most compacts won't work at all without a battery."),
   ("Why is my camera dead with a new battery?", "Clean the battery contacts with a pencil eraser or isopropyl alcohol — corrosion is the most common culprit.")]),
"cost-per-shot-calculator": ("""<h2>What does film photography really cost?</h2><p>The cost of a film photo is the price of the roll plus developing and scanning, divided by the number of shots. Half-frame cameras halve your cost per photo; medium format costs more per frame but gives you a far bigger negative; instant film has no lab costs at all.</p>
<h3>Ways to spend less</h3><ul><li>Shoot a <a href="/products/olympus-pen-ee-1961">half-frame camera</a> for 72 shots per roll.</li><li>Develop black & white at home — see our <a href="/blogs/guides/how-to-develop-film-at-home">guide</a>.</li><li>Buy film in multi-packs.</li></ul>""",
  [("How much does a roll of film cost to develop?", "Typically $12–$20 per roll for develop and scan at a US lab, depending on scan resolution."),
   ("What's the cheapest way to shoot film?", "A half-frame 35mm camera with budget colour film, or black & white film you develop yourself.")]),
"depth-of-field-calculator": ("""<h2>Depth of field, explained</h2><p>Depth of field is the zone in front of and behind your subject that looks acceptably sharp. It gets shallower with a wider aperture (smaller f-number), a longer lens and a closer subject — and deeper with the opposite.</p>
<h3>Hyperfocal focusing</h3><p>Focus at the hyperfocal distance and everything from half that distance to infinity is sharp — the classic street-photography trick for zone-focus cameras like the <a href="/products/olympus-xa2-2">Olympus XA2</a> and <a href="/products/olympus-trip-35">Trip 35</a>.</p>""",
  [("What aperture gives the most depth of field?", "The smallest aperture (largest f-number), such as f/16 or f/22, combined with a wide-angle lens."),
   ("Why does medium format have shallower depth of field?", "For the same framing you use a longer lens, which gives less depth of field at the same aperture.")]),
"super-8-calculator": ("""<h2>How long is a Super 8 cartridge?</h2><p>Each Super 8 cartridge holds 50 feet of film — 3,600 frames. At 18 frames per second that's 3 minutes 20 seconds; at 24 fps it's 2 minutes 30 seconds. Shoot 24 fps for a smoother, cinematic look, or 18 fps to stretch your film.</p>
<h3>Planning a shoot</h3><ul><li>Short wedding highlights: 3–4 cartridges.</li><li>Full day coverage: 6–8 cartridges.</li><li>Keep takes to 3–5 seconds — Super 8 rewards short, deliberate shots.</li></ul><p>More in our <a href="/blogs/guides/the-ultimate-guide-to-shooting-super-8-for-weddings-a-relics-film-lab-manual">Super 8 wedding guide</a>.</p>""",
  [("How many minutes is a roll of Super 8?", "About 3 minutes 20 seconds at 18 fps, or 2 minutes 30 seconds at 24 fps."),
   ("Which Super 8 film should I buy?", "Kodak Vision3 200T is the best all-rounder; 50D for bright daylight and 500T for low light.")]),
}

def build_tools(ctx):
    write, crumbs, phero, site_img, esc, faq_html, build = (ctx[k] for k in ("write", "crumbs", "phero", "site_img", "esc", "faq_html", "build"))
    build_data(ctx)
    ICONS = {"camera-finder": "◎", "exposure-calculator": "☀", "film-stock-finder": "▤", "battery-finder": "⚡", "cost-per-shot-calculator": "$",
             "depth-of-field-calculator": "↔", "super-8-calculator": "▶"}
    cards = "".join(f'<a class="toolcard reveal" href="/tools/{s}"><span class="toolcard__ico">{ICONS[s]}</span><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="card__cta">Open tool →</span></a>' for s, t, d, _ in TOOLS)
    cr_h, cr_ld = crumbs([(None, "Tools")])
    write("/tools", "Free Film Photography Tools & Calculators", "Free film photography tools: camera finder quiz, exposure calculator, film stock finder, battery finder, cost-per-shot, depth of field and Super 8 calculators.",
          phero("Film <em>tools</em>", "Free calculators and finders that help you choose, load and shoot the right camera and film.", cr_h, site_img("hero2"))
          + f'<section class="section" style="padding-top:40px"><div class="wrap"><div class="toolgrid">{cards}</div></div></section>', schema=[cr_ld], preload=site_img("hero2"))
    for slug, title, desc, short in TOOLS:
        path = "/tools/" + slug
        cr_h, cr_ld = crumbs([("/tools", "Tools"), (None, esc(title))])
        prose, faqs = PROSE[slug]
        fh, fld = faq_html(faqs)
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": title, "description": desc, "applicationCategory": "PhotographyApplication",
               "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": build.SITE + path}
        others = "".join(f'<a class="chip" href="/tools/{s}">{esc(sh)}</a>' for s, t, d, sh in TOOLS if s != slug)
        body = (phero(esc(title).replace(" ", " ", 1), esc(desc), cr_h)
                + f'<section class="section" style="padding-top:36px"><div class="wrap"><div class="toolwrap">{WIDGETS[slug]}</div>'
                + f'<div class="prose mt">{prose}<h2>FAQ</h2>{fh}</div><div class="mt"><div class="eyebrow">More tools</div><div class="toolbar">{others}</div></div></div></section>')
        write(path, title, desc, body, schema=[cr_ld, fld, app], scripts=["/assets/tools.js"])
