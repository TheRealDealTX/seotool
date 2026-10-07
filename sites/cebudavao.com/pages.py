"""Static pages: about, contact, policies, FAQs, photo credits, HTML sitemap, 404."""
from config import SITE, TODAY

ORIGIN = SITE["origin"]


def _simple(page, write, crumbs, crumb_ld, url, title, h1, desc, inner, ld_extra=None, robots=None):
    trail = [("Home", "/"), (h1, url)]
    body = f'''<section class="page-hero"><div class="wrap">{crumbs(trail)}<h1>{h1}</h1></div></section>
<div class="wrap-narrow prose static-page">{inner}</div>'''
    write(url, page(url, title, desc, body, ld=[crumb_ld(trail)] + (ld_extra or []), robots=robots))
    return url


def build(page, write, crumbs, crumb_ld, posts, photos, categories, cat_url, esc):
    urls = []
    S = lambda *a, **k: urls.append(_simple(page, write, crumbs, crumb_ld, *a, **k))

    S("/about/", "About Cebu-Davao", "About Cebu-Davao",
      "Cebu-Davao is an independent news, travel, food and lifestyle site covering Cebu, Davao and the wider Philippines.",
      f'''<p class="lede">Cebu-Davao is an independent digital magazine about the two great cities of the southern Philippines — <a href="/cebu/">Cebu</a>, the Queen City of the South, and <a href="/davao/">Davao</a>, the gateway to Mindanao — and the islands in between.</p>
<h2>What we cover</h2>
<ul><li><a href="/news/">News and explainers</a> — public-service guides on typhoon signals, IDs, travel rules and big local projects, plus a live headline wire.</li>
<li><a href="/category/travel/">Travel</a> — how to actually get there, what it costs and when to go.</li>
<li><a href="/category/food/">Food</a> — lechon, kinilaw and home recipes from Visayas and Mindanao kitchens.</li>
<li><a href="/category/culture/">Culture</a>, <a href="/category/sports/">sports</a>, <a href="/category/entertainment/">entertainment</a>, <a href="/category/money/">money &amp; work</a> and <a href="/category/tech/">tech</a>.</li>
<li>Free <a href="/tools/">reader tools</a>: <a href="/weather/">weather forecasts</a>, a peso converter, a Bisaya dictionary and more.</li></ul>
<h2>Our story</h2>
<p>The site started more than a decade ago as a personal blog about life between Cebu and Davao — recipes, road trips, music and the occasional rant about slow internet. It later became a travel journal written from Texas with a wanderer's eye on the Philippines; those moving and renting guides live on in our <a href="/category/expat-living/">Living Abroad</a> archive. In 2026 we relaunched Cebu-Davao as a fuller magazine, rebuilt our most-read guides from scratch and added live tools for readers.</p>
<h2>How we work</h2>
<p>Our guides are written and updated by the {SITE["editorial"]}. We check facts against official sources, label prices as estimates, and correct mistakes openly. Read our <a href="/editorial-policy/">editorial policy</a>.</p>
<h2>Get in touch</h2>
<p>Story tips, corrections and partnership enquiries: <a href="/contact/">contact us</a> or email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</p>''',
      ld_extra=[{"@type": "AboutPage", "url": ORIGIN + "/about/", "name": "About Cebu-Davao", "about": {"@id": ORIGIN + "/#org"}}])

    S("/contact/", "Contact Cebu-Davao", "Contact Us",
      "Contact Cebu-Davao with story tips, corrections, advertising and partnership enquiries.",
      f'''<p class="lede">Got a story tip from Cebu or Davao, spotted an error, or want to work with us? Send a message — we read everything.</p>
<form class="contact-form" action="/api/contact.php" method="post" data-ajax-form>
<div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" required maxlength="100" autocomplete="name"></div>
<div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required maxlength="150" autocomplete="email"></div>
<div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>Story tip</option><option>Correction</option><option>Advertising &amp; partnerships</option><option>Something else</option></select></div>
<div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required maxlength="5000"></textarea></div>
<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" type="submit">Send message</button>
<p class="form-msg" role="status" aria-live="polite"></p>
</form>
<p>Prefer email? Write to <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>. For corrections, include the page link and what needs fixing.</p>''',
      ld_extra=[{"@type": "ContactPage", "url": ORIGIN + "/contact/", "name": "Contact Cebu-Davao"}])

    S("/editorial-policy/", "Editorial Policy", "Editorial Policy",
      "How Cebu-Davao researches, fact-checks, updates and corrects its news, travel and lifestyle content.",
      '''<h2>Accuracy first</h2><p>We write for readers who will act on what we publish — book a ferry, cook a recipe, prepare for a typhoon. We check facts against official sources (PAGASA, DFA, DOT, local government units, operators' own channels) and link to them where useful.</p>
<h2>Prices, fares and schedules</h2><p>Costs change quickly in the Philippines. We give prices as approximate ranges, say when we last checked, and always recommend confirming with the operator before you travel.</p>
<h2>Independence</h2><p>We do not accept payment for favourable coverage. If we ever publish sponsored content it will be clearly labelled.</p>
<h2>Corrections and updates</h2><p>When we get something wrong we fix it and update the article date. Tell us via the <a href="/contact/">contact form</a>.</p>
<h2>Live headlines</h2><p>Our live news wire shows headlines gathered automatically from other publishers through Google News. We do not edit those headlines; each links to its original source.</p>
<h2>Health and money topics</h2><p>Health and finance articles are general information, not professional advice. Talk to a doctor or a licensed adviser about your own situation.</p>
<h2>Photos</h2><p>Most photos are used under Creative Commons or public-domain licences and credited on the page and on our <a href="/photo-credits/">photo credits</a> page.</p>''')

    faqs = [
        ("What is Cebu-Davao?", "An independent news, travel, food and lifestyle site focused on Cebu and Davao, with guides to the rest of the Philippines."),
        ("Is the weather forecast official?", "No. Our forecasts come from global weather models via Open-Meteo. For official warnings and typhoon signals, always follow PAGASA and your local government."),
        ("Where do the live headlines come from?", "They are gathered automatically from news publishers through Google News and link to the original stories."),
        ("Are the prices in your guides exact?", "No — they are approximate planning ranges. Fares, fees and room rates change often, so confirm with the operator."),
        ("Can I suggest a story or a correction?", "Yes, please use our contact form. We read every message."),
        ("Do you have a newsletter?", "Yes — subscribe with the form at the bottom of any page to get a weekly round-up."),
        ("What happened to the older articles?", "We rebuilt our most-read guides with fully updated information at the same addresses. Outdated posts now point to the homepage or to the closest updated guide."),
    ]
    inner = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs)
    S("/faqs/", "Frequently Asked Questions", "Frequently Asked Questions",
      "Answers to common questions about Cebu-Davao: our weather data, live headlines, price estimates, corrections and newsletter.",
      inner, ld_extra=[{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}])

    S("/privacy-policy/", "Privacy Policy", "Privacy Policy",
      "How Cebu-Davao handles personal data from visitors, the contact form and the newsletter, in line with the Philippine Data Privacy Act.",
      f'''<p>Last updated: {TODAY}. This policy explains what personal data cebudavao.com collects and how we use it, consistent with the Philippine Data Privacy Act of 2012 (Republic Act No. 10173).</p>
<h2>What we collect</h2><ul><li><b>Contact form:</b> your name, email address and message, used only to reply to you.</li><li><b>Newsletter:</b> your email address, used only to send the newsletter. Every email has an unsubscribe option, or contact us to be removed.</li>
<li><b>Server logs:</b> our host records standard technical data (IP address, browser, pages requested) for security and to keep the site running.</li></ul>
<h2>Cookies and local storage</h2><p>We do not use advertising cookies. Your browser stores a few preferences locally — dark mode, temperature units, your packing checklist ticks and cached weather data. They never leave your device.</p>
<h2>Third-party services</h2><p>Pages load fonts from Google Fonts. The weather tool requests forecasts from Open-Meteo, the currency converter loads rates from ExchangeRate-API, and the location button (only if you press it) shares your approximate coordinates with Open-Meteo to fetch your local forecast. Share buttons open the respective social network only when clicked.</p>
<h2>Your rights</h2><p>You may ask to access, correct or delete the personal data we hold about you. Email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</p>''')

    S("/terms/", "Terms of Use", "Terms of Use",
      "Terms of use for cebudavao.com: content, tools, accuracy, links and liability.",
      f'''<p>Last updated: {TODAY}. By using cebudavao.com you agree to these terms.</p>
<h2>Content</h2><p>Articles are for general information. Prices, schedules and rules change; confirm with official sources before relying on them. Health, legal and finance content is not professional advice.</p>
<h2>Tools</h2><p>Weather forecasts, exchange rates, distances and budget estimates are provided as-is, may be inaccurate or delayed, and must not be used for safety-critical decisions. Follow PAGASA and local authorities in severe weather.</p>
<h2>Copyright</h2><p>Text © {SITE["name"]}. Photos belong to their credited authors and are used under the licences shown. You may quote short excerpts with a link back.</p>
<h2>External links</h2><p>We link to other websites for convenience and are not responsible for their content.</p>
<h2>Contact</h2><p><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></p>''')

    rows = []
    for key, p in sorted(photos.items()):
        rows.append(f'<tr><td><img src="/assets/img/photos/{key}-sm.webp" alt="" width="96" height="64" loading="lazy"></td><td>{esc(p["title"])}</td>'
                    f'<td>{esc(p["author"])}</td><td><a href="{esc(p["source"])}" target="_blank" rel="noopener">{esc(p["license"])}</a></td></tr>')
    S("/photo-credits/", "Photo Credits", "Photo Credits",
      "Credits and licences for the Creative Commons and public-domain photographs used on Cebu-Davao.",
      '<p>We are grateful to the photographers who share their work on Wikimedia Commons. Each image below is used under the licence shown; follow the link for the original file and full licence terms. Images may be resized and cropped.</p>'
      '<div class="table-wrap"><table class="credits"><thead><tr><th>Image</th><th>Title</th><th>Author</th><th>Licence</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")

    groups = []
    for slug, (name, _d, _c) in categories.items():
        items = sorted([p for p in posts if p["category"] == slug], key=lambda p: p["title"])
        if items:
            groups.append(f'<h2><a href="{cat_url(slug)}">{esc(name)}</a></h2><ul class="link-cols">' + "".join(f'<li><a href="{p["path"]}">{esc(p["title"])}</a></li>' for p in items) + "</ul>")
    S("/sitemap/", "Sitemap", "Sitemap", "Every article, guide and tool on Cebu-Davao in one list.",
      '<p>Also see <a href="/tools/">reader tools</a>, <a href="/weather/">weather forecasts</a> and <a href="/news/">live news</a>.</p>' + "".join(groups))

    # Blog redirect convenience page for old WP "/blog/" handled by build.blog_index.
    body = '''<section class="page-hero"><div class="wrap"><h1>Page not found</h1><p class="lede">Sorry — that page doesn't exist or has moved. Try a search, or start from one of these.</p>
<form class="search-page-form" action="/search/" role="search"><label class="sr" for="q404">Search</label><input id="q404" type="search" name="q" placeholder="Search Cebu-Davao"></form></div></section>
<div class="wrap"><div class="tool-grid"><a class="tool-tile" href="/cebu/"><b>Cebu guide</b><span>Travel, food, news</span></a><a class="tool-tile" href="/davao/"><b>Davao guide</b><span>Samal, Mount Apo, durian</span></a>
<a class="tool-tile" href="/weather/"><b>Weather</b><span>Live and 7-day forecasts</span></a><a class="tool-tile" href="/news/"><b>Live news</b><span>Today's headlines</span></a></div></div>'''
    write("/404.html", page("/404.html", "Page not found", "The page you were looking for could not be found.", body, robots="noindex, follow"))
    return urls
