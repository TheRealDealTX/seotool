"""Hand-written site pages (about, contact, editorial and corrections policies)
plus additions appended to the imported WordPress legal pages."""

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_legacy = {p["slug"]: p for p in json.load(open(os.path.join(_HERE, "legacy_pages.json")))}

EMAIL = "info@renternews.net"

COVERAGE = [
    ("flame", "Fire & emergencies", "Apartment and multifamily fires, building emergencies, displacement and recovery.", "/news/category/fire/"),
    ("chart", "Rent & market", "Rent reports, vacancy, new supply and what it means for your next lease.", "/news/category/rent-prices/"),
    ("scale", "Tenant rights", "Court rulings, enforcement and plain-English explainers on renters' rights.", "/news/category/tenant-rights/"),
    ("landmark", "Housing policy", "Rent caps, eviction rules, vouchers and the programs that shape renting.", "/news/category/housing-policy/"),
    ("book", "Renter guides", "Sourced how-tos on insurance, deposits, repairs, scams and safety.", "/news/category/guides/"),
    ("cloud", "Tools & weather", "Free calculators and live local weather built for renters.", "/tools/"),
]

_cov = "".join(f'<a class="cov reveal" href="{h}"><span class="tool-ico">{{icon:{i}}}</span><strong>{t}</strong><span>{d}</span></a>'
               for i, t, d, h in COVERAGE)

PAGES = {
    "about": {
        "title": "About Us",
        "h1": "About Renter News",
        "description": "Renter News is an independent US news site covering apartment fires, renter safety, rent prices, tenant rights and housing policy.",
        "lede": "Independent news for the people who rent America's homes.",
        "html": f"""<div class="prose">{_legacy['about']['body_html']}</div>
<h2 class="h-section">What we cover</h2>
<div class="cov-grid">{_cov}</div>
<div class="prose">
<h2>How we report</h2>
<p>Our stories are built on named, checkable sources: fire department and police statements, court records, government data, Red Cross and city announcements, published market reports and reporting by local news outlets. Newer articles list their sources at the end, and every article shows when it was published and when it was last updated.</p>
<p>We do not accept payment for news coverage. Sponsored links, such as partner offers in our sidebar, are always labeled <em>Sponsored</em> and are kept separate from news content. Read the full <a href="/editorial-policy/">editorial policy</a> and our <a href="/corrections-policy/">corrections policy</a>.</p>
<h2>Contact the newsroom</h2>
<p>Tips, corrections and questions go to <a href="mailto:{EMAIL}">{EMAIL}</a> or through our <a href="/contact/">contact form</a>.</p>
</div>""",
        "schema": [{"@type": "AboutPage", "url": "https://renternews.net/about/", "name": "About Renter News",
                    "about": {"@id": "https://renternews.net/#organization"}}],
    },
    "contact": {
        "title": "Contact Us",
        "h1": "Contact Renter News",
        "description": "Contact the Renter News newsroom with story tips, corrections, questions or feedback.",
        "lede": "Have a question, a correction or a story tip? We read every message.",
        "html": f"""<div class="contact-grid">
<div class="prose">
<h2>Get in touch with Renter News</h2>
<p>Have a question, comment, or story to share? Whether you're seeking clarification on a news article, submitting a rental-related tip, or just want to connect with our team, use the form to reach out. Our editorial staff reviews every message and will respond as soon as possible.</p>
<ul class="contact-points">
<li><strong>News tips:</strong> tell us what happened, where and when, and how we can verify it.</li>
<li><strong>Corrections:</strong> link the article and tell us what is wrong. See our <a href="/corrections-policy/">corrections policy</a>.</li>
<li><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></li>
</ul>
</div>
<form class="contact-form" method="post" action="/contact.php" data-contact>
  <label>Name<input name="name" required maxlength="100" autocomplete="name"></label>
  <label>Email<input name="email" type="email" required maxlength="200" autocomplete="email"></label>
  <label>Topic<select name="topic"><option>News tip</option><option>Correction</option><option>Question</option><option>Advertising</option><option>Other</option></select></label>
  <label>Message<textarea name="message" required rows="6" maxlength="5000"></textarea></label>
  <label class="hp" aria-hidden="true">Leave blank<input name="website" tabindex="-1" autocomplete="off"></label>
  <button class="btn" type="submit">Send message</button>
  <p class="form-status" data-form-status aria-live="polite"></p>
</form>
</div>""",
        "schema": [{"@type": "ContactPage", "url": "https://renternews.net/contact/", "name": "Contact Renter News"}],
    },
    "editorial-policy": {
        "title": "Editorial Policy",
        "description": "How Renter News reports, sources, verifies, updates and labels its news coverage, and how we keep sponsored content separate.",
        "lede": "The standards behind every Renter News story.",
        "html": f"""<div class="prose">
<h2>Our mission</h2>
<p>Renter News reports on the events, data and decisions that affect people who rent their homes in the United States: apartment fires and building emergencies, rent prices, tenant rights and housing policy. We aim to be accurate, fair, clear and useful.</p>
<h2>Sourcing and verification</h2>
<ul>
<li>Facts about an incident (casualties, displacement figures, causes) come from official statements, public records or named news reports. When figures conflict or are preliminary, we say so.</li>
<li>We do not report the cause of a fire as settled until investigators have stated it.</li>
<li>We link to our sources. Newer articles carry a <em>Sources</em> list at the end.</li>
<li>We avoid naming victims who have not been publicly identified by authorities or their families.</li>
</ul>
<h2>Independence and sponsored content</h2>
<p>Coverage decisions are made by the editorial team alone. We do not accept payment for news coverage. Partner offers and advertising are labeled <em>Sponsored</em>, use sponsored links, and are kept separate from articles.</p>
<h2>Affiliate links</h2>
<p>Some pages include "Gear that could help" boxes with Amazon affiliate links to safety, emergency and moving products. As an Amazon Associate, Renter News earns from qualifying purchases. Editors choose which product types appear based on relevance to the story, never the other way around, and affiliate relationships do not influence our reporting.</p>
<h2>Bylines and dates</h2>
<p>Articles are published under the <a href="/news/author/renter-news-staff/">Renter News Staff</a> byline. Every article shows its publication date, and an update date when it has been materially changed.</p>
<h2>Guides and tools</h2>
<p>Renter guides explain general rules and point to official sources. Tenant law varies by state and city, so guides are not legal advice. Our calculators produce estimates for planning only, and run entirely in your browser.</p>
<h2>Corrections</h2>
<p>We correct errors promptly and transparently. See our <a href="/corrections-policy/">corrections policy</a>, or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div>""",
    },
    "corrections-policy": {
        "title": "Corrections Policy",
        "description": "How Renter News handles corrections, clarifications and updates, and how to report an error in one of our stories.",
        "lede": "When we get something wrong, we fix it and say so.",
        "html": f"""<div class="prose">
<h2>How to report an error</h2>
<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or use our <a href="/contact/">contact form</a> with the article link, the statement you believe is wrong, and any source that shows the correct information.</p>
<h2>What we do</h2>
<ul>
<li><strong>Corrections:</strong> when a factual error is confirmed, we fix the article and add a dated note at the end describing what changed.</li>
<li><strong>Clarifications:</strong> when an article is accurate but unclear or missing context, we revise it and note the clarification.</li>
<li><strong>Updates:</strong> developing stories are updated as officials release new information; the article's "Updated" date changes accordingly.</li>
</ul>
<p>We do not silently remove published articles. If a story must be withdrawn, we explain why on the page.</p>
</div>""",
    },
    "frequently-asked-questions-desc": "Answers to common questions about Renter News: what we cover, how stories are sourced and verified, sharing articles and sending tips.",
    "privacy-policy-desc": "How Renter News collects, uses and protects information, including the contact form, weather features, cookies and third-party embeds.",
    "terms-of-service-desc": "The terms that govern your use of the Renter News website, articles, calculators and other features.",
    "privacy-policy-append": """
<h2>9. Weather, maps and browser storage</h2>
<p>Our <a href="/weather/">live weather</a> page and the weather widget fetch forecasts, observations and alerts directly from your browser from the National Weather Service (api.weather.gov). If you choose "Use my location", your browser asks for permission and the coordinates are sent only to the National Weather Service, never to Renter News. The city you pick, your theme and your checklist progress are saved in your browser's local storage and can be cleared at any time in your browser settings.</p>
<p>The <a href="/fire-map/">fire map</a> loads map tiles from OpenStreetMap. Our calculators run entirely in your browser; the numbers you enter are not sent to us. Fonts are served by Google Fonts, and some older articles embed content from YouTube, Google Maps, X (Twitter) or Instagram, which may set their own cookies.</p>
<h2>10. Google Analytics</h2>
<p>We use Google Analytics to understand how readers use the site, such as which pages are visited and how people arrive. Google Analytics sets cookies and processes data under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's privacy policy</a>. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics opt-out browser add-on</a>.</p>
<h2>11. Sponsored and affiliate links</h2>
<p>Renter News is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate, Renter News earns from qualifying purchases. Amazon may use cookies to attribute purchases made after you follow one of our links. Partner offers labeled "Sponsored" link to third-party sites that may track the referral. Their privacy policies apply once you leave Renter News.</p>
""",
}
