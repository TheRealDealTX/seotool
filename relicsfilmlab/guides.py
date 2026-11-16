"""Long-form guides at /blogs/guides/<slug> (old Shopify blog URLs kept)."""
import re, html
import content as C

def P(slug):  # product link
    return f"/products/{slug}"

ARTICLES = {
"pentax-k1000-review-35mm-camera": lambda a: f"""
<p class="lede">The Asahi Pentax K1000 was introduced in 1976 and made, almost unchanged, until 1997. It has no autofocus, no auto exposure and no program modes — and that is exactly why generations of photography teachers put it in students' hands.</p>
<h2>Pentax K1000 at a glance</h2>
<table><tr><th>Type</th><td>35mm manual-focus SLR</td></tr><tr><th>Lens mount</th><td>Pentax K (bayonet)</td></tr><tr><th>Shutter</th><td>Mechanical cloth focal-plane, 1 s – 1/1000 s + B</td></tr><tr><th>Flash sync</th><td>1/60 s</td></tr><tr><th>Metering</th><td>Centre-weighted match-needle CdS meter</td></tr><tr><th>Battery</th><td>One LR44/SR44 — for the meter only</td></tr><tr><th>Made</th><td>1976–1997 (Japan, later Hong Kong and China)</td></tr></table>
<h2>What the K1000 does brilliantly</h2>
<ul><li><strong>It works without a battery.</strong> The shutter is entirely mechanical; the battery only powers the light meter. Run it flat in the mountains and you can keep shooting with the Sunny 16 rule.</li>
<li><strong>It teaches exposure.</strong> A needle in the viewfinder tells you to open up or stop down. You set aperture and shutter speed yourself, so every frame is a small lesson.</li>
<li><strong>K-mount lenses are everywhere.</strong> The SMC Pentax-M 50mm f/1.7 and f/2 are cheap and excellent, and decades of third-party K-mount lenses fit.</li>
<li><strong>It is built like a tank.</strong> A metal body, few electronics, and a simple layout mean there is not much to break.</li></ul>
<h2>The quirks</h2>
<ul><li>No depth-of-field preview, no self-timer and no mirror lock-up.</li><li>The meter is always on when the lens cap is off — keep the cap on in your bag to save the battery.</li><li>Later Chinese-made bodies have more plastic parts than the early Asahi versions.</li></ul>
<h2>Pentax K1000 photos: what to expect</h2><p>The K1000 doesn't have a "look" of its own — the lens and film do. With a 50mm f/1.7 and a roll of Kodak Portra 400 you'll get warm, natural skin tones; with Ilford HP5 Plus you'll get classic, punchy black &amp; white. The meter is reliable for average scenes, so watch for backlit subjects and snow.</p>
<h2>What to check before buying</h2>
<ol><li>Fire the shutter at 1 s and 1/1000 s: the difference should be obvious.</li><li>Check that the meter needle moves when you point the camera at light and dark areas (with a fresh LR44).</li><li>Look for sticky or crumbling light-seal foam around the back and mirror box.</li><li>Inspect the lens for haze or fungus and make sure the aperture blades are dry and snappy.</li></ol>
<h2>Best film for the Pentax K1000</h2>
<p>Start with a 400-speed film — Kodak UltraMax 400, Portra 400 or Ilford HP5 Plus — for flexibility indoors and out.</p>
<div class="kit" style="max-width:560px">{a("Kodak Portra 400 35mm <span>Amazon →</span>", "Kodak Portra 400 35mm film")}{a("Ilford HP5 Plus 400 <span>Amazon →</span>", "Ilford HP5 Plus 35mm film")}{a("LR44 batteries <span>Amazon →</span>", "LR44 batteries")}{a("SMC Pentax-M 50mm f/1.7 <span>Amazon →</span>", "Pentax-M 50mm f1.7 lens")}</div>
<h2>Verdict: is the Pentax K1000 still worth it?</h2>
<p>Yes — if you want to learn. The K1000 is honest, durable and simple; nothing gets between you and the exposure. If you'd like aperture-priority automation, look at the <a href="{P('pentax-me-super-with-50mm-lens')}">Pentax ME Super</a> or <a href="{P('minolta-x-700-mps-with-50mm-lens')}">Minolta X-700</a>; for a similar fully mechanical experience from Nikon, the <a href="{P('nikon-fm-with-50mm-lens')}">Nikon FM</a>.</p>
<p><a class="btn" href="{P('pentax-k-1000-with-50mm-lens-1')}">See the Pentax K1000 →</a></p>""",

"best-disposable-cameras-2026": lambda a: f"""
<p class="lede">Disposable cameras are still the easiest way to put film in a hundred hands at once — at weddings, on holiday, or in a kid's backpack. These are the single-use cameras worth buying in 2026, plus how to get them developed.</p>
<h2>Our picks</h2>
<h3>1. Kodak FunSaver (800 speed, with flash)</h3><p>The classic. 27 exposures of Kodak 800-speed colour film, a reliable flash and the warm, punchy Kodak look. Best all-rounder.</p>
<h3>2. Fujifilm QuickSnap Flash 400</h3><p>Cooler, cleaner colour than the Kodak, with greens and blues that pop. Great for travel and outdoor events.</p>
<h3>3. Ilford XP2 Super single-use</h3><p>Black &amp; white film that develops in standard colour (C-41) chemistry, so any lab can process it. Fantastic for weddings.</p>
<h3>4. Ilford HP5 Plus single-use</h3><p>True black &amp; white with more grit and contrast. Needs a lab that does B&amp;W.</p>
<h3>5. Kodak Ektar H35 (reusable half-frame)</h3><p>Not disposable — but if you'd buy more than three single-use cameras, a cheap reusable camera with a roll of film is better value and less waste.</p>
<div class="kit" style="max-width:560px">{a("Kodak FunSaver disposable <span>Amazon →</span>", "Kodak FunSaver disposable camera")}{a("Fujifilm QuickSnap <span>Amazon →</span>", "Fujifilm QuickSnap disposable camera")}{a("Ilford XP2 single-use <span>Amazon →</span>", "Ilford XP2 single use camera")}{a("Disposable cameras wedding bulk pack <span>Amazon →</span>", "disposable cameras bulk wedding")}</div>
<h2>Tips for better disposable photos</h2><ul><li>Use the flash indoors and in shade — even in daytime.</li><li>Stay at least 4 feet (1.2 m) from your subject; the lens is fixed-focus.</li><li>Wind fully after every shot.</li><li>Avoid leaving cameras in hot cars.</li></ul>
<h2>Where to develop a disposable camera</h2><p>Any C-41 lab can process it — see <a href="/order-now">where to develop film</a>. Some labs ask you to send the whole camera; others want only the film.</p>
<h2>Better than disposable: cheap point-and-shoots</h2><p>A secondhand compact such as the <a href="{P('olympus-trip-35')}">Olympus Trip 35</a> or <a href="{P('canon-sure-shot-owl-date')}">Canon Sure Shot Owl</a> costs about the same as three disposables and gives you a sharper lens and better exposures, roll after roll. Browse our <a href="/collections/point-shoot-cameras">point and shoot collection</a>.</p>""",

"the-ultimate-guide-to-shooting-super-8-for-weddings-a-relics-film-lab-manual": lambda a: f"""
<p class="lede">Nothing captures a wedding like Super 8: the warm colour, the grain, the soft flicker. This is the manual we gave couples and filmmakers who came to the Relics lab — from choosing a camera to getting the footage scanned.</p>
<h2>1. Choose the right camera</h2><p>Look for a camera with an <strong>XL</strong> (existing light) lens and shutter, reliable auto exposure and 24 fps. Our favourites are the <a href="{P('canon-514xl-super-8-camera')}">Canon 514XL</a>, the low-light <a href="{P('canon-310xl-super-8-camera')}">Canon 310XL</a> with its f/1.0 lens, and the <a href="{P('chinon-20-p-xl-direct-sound-super-8-camera')}">Chinon 20P XL</a>. Test it with a cartridge before the big day.</p>
<h2>2. Pick your film</h2><table><tr><th>Film</th><th>Use it for</th></tr><tr><td>Kodak Vision3 50D</td><td>Outdoor ceremonies in daylight — finest grain</td></tr><tr><td>Kodak Vision3 200T</td><td>Indoor and shade, mixed light</td></tr><tr><td>Kodak Vision3 500T</td><td>Receptions, candlelight and dance floors</td></tr><tr><td>Kodak Tri-X</td><td>Timeless black &amp; white</td></tr></table>
<div class="kit" style="max-width:560px">{a("Kodak Vision3 50D Super 8 <span>Amazon →</span>", "Kodak Vision3 50D Super 8 film")}{a("Kodak Vision3 200T Super 8 <span>Amazon →</span>", "Kodak Vision3 200T Super 8 film")}{a("Kodak Vision3 500T Super 8 <span>Amazon →</span>", "Kodak Vision3 500T Super 8")}{a("Video light (LED) <span>Amazon →</span>", "LED video light")}</div>
<h2>3. How many cartridges?</h2><p>A 50ft cartridge runs about 2.5 minutes at 24 fps. For a highlights film plan on 3–4 cartridges for a short ceremony, and 6–8 to cover getting ready, ceremony, portraits and reception.</p>
<h2>4. Shooting technique</h2><ul><li>Hold each shot for 3–5 seconds, then stop — Super 8 rewards short, deliberate takes.</li><li>Move slowly, or keep still and let the couple move through the frame.</li><li>Keep the sun behind or beside you; backlight is beautiful but check your exposure.</li><li>Indoors, add a continuous light or use 500T.</li><li>Label every cartridge as you finish it.</li></ul>
<h2>5. Developing and scanning</h2><p>Vision3 Super 8 is ECN-2 film — send it to a lab that processes and scans Super 8, and ask for a 2K or higher scan with the full frame visible. See our <a href="/products/develop-scan-ecn-2-motion-picture-film">ECN-2 guide</a>.</p>
<h2>Super 8 wedding checklist</h2><ol><li>Camera tested with fresh batteries</li><li>Spare batteries for the camera and meter</li><li>Film cartridges in a cool bag</li><li>A marker for labels</li><li>An LED light for the reception</li></ol>""",

"best-point-and-shoot-film-cameras": lambda a: f"""
<p class="lede">A great point and shoot film camera fits in a pocket, focuses for you and still makes pictures you'll print. After years of selling and repairing them, these are the compacts we recommend — grouped by what you want to spend and how you shoot.</p>
<h2>The best overall: Olympus Stylus Epic (mju-II)</h2><p>A fast, sharp 35mm f/2.8 lens, weather sealing, spot metering and a body the size of a bar of soap. It's the benchmark. <a href="{P('olympus-stylus')}">See the Olympus Stylus Epic →</a></p>
<h2>Best with no batteries: Olympus Trip 35</h2><p>Solar-powered selenium auto exposure, a superb 40mm Zuiko lens and zone focusing. Ten million sold for good reason. <a href="{P('olympus-trip-35')}">See the Olympus Trip 35 →</a></p>
<h2>Best lens for the money: Nikon L35AF</h2><p>Nicknamed the Pikaichi in Japan, its 35mm f/2.8 Nikkor is one of the sharpest compact lenses of the 80s, and it runs on AA batteries. <a href="{P('nikon-l35-af')}">See the Nikon L35AF →</a></p>
<h2>Best low light: Canon AF35ML</h2><p>A 40mm f/1.9 lens — almost unheard of in a compact — makes it a night-time star. <a href="{P('canon-af-35-ml')}">See the Canon AF35ML →</a></p>
<h2>Best zoom: Canon Sure Shot Z115 / Olympus Stylus Epic Zoom 80</h2><p>For travel, a zoom compact covers more situations. The <a href="{P('canon-sure-shot-z-115')}">Canon Z115</a> reaches 115mm; the <a href="{P('olympus-stylus-epic-zoom-80')}">Stylus Epic Zoom 80</a> is smaller and weather-sealed.</p>
<h2>Best budget: Canon Sure Shot Owl, Olympus Infinity Stylus</h2><p>The <a href="{P('canon-sure-shot-owl-date')}">Sure Shot Owl</a>'s huge viewfinder makes it a joy to use, and the <a href="{P('olympus-stylus-35-mm-black')}">original Olympus Stylus</a> is a genuine pocket camera.</p>
<h2>The luxury pick: Contax T2 and T3</h2><p>Titanium bodies and Carl Zeiss Sonnar lenses — the <a href="{P('contax-t2')}">Contax T2</a> and <a href="{P('contax-t3-like-new')}">Contax T3</a> are as good as compacts get, priced accordingly.</p>
<h2>How to choose</h2><table><tr><th>If you want…</th><th>Choose</th></tr><tr><td>The sharpest pictures</td><td>Stylus Epic, Nikon L35AF, Contax T2/T3</td></tr><tr><td>No batteries</td><td>Olympus Trip 35</td></tr><tr><td>Night shots</td><td>Canon AF35ML</td></tr><tr><td>Zoom for travel</td><td>Canon Z115, Stylus Epic Zoom 80</td></tr><tr><td>The cheapest start</td><td>Canon Sure Shot / Olympus Infinity</td></tr></table>
<div class="kit" style="max-width:560px">{a("Kodak UltraMax 400 (point-and-shoot favourite) <span>Amazon →</span>", "Kodak UltraMax 400 35mm")}{a("CR123A batteries <span>Amazon →</span>", "CR123A lithium batteries")}{a("Small padded camera pouch <span>Amazon →</span>", "compact camera case padded")}</div>
<p>Browse every compact we cover in the <a href="/collections/point-shoot-cameras">point and shoot collection</a>.</p>""",

"how-to-develop-film-at-home": lambda a: f"""
<p class="lede">Developing film at home is cheaper than you think, takes about 30 minutes, and is one of the most satisfying things in photography. Here's the method we taught in the Relics black &amp; white workshop.</p>
<h2>What you need</h2><ul><li>A daylight developing tank and reels (Paterson is the standard)</li><li>A changing bag</li><li>A bottle opener (for 35mm cassettes) and scissors</li><li>Developer, stop bath (or water) and fixer</li><li>A thermometer, measuring jugs and a timer</li><li>Wetting agent and film clips</li></ul>
<div class="kit" style="max-width:560px">{a("Paterson tank & reels <span>Amazon →</span>", "Paterson universal developing tank")}{a("Changing bag <span>Amazon →</span>", "film changing bag")}{a("Kodak D-76 developer <span>Amazon →</span>", "Kodak D-76 developer")}{a("Ilford Rapid Fixer <span>Amazon →</span>", "Ilford rapid fixer")}{a("Ilfotol wetting agent <span>Amazon →</span>", "Ilford Ilfotol wetting agent")}{a("C-41 colour kit <span>Amazon →</span>", "C-41 color developing kit")}</div>
<h2>Step-by-step: black &amp; white</h2><ol>
<li><strong>Load the reel in the dark.</strong> In the changing bag, open the cassette, cut off the leader, feed the film onto the reel and put it in the tank. Practise first with a dud roll.</li>
<li><strong>Mix chemistry at 20 °C (68 °F).</strong></li>
<li><strong>Develop.</strong> Pour in developer, start the timer, agitate for the first 30 seconds, then 10 seconds every minute (follow your developer's chart).</li>
<li><strong>Stop.</strong> Pour out developer; add stop bath or water for 1 minute.</li>
<li><strong>Fix.</strong> 5 minutes with agitation. After this the film is light-safe.</li>
<li><strong>Wash.</strong> 5–10 minutes of fresh water changes (the Ilford method uses 5, 10 and 20 inversions).</li>
<li><strong>Dry.</strong> A drop of wetting agent, then hang with a clip at the bottom to stop curling.</li></ol>
<h2>What about colour?</h2><p>C-41 colour kits work the same way but at 38–39 °C, held within about half a degree. A sous-vide stick in a water bath makes this easy.</p>
<h2>Scanning your negatives</h2><p>Use a dedicated scanner, a flatbed with film holders, or a digital camera with a macro lens. See our <a href="/products/scan-only">scanning guide</a>.</p>
<h2>Troubleshooting</h2><table><tr><th>Problem</th><th>Cause</th></tr><tr><td>Clear film, no edge markings</td><td>Fixer before developer, or no developer</td></tr><tr><td>Milky purple tint</td><td>Under-fixed — fix again</td></tr><tr><td>Half-moon marks</td><td>Film was kinked while loading</td></tr><tr><td>Water spots</td><td>Skip the wetting agent? Add it.</td></tr></table>""",

"where-to-develop-110-127-and-old-film": lambda a: f"""
<p class="lede">Found an old roll in a drawer, or shooting a quirky format like 110 or 127? Here's where you can develop it — and how to do it yourself.</p>
<h2>110 film</h2><p>110 is still made (by Lomography) and most mail-in labs that do C-41 will process it. The challenge is scanning: ask the lab whether they scan 110 and at what resolution. At home, 110 loads onto many adjustable reels at the 16mm setting.</p>
<h2>127 film</h2><p>127 is 46mm wide, between 35mm and 120. Labs that hand-process 120 can usually process 127; at home, set an adjustable reel to the 127 width and process it like 120.</p>
<h2>620 film</h2><p>620 is the same film as 120 on a thinner spool, so any 120 lab can process it.</p>
<h2>8mm and Super 8</h2><p>Where can you develop 8mm film? Look for specialist motion-picture labs. Modern Super 8 colour stock (Vision3) is ECN-2; old Kodachrome movie film can only be processed as black &amp; white today.</p>
<h2>Expired and found film</h2><ul><li>Tell the lab the film's approximate age — they can adjust development.</li><li>Very old film is best processed as black &amp; white by a specialist, even if it's colour.</li><li>Kodachrome can no longer be processed in colour.</li></ul>
<h2>Develop it yourself</h2><p>For black &amp; white, a slow developer like HC-110 dilution B or Rodinal stand development handles unknown film well. Read <a href="/blogs/guides/how-to-develop-film-at-home">how to develop film at home</a>.</p>
<div class="kit" style="max-width:560px">{a("Lomography 110 film <span>Amazon →</span>", "Lomography 110 film")}{a("Adjustable developing reels <span>Amazon →</span>", "adjustable film developing reel")}{a("Kodak HC-110 developer <span>Amazon →</span>", "Kodak HC-110 developer")}</div>
<p>Looking for a 110 camera? Try the <a href="{P('pentax-auto-110-film-camera')}">Pentax Auto 110</a> or <a href="{P('minolta-110-zoom-date')}">Minolta 110 Zoom</a>.</p>""",
}

def build_guides(ctx):
    write, crumbs, phero, site_img, img_path, esc, amz_link, SITE, TODAY = (ctx[k] for k in ("write", "crumbs", "phero", "site_img", "img_path", "esc", "amz_link", "SITE", "TODAY"))
    a = lambda label, q: amz_link(label, q, "")
    cards = []
    for g in C.GUIDES:
        path = "/blogs/guides/" + g["slug"]
        img = img_path(g.get("img_product", "")) if g.get("img_product") else None
        img = img or site_img(g.get("img_site", "hero"))
        plain = re.sub("<.*?>", "", html.unescape(g["h1"]))
        cr_h, cr_ld = crumbs([("/blogs/guides", "Guides"), (None, esc(plain))])
        art = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"], "image": SITE + img,
               "datePublished": "2026-01-15", "dateModified": TODAY, "author": {"@type": "Organization", "name": "Relics Film Lab"},
               "publisher": {"@type": "Organization", "name": "Relics Film Lab", "logo": {"@type": "ImageObject", "url": SITE + "/apple-touch-icon.png"}},
               "mainEntityOfPage": SITE + path}
        body = (phero(g["h1"], "", cr_h, img)
                + f'<section class="section" style="padding-top:48px"><div class="wrap"><article class="prose">{ARTICLES[g["slug"]](a)}'
                + '<p class="note">Relics Film Lab earns from qualifying Amazon purchases made through links in this guide.</p></article></div></section>')
        write(path, g["title"], g["desc"], body, schema=[cr_ld, art], preload=img, ogimg=img)
        cards.append(f'<a class="post reveal" href="{path}"><img src="{img}" alt="" loading="lazy"><div><div class="mono muted">Guide</div><h3>{g["h1"]}</h3><p>{esc(g["desc"])}</p></div></a>')
    cr_h, cr_ld = crumbs([(None, "Guides")])
    write("/blogs/guides", "Film Photography Guides & Camera Reviews", "Film photography guides from Relics Film Lab: camera reviews, buying guides, developing at home and shooting Super 8.",
          phero("Film photography <em>guides</em>", "Reviews, buying guides and how-tos from the team behind the Relics film lab.", cr_h, site_img("photographer"))
          + f'<section class="section" style="padding-top:48px"><div class="wrap"><div class="posts">{"".join(cards)}</div></div></section>', schema=[cr_ld])
