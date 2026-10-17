"""Home copy, tool pages and simple pages."""

from content.site import SITE

HOME_TITLE = "VIP Gifts – Luxury Gift Ideas & Curated Gift Guides | Shop VIP Gifts"
HOME_DESC = ("Shop VIP Gifts: curated VIP gift ideas and luxury gift guides for him, her, clients and the person who has "
             "everything — plus a free gift finder, budget planner and card message generator.")

HOME_FAQS = [
    ("What is a VIP gift?", "A VIP gift is a present that makes someone feel truly valued — personal to them, the best quality you can manage and beautifully presented. Read <a href=\"/blog/vip-gift-ideas-what-makes-a-gift-feel-vip/\">what makes a gift feel VIP</a>."),
    ("What are good VIP gift ideas for clients?", "Champagne with crystal flutes, executive gift boxes, engraved pens with leather journals and gourmet hampers are reliable client VIP gifts. See our <a href=\"/corporate-gifts/\">corporate gifts guide</a>."),
    ("Do I have to spend a lot on a VIP gift?", "Not at all. Our guide to <a href=\"/blog/luxury-gifts-under-100/\">luxury gifts under $100</a> shows how quality, personalization and presentation make modest gifts feel special."),
    ("How does the Gift Finder work?", "Answer four questions — who, occasion, budget and personality — and the <a href=\"/gift-finder/\">Gift Finder</a> scores more than 30 curated ideas and shows your six best matches."),
    ("Does Shop VIP Gifts sell products?", "We're an independent gift-ideas and gifting-advice site. We curate ideas, write guides and build free tools; we don't sell products directly."),
]


def chips(key, items, multi=False):
    return "".join(
        f'<button type="button" class="chip" aria-pressed="false" data-val="{v}">{e} {l}</button>' for v, l, e in items)


FINDER_HTML = f'''<div class="tool-shell overlap reveal in" data-gift-finder>
  <div class="progress" aria-hidden="true"><span></span></div>
  <div class="q-step active" data-key="who">
    <span class="eyebrow">Step 1 of 4</span>
    <h2>Who is the VIP?</h2>
    <p class="hint">Pick the person you're shopping for.</p>
    <div class="chip-group">{chips("who", [("partner", "Partner", "💞"), ("parent", "Parent", "🏡"), ("friend", "Friend", "🥂"), ("client", "Client", "🤝"), ("boss", "Boss / colleague", "💼"), ("host", "Host", "🕯️")])}</div>
  </div>
  <div class="q-step" data-key="occ">
    <span class="eyebrow">Step 2 of 4</span>
    <h2>What's the occasion?</h2>
    <p class="hint">This helps us weight celebratory vs. thank-you gifts.</p>
    <div class="chip-group">{chips("occ", [("birthday", "Birthday", "🎂"), ("anniversary", "Anniversary", "💍"), ("holiday", "Holiday", "🎄"), ("thankyou", "Thank you", "🙏"), ("milestone", "Milestone / promotion", "🏆"), ("justbecause", "Just because", "✨")])}</div>
  </div>
  <div class="q-step" data-key="budget">
    <span class="eyebrow">Step 3 of 4</span>
    <h2>What's your budget?</h2>
    <p class="hint">We'll prioritize ideas in your range and show a few just above it.</p>
    <div class="chip-group">{chips("budget", [("1", "Under $50", "💵"), ("2", "$50–$150", "💳"), ("3", "$150–$400", "💎"), ("4", "$400–$1,000", "👑"), ("5", "$1,000+", "🛥️")])}</div>
  </div>
  <div class="q-step" data-key="vibe" data-multi>
    <span class="eyebrow">Step 4 of 4</span>
    <h2>What are they into?</h2>
    <p class="hint">Choose up to three.</p>
    <div class="chip-group">{chips("vibe", [("foodie", "Food & drink", "🍷"), ("traveler", "Travel", "✈️"), ("techie", "Tech", "🎧"), ("homebody", "Home & cozy", "🛋️"), ("wellness", "Wellness", "🧖"), ("style", "Style & fashion", "👜"), ("professional", "Work & desk", "🖋️")])}</div>
  </div>
  <div class="q-step" data-key="results">
    <span class="eyebrow">Your matches</span>
    <h2>Six VIP gift ideas, ranked for you</h2>
    <p class="hint" data-summary></p>
    <div class="results-grid" data-results></div>
    <p style="margin-top:26px"><button type="button" class="btn btn-line" data-restart>↺ Start over</button></p>
  </div>
  <div class="q-nav">
    <button type="button" class="btn btn-line" data-back>← Back</button>
    <button type="button" class="btn btn-dark" data-next>Next →</button>
  </div>
</div>'''

BUDGET_HTML = '''<div class="tool-shell overlap reveal in" data-budget>
  <div class="budget-wrap">
    <div>
      <div class="field" style="max-width:280px">
        <label for="bp-total">Total gift budget ($)</label>
        <input id="bp-total" type="number" min="0" step="10" inputmode="decimal">
      </div>
      <label>Your gift list</label>
      <div class="rows"></div>
      <div class="msg-actions">
        <button type="button" class="btn btn-dark btn-sm" data-add>+ Add person</button>
        <button type="button" class="btn btn-gold btn-sm" data-auto>✦ Auto-split budget</button>
        <button type="button" class="btn btn-line btn-sm" data-copy>Copy list</button>
        <button type="button" class="btn btn-line btn-sm" data-clear>Clear</button>
      </div>
      <p style="font-size:.85rem;color:var(--muted);margin-top:14px">Auto-split weights closer relationships more heavily (partner 4×, parent/child 3×, sibling/client 2×, friend 1.5×, others 1×). Your list is saved in this browser only.</p>
    </div>
    <aside class="summary-card" aria-live="polite">
      <h3>Budget summary</h3>
      <div class="split-row"><span>Planned</span><span class="big-num" data-spent>$0</span></div>
      <div class="meter"><span></span></div>
      <p style="margin:0;font-size:.85rem;color:rgba(255,255,255,.7)" data-pct></p>
      <hr style="border:0;border-top:1px solid rgba(255,255,255,.12);margin:18px 0">
      <div class="split-row"><span><b data-left>$0</b> <span data-left-label>left to spend</span></span></div>
      <div class="split-row" style="margin-top:6px;font-size:.9rem;color:rgba(255,255,255,.75)"><span><b data-people>0</b> people</span><span>avg <b data-avg>$0</b></span></div>
      <div class="bars"></div>
    </aside>
  </div>
</div>'''

MSG_HTML = '''<div class="tool-shell overlap reveal in" data-msg>
  <div class="field"><label>Occasion</label>
    <div class="chip-group" data-group="occ">
      <button type="button" class="chip" aria-pressed="true" data-val="birthday">🎂 Birthday</button>
      <button type="button" class="chip" aria-pressed="false" data-val="anniversary">💍 Anniversary</button>
      <button type="button" class="chip" aria-pressed="false" data-val="holiday">🎄 Holiday</button>
      <button type="button" class="chip" aria-pressed="false" data-val="thankyou">🙏 Thank you</button>
      <button type="button" class="chip" aria-pressed="false" data-val="congrats">🏆 Congratulations</button>
      <button type="button" class="chip" aria-pressed="false" data-val="client">🤝 Client</button>
      <button type="button" class="chip" aria-pressed="false" data-val="wedding">💐 Wedding</button>
    </div>
  </div>
  <div class="field"><label>Tone</label>
    <div class="chip-group" data-group="tone">
      <button type="button" class="chip" aria-pressed="true" data-val="heartfelt">❤️ Heartfelt</button>
      <button type="button" class="chip" aria-pressed="false" data-val="witty">😄 Witty</button>
      <button type="button" class="chip" aria-pressed="false" data-val="formal">🎩 Formal</button>
    </div>
  </div>
  <div class="form-grid">
    <div class="field"><label for="mg-name">Their name</label><input id="mg-name" type="text" placeholder="e.g. Olivia" maxlength="40"></div>
    <div class="field"><label for="mg-from">Your name (optional)</label><input id="mg-from" type="text" placeholder="e.g. James" maxlength="40"></div>
  </div>
  <div class="msg-out" aria-live="polite"></div>
  <div class="msg-actions">
    <button type="button" class="btn btn-gold btn-sm" data-shuffle>↻ Another idea</button>
    <button type="button" class="btn btn-dark btn-sm" data-copy-msg>Copy message</button>
  </div>
</div>'''

ANNIV_HTML = '''<div class="tool-shell overlap reveal in" data-anniv>
  <form class="form-grid" data-anniv-form style="align-items:end">
    <div class="field"><label for="an-date">Wedding date</label><input id="an-date" type="date"></div>
    <div class="field"><label for="an-year">…or anniversary year</label><input id="an-year" type="number" min="1" max="75" placeholder="e.g. 10" inputmode="numeric"></div>
    <div class="field" style="grid-column:1/-1;margin:0"><button class="btn btn-dark" type="submit">Show my anniversary gifts</button></div>
  </form>
  <div class="years" role="group" aria-label="Choose an anniversary year"></div>
  <div data-anniv-card aria-live="polite"></div>
</div>'''

TOOL_PAGES = [
    dict(
        path="/gift-finder/", name="Gift Finder",
        title="Gift Finder Quiz – Find the Perfect VIP Gift in 60 Seconds | Shop VIP Gifts",
        desc="Free gift finder quiz: answer four questions about who it's for, the occasion, budget and interests to get six matched VIP gift ideas instantly.",
        eyebrow="Free tool · Gift Finder", h1='Gift Finder: the perfect VIP gift in <span class="shimmer">60 seconds</span>',
        lead="Four quick questions. Six ranked gift ideas from our curated guides. No sign-up, no email required.",
        image="gift-ribbon", tool_html=FINDER_HTML,
        content_html="""<h2>How the Gift Finder works</h2>
<p>Our Gift Finder scores more than thirty hand-picked gift ideas from our <a href="/gift-guides/">gift guides</a> against your answers. Who the gift is for and your budget carry the most weight, the occasion fine-tunes the list, and each interest you pick boosts ideas that match their personality.</p>
<p>The six highest-scoring ideas are shown with a match score, typical price range and a link to the guide where you'll find more context and presentation tips.</p>
<h2>Tips for better results</h2>
<ul>
<li><strong>Pick their interests, not yours.</strong> Think about how they spend a free Saturday.</li>
<li><strong>Be honest about budget.</strong> We'll still show one or two ideas slightly above it when they're a great fit.</li>
<li><strong>Run it twice.</strong> Try different interest combinations to explore new directions.</li>
</ul>
<p>Once you've chosen, make it VIP with a handwritten note — our <a href="/gift-message-generator/">gift message generator</a> can help.</p>""",
        faqs=[
            ("Is the Gift Finder free?", "Yes — completely free, with no sign-up or email required."),
            ("Where do the gift ideas come from?", "Every idea is drawn from our curated gift guides for him, her, clients, gift boxes, experiences and personalized gifts."),
            ("Can I buy the gifts here?", "Shop VIP Gifts is an ideas and advice site. Use the ideas to shop at your favorite retailers, boutiques or local makers."),
        ],
    ),
    dict(
        path="/gift-budget-planner/", name="Gift Budget Planner",
        title="Gift Budget Planner – Free Holiday Gift Budget Calculator | Shop VIP Gifts",
        desc="Free holiday gift budget planner and calculator: list everyone you're buying for, auto-split your budget by relationship and track what's left to spend.",
        eyebrow="Free tool · Budget planner", h1="Gift budget planner &amp; calculator",
        lead="List everyone you're buying for, set a total and let the planner split it fairly. Your list saves automatically in your browser.",
        image="gifts-stack", tool_html=BUDGET_HTML,
        content_html="""<h2>How to set a gift budget</h2>
<p>Start with a total you're genuinely comfortable spending — ideally decided before you start browsing. Then list everyone you're buying for, including the easy-to-forget people: hosts, teachers, neighbors, clients and colleagues.</p>
<p>Closer relationships usually get a larger share. The planner's <strong>auto-split</strong> button applies typical weights (a partner gets four shares, a parent or child three, siblings and clients two, friends one and a half, everyone else one), rounded to the nearest $5. Adjust any amount and the summary updates instantly.</p>
<h2>Typical gift spending by relationship</h2>
<div class="table-scroll"><table>
<tr><th>Relationship</th><th>Common range</th></tr>
<tr><td>Partner / spouse</td><td>$100–$500+</td></tr>
<tr><td>Parents and children</td><td>$50–$250</td></tr>
<tr><td>Siblings</td><td>$30–$100</td></tr>
<tr><td>Close friends</td><td>$25–$100</td></tr>
<tr><td>Clients</td><td>$30–$500 (by tier and policy)</td></tr>
<tr><td>Colleagues, hosts, teachers</td><td>$15–$50</td></tr>
</table></div>
<p>These are planning ranges, not rules — spend what's right for you. For holiday planning, follow our <a href="/blog/holiday-gift-planning-timeline/">holiday gift timeline</a>, and for ideas in every price band see <a href="/blog/luxury-gifts-under-100/">luxury gifts under $100</a>.</p>""",
        faqs=[
            ("Is my gift list stored anywhere?", "Only in your own browser's local storage on this device. Nothing is sent to us."),
            ("How does auto-split work?", "Each person gets a number of shares based on their relationship, and your total is divided proportionally, rounded down to the nearest $5."),
            ("Can I print or share my list?", "Use the Copy list button to copy a clean text version you can paste into notes, email or a spreadsheet."),
        ],
    ),
    dict(
        path="/gift-message-generator/", name="Gift Message Generator",
        title="Gift Message Generator – What to Write in a Gift Card | Shop VIP Gifts",
        desc="Free gift message generator: choose the occasion and tone (heartfelt, witty or formal), add a name and get ready-to-write gift card messages instantly.",
        eyebrow="Free tool · Message generator", h1="Gift message generator",
        lead="Pick an occasion and a tone, add their name, and get a polished card message in one tap. Shuffle for more ideas.",
        image="note-pen", tool_html=MSG_HTML,
        content_html="""<h2>Make the message your own</h2>
<p>Generated messages are a starting point. The most memorable cards add one specific detail only you could write — a shared memory, an inside joke, or why you chose this particular gift. Try the formula from our guide to <a href="/blog/what-to-write-in-a-gift-card/">what to write in a gift card</a>: open with them, say one specific thing, close with a wish.</p>
<h2>Choosing the right tone</h2>
<ul>
<li><strong>Heartfelt</strong> — partners, family, close friends and meaningful milestones.</li>
<li><strong>Witty</strong> — friends, siblings and anyone who'd rather laugh than cry.</li>
<li><strong>Formal</strong> — clients, colleagues, bosses and acquaintances.</li>
</ul>
<p>Then present it beautifully: heavyweight card, good pen, matching envelope. See <a href="/blog/how-to-wrap-gifts-like-a-luxury-boutique/">how to wrap like a luxury boutique</a>.</p>""",
        faqs=[
            ("How many messages are in the generator?", "Sixty-three — three for every combination of seven occasions and three tones — plus rotating sign-offs."),
            ("Can I use these messages for business gifts?", "Yes. Choose the Client occasion or the Formal tone for professional relationships."),
        ],
    ),
    dict(
        path="/anniversary-gifts-by-year/", name="Anniversary Gifts by Year",
        title="Anniversary Gifts by Year – Traditional & Modern Gift Chart | Shop VIP Gifts",
        desc="Interactive anniversary gifts by year chart: traditional, modern, gemstone and flower for years 1–60, with VIP gift ideas. Enter your wedding date to find yours.",
        eyebrow="Free tool · Anniversaries", h1="Anniversary gifts by year",
        lead="Enter your wedding date or tap a year to see the traditional and modern themes, gemstone, flower and VIP gift ideas.",
        image="anniversary", tool_html=ANNIV_HTML,
        content_html="""<h2>Where anniversary gift themes come from</h2>
<p>The tradition of assigning materials to wedding anniversaries dates back centuries, with silver (25 years) and gold (50 years) the oldest. In the 20th century, lists were expanded to cover each early year, and "modern" alternatives were introduced to give couples more choice. Gemstone and flower associations followed.</p>
<p>Lists vary slightly between sources, so treat them as inspiration rather than rules. The best anniversary gift still follows the VIP formula: personal, premium and beautifully presented.</p>
<h2>Using the themes creatively</h2>
<ul>
<li><strong>Paper (1st):</strong> a love letter, concert tickets, a framed map print.</li>
<li><strong>Leather (3rd):</strong> a monogrammed weekender or watch strap.</li>
<li><strong>Wood (5th):</strong> a custom keepsake box or planting a tree together.</li>
<li><strong>Pottery (9th):</strong> a pottery class for two.</li>
<li><strong>Silver (25th) and gold (50th):</strong> engraved heirlooms and a celebration with family.</li>
</ul>
<p>Browse more ideas in our <a href="/gifts-for-her/">gifts for her</a>, <a href="/gifts-for-him/">gifts for him</a> and <a href="/experience-gifts/">experience gifts</a> guides.</p>""",
        faqs=[
            ("What is the traditional 1st anniversary gift?", "Paper is the traditional first anniversary gift, and clocks are the modern alternative."),
            ("What is the 10th anniversary gift?", "Tin or aluminum is traditional; diamond jewelry is the modern choice."),
            ("What is the difference between traditional and modern anniversary gifts?", "Traditional themes are the older material associations, while modern themes were added later to offer more contemporary options. Many couples mix both."),
        ],
    ),
]

CONTACT_FORM = f'''<section class="section"><div class="wrap split" style="align-items:start">
  <div class="reveal">
    <span class="eyebrow">Get in touch</span>
    <h2>We'd love to hear from you</h2>
    <p>Questions about a gift guide, a suggestion for a VIP gift idea, a corporate gifting question or a partnership enquiry — send us a message and we'll reply as soon as we can.</p>
    <ul class="ticks">
      <li>Email: <a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
      <li>We aim to reply within two business days</li>
      <li>For corporate gifting advice, include your rough budget and timeline</li>
    </ul>
    <img src="/assets/img/gift-hands.webp" alt="Person holding a wrapped gift" width="1200" height="800" loading="lazy" style="border-radius:var(--radius);box-shadow:var(--shadow);margin-top:20px">
  </div>
  <form class="tool-shell reveal d1" action="/contact.php" method="post" data-ajax data-success="Thank you — your message is on its way. We'll reply soon.">
    <input type="hidden" name="form" value="contact">
    <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
    <div class="form-grid">
      <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
      <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="field"><label for="c-topic">Topic</label>
      <select id="c-topic" name="topic"><option>General question</option><option>Gift idea suggestion</option><option>Corporate gifting</option><option>Partnership</option><option>Feedback</option></select>
    </div>
    <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required></textarea></div>
    <button class="btn btn-gold" type="submit">Send message</button>
    <p class="form-note" aria-live="polite"></p>
  </form>
</div></section>'''

ABOUT = '''<section class="section"><div class="wrap split">
  <div class="split-media reveal">
    <img src="/assets/img/gifts-stack.webp" alt="Stack of colorfully wrapped presents" width="1200" height="800" loading="lazy">
    <img class="float-img" src="/assets/img/bouquet.webp" alt="Bouquet of roses and wildflowers" width="600" height="600" loading="lazy">
  </div>
  <div class="reveal d1">
    <span class="eyebrow">Our story</span>
    <h2>We believe everyone deserves to feel like a VIP</h2>
    <p>Shop VIP Gifts started with a simple frustration: too many gift lists are generic, recycled and built to sell whatever is in stock. We wanted a place that starts with the <em>person</em> — and helps you find something that makes them feel genuinely celebrated.</p>
    <p>Today we publish curated gift guides, in-depth gifting advice and free interactive tools for anyone who wants to give better: partners, parents, friends, and businesses thanking their clients and teams.</p>
  </div>
</div></section>
<section class="section dark"><div class="wrap">
  <div class="sec-head center reveal"><span class="eyebrow">Editorial standards</span><h2>How we choose what we recommend</h2></div>
  <div class="tiles">
    <div class="tile reveal"><h3>Independent</h3><p>We don't sell products, and brands can't pay to be included in our guides.</p></div>
    <div class="tile reveal d1"><h3>Quality first</h3><p>We favor materials, craftsmanship and longevity over logos and trends.</p></div>
    <div class="tile reveal d2"><h3>Every budget</h3><p>Every guide includes thoughtful options well under $100 alongside splurges.</p></div>
    <div class="tile reveal d3"><h3>Kept current</h3><p>Guides and price ranges are reviewed regularly. Prices are typical ranges, not quotes.</p></div>
  </div>
</div></section>
<section class="section"><div class="narrow" style="text-align:center">
  <div class="reveal"><span class="eyebrow">Say hello</span><h2>Have a gift idea we should feature?</h2>
  <p>We love hearing from readers, makers and gifting professionals.</p>
  <a class="btn btn-dark" href="/contact/">Contact us</a></div>
</div></section>'''

PRIVACY = f'''<section class="section"><div class="narrow prose">
<p><em>Last updated: October 17, 2026</em></p>
<p>This policy explains what information {SITE["name"]} ("we", "us") collects when you use shopvipgifts.com and how we use it.</p>
<h2>Information you give us</h2>
<p>If you use our contact form or join our email list, we receive the details you provide — typically your name, email address and message. We use this only to reply to you or to send the emails you requested. You can unsubscribe at any time by replying to any email or writing to <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</p>
<h2>Interactive tools</h2>
<p>Our Gift Finder, Gift Message Generator and Anniversary tool run entirely in your browser. The Gift Budget Planner saves your list in your browser's local storage on your device so it's there when you return; it is never sent to us. You can clear it with the planner's Clear button or by clearing your browser data.</p>
<h2>Automatically collected information</h2>
<p>Like most websites, our hosting provider may log technical information such as IP address, browser type and pages requested, for security and performance purposes. We do not use advertising cookies.</p>
<h2>Third-party services</h2>
<p>We load web fonts from Google Fonts, which may receive your IP address when fonts are requested. Links to other websites are provided for convenience; we are not responsible for their privacy practices.</p>
<h2>Sharing</h2>
<p>We do not sell or rent your personal information. We share it only with service providers who help us run the site (such as hosting and email) or where required by law.</p>
<h2>Your rights</h2>
<p>Depending on where you live, you may have rights to access, correct or delete your personal information. Contact us at <a href="mailto:{SITE["email"]}">{SITE["email"]}</a> and we'll respond promptly.</p>
<h2>Children</h2>
<p>This site is not directed at children under 13, and we do not knowingly collect their information.</p>
<h2>Changes</h2>
<p>We may update this policy from time to time. The date at the top shows when it was last revised.</p>
</div></section>'''

TERMS = f'''<section class="section"><div class="narrow prose">
<p><em>Last updated: October 17, 2026</em></p>
<p>By using shopvipgifts.com you agree to these terms.</p>
<h2>Informational content</h2>
<p>{SITE["name"]} publishes gift ideas, guides and tools for general information and inspiration. Price ranges are typical estimates and may differ from what you find at retailers. We don't sell products directly and are not responsible for third-party products, services or retailers.</p>
<h2>Tools</h2>
<p>Our interactive tools are provided "as is" for convenience. Budget figures, anniversary themes and generated messages are suggestions — please use your own judgement. Tax and gift-policy information is general and not professional advice.</p>
<h2>Intellectual property</h2>
<p>The text, design and code of this site belong to {SITE["name"]} unless otherwise stated. You may share links and short quotations with attribution, but may not republish whole articles without permission.</p>
<h2>Acceptable use</h2>
<p>Please don't misuse the site, attempt to disrupt it, or submit spam through our forms.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, {SITE["name"]} is not liable for any loss arising from your use of the site or reliance on its content.</p>
<h2>Contact</h2>
<p>Questions about these terms? Email <a href="mailto:{SITE["email"]}">{SITE["email"]}</a>.</p>
</div></section>'''

SIMPLE_PAGES = [
    dict(path="/about/", crumb="About", title="About Shop VIP Gifts – Curated Luxury Gift Ideas",
         desc="About Shop VIP Gifts: an independent gift-ideas site publishing curated VIP gift guides, gifting advice and free interactive gift tools.",
         eyebrow="About us", h1="About Shop VIP Gifts", lead="Curated gift ideas, honest advice and free tools — so every gift you give feels VIP.",
         image="gift-pattern", inner=ABOUT),
    dict(path="/contact/", crumb="Contact", title="Contact Shop VIP Gifts",
         desc="Contact Shop VIP Gifts at info@shopvipgifts.com with gift questions, suggestions, corporate gifting enquiries or partnership ideas.",
         eyebrow="Contact", h1="Contact us", lead=f'Email <a href="mailto:{SITE["email"]}" style="color:var(--gold-2)">{SITE["email"]}</a> or use the form below.',
         image="note-pen", inner=CONTACT_FORM,
         schema_extra=[{"@type": "ContactPage", "url": "https://shopvipgifts.com/contact/", "name": "Contact Shop VIP Gifts"}]),
    dict(path="/privacy-policy/", crumb="Privacy Policy", title="Privacy Policy | Shop VIP Gifts",
         desc="How Shop VIP Gifts collects, uses and protects your information, including our contact form, email list and browser-based gift tools.",
         eyebrow="Legal", h1="Privacy policy", lead="", image="gift-pattern", inner=PRIVACY),
    dict(path="/terms/", crumb="Terms of Use", title="Terms of Use | Shop VIP Gifts",
         desc="Terms of use for shopvipgifts.com, covering informational content, interactive tools, intellectual property and liability.",
         eyebrow="Legal", h1="Terms of use", lead="", image="gift-pattern", inner=TERMS),
]
