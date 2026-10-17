#!/usr/bin/env python3
"""Static build for collinhughesweddings.com. Writes everything into ./public."""
import html, json, os, shutil
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
SRC = os.path.join(ROOT, "src")
SITE = "https://collinhughesweddings.com"
NAME = "Collin Hughes Weddings"
EMAIL = "info@collinhughesweddings.com"
AREA = "Minneapolis & St. Paul, Minnesota"
VER = "4"
GA_ID = "G-3FFZD336L6"
GTAG = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>"""
_DIMS = {}
IMAGES_USED = {}  # page path -> [(name, alt)] for the image sitemap
_CUR = [None]


def dims(name):
    if name not in _DIMS:
        with Image.open(os.path.join(SRC, "img", name + ".webp")) as im:
            _DIMS[name] = im.size
    return _DIMS[name]

NAV = [("/", "Home"), ("/about/", "About"), ("/weddings/", "Weddings"),
       ("/collections/", "Collections"), ("/destination-weddings/", "Destination"),
       ("/contact/", "Contact")]

e = html.escape


def img(name, alt, cls="", w=None, h=None, lazy=True, extra=""):
    a = f' class="{cls}"' if cls else ""
    w, h = dims(name)
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    if _CUR[0] is not None:
        IMAGES_USED.setdefault(_CUR[0], []).append((name, alt))
    return f'<img src="/assets/img/{name}.webp" alt="{e(alt)}"{a} width="{w}" height="{h}"{ld}{extra}>'


def org_schema():
    return {
        "@type": ["ProfessionalService", "LocalBusiness"],
        "@id": SITE + "/#business",
        "name": NAME,
        "url": SITE + "/",
        "email": EMAIL,
        "image": SITE + "/assets/img/hills-couple.webp",
        "description": "Wedding photography studio based in Minneapolis–St. Paul, photographing weddings across Minnesota and destination weddings in the UK and beyond.",
        "address": {"@type": "PostalAddress", "addressLocality": "Minneapolis", "addressRegion": "MN", "addressCountry": "US"},
        "areaServed": ["Minneapolis", "St. Paul", "Minnesota", "Wisconsin", "United Kingdom"],
        "priceRange": "$$$",
        "knowsAbout": ["Wedding photography", "Engagement photography", "Destination wedding photography"],
    }


def page(path, title, desc, body, schema=None, hero_img=None, solid=False, crumbs=None, robots="index,follow",
         og_type="website", og_alt=None, published=None):
    url = SITE + path
    og = SITE + "/assets/og/" + (hero_img or "hills-couple") + ".jpg"
    graph = [org_schema(), {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": NAME,
                            "publisher": {"@id": SITE + "/#business"}}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (p, n) in enumerate(crumbs)]})
    graph.append({"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
                  "isPartOf": {"@id": SITE + "/#site"}, "inLanguage": "en-US",
                  "primaryImageOfPage": {"@type": "ImageObject", "url": og, "width": 1200, "height": 630},
                  **({"breadcrumb": {"@id": url + "#breadcrumb"}} if crumbs else {})})
    graph += schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    og = SITE + "/assets/og/" + (hero_img or "hills-couple") + ".jpg"
    og_alt = og_alt or title
    canon = f'<link rel="canonical" href="{url}">' if robots.startswith("index") else ""
    art = (f'<meta property="article:published_time" content="{published}">'
           f'<meta property="article:author" content="{NAME}">') if published else ""
    links = "".join(
        f'<li><a href="{p}"{" aria-current=\"page\"" if p == path else ""}{" class=\"cta\"" if p == "/contact/" else ""}>{"Inquire" if p == "/contact/" else n}</a></li>'
        for p, n in NAV)
    preload = f'<link rel="preload" as="image" href="/assets/img/{hero_img}.webp">' if hero_img else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GTAG}
<script>document.documentElement.className+=" js"</script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
{canon}
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{og}">
<meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(og_alt)}">{art}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{og}"><meta name="twitter:image:alt" content="{e(og_alt)}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#1f1b18">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="apple-mobile-web-app-title" content="Collin Hughes">
<link rel="preconnect" href="https://www.googletagmanager.com">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&family=Pinyon+Script&display=swap" rel="stylesheet">
{preload}
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<header class="hdr{' solid' if solid else ''}">
 <div class="wrap">
  <a class="logo" href="/" aria-label="{NAME} home"><b>Collin Hughes</b><small>Weddings</small></a>
  <button class="burger" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  <nav class="nav" id="site-nav" aria-label="Main">
   <ul>{links}</ul>
   <div class="nav-foot"><p>Minneapolis–St. Paul &amp; destinations worldwide<br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  </nav>
 </div>
</header>
<main id="main">
{body}
</main>
{footer()}
<button class="totop" type="button" aria-label="Back to top">&uarr;</button>
<script src="/assets/js/site.js?v={VER}" defer></script>
</body>
</html>
"""


def footer():
    return f"""<footer class="ftr">
 <div class="wrap">
  <p class="big-word" aria-hidden="true">forever, honestly.</p>
  <div class="grid">
   <div>
    <a class="logo" href="/"><b>Collin Hughes</b><small>Weddings</small></a>
    <p>Documentary-minded wedding photography for couples who would rather live their day than pose through it. Based in the Twin Cities, travelling wherever love takes us.</p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
   </div>
   <div><p class="fh">Explore</p><ul>
    <li><a href="/about/">About the studio</a></li><li><a href="/weddings/">Real weddings</a></li>
    <li><a href="/collections/">Collections &amp; FAQ</a></li><li><a href="/destination-weddings/">Destination weddings</a></li>
    <li><a href="/contact/">Check your date</a></li></ul></div>
   <div><p class="fh">Recent stories</p><ul>
    <li><a href="/wedding-chrisjasmine/">Chris &amp; Jasmine — Newport, MN</a></li>
    <li><a href="/maddy-ben-surrey-uk/">Maddy &amp; Ben — Surrey, UK</a></li>
    <li><a href="/privacy-policy/">Privacy policy</a></li></ul></div>
  </div>
  <div class="base"><span>&copy; 2026 {NAME}. All rights reserved.</span><span>Minneapolis · St. Paul · Minnesota · United Kingdom</span></div>
 </div>
</footer>"""


def phero(image, alt, eyebrow, h1, sub, crumbs):
    cr = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span>/</span>'.join(
        f'<a href="{p}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page" style="margin:0;opacity:1">{e(n)}</span>'
        for i, (p, n) in enumerate(crumbs)) + '</nav>'
    return f"""<section class="phero">
 {img(image, alt, lazy=False, extra=' data-parallax="0.12"')}
 <div class="wrap">{cr}<span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p>{sub}</p></div>
</section>"""


def cta(image="dark-bouquet", title="Tell us about <em class=\"s\">your</em> day", text="We take a limited number of weddings each season so every couple gets our full attention. Share your date and we’ll reply within two business days."):
    return f"""<section class="cta-strip">
 {img(image, "Bride holding a bouquet in soft evening light", extra=' data-parallax="0.15"')}
 <div class="wrap rv"><span class="eyebrow" style="color:#f3e2d6">Now booking 2027 &amp; 2028</span><h2>{title}</h2><p>{text}</p>
 <a class="btn light" href="/contact/">Check availability <span class="arr">&rarr;</span></a></div>
</section>"""


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details class="rv"><summary>{e(q)}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs) + "</div>"


PUBLISHED = "2026-10-16"
LASTMOD = "2026-10-17"

STORIES = [
    {"path": "/wedding-chrisjasmine/", "title": "Chris &amp; Jasmine", "place": "Newport, Minnesota",
     "season": "Late summer", "img": "lake-couple",
     "alt": "Bride and groom standing beside a lake in golden late-summer light"},
    {"path": "/maddy-ben-surrey-uk/", "title": "Maddy &amp; Ben", "place": "Surrey, United Kingdom",
     "season": "Early summer", "img": "hills-couple",
     "alt": "Bride and groom embracing on a hillside above rolling English countryside"},
]


def story_cards():
    return '<div class="stories">' + "".join(f"""<a class="story rv{' d1' if i else ''}" href="{s['path']}">
 <div class="zoom rv-img">{img(s['img'], s['alt'], w=1400, h=933)}</div>
 <div class="meta"><span>{s['place']}</span><span>{s['season']}</span></div>
 <h3>{s['title']}</h3><span class="link">View the story</span></a>""" for i, s in enumerate(STORIES)) + "</div>"


# ---------------------------------------------------------------- pages
def home():
    slides = [("hills-couple", "Couple embracing on a hillside above green countryside at sunset"),
              ("barn-reception", "Candlelit barn wedding reception with draped fabric and a chandelier"),
              ("bw-veil", "Black and white photo of a bride and groom kissing as her veil lifts in the wind")]
    sl = "".join(f'<figure class="{"on" if i == 0 else ""}">{img(n, a, lazy=(i > 0))}</figure>' for i, (n, a) in enumerate(slides))
    dots = "".join(f'<button type="button" class="{"on" if i == 0 else ""}" aria-label="Show photo {i + 1}"></button>' for i in range(len(slides)))
    services = [
        ("i.", "Wedding day", "aisle", "Ceremony aisle lined with roses and gold chairs",
         "From getting ready to the last dance — told as it happens, with a light touch and an eye for the in-between moments.", "/collections/"),
        ("ii.", "Engagement sessions", "hilltop-walk", "Couple walking hand in hand across a hilltop at dusk",
         "An unhurried walk somewhere that feels like you: a lake path, a city street, a favourite trail.", "/collections/"),
        ("iii.", "Destination weddings", "black-beach", "Bride and groom on a black sand beach under a dramatic sky",
         "England, Scotland, Iceland, the coasts and countrysides in between — we travel light and plan ahead.", "/destination-weddings/"),
    ]
    cards = "".join(f"""<a class="card rv{' d' + str(i) if i else ''}" href="{u}">{img(im, al)}
 <div class="c"><span class="n">{n}</span><h3>{t}</h3><p>{p}</p></div></a>""" for i, (n, t, im, al, p, u) in enumerate(services))
    words = ["Real moments", "Honest light", "Twin Cities", "Lakeside vows", "English gardens", "First looks", "Last dances", "Quiet glances"]
    mq = "".join(f"<span>{w}</span>" for w in words * 2)
    faqs = [
        ("Where is Collin Hughes Weddings based?", "The studio is based in the Twin Cities of Minneapolis and St. Paul, Minnesota. We photograph weddings all over Minnesota and western Wisconsin, and travel for destination weddings in the UK, Europe and across the US."),
        ("What style of wedding photography do you shoot?", "Documentary first, with gentle direction when it helps. Most of your gallery is real moments as they happen; portraits are relaxed and quick so you can get back to your guests."),
        ("How far ahead should we book?", "Popular Saturdays from June to October fill 12 to 18 months ahead. Weekdays, winter weddings and elopements often have shorter notice availability, so it is always worth asking."),
    ]
    body = f"""<section class="hero">
 <div class="slides">{sl}</div>
 <div class="hero-in">
  <span class="eyebrow">Minneapolis – St. Paul wedding photographer</span>
  <h1><span class="ln"><span>Collin Hughes</span></span><span class="ln"><span><em class="s">Weddings</em></span></span></h1>
  <p>Honest, light-filled wedding photography for couples in Minnesota and far beyond — the laughter, the nerves, the glances nobody else saw.</p>
  <div class="btns"><a class="btn light" href="/weddings/">See real weddings <span class="arr">&rarr;</span></a><a class="btn light" href="/contact/">Check your date</a></div>
 </div>
 <div class="dots">{dots}</div>
 <div class="scroll-cue" aria-hidden="true"></div>
</section>

<section class="sec">
 <div class="wrap split">
  <div class="stack rv">
   {img("hero-couple", "Bride and groom laughing together under the trees", "a rv-img", 1280, 1920)}
   {img("ring-hands", "Close-up of wedding rings on the couple's joined hands over a bouquet", "b", 1200, 800)}
   <span class="tag">Est. in the Twin Cities</span>
  </div>
  <div class="rv d1">
   <span class="eyebrow">Hello, we’re so glad you’re here</span>
   <h2>Photographs that feel like <em class="s">the day felt</em></h2>
   <p class="lead">Collin Hughes Weddings is a small wedding photography studio rooted in Minneapolis and St. Paul. We photograph about two dozen weddings a year, which means your day gets our whole attention — not a production line.</p>
   <p>Our approach is simple: be present, stay unobtrusive, and notice. The father who can’t quite get through his toast. The flower girl asleep under the head table. The quiet second when you both realise it actually happened. Those are the frames people keep coming back to, years later.</p>
   <a class="link" href="/about/">More about the studio</a>
  </div>
 </div>
</section>

<div class="marquee" aria-hidden="true"><div class="track">{mq}</div></div>

<section class="sec bg-ivory">
 <div class="wrap">
  <div class="center rv"><span class="eyebrow">What we photograph</span><h2>From the first look to <em class="s">the last dance</em></h2></div>
  <div class="cards">{cards}</div>
 </div>
</section>

<section class="band">
 {img("bw-veil", "Black and white image of a bride and groom kissing, veil caught by the wind", extra=' data-parallax="0.18"')}
 <div class="in rv"><blockquote>“The best wedding photographs aren’t taken. They’re noticed — and then you get out of the way.”</blockquote><cite>The studio philosophy</cite></div>
</section>

<section class="sec">
 <div class="wrap">
  <div class="split">
   <div class="rv"><span class="eyebrow">Real weddings</span><h2>Recent <em class="s">love stories</em></h2></div>
   <p class="lead rv d1">A lakeside celebration just outside St. Paul and a garden wedding in the Surrey countryside — two very different days, photographed the same way: honestly.</p>
  </div>
  {story_cards()}
  <p class="center" style="margin-top:56px"><a class="btn" href="/weddings/">All weddings <span class="arr">&rarr;</span></a></p>
 </div>
</section>

<section class="sec bg-ink">
 <div class="wrap">
  <div class="center rv"><span class="eyebrow">How it works</span><h2>Simple, from hello to <em class="s">heirloom</em></h2></div>
  <div class="steps">
   <div class="step rv"><h3>Say hello</h3><p>Send your date, venue and a little about you. We reply within two business days with availability.</p></div>
   <div class="step rv d1"><h3>Meet &amp; plan</h3><p>A relaxed call or coffee in the Cities. We talk timeline, family photos and the moments that matter most.</p></div>
   <div class="step rv d2"><h3>The day</h3><p>We arrive early, stay late, and keep things calm. You get to be present — we’ll handle the remembering.</p></div>
   <div class="step rv d3"><h3>Your gallery</h3><p>A private online gallery with sneak peeks inside a week and your full collection within eight weeks.</p></div>
  </div>
 </div>
</section>

<section class="sec">
 <div class="wrap split rev">
  <div class="frame rv">{img("confetti", "Bride and groom kiss as guests throw petals after the ceremony", "rv-img", 933, 1400)}</div>
  <div class="rv d1">
   <span class="eyebrow">Minnesota, our home</span>
   <h2>Photographing weddings across <em class="s">the Twin Cities</em></h2>
   <p>We know these venues and this light: riverside ceremonies along the Mississippi, summer evenings on the St. Croix, barn receptions in the farmland south of the Cities, winter weddings when the snow turns everything quiet and blue.</p>
   <p>Whether you are marrying in a downtown Minneapolis loft, a St. Paul cathedral, a lake cabin up north or your parents’ back garden, we plan around the light and the timeline so nothing feels rushed.</p>
   <ul class="cinfo" style="margin-top:10px">
    <li><small>Most photographed</small>Minneapolis · St. Paul · Stillwater · Newport · Lake Minnetonka · Duluth</li>
   </ul>
  </div>
 </div>
</section>

<section class="sec tight bg-ivory">
 <div class="narrow">
  <div class="center rv"><span class="eyebrow">Good to know</span><h2>Questions couples ask</h2></div>
  {faq_html(faqs)}
  <p class="center" style="margin-top:40px"><a class="link" href="/collections/">See collections &amp; the full FAQ</a></p>
 </div>
</section>
{cta()}"""
    return page("/", "Collin Hughes Weddings | Minneapolis Wedding Photographer",
                "Collin Hughes Weddings — documentary-style wedding photography in Minneapolis–St. Paul, across Minnesota and at destination weddings in the UK and beyond.",
                body, schema=[faq_schema(faqs)], hero_img="hills-couple")


def about():
    crumbs = [("/", "Home"), ("/about/", "About")]
    body = phero("signing", "Bride and groom signing their marriage certificate", "About the studio",
                 "Hello — this is <em class=\"s\">Collin Hughes Weddings</em>",
                 "A small Twin Cities wedding photography studio that believes the best pictures come from paying attention.", crumbs) + f"""
<section class="sec">
 <div class="wrap split">
  <div class="frame rv">{img("field-veil", "Groom lifting his bride in a wheat field, her veil wrapped around them", "rv-img", 993, 1400)}</div>
  <div class="rv d1 prose">
   <span class="eyebrow">Our story</span>
   <h2>Less posing, <em class="s">more living</em></h2>
   <p class="lead">Collin Hughes Weddings started with a simple idea: a wedding gallery should feel like the day felt, not like a catalogue shoot that happened to have a wedding in the background.</p>
   <p>We’re based in Minneapolis–St. Paul and photograph weddings all over Minnesota, plus a handful of destination weddings each year — most often in England, where green hills and old stone churches make for something special.</p>
   <p>On the day you’ll find us moving quietly around the edges, watching for the real stuff. When a little direction helps — a portrait at golden hour, a family photo that needs wrangling — we step in, get it done quickly and kindly, and let you get back to the party.</p>
  </div>
 </div>
</section>

<section class="band">
 {img("hand-hold", "Bride and groom holding hands, their shadows on the grass", extra=' data-parallax="0.18"')}
 <div class="in rv"><blockquote>“You will forget what the centrepieces looked like. You won’t forget how your grandmother cried during the vows.”</blockquote></div>
</section>

<section class="sec bg-ivory">
 <div class="wrap">
  <div class="center rv"><span class="eyebrow">What we believe</span><h2>Three promises to <em class="s">every couple</em></h2></div>
  <div class="steps" style="grid-template-columns:repeat(3,1fr)">
   <div class="step rv"><h3>Calm presence</h3><p>Weddings run late, rain happens, cakes lean. We stay relaxed, solve problems quietly and keep the energy warm.</p></div>
   <div class="step rv d1"><h3>Honest images</h3><p>Natural colour, true skin tones and real emotion. Edits that will still look right in thirty years.</p></div>
   <div class="step rv d2"><h3>Real attention</h3><p>A limited number of weddings each year, so planning calls get answered and galleries arrive on time.</p></div>
  </div>
 </div>
</section>

<section class="sec">
 <div class="wrap split rev">
  <div class="rv">{img("barn-reception", "Warmly lit barn reception hall with draped ceiling fabric", "rv-img", 1600, 1065)}</div>
  <div class="rv d1">
   <span class="eyebrow">Where we work</span>
   <h2>Twin Cities roots, <em class="s">passport ready</em></h2>
   <p>Most of our weddings happen within a couple of hours of the Cities — Minneapolis, St. Paul, Stillwater and the St. Croix Valley, Lake Minnetonka, the river towns south toward Red Wing, and up north to Duluth and the lake country.</p>
   <p>We also love to travel. Destination weddings, from English country houses to coastal elopements, are planned with the same care as a wedding down the road.</p>
   <a class="btn" href="/destination-weddings/">Destination weddings <span class="arr">&rarr;</span></a>
  </div>
 </div>
</section>
{cta()}"""
    return page("/about/", "About Collin Hughes | Twin Cities Wedding Photography",
                "Meet Collin Hughes Weddings, a documentary-minded wedding photography studio in Minneapolis–St. Paul photographing Minnesota and destination weddings.",
                body, hero_img="signing", crumbs=crumbs,
                schema=[{"@type": "AboutPage", "url": SITE + "/about/", "about": {"@id": SITE + "/#business"}}])


def weddings():
    crumbs = [("/", "Home"), ("/weddings/", "Weddings")]
    gal = [("aisle", "Rose-lined ceremony aisle with gold chiavari chairs"), ("brick-bouquet", "Bride holding a peach and white bouquet against a brick wall"),
           ("toast", "Guests raising champagne glasses during a reception toast"), ("peach-bouquet", "Peach rose bridal bouquet held against a white gown"),
           ("buttonholes", "Row of rustic floral buttonholes pinned to a wooden board"), ("seaside", "Bride and groom embracing by the sea, veil trailing on the pebbles"),
           ("table", "Reception table set with crystal glasses and peach roses"), ("rings-peony", "Two wedding rings resting on pink peonies"),
           ("mr-mrs", "Wooden Mr & Mrs sign hanging in a blossoming tree"), ("lawn-chairs", "Two decorated chairs for the couple on a lakeside lawn")]
    g = "".join(f'<a href="/assets/img/{n}.webp">{img(n, a)}</a>' for n, a in gal)
    body = phero("aisle", "Ceremony aisle lined with roses", "Portfolio", "Real <em class=\"s\">weddings</em>",
                 "Full wedding stories from Minnesota and abroad, plus a few favourite frames from recent seasons.", crumbs) + f"""
<section class="sec">
 <div class="wrap">
  <div class="split"><div class="rv"><span class="eyebrow">Featured stories</span><h2>Two days, <em class="s">two countries</em></h2></div>
  <p class="lead rv d1">Every wedding we photograph is delivered as a full story. These are two couples who kindly let us share theirs.</p></div>
  {story_cards()}
 </div>
</section>
<section class="sec bg-ivory">
 <div class="wrap">
  <div class="center rv"><span class="eyebrow">Moments &amp; details</span><h2>From recent <em class="s">seasons</em></h2><p class="lead narrow">Tap any image to view it larger.</p></div>
  <div class="gallery">{g}</div>
 </div>
</section>
{cta("seaside")}"""
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE + s["path"], "name": html.unescape(s["title"])} for i, s in enumerate(STORIES)]
    return page("/weddings/", "Real Weddings | Collin Hughes Weddings Portfolio",
                "Real weddings photographed by Collin Hughes Weddings — Minnesota lakeside celebrations, English country weddings and favourite moments from recent seasons.",
                body, hero_img="aisle", crumbs=crumbs,
                schema=[{"@type": "CollectionPage", "url": SITE + "/weddings/", "mainEntity": {"@type": "ItemList", "itemListElement": items}}])


def story_page(path, crumbs_name, title, desc, hero, hero_alt, eyebrow, h1, sub, facts, prose, gallery, related):
    crumbs = [("/", "Home"), ("/weddings/", "Weddings"), (path, crumbs_name)]
    f = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in facts)
    g = "".join(f'<a href="/assets/img/{n}.webp">{img(n, a)}</a>' for n, a in gallery)
    body = phero(hero, hero_alt, eyebrow, h1, sub, crumbs) + f"""
<article class="sec">
 <div class="narrow prose">
  <dl class="facts rv">{f}</dl>
  {prose}
 </div>
 <div class="wrap"><div class="gallery">{g}</div></div>
</article>
<section class="sec tight bg-ivory">
 <div class="wrap split">
  <div class="rv"><span class="eyebrow">Next story</span><h2>{related['title']}</h2><p>{related['place']}</p><a class="btn" href="{related['path']}">Read their story <span class="arr">&rarr;</span></a></div>
  <a class="zoom rv d1" href="{related['path']}" aria-label="{e(html.unescape(related['title']))}">{img(related['img'], related['alt'], w=1400, h=933)}</a>
 </div>
</section>
{cta()}"""
    schema = [{"@type": "BlogPosting", "headline": html.unescape(crumbs_name) + " — " + html.unescape(sub), "description": desc,
               "datePublished": PUBLISHED, "dateModified": PUBLISHED, "inLanguage": "en-US",
               "image": SITE + f"/assets/img/{hero}.webp", "url": SITE + path, "mainEntityOfPage": SITE + path,
               "author": {"@id": SITE + "/#business"}, "publisher": {"@id": SITE + "/#business"},
               "about": {"@type": "Event", "name": html.unescape(crumbs_name) + " wedding", "eventStatus": "https://schema.org/EventScheduled",
                         "location": {"@type": "Place", "name": dict(facts)["Location"]}}}]
    return page(path, title, desc, body, hero_img=hero, crumbs=crumbs, schema=schema, og_type="article",
                og_alt=hero_alt, published=PUBLISHED)


def chris_jasmine():
    prose = f"""
<p class="lead rv">Chris and Jasmine’s wedding was everything a late-summer Minnesota day should be: warm air off the river, long golden light and a guest list full of people who had known them forever.</p>
<p class="rv">Newport sits on the Mississippi just south-east of St. Paul — close enough to the Cities that guests could drive in for the afternoon, far enough out that the evening felt like a proper escape. The couple wanted a day that felt relaxed rather than staged, so we kept the timeline loose and the portraits short.</p>
<h2 class="rv">Getting ready</h2>
<p class="rv">The morning started slowly. Jasmine got ready with her sisters and closest friends, coffee going cold on the windowsill while everyone found the right playlist. Across town Chris and his groomsmen were mostly arguing about how to tie a bow tie. We split our time between the two, catching the small things — a mother fastening a necklace, a best man practising his speech under his breath.</p>
<div class="duo rv">{img("brick-bouquet", "Bride holding her bouquet beside the groom", w=1200, h=801)}{img("hands-rings-leaves", "The couple's hands with new wedding rings among green leaves", w=1200, h=801)}</div>
<h2 class="rv">A first look by the water</h2>
<p class="rv">They chose to see each other before the ceremony, down by the water where the trees opened up. Chris kept his back turned for what felt like a very long minute. When he finally turned around he didn’t say anything at all — which said everything. A first look like this also bought them time: family photos were finished before guests arrived, and they walked straight from the ceremony into cocktail hour.</p>
<blockquote class="rv">The vows were short, personal and funny, and half the room was crying by the end of them.</blockquote>
<h2 class="rv">Ceremony &amp; celebration</h2>
<p class="rv">The ceremony took place outdoors, chairs lined up on the lawn with the river behind. Afterwards the guests showered the couple in petals and the party moved under the lights. Toasts were loud, the dance floor filled quickly and the sun put on a show just before nine — so we borrowed the couple for ten minutes of quiet golden-hour portraits by the water.</p>
<figure class="rv">{img("toast", "Wedding guests raising glasses during the reception toasts", w=1200, h=800)}<figcaption>Toasts under the string lights.</figcaption></figure>
<h2 class="rv">Planning a wedding near Newport, MN?</h2>
<p class="rv">A few things we learned that are worth passing on:</p>
<ul class="rv">
 <li><strong>Chase the river light.</strong> In August the sun sets around 8:15pm. Schedule portraits for 45 minutes before that and you’ll get the soft, warm glow seen here.</li>
 <li><strong>Think about a first look.</strong> It lets you finish family photos early and actually enjoy your cocktail hour.</li>
 <li><strong>Have a weather plan.</strong> Minnesota summer storms roll in fast. A tent or indoor back-up keeps the day calm if the sky changes its mind.</li>
 <li><strong>Mind the bugs.</strong> Riverside evenings are beautiful, and so are the mosquitoes. A basket of bug spray is a guest favour everyone uses.</li>
</ul>
<p class="rv">Thank you, Chris and Jasmine, for letting us be part of it. If you are planning a wedding in Newport, St. Paul or anywhere in the Twin Cities, we would love to hear about it — <a href="/contact/">check your date here</a>.</p>
"""
    gallery = [("confetti", "Guests throwing petals over the newlyweds"), ("lake-couple", "The couple standing by the lake in evening light"),
               ("table", "Reception table with roses and glassware"), ("peach-bouquet", "Bride's peach rose bouquet"),
               ("lawn-chairs", "Decorated chairs for the bride and groom on the lawn"), ("ring-hands", "Wedding rings and bouquet")]
    return story_page("/wedding-chrisjasmine/", "Chris & Jasmine",
                      "Chris & Jasmine’s Newport, MN Wedding | Collin Hughes",
                      "Chris and Jasmine’s late-summer riverside wedding in Newport, Minnesota, near St. Paul — a relaxed first look, golden-hour portraits and a packed dance floor.",
                      "lake-couple", "Chris and Jasmine by the water in Newport, Minnesota", "Real wedding · Newport, MN",
                      "Chris &amp; <em class=\"s\">Jasmine</em>", "A late-summer riverside wedding just outside St. Paul, Minnesota.",
                      [("Location", "Newport, Minnesota"), ("Season", "Late summer"), ("Setting", "Riverside, outdoors"), ("Highlights", "First look &amp; golden hour")],
                      prose, gallery, STORIES[1])


def maddy_ben():
    prose = f"""
<p class="lead rv">Maddy and Ben were married in the Surrey countryside on one of those early-summer English days when the hills go on forever and the light never quite seems to fade.</p>
<p class="rv">Surrey is less than an hour from London, but it feels like another world: the North Downs, flint-walled villages, country houses at the end of long gravel drives and churches older than most countries. It was a joy to photograph a wedding here — the landscape does half the work for you.</p>
<h2 class="rv">An English country morning</h2>
<p class="rv">Preparations happened in an old house with tall sash windows that poured soft daylight across the room. Maddy’s dress hung in the window while her bridesmaids pinned buttonholes for the groomsmen — wildflowers, thistle and a little rosemary, all from a local grower. Ben, meanwhile, was taking a very calm walk around the garden, which apparently is how he deals with nerves.</p>
<div class="duo rv">{img("buttonholes", "Wildflower buttonholes laid out on a wooden board", w=1200, h=800)}{img("field-veil", "Ben holding Maddy in a field of long grass, her veil around them", w=993, h=1400)}</div>
<h2 class="rv">Vows in the village</h2>
<p class="rv">The ceremony was in the village church, with bells ringing as they walked out into a confetti tunnel of family and friends. From there, everyone strolled across the fields to the reception — a short walk that turned into one of our favourite parts of the day, guests chatting in little groups, kids racing ahead through the long grass.</p>
<blockquote class="rv">English summer evenings are long. Sunset was after nine, which meant golden hour arrived right as the speeches finished.</blockquote>
<h2 class="rv">Up on the hill</h2>
<p class="rv">Late in the evening we walked up the hill behind the venue. The whole valley was glowing and the two of them just stood there for a while, taking it in. We barely said a word — we didn’t need to. Then back down for the first dance, a ceilidh band and a very competitive round of the Gay Gordons.</p>
<figure class="rv">{img("hilltop-walk", "Bride and groom walking hand in hand along a hilltop at dusk", w=1600, h=1067)}<figcaption>A quiet walk above the valley at the end of the day.</figcaption></figure>
<h2 class="rv">Thinking about a wedding in Surrey or the UK?</h2>
<ul class="rv">
 <li><strong>Use the long evenings.</strong> In June, sunset in southern England is around 9:20pm. Leave room in the timeline for a golden-hour walk after dinner.</li>
 <li><strong>Plan for showers.</strong> English weather changes quickly. Umbrellas in neutral colours look great in photos — and the light after rain is often the best of the day.</li>
 <li><strong>Church timings matter.</strong> Many village churches have set ceremony slots and rules about photography during the service. Ask early and share them with your photographer.</li>
 <li><strong>Travelling from the US?</strong> Allow time for the UK legal requirements, or hold the legal ceremony at home and celebrate in England. We can help you plan either way — see <a href="/destination-weddings/">destination weddings</a>.</li>
</ul>
<p class="rv">Maddy and Ben — thank you for having us. Wherever in the world your wedding is happening, <a href="/contact/">we would love to hear from you</a>.</p>
"""
    gallery = [("hills-couple", "Maddy and Ben embracing on the hillside"), ("mr-mrs", "Mr & Mrs sign in a blossoming tree"),
               ("rings-peony", "Wedding rings on pink peonies"), ("seaside", "The couple by the sea the day after"),
               ("aisle", "Rose-lined aisle"), ("hand-hold", "Hands joined at sunset")]
    return story_page("/maddy-ben-surrey-uk/", "Maddy & Ben",
                      "Maddy & Ben’s Surrey, UK Wedding | Collin Hughes Weddings",
                      "Maddy and Ben’s English country wedding in Surrey, UK — village church vows, a walk across the fields and golden-hour portraits above the valley.",
                      "hills-couple", "Maddy and Ben on a hillside in the Surrey countryside", "Real wedding · Surrey, UK",
                      "Maddy &amp; <em class=\"s\">Ben</em>", "An early-summer English country wedding in the Surrey Hills.",
                      [("Location", "Surrey, United Kingdom"), ("Season", "Early summer"), ("Setting", "Village church &amp; country house"), ("Highlights", "Hilltop golden hour")],
                      prose, gallery, STORIES[0])


COLLECTION_FAQS = [
    ("How much does wedding photography cost?", "Every wedding is different, so we build a quote around your hours, locations and any extras like an engagement session or album. Send us your date and plans and we will reply with a tailored proposal and full collection guide."),
    ("Do you travel for weddings?", "Yes. We photograph weddings throughout Minnesota and western Wisconsin with no travel fee inside the Twin Cities metro, and we travel for destination weddings in the UK, Europe and across the US."),
    ("Is there a second photographer?", "Our Signature and Heirloom collections include a second photographer. For smaller weddings a single photographer is usually all you need."),
    ("When will we get our photos?", "You will receive a sneak peek within a week and your full, edited gallery within eight weeks of the wedding."),
    ("How many photos will we receive?", "It depends on coverage, but most full-day weddings receive between 600 and 900 finished images, all high resolution and with printing rights."),
    ("How do we book our date?", "Your date is reserved with a signed agreement and a retainer. The balance is due a month before the wedding."),
    ("Do you photograph elopements and small weddings?", "Absolutely. Courthouse weddings, backyard ceremonies and mountaintop elopements are some of our favourite days to photograph."),
]


def collections():
    crumbs = [("/", "Home"), ("/collections/", "Collections")]
    tiers = [
        ("Intimate", "Elopements &amp; small weddings", ["Up to 4 hours of coverage", "One photographer", "Online gallery with print rights", "Sneak peek within a week"], False),
        ("Signature", "Our most loved collection", ["8 hours of coverage", "Lead &amp; second photographer", "Engagement session", "Online gallery with print rights", "Planning call &amp; timeline help"], True),
        ("Heirloom", "Full-day storytelling", ["10 hours of coverage", "Lead &amp; second photographer", "Engagement session", "Handmade linen album", "Parent albums available"], False),
    ]
    t = "".join(f"""<div class="tier{' feat' if f else ''} rv{' d' + str(i) if i else ''}"><span class="eyebrow">{s}</span><h3>{n}</h3>
<ul>{''.join(f'<li>{x}</li>' for x in items)}</ul><a class="btn" href="/contact/">Request pricing <span class="arr">&rarr;</span></a></div>"""
                for i, (n, s, items, f) in enumerate(tiers))
    body = phero("rings-peony", "Two wedding rings resting on pink peonies", "Collections", "Wedding photography <em class=\"s\">collections</em>",
                 "Thoughtfully built coverage for every kind of wedding — from a courthouse elopement to a three-day celebration.", crumbs) + f"""
<section class="sec">
 <div class="wrap">
  <div class="split"><div class="rv"><span class="eyebrow">Choose your coverage</span><h2>Every collection <em class="s">includes</em></h2></div>
  <p class="lead rv d1">A planning call, help with your timeline, a private online gallery, full-resolution images with printing rights and our complete attention on the day. Collections can be tailored — just ask.</p></div>
  <div class="tiers">{t}</div>
 </div>
</section>
<section class="band">
 {img("table", "Elegant reception table with candles and roses", extra=' data-parallax="0.18"')}
 <div class="in rv"><blockquote>“Spend on the things you’ll keep. The flowers fade by Monday. The photographs are for your grandchildren.”</blockquote></div>
</section>
<section class="sec bg-ivory">
 <div class="narrow">
  <div class="center rv"><span class="eyebrow">FAQ</span><h2>Frequently asked <em class="s">questions</em></h2></div>
  {faq_html(COLLECTION_FAQS)}
 </div>
</section>
{cta()}"""
    return page("/collections/", "Wedding Photography Collections & FAQ | Collin Hughes",
                "Wedding photography collections from Collin Hughes Weddings in Minneapolis–St. Paul: elopements, full-day coverage, engagement sessions and heirloom albums.",
                body, hero_img="rings-peony", crumbs=crumbs, schema=[faq_schema(COLLECTION_FAQS)])


def destination():
    crumbs = [("/", "Home"), ("/destination-weddings/", "Destination weddings")]
    faqs = [("Do you charge travel fees for destination weddings?", "Travel is quoted at cost — flights, accommodation and ground transport — with no mark-up. We will always give you the full figure upfront."),
            ("Where have you photographed destination weddings?", "Our favourite destination is the English countryside, including Surrey, the Cotswolds and the Lake District, along with coastal elopements and city weddings in Europe and across the US."),
            ("Can you photograph an elopement abroad?", "Yes. Elopements are a wonderful way to marry somewhere spectacular. We can help with location ideas, timing for the best light and local logistics.")]
    body = phero("black-beach", "Bride and groom on a dramatic black sand beach", "Destination weddings", "Wherever you say <em class=\"s\">I do</em>",
                 "Destination wedding and elopement photography — English country houses, rugged coastlines and cities across Europe and the US.", crumbs) + f"""
<section class="sec">
 <div class="wrap split">
  <div class="rv prose">
   <span class="eyebrow">Passport ready</span>
   <h2>The same care, <em class="s">anywhere</em></h2>
   <p class="lead">A destination wedding asks a lot of the people you invite — so the photographs should be worth the journey. We travel light, arrive early and scout the location so we know where the light falls before the day begins.</p>
   <p>The UK holds a special place for us. Weddings like <a href="/maddy-ben-surrey-uk/">Maddy &amp; Ben’s in Surrey</a> — village church, walk across the fields, a hilltop at golden hour — are exactly the kind of day we love. We also photograph elopements on coastlines, in mountains and in old European cities.</p>
   <ul><li>Location scouting the day before</li><li>Help planning a timeline around local sunset</li><li>Advice on permits, weather windows and back-up spots</li><li>Travel quoted at cost, upfront</li></ul>
  </div>
  <div class="stack rv d1">
   {img("seaside", "Bride and groom embracing on a pebble beach", "a rv-img", 933, 1400)}
   {img("hilltop-walk", "Couple walking along a hilltop", "b", 1600, 1067)}
  </div>
 </div>
</section>
<section class="sec bg-ink">
 <div class="wrap">
  <div class="center rv"><span class="eyebrow">Favourite destinations</span><h2>Where we love to <em class="s">travel</em></h2></div>
  <div class="steps">
   <div class="step rv"><h3>Surrey &amp; the South</h3><p>Country houses, village churches and the North Downs, within easy reach of London airports.</p></div>
   <div class="step rv d1"><h3>Cotswolds</h3><p>Honey-coloured stone, barns and gardens. Pure English romance in every direction.</p></div>
   <div class="step rv d2"><h3>Coasts &amp; cliffs</h3><p>Wild beaches and clifftop vows for couples who want weather, drama and space.</p></div>
   <div class="step rv d3"><h3>Across the US</h3><p>From Lake Superior’s North Shore to the coasts — if you’re there, we can be too.</p></div>
  </div>
 </div>
</section>
<section class="sec tight">
 <div class="narrow">{faq_html(faqs)}</div>
</section>
{cta("hills-couple", "Planning a wedding <em class=\"s\">abroad?</em>")}"""
    return page("/destination-weddings/", "Destination Wedding Photographer UK & Europe | Collin Hughes",
                "Destination wedding and elopement photography by Collin Hughes Weddings — English country weddings in Surrey and the Cotswolds, coastal elopements and Europe.",
                body, hero_img="black-beach", crumbs=crumbs, schema=[faq_schema(faqs)])


def contact():
    crumbs = [("/", "Home"), ("/contact/", "Contact")]
    body = phero("mr-mrs", "Mr & Mrs sign hanging in a tree in blossom", "Inquire", "Let’s talk about <em class=\"s\">your day</em>",
                 "Tell us a little about your plans and we’ll reply with availability and a collection guide within two business days.", crumbs) + f"""
<section class="sec">
 <div class="wrap split" style="align-items:start">
  <div class="rv">
   <span class="eyebrow">Check your date</span>
   <h2>Say <em class="s">hello</em></h2>
   <p class="notice" data-form-status role="status" hidden></p>
   <form class="form" action="/send.php" method="post">
    <div class="field"><input id="f-name" name="name" type="text" placeholder=" " required autocomplete="name"><label for="f-name">Your names</label></div>
    <div class="field"><input id="f-email" name="email" type="email" placeholder=" " required autocomplete="email"><label for="f-email">Email</label></div>
    <div class="field"><input id="f-date" name="date" type="text" placeholder=" "><label for="f-date">Wedding date</label></div>
    <div class="field"><input id="f-venue" name="venue" type="text" placeholder=" "><label for="f-venue">Venue or location</label></div>
    <div class="field full"><textarea id="f-msg" name="message" placeholder=" " required></textarea><label for="f-msg">Tell us about your day</label></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Website</label><input id="f-web" name="website" type="text" tabindex="-1" autocomplete="off"></div>
    <div class="full"><button class="btn fill" type="submit">Send inquiry <span class="arr">&rarr;</span></button></div>
   </form>
  </div>
  <div class="rv d1">
   <div class="frame">{img("ring-hands", "Couple's hands with wedding rings resting on a bouquet", "rv-img", 1200, 800)}</div>
   <ul class="cinfo" style="margin-top:50px">
    <li><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li><small>Studio</small>Minneapolis – St. Paul, Minnesota</li>
    <li><small>Serving</small>Minnesota, Wisconsin, the UK &amp; destinations worldwide</li>
    <li><small>Reply time</small>Within two business days</li>
   </ul>
  </div>
 </div>
</section>"""
    return page("/contact/", "Contact & Check Availability | Collin Hughes Weddings",
                "Contact Collin Hughes Weddings to check availability for your Minneapolis–St. Paul, Minnesota or destination wedding. Email info@collinhughesweddings.com.",
                body, hero_img="mr-mrs", crumbs=crumbs,
                schema=[{"@type": "ContactPage", "url": SITE + "/contact/", "about": {"@id": SITE + "/#business"}}])


def privacy():
    crumbs = [("/", "Home"), ("/privacy-policy/", "Privacy policy")]
    body = f"""<section class="sec" style="padding-top:170px"><div class="narrow prose">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Privacy policy</nav>
<h1>Privacy policy</h1>
<p>Last updated October 2026.</p>
<p>{NAME} (“we”, “us”) respects your privacy. This policy explains what we collect through collinhughesweddings.com and how we use it.</p>
<h2>What we collect</h2>
<p>When you send an inquiry we receive the details you enter: your names, email address, wedding date, venue and message. We do not use advertising trackers.</p>
<h2>How we use it</h2>
<p>We use your details only to reply to your inquiry, plan your photography and deliver your gallery. We never sell or rent personal information.</p>
<h2>Your photographs</h2>
<p>Wedding images may be shared in our portfolio only with the couple’s permission. You can ask us to remove any image at any time.</p>
<h2>Retention &amp; your rights</h2>
<p>Inquiry emails are kept for as long as needed to respond and for our business records. You may ask to see, correct or delete your information by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Cookies &amp; analytics</h2>
<p>We use Google Analytics to understand how visitors find and use the site — for example which pages are read most. Google Analytics sets cookies and collects information such as pages visited, approximate location, device and browser. We do not use it to identify you personally. You can opt out with Google’s <a href="https://tools.google.com/dlpage/gaoptout" rel="nofollow noopener">Analytics opt-out browser add-on</a> or by blocking cookies in your browser.</p>
<p>Fonts are loaded from Google Fonts, which may log standard request data.</p>
<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>"""
    return page("/privacy-policy/", "Privacy Policy | Collin Hughes Weddings",
                "How Collin Hughes Weddings collects, uses and protects the information you share through collinhughesweddings.com.",
                body, solid=True, crumbs=crumbs)


def notfound():
    body = f"""<section class="hero" style="min-height:100svh">
 <div class="slides"><figure class="on">{img("dark-bouquet", "Bride holding a bouquet in soft light", lazy=False)}</figure></div>
 <div class="hero-in"><span class="eyebrow">Error 404</span><h1>This page has <em class="s">wandered off</em></h1>
 <p>Like a groomsman before the photos. Let’s get you back to the party.</p>
 <div class="btns"><a class="btn light" href="/">Home</a><a class="btn light" href="/weddings/">Real weddings</a></div></div>
</section>"""
    return page("/404.html", "Page not found | Collin Hughes Weddings", "The page you were looking for could not be found.", body, robots="noindex,follow")


def render(fn, path):
    _CUR[0] = path
    try:
        return fn()
    finally:
        _CUR[0] = None


def og_images(names):
    os.makedirs(os.path.join(OUT, "assets/og"))
    for n in names:
        with Image.open(os.path.join(SRC, "img", n + ".webp")) as im:
            im = im.convert("RGB")
            w, h = im.size
            r = 1200 / 630
            if w / h > r:
                nw = int(h * r); box = ((w - nw) // 2, 0, (w + nw) // 2, h)
            else:
                nh = int(w / r); top = max(0, int((h - nh) * 0.35)); box = (0, top, w, top + nh)
            im.crop(box).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, "assets/og", n + ".jpg"), quality=82, optimize=True, progressive=True)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    routes = [
        ("home.html", "/", home), ("about/index.html", "/about/", about), ("weddings/index.html", "/weddings/", weddings),
        ("wedding-chrisjasmine/index.html", "/wedding-chrisjasmine/", chris_jasmine),
        ("maddy-ben-surrey-uk/index.html", "/maddy-ben-surrey-uk/", maddy_ben),
        ("collections/index.html", "/collections/", collections), ("destination-weddings/index.html", "/destination-weddings/", destination),
        ("contact/index.html", "/contact/", contact), ("privacy-policy/index.html", "/privacy-policy/", privacy), ("404.html", None, notfound),
    ]
    heroes = set()
    for rel, path, fn in routes:
        content = render(fn, path)
        heroes.update(__import__("re").findall(r'/assets/og/([\w-]+)\.jpg', content))
        p = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
    os.makedirs(os.path.join(OUT, "assets/css")); os.makedirs(os.path.join(OUT, "assets/js"))
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(OUT, "assets/css/site.css"))
    shutil.copy(os.path.join(SRC, "site.js"), os.path.join(OUT, "assets/js/site.js"))
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "assets/img"))
    og_images(sorted(heroes))
    for n in ("index.php", "send.php", "googlecccfbf2f7e9e5ae4.html"):
        shutil.copy(os.path.join(SRC, n), os.path.join(OUT, n))
    for n in os.listdir(os.path.join(SRC, "icons")):
        shutil.copy(os.path.join(SRC, "icons", n), os.path.join(OUT, n))
    with open(os.path.join(OUT, "site.webmanifest"), "w") as f:
        json.dump({"name": NAME, "short_name": "Collin Hughes", "start_url": "/", "display": "standalone",
                   "background_color": "#fffdf9", "theme_color": "#1f1b18",
                   "icons": [{"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                             {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, f, indent=1)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for rel, path, fn in routes:
        if path is None:
            continue
        seen, imgs = set(), []
        for n, alt in IMAGES_USED.get(path, []):
            if n not in seen:
                seen.add(n); imgs.append(f"<image:image><image:loc>{SITE}/assets/img/{n}.webp</image:loc></image:image>")
        xml.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{LASTMOD}</lastmod>{''.join(imgs)}</url>")
    xml.append("</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write("\n".join(xml))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /home.html\nDisallow: /send.php\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(routes), "pages ->", OUT)

if __name__ == "__main__":
    main()
