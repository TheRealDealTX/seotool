"""Company and legal pages, consumed by build.build_prose() as plain dicts.

/about/, /how-it-works/, /faqs/, /areas/, /privacy-policy/, /terms-of-use/.
"""

from siteconfig import BIZ, TEXAS_REGIONS, US_REGIONS, TOOLS, SERVICES

PHONE = BIZ["phone_display"]
EMAIL = BIZ["email"]
REVIEW = BIZ["price_claim_review"]
SCOPE = BIZ["price_scope"]
ADDR = f'{BIZ["street"]}, {BIZ["city"]}, {BIZ["state"]} {BIZ["zip"]}'

# Small inline icons (same stroke style as build.icon) so this module stays
# independent of build.py's globals.
_ICO = {
    "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    "map": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15"/><path d="M15 6v15"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8"/><path d="M8 11h.01"/><path d="M12 11h.01"/><path d="M16 11h.01"/><path d="M8 15h.01"/><path d="M12 15h.01"/><path d="M16 15v3"/>',
    "hardhat": '<path d="M3 18h18"/><path d="M5 18v-3a7 7 0 0 1 14 0v3"/><path d="M10 8V5h4v3"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "clip": '<path d="M9 4h6v3H9z"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2"/><path d="M9 12h6"/><path d="M9 16h4"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
}


def ico(name):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{_ICO[name]}</svg>')


def checks(items):
    return '<ul class="check-list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def tool_link(slug):
    t = next(t for t in TOOLS if t["slug"] == slug)
    return f'<a href="/tools/{slug}/">{t["name"]}</a>'


# --------------------------------------------------------------------------
# /about/
# --------------------------------------------------------------------------

ABOUT_BODY = f"""
<h2 id="who-we-are">Who we are</h2>
<p>Roof Estimate Pro is a roof estimating company. We build line-item roof estimates, claim estimate reviews and scopes
of damages for roofing contractors, public adjusters, desk and independent adjusters, property managers and
homeowners. We also publish a set of <a href="/tools/">free roof estimating calculators</a> that anyone can use without
signing up.</p>
<p>That is the whole business: estimates. We prepare estimates and scopes; we don't sell roofs, install roofs or take a
cut of anyone's roofing job. An estimate from us is about what the roof needs and what that work costs, not about
closing a sale.</p>

<h2 id="why-the-tools">Why we give the tools away</h2>
<p>Most online roof calculators ask for a ZIP code and an email address, then return one number with no explanation.
That number is not much use to a contractor checking a bid, an adjuster sanity-checking a claim, or a homeowner trying
to understand a carrier's check.</p>
<p>Our calculators work the way an estimator works. They show the line items, the quantities and the math; every unit
price can be edited; and the results can be printed, saved as a PDF or shared by link. The {tool_link("roof-replacement-cost-calculator")}
itemizes tear-off, materials, labor, decking, permits and overhead and profit. The {tool_link("roof-insurance-claim-calculator")}
walks from replacement cost to the first check, the depreciation holdback and your out-of-pocket. The
{tool_link("roofing-bid-calculator")} shows why markup and margin are not the same number.</p>
<p>Plenty of people will use the tools and never need us. That is fine. When a roof is complicated, a claim is
contested or the number has to hold up in front of someone else, the same tools have a button that sends your inputs
straight to an estimator.</p>

<h2 id="texas-first">Texas first, other states welcome</h2>
<p>We are based in Dallas, and most of our work is in Texas: hail in Dallas–Fort Worth, the Panhandle and Central Texas;
hurricanes and tropical storms on the Gulf Coast and in the Rio Grande Valley; trees and humidity in East Texas. Our
calculators default to Texas 2026 pricing with regional factors for each part of the state. See the <a
href="/areas/">service areas page</a> for what we see region by region.</p>
<p>Because the work is remote, location is not a limit. We prepare estimates for properties in other states as well,
priced for that property's market, and the calculators include regional price factors for other parts of the U.S.</p>

<h2 id="how-we-work">How we work</h2>
<p>Everything is done remotely. Clients send photos, measurement reports (EagleView, Hover, GAF QuickMeasure, Roofr and
similar), drone images, carrier estimates and notes through our <a href="/get-estimate/">estimate form</a> or by email.
An estimator reconciles the measurements against the photos, writes every line item the roof calls for, and prices it
for the property's location. If something can't be confirmed from the files, the estimate says so rather than
guessing quietly.</p>
<p>Two services have fixed prices: a <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> is
${REVIEW} per claim, and a <a href="/services/scope-of-damages/">scope of damages</a> is ${SCOPE} per property. Full
<a href="/services/xactimate-roof-estimates/">residential</a> and <a
href="/services/commercial-roof-estimates/">commercial</a> estimates are quoted per project before any work starts. <a
href="/how-it-works/">How it works</a> walks through each process step by step.</p>

<h2 id="what-we-dont-do">What we don't do</h2>
<p>Being clear about this saves everyone time:</p>
<ul>
<li><strong>We are not a roofing contractor.</strong> We don't bid, sell or install roofing work.</li>
<li><strong>We are not a law firm,</strong> and nothing we produce is legal advice.</li>
<li><strong>We don't decide coverage.</strong> Our estimates and scopes describe the roof and the cost of the work.
What a policy pays is determined by the policy, the carrier and, if it comes to that, appraisal or the courts.</li>
<li><strong>We don't negotiate claims or contact carriers on your behalf.</strong> In Texas, representing an insured on
a claim is the job of a licensed public adjuster or an attorney. We prepare the documents they, or you, can use.</li>
<li><strong>We don't inspect properties in person.</strong> Our work is built from the photos, reports and information
you provide.</li>
</ul>

<h2 id="contact">Contact</h2>
<p>Call or text <a href="tel:{BIZ['phone_href']}">{PHONE}</a>, email <a href="mailto:{EMAIL}">{EMAIL}</a>, or send the
details through the <a href="/get-estimate/">estimate request form</a>. Our mailing address is {ADDR}.</p>
"""

ABOUT = {
    "path": "/about/",
    "title": "About Roof Estimate Pro: Estimators & Free Roof Tools",
    "description": "Roof Estimate Pro builds line-item roof estimates, claim reviews and scopes for Texas and other states, and publishes free roof estimating calculators.",
    "h1": "About Roof Estimate Pro",
    "kicker": "About us",
    "lede": "We are roof estimators. We build line-item estimates, claim estimate reviews and scopes of damages for contractors, adjusters and property owners, and we publish free calculators that work the way an estimator works.",
    "body": ABOUT_BODY,
    "schema_type": "AboutPage",
    "active": "/about/",
    "crumb": "About",
    "priority": "0.5",
}

# --------------------------------------------------------------------------
# /how-it-works/
# --------------------------------------------------------------------------


def _steps(items):
    out = []
    for i, (h, p) in enumerate(items):
        out.append(f'<div class="step" data-reveal style="--d:{i * 0.06:.2f}s"><h3>{h}</h3><p>{p}</p></div>')
    return '<div class="steps">' + "".join(out) + "</div>"


HOW_HTML = f"""<section class="section section--paper" id="free-tools"><div class="wrap">
  <div class="section-head"><span class="kicker">Path 1 · Free</span><h2>Use the free tools</h2>
    <p>No account, no email address. Your inputs stay in your browser.</p></div>
  {_steps([
      ("Pick a tool", 'Twelve calculators cover cost, measurement, materials, insurance and bidding. Start with the <a href="/tools/">tools hub</a> or the ' + tool_link("roof-replacement-cost-calculator") + '.'),
      ("Enter measurements", 'Footprint and pitch, plane-by-plane areas, or the totals from a measurement report. The ' + tool_link("roof-square-footage-calculator") + ' and ' + tool_link("roof-pitch-calculator") + ' help when you are starting from a tape measure.'),
      ("Edit the prices", "Every unit price is a starting point for Texas 2026, adjusted for the region you pick. Contractors can enter their own costs; everyone can see what drives the total."),
      ("Print, share or send", 'Print or save as PDF, copy a share link that rebuilds the same estimate, or send the results to an estimator, who sees exactly what you entered.'),
  ])}
</div></section>
<section class="section" id="professional-estimate"><div class="wrap">
  <div class="section-head"><span class="kicker">Path 2 · Professional</span><h2>Have an estimator build it</h2>
    <p>For claims, bids, budgets and disputes, when the number has to hold up in front of someone else.</p></div>
  {_steps([
      ("Send details and files", 'Use the <a href="/get-estimate/">estimate request form</a>: address, roof type, what the estimate is for, and photos, measurement reports or the carrier estimate.'),
      ("We review and measure", "We check the files, reconcile the measurement report against the photos, ask for anything missing, and confirm the price and a delivery time."),
      ("We write the line items", "Every line the roof calls for, in the format carriers use, with quantities, units and pricing for the property's market."),
      ("You review, we revise", "Questions and corrections are part of the job. If you change the scope, we tell you before anything changes in price."),
  ])}
</div></section>
<section class="section section--dark" id="claims-and-scopes"><div class="wrap">
  <div class="section-head"><span class="kicker">Fixed-price services</span><h2>Claim reviews and scopes</h2>
    <p>Two services with set prices, both paid by secure Stripe checkout after you submit.</p></div>
  <div class="grid grid--2">
    <div class="card card--dark" data-reveal><span class="ico">{ico('search')}</span>
      <h3>Claim estimate review · ${REVIEW} per claim</h3>
      <ol class="check-list">
        <li>Submit the claim on the <a href="/claim/">claim form</a> with the full carrier estimate (PDF or ESX) and your photos.</li>
        <li>Pay the ${REVIEW} review fee by Stripe checkout.</li>
        <li>An estimator compares the estimate to the roof line by line: quantities, missing items, labor charges and code items.</li>
        <li>You get a written list of what is missing or short, with quantities and reasons, ready to forward.</li>
      </ol>
      <p style="margin-top:16px"><a class="btn btn--peach btn--sm" href="/claim/">Submit a claim {ico('arrow')}</a></p></div>
    <div class="card card--dark" data-reveal style="--d:.08s"><span class="ico">{ico('clip')}</span>
      <h3>Scope of damages · ${SCOPE} per property</h3>
      <ol class="check-list">
        <li>Choose: build your own scope on <a href="https://pascope.com/" rel="noopener" target="_blank">PAscope.com</a>, or order a professional scope from us.</li>
        <li>To order, use the <a href="/get-a-scope/">scope form</a>: address, type of damage, cause of loss, photos and measurements.</li>
        <li>Pay the ${SCOPE} fee by Stripe checkout.</li>
        <li>You get an itemized scope by roof area, elevation and room, with quantities, repair methods and cause-of-loss notes.</li>
      </ol>
      <p style="margin-top:16px"><a class="btn btn--peach btn--sm" href="/get-a-scope/">Get a scope {ico('arrow')}</a></p></div>
  </div>
</div></section>
<section class="section"><div class="wrap"><div class="article-layout">
  <article class="prose">
    <h2 id="which-path">Which path is right for you?</h2>
    <p><strong>Use the free tools</strong> when you want a planning number: budgeting a re-roof, checking whether a bid is in
    the right range, figuring out how many bundles to order, or seeing how depreciation and a deductible turn into the
    check you will actually receive. The tools are complete enough to stand on their own.</p>
    <p><strong>Order a ${REVIEW} claim review</strong> when you already have the carrier's estimate and it looks short. It
    is the fastest way to find out exactly which items and quantities are missing.</p>
    <p><strong>Order a ${SCOPE} scope</strong> when there is no estimate yet, the claim was denied, or you want your own
    record of the damage before the inspection or appraisal.</p>
    <p><strong>Request a full estimate</strong> when you need a priced, line-item document for a claim, a supplement, a
    bid, a capital budget or a dispute. Full <a href="/services/xactimate-roof-estimates/">residential</a> and <a
    href="/services/commercial-roof-estimates/">commercial</a> estimates are quoted per project before any work starts.</p>

    <h2 id="files">What files help most</h2>
    <ul>
      <li><strong>Photos:</strong> every slope and elevation, then close-ups of damage, flashing, vents, pipe jacks,
      valleys and the roof edge (to show layers and drip edge).</li>
      <li><strong>Measurements:</strong> an EagleView, Hover, GAF QuickMeasure, Roofr or drone report, or a sketch with
      pitches and lengths.</li>
      <li><strong>Carrier documents:</strong> the full estimate as PDF or ESX, plus any engineer report or denial letter.</li>
      <li><strong>Commercial roofs:</strong> roof plans, core-cut or moisture-survey results, and photos of parapets,
      curbs and drains.</li>
    </ul>
    <p>The forms accept up to 20 MB of attachments. For larger sets, email them to <a href="mailto:{EMAIL}">{EMAIL}</a>
    with the property address in the subject line.</p>

    <h2 id="timing">Timing and turnaround</h2>
    <p>Turnaround depends on the size of the property and how complete the files are. A single-slope repair and a
    multi-building commercial claim are not the same job. We confirm a delivery time when you order, and if we need
    something more from you, we ask right away instead of letting the job sit.</p>

    <h2 id="what-we-dont-do">What we don't do</h2>
    <p>We prepare estimates and scopes; we don't sell roofs, inspect properties in person, decide coverage or contact
    carriers on your behalf. Our documents are built for you, your contractor, your public adjuster or your attorney to
    use. More about us on the <a href="/about/">about page</a>.</p>
  </article>
  <aside class="article-side">
    <div class="side-card side-card--cta"><h3>Ready to send it over?</h3><p>Tell us about the roof and attach what you have. We will confirm price and timing first.</p><a class="btn btn--peach btn--sm" href="/get-estimate/">Request an estimate</a></div>
    <div class="side-card"><h3>Start here</h3><ul>
      <li><a href="/tools/">{ico('calc')}All free tools</a></li>
      <li><a href="/claim/">{ico('search')}Submit a claim (${REVIEW})</a></li>
      <li><a href="/get-a-scope/">{ico('clip')}Get a scope (${SCOPE})</a></li>
      <li><a href="/services/">{ico('hardhat')}All services</a></li>
    </ul></div>
  </aside>
</div></div></section>
"""

HOW_FAQS = [
    ("Do I need an account to use the tools?",
     "<p>No. The calculators are free and need no sign-up. Your inputs are saved in your own browser so you can come back to them, and nothing is sent to us unless you choose to send it.</p>"),
    ("What happens when I send tool results to an estimator?",
     "<p>The tool opens our <a href=\"/get-estimate/\">estimate request form</a> with your results and a link to your inputs attached to the message. You add contact details and anything else you know, then submit. Nothing is sent until you press submit.</p>"),
    ("How do I pay?",
     f"<p>The ${REVIEW} claim review and ${SCOPE} scope are paid by secure Stripe checkout after you submit the form. Full estimates are quoted first, and we confirm how to pay when you accept the quote.</p>"),
    ("Can I talk to someone before ordering?",
     f"<p>Yes. Call or text <a href=\"tel:{BIZ['phone_href']}\">{PHONE}</a> or email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. We can usually tell you on the first call which service fits and what files we will need.</p>"),
    ("What if my files are incomplete?",
     "<p>Send what you have. We will tell you what is missing and whether the job can be done without it. If a quantity can't be confirmed, the estimate notes it instead of guessing.</p>"),
]

HOW = {
    "path": "/how-it-works/",
    "title": "How It Works: Free Roof Tools & Pro Estimates | Roof Estimate Pro",
    "description": "Two ways to estimate a roof: use our free calculators and edit the prices, or send photos and measurements and have an estimator build a line-item estimate.",
    "h1": "How it works",
    "kicker": "Two paths",
    "lede": "Run the numbers yourself with free calculators, or send us the files and have an estimator build a line-item estimate, review a carrier's estimate or write a scope of damages.",
    "hero_extra": ('<div class="btn-row"><a class="btn btn--peach" href="#free-tools">Use the free tools</a>'
                   '<a class="btn btn--ghost-light" href="#professional-estimate">Get a professional estimate</a></div>'),
    "html": HOW_HTML,
    "faqs": HOW_FAQS,
    "active": "/how-it-works/",
    "crumb": "How it works",
    "priority": "0.6",
}

# --------------------------------------------------------------------------
# /faqs/
# --------------------------------------------------------------------------

FAQ_BODY = f"""
<p>Straight answers about our free tools, our professional services, pricing, coverage and how we handle your files.
Don't see your question? Call or text <a href="tel:{BIZ['phone_href']}">{PHONE}</a> or email
<a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>Jump to: <a href="/tools/">free tools</a> · <a href="/services/">services</a> · <a href="/how-it-works/">how it works</a>
· <a href="/areas/">service areas</a></p>
"""

FAQS = [
    # Tools
    ("Are the calculators really free?",
     "<p>Yes. All 12 <a href=\"/tools/\">calculators</a> are free, with no sign-up and no email required. We offer them because they are useful, and because some people who use them later need a professional estimate.</p>"),
    ("How accurate are the calculator results?",
     f"<p>They are planning figures, not quotes. Unit prices are Texas 2026 ranges adjusted by region, and every price can be edited. Accuracy depends mostly on your measurements: a roof measured from the ground with the wrong pitch can be off by several squares. The {tool_link('roof-pitch-calculator')} and {tool_link('roof-square-footage-calculator')} help get those right.</p>"),
    ("Can I save or share my results?",
     "<p>Yes. Inputs are saved in your browser automatically. Each tool can print or save a PDF, copy a share link that rebuilds the same estimate, or send the results to an estimator.</p>"),
    ("Can contractors use the tools with their own prices?",
     f"<p>Yes. Edit any unit price, waste factor or markup. The {tool_link('roofing-bid-calculator')} is built for pricing a job per square with overhead, profit and commission.</p>"),
    # Services
    ("What services do you offer?",
     f"<p>Line-item <a href=\"/services/xactimate-roof-estimates/\">residential roof estimates</a>, <a href=\"/services/commercial-roof-estimates/\">commercial roof estimates</a>, a ${REVIEW} <a href=\"/services/insurance-claim-estimate-review/\">claim estimate review</a> and a ${SCOPE} <a href=\"/services/scope-of-damages/\">scope of damages</a>. All are prepared remotely.</p>"),
    ("Are your estimates in Xactimate format?",
     "<p>Our estimates use Xactimate-style line items, in the format carriers use, so adjusters see familiar descriptions, units and organization. If you need a specific file type, ask when you order.</p>"),
    ("Are you a roofing company?",
     "<p>No. We prepare estimates and scopes; we don't sell or install roofs. We also don't decide coverage, give legal advice or negotiate with carriers on anyone's behalf.</p>"),
    ("Who are your clients?",
     "<p>Roofing contractors, public adjusters, desk and independent adjusters, homeowners, property managers, attorneys and appraisers. Anyone who needs a roof number that holds up in front of someone else.</p>"),
    # Pricing
    ("How much does a professional estimate cost?",
     f"<p>A claim estimate review is ${REVIEW} per claim. A professional scope of damages is ${SCOPE} per property. Full residential and commercial estimates are quoted per project, based on size and complexity, before any work starts.</p>"),
    ("How do I pay?",
     "<p>The claim review and scope are paid through secure Stripe checkout after you submit the form; we never see your full card number. For full estimates we confirm payment details with the quote. Have a discount code? There is a field for it on the claim and scope forms.</p>"),
    # Coverage
    ("Do you only work in Texas?",
     "<p>No. Texas is our focus, and we cover every region of the state, but we prepare estimates for properties in other states too, priced for that property's market. See <a href=\"/areas/\">service areas</a>.</p>"),
    ("Do you visit the property?",
     "<p>No. All work is remote, from photos, measurement reports, drone images and documents you send. That is what lets us work anywhere in Texas and beyond.</p>"),
    # Files
    ("What files do you accept?",
     f"<p>Photos (JPG, PNG, HEIC, WebP), PDFs, carrier estimates as PDF or ESX, measurement reports from EagleView, Hover and similar, spreadsheets, Word documents and ZIP files. The forms take up to 20 MB; email larger sets to <a href=\"mailto:{EMAIL}\">{EMAIL}</a>.</p>"),
    ("I don't have a measurement report. Can you still help?",
     "<p>Often, yes. A sketch with lengths and pitches works, and so do good photos combined with the footprint. If the roof can't be measured reliably from what you have, we will tell you before you pay for anything beyond what it needs.</p>"),
    # Turnaround
    ("How long does an estimate take?",
     "<p>It depends on the size of the property and how complete the files are. We confirm a delivery time when you order, before you commit.</p>"),
    # Privacy
    ("What do you do with my files and information?",
     "<p>We use them only to prepare your estimate, review or scope, and to contact you about it. We don't sell personal information. Calculator inputs stay in your browser unless you submit a form or share a link. Details in our <a href=\"/privacy-policy/\">privacy policy</a>.</p>"),
    ("Is a calculator result or your estimate an insurance determination?",
     "<p>No. Calculator results are planning figures. Our estimates and scopes document the roof and the cost of the work; what a policy pays is decided under the policy by the carrier, and disputes go to appraisal or the courts. For coverage questions, talk to your agent, a licensed public adjuster or an attorney.</p>"),
]

FAQ_PAGE = {
    "path": "/faqs/",
    "title": "Roof Estimate FAQs: Tools, Pricing & Claims | Roof Estimate Pro",
    "description": "Answers about our free roof calculators, $50 claim reviews, $200 scopes, full estimate pricing, files we accept, turnaround, coverage areas and privacy.",
    "h1": "Frequently asked questions",
    "kicker": "FAQs",
    "lede": "Tools, services, pricing, coverage and files: the questions we hear most, answered plainly.",
    "body": FAQ_BODY,
    "side": False,
    "faqs": FAQS,
    "schema_type": "WebPage",
    "crumb": "FAQs",
    "priority": "0.5",
}

# --------------------------------------------------------------------------
# /areas/
# --------------------------------------------------------------------------

TX_BORDER = [(-103.04, 36.5), (-100.0, 36.5), (-100.0, 34.56), (-99.2, 34.4), (-98.1, 34.13), (-97.2, 33.85), (-96.5, 33.8),
             (-95.5, 33.88), (-94.48, 33.64), (-94.04, 33.55), (-94.04, 33.02), (-94.04, 31.99), (-93.8, 31.5), (-93.55, 31.0),
             (-93.75, 30.3), (-93.84, 29.7), (-94.4, 29.55), (-94.9, 29.3), (-95.3, 28.95), (-96.0, 28.6), (-96.6, 28.3),
             (-97.0, 27.9), (-97.2, 27.6), (-97.4, 27.0), (-97.4, 26.4), (-97.15, 25.95), (-97.6, 26.0), (-98.2, 26.1),
             (-98.8, 26.4), (-99.2, 26.9), (-99.5, 27.5), (-100.1, 28.1), (-100.4, 28.6), (-100.9, 29.3), (-101.4, 29.77),
             (-102.0, 29.8), (-102.4, 29.77), (-102.7, 29.6), (-103.0, 29.0), (-103.3, 28.98), (-103.8, 29.3), (-104.4, 29.6),
             (-104.7, 30.2), (-105.0, 30.7), (-105.6, 31.1), (-106.2, 31.45), (-106.53, 31.78), (-106.62, 32.0), (-103.06, 32.0)]

# name, lon, lat, label side ("r" right / "l" left / "b" below), hub city (larger dot)
TX_CITIES = [
    ("Dallas", -96.80, 32.78, "l", True), ("Houston", -95.37, 29.76, "r", True), ("Austin", -97.74, 30.27, "l", True),
    ("San Antonio", -98.49, 29.42, "l", True), ("El Paso", -106.49, 31.76, "b", False), ("Lubbock", -101.86, 33.58, "r", False),
    ("Amarillo", -101.83, 35.22, "r", False), ("McAllen", -98.23, 26.20, "r", False), ("Corpus Christi", -97.40, 27.80, "r", False),
    ("Tyler", -95.30, 32.35, "r", False), ("Midland", -102.08, 31.99, "r", False),
]

K = 40


def _xy(lon, lat):
    return (lon + 106.7) * K, (36.6 - lat) * K * 1.17


def tx_map_svg():
    pts = [_xy(lo, la) for lo, la in TX_BORDER]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    dots = []
    for i, (name, lo, la, side, hub) in enumerate(TX_CITIES):
        x, y = _xy(lo, la)
        r = 6 if hub else 4.5
        if side == "r":
            tx, ty, anchor = x + 11, y + 5, "start"
        elif side == "l":
            tx, ty, anchor = x - 11, y + 5, "end"
        else:
            tx, ty, anchor = x + 2, y + 24, "start"
        delay = f"{(i * 0.37) % 2.6:.2f}s"
        dots.append(
            f'<g><circle class="ping" cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="animation-delay:{delay}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
            f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}"{" font-weight=\"700\"" if hub else ""}>{name}</text></g>')
    return f"""<svg class="tx-map" viewBox="-14 -14 580 530" role="img" aria-labelledby="txmap-t">
  <title id="txmap-t">Map of Texas showing the cities we serve, from El Paso to Tyler and Amarillo to McAllen</title>
  <defs>
    <linearGradient id="txfill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1fa59e" stop-opacity=".30"/><stop offset="1" stop-color="#007A75" stop-opacity=".08"/></linearGradient>
    <pattern id="txgrid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#9fd9d5" stroke-opacity=".10" stroke-width="1"/></pattern>
    <filter id="txglow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter>
  </defs>
  <path d="{d}" fill="#1fa59e" opacity=".35" filter="url(#txglow)"/>
  <path class="state" d="{d}" style="fill:url(#txfill)"/>
  <path d="{d}" fill="url(#txgrid)"/>
  {''.join(dots)}
</svg>"""


REGION_COPY = {
    "dfw": ("North Texas sits in the heart of hail alley. Spring supercells from March through June regularly drop hail large "
            "enough to bruise shingles and dent soft metals across Collin, Denton, Dallas and Tarrant counties, and a single "
            "storm can put thousands of claims into the system at once. We see a lot of Class 4 impact-resistant shingle "
            "estimates here, and a lot of carrier estimates written in a hurry."),
    "houston": ("On the Gulf Coast the threat is wind and water: hurricanes, tropical storms and the leaks they leave behind. "
                "Properties in the coastal counties covered by TWIA generally need a Texas Department of Insurance windstorm "
                "inspection on new roofing to stay eligible for that coverage, so the scope should account for windstorm-code "
                "details from the start. Heat and humidity also shorten the life of underlayment and sealants."),
    "central": ("Austin and the I-35 corridor get serious hail, often in the same spring storm systems that hit DFW, plus some of "
                "the hardest summer heat in the state, which ages asphalt shingles faster. Fast-growing suburbs mean many "
                "newer homes with HOA rules on roof color and material, which an estimate for a replacement has to respect."),
    "sa": ("San Antonio has a long history of damaging hailstorms, and the Hill Country mixes asphalt with standing seam metal, "
           "concrete and clay tile. Tile and metal need their own line items (underlayment, battens, trim, breakage allowance), "
           "and a shingle template applied to a tile roof is one of the most common under-scoping problems we see."),
    "south": ("In the Rio Grande Valley and along the South Texas coast, hurricanes and tropical storms bring the big claims, while "
              "year-round heat and humidity drive steady repair and replacement work. Low-slope and flat roofs are common on "
              "commercial buildings. Our cost tools apply a regional factor about 10% below the DFW baseline here."),
    "west": ("The Panhandle and South Plains see some of the most frequent large hail in the country, often with strong straight-line "
             "winds that lift and crease shingles. Wind-rated shingles, starter and proper nailing matter in estimates here. "
             "Farther west, El Paso and the Permian Basin add flat roofs with parapets, stucco and metal buildings to the mix."),
    "east": ("Piney woods mean tree damage: limbs and whole trees through roofs during storms, plus moss, algae and debris-clogged "
             "valleys in the humid climate. East Texas also gets tornadoes and the inland reach of Gulf storms. Tree claims need "
             "careful scoping of decking, framing and interior damage, not just shingles."),
}


def areas_html():
    regions = []
    for i, r in enumerate(TEXAS_REGIONS):
        cities = "".join(f"<li>{c}</li>" for c in r["cities"])
        regions.append(
            f'<div class="region" data-reveal style="--d:{i % 3 * 0.06:.2f}s"><h3>{ico("pin")}{r["name"]}</h3>'
            f'<p>{REGION_COPY[r["key"]]}</p><ul class="city-list">{cities}</ul></div>')
    us = []
    for r in US_REGIONS:
        pct = round((r["factor"] - 1) * 100)
        us.append(f'<li><span>{r["name"]}</span><b>{"+" if pct >= 0 else ""}{pct}%</b></li>')
    us_rows = "".join(
        f'<tr><td>{r["name"]}</td><td>{"+" if r["factor"] >= 1 else ""}{round((r["factor"] - 1) * 100)}% vs. DFW</td></tr>'
        for r in US_REGIONS)
    tx_rows = "".join(
        f'<tr><td>{r["name"]}</td><td>{"" if r["factor"] == 1 else ("+" if r["factor"] > 1 else "")}{"baseline" if r["factor"] == 1 else str(round((r["factor"] - 1) * 100)) + "% vs. DFW"}</td></tr>'
        for r in TEXAS_REGIONS)
    stats = (f'<div class="stats" style="margin-top:28px">'
             f'<div class="stat"><b>254</b><span>Texas counties</span></div>'
             f'<div class="stat"><b>{len(TEXAS_REGIONS)}</b><span>Texas pricing regions</span></div>'
             f'<div class="stat"><b>{len(US_REGIONS)}</b><span>U.S. pricing regions</span></div>'
             f'<div class="stat"><b><em>$0</em></b><span>Site visits needed</span></div></div>')
    return f"""<section class="section section--dark"><div class="wrap">
  <div class="split">
    <div data-reveal>
      <span class="kicker">Statewide coverage</span>
      <h2>From the Panhandle to the Valley</h2>
      <p class="lede" style="color:#b4c6c3">Every estimate is built remotely from photos, measurement reports and documents, so we
      work the same way in Amarillo as in Houston. What changes from region to region is the weather, the roofing and the claims.</p>
      <ul class="check-list">
        <li>Every Texas county, cities and rural properties alike</li>
        <li>Pricing set for the property's market, not ours</li>
        <li>Hail, wind, hurricane, tree and leak claims</li>
        <li>Residential and commercial, steep-slope and low-slope</li>
      </ul>
      <div class="btn-row" style="margin-top:24px"><a class="btn btn--peach" href="/get-estimate/">Request an estimate {ico('arrow')}</a>
        <a class="btn btn--ghost-light" href="/tools/">Try the free tools</a></div>
    </div>
    <div data-reveal style="--d:.1s">{tx_map_svg()}</div>
  </div>
  {stats}
</div></section>
<section class="section section--paper"><div class="wrap">
  <div class="section-head"><span class="kicker">Region by region</span><h2>What we see across Texas</h2>
    <p>The same shingle roof fails differently in Lubbock than in Galveston. Here is what drives roof estimates and claims in each part of the state.</p></div>
  <div class="grid grid--3">{''.join(regions)}</div>
</div></section>
<section class="section"><div class="wrap"><div class="article-layout">
  <article class="prose">
    <h2 id="outside-texas">Outside Texas</h2>
    <p>Texas is our focus, but it is not a boundary. Because every estimate is built from photos, measurement reports
    and documents, we prepare estimates, claim reviews and scopes for properties in other states too. Pricing is
    adjusted for the property's region: labor and material costs on the West Coast or in the Northeast run well above
    Texas, and the estimate reflects that.</p>
    <p>Our free calculators use the same regional factors, relative to the Dallas–Fort Worth baseline:</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Region</th><th>Price factor in our tools</th></tr></thead>
      <tbody>{us_rows}</tbody>
    </table></div>
    <p>These factors are starting points for planning. A professional estimate is priced for the specific property's market.
    The same ${REVIEW} <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> and ${SCOPE} <a
    href="/services/scope-of-damages/">scope of damages</a> prices apply in every state.</p>

    <h2 id="texas-pricing">Texas regional pricing</h2>
    <p>Inside Texas, the cost tools adjust the DFW baseline for each region. These reflect typical differences in labor
    and material costs; your contractor's actual prices may differ, and every unit price in the tools can be edited.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Texas region</th><th>Price factor in our tools</th></tr></thead>
      <tbody>{tx_rows}</tbody>
    </table></div>

    <h2 id="local-rules">Local rules worth checking</h2>
    <p>Permit requirements, permit fees and adopted building codes vary by city and county, and a few items vary by
    region: windstorm inspections in the TWIA coastal counties, HOA material rules in many suburbs, and how local
    code handles drip edge, underlayment and re-roofing over an existing layer. We note the items that apply in each
    estimate, but always check with the local building department before work starts.</p>
  </article>
  <aside class="article-side">
    <div class="side-card side-card--cta"><h3>Property outside Texas?</h3><p>Send the address and files the same way. We price for the property's market.</p><a class="btn btn--peach btn--sm" href="/get-estimate/">Request an estimate</a></div>
    <div class="side-card"><h3>Regional pricing in the tools</h3><ul>
      <li><a href="/tools/roof-replacement-cost-calculator/">{ico('calc')}Replacement Cost</a></li>
      <li><a href="/tools/roof-repair-cost-calculator/">{ico('calc')}Repair Cost</a></li>
      <li><a href="/tools/flat-roof-calculator/">{ico('calc')}Flat / Commercial</a></li>
      <li><a href="/tools/metal-roof-calculator/">{ico('calc')}Metal Roof</a></li>
    </ul></div>
  </aside>
</div></div></section>
"""


AREAS_FAQS = [
    ("Do you only work in Texas?",
     "<p>No. Texas is our focus and we cover the whole state, but we prepare estimates, claim reviews and scopes for properties in other states as well, priced for that property's market.</p>"),
    ("Do you need to visit the property?",
     "<p>No. All of our work is remote, from photos, measurement reports, drone images and documents. That is how we serve rural West Texas and out-of-state properties the same way we serve Dallas.</p>"),
    ("My city isn't listed. Can you still help?",
     "<p>Yes. The cities above are examples, not a limit. If the property is in Texas, or anywhere in the U.S., we can work on it.</p>"),
    ("Are prices different in different parts of Texas?",
     "<p>Yes. Labor and material costs vary by region, and our estimates and calculators account for it. The tools let you pick the region and edit every unit price.</p>"),
    ("Do you handle TWIA windstorm claims on the coast?",
     "<p>We prepare estimates, reviews and scopes for coastal wind claims, including properties insured through TWIA. We don't act as anyone's adjuster; coverage and claim questions belong with TWIA, your agent, a licensed public adjuster or an attorney.</p>"),
]

AREAS = {
    "path": "/areas/",
    "title": "Roof Estimating Across Texas and Beyond | Roof Estimate Pro",
    "description": "Remote roof estimates, claim reviews and scopes for every Texas region, from DFW and Houston to the Panhandle and the Valley, plus properties in other states.",
    "h1": "Roof estimating across Texas, and beyond",
    "kicker": "Service areas",
    "lede": "Texas is home and our focus: hail in DFW and the Panhandle, hurricanes on the Gulf Coast, heat and hail in Central Texas, trees in East Texas. We also prepare estimates for properties in other states.",
    "html": areas_html(),
    "faqs": AREAS_FAQS,
    "active": "/areas/",
    "crumb": "Service areas",
    "priority": "0.6",
}

# --------------------------------------------------------------------------
# Legal
# --------------------------------------------------------------------------

EFFECTIVE = "October 20, 2026"

PRIVACY_BODY = f"""
<p><strong>Effective date: {EFFECTIVE}</strong></p>
<p>This policy explains what information Roof Estimate Pro ("we", "us") collects through roofestimatepro.com, how we use
it and the choices you have. We have tried to write it in plain English. If anything is unclear, email
<a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

<h2 id="summary">The short version</h2>
<ul>
<li>The calculators run in your browser. What you type into them stays on your device unless you choose to submit a
form or share a link.</li>
<li>When you submit a form, we receive what you entered and any files you attach, and we use them to prepare your
estimate and contact you about it.</li>
<li>We don't sell your personal information, and we don't share it for advertising.</li>
<li>Payments are processed by Stripe. We never see or store your full card number.</li>
</ul>

<h2 id="calculators">Calculators and browser storage</h2>
<p>Our calculators save your inputs in your browser's local storage so they are still there when you come back. That
data stays on your device; it is not sent to us. You can clear it at any time by clearing your browser's site data for
roofestimatepro.com.</p>
<p>When you use a tool's share feature, your inputs are encoded into the link itself. Anyone you give that link to can
see those inputs, so share it with care. When you choose to send results to an estimator, the tool passes your
results to our estimate request form within your browser session; nothing reaches us until you submit that form.</p>

<h2 id="information-we-collect">Information we collect</h2>
<h3>Information you give us</h3>
<p>When you submit the estimate, claim or scope forms, or email or call us, we collect what you provide. That can
include your name, company, email, phone number, role, the property address, claim details (such as the insured's name,
claim number, carrier, date of loss and desk adjuster's email), a description of the project or damage, discount codes,
and attached files such as photos, measurement reports, carrier estimates and other documents. Please only send
information about other people (for example, an insured you represent) when you have the right to share it.</p>
<h3>Information collected automatically</h3>
<p>Like most websites, our hosting provider records standard server logs: IP address, browser type, the page requested,
the referring page and the time of the request. We use these logs to keep the site running, secure and free of abuse.
Our forms include basic spam protection that does not require tracking you.</p>
<h3>Cookies and analytics</h3>
<p>We don't use advertising or tracking cookies. We may use privacy-respecting analytics to understand which pages and
tools are used, in aggregate. If we add analytics, we will choose a service that does not build advertising profiles,
and we will update this policy.</p>

<h2 id="how-we-use">How we use information</h2>
<ul>
<li>To prepare the estimate, claim review or scope you requested, and to contact you about it.</li>
<li>To answer your questions and send quotes.</li>
<li>To process payment, through Stripe.</li>
<li>To keep records of the work we did for you, and for our legal, accounting and tax obligations.</li>
<li>To protect the site and our business from fraud, spam and abuse.</li>
</ul>
<p>We don't use your files or claim information for marketing, and we don't sell personal information to anyone.</p>

<h2 id="forms-and-files">How forms and files are handled</h2>
<p>When you submit a form, its contents and attachments are emailed to our team so an estimator can work on your
request. A copy of the text of each submission may also be kept on our server, outside the public website, as a backup
in case email delivery fails. Files are used only for the work you requested.</p>

<h2 id="sharing">When we share information</h2>
<p>We share information only:</p>
<ul>
<li>With service providers who help us run the business, such as our web host, email provider and Stripe for
payments, and only as needed for them to provide their service.</li>
<li>With people you direct us to share it with.</li>
<li>When required by law, subpoena or court order, or to protect our rights, property or safety, or that of others.</li>
<li>As part of a sale or transfer of our business, in which case this policy continues to apply to the information.</li>
</ul>
<p>The estimates and reviews we prepare are delivered to you. What you do with them, including sending them to a
carrier, contractor or adjuster, is up to you.</p>

<h2 id="payments">Payments</h2>
<p>Payments for the ${REVIEW} claim review, the ${SCOPE} scope and other services are processed by Stripe on its secure
checkout pages. Stripe collects and processes your payment details under its own privacy policy. We receive
confirmation of payment and basic details such as your name, email and amount, but not your full card number.</p>

<h2 id="retention">How long we keep information</h2>
<p>We keep form submissions, files and the work we produce for as long as needed to provide the service, respond to
follow-up questions and meet legal, tax and record-keeping obligations. When we no longer need it, we delete it or
keep it in a form that no longer identifies you.</p>

<h2 id="security">Security</h2>
<p>The site is served over HTTPS, and we limit access to submissions to the people who need them to do the work. No
method of transmission or storage is perfectly secure, so we can't guarantee absolute security. Please don't send
information we don't need, such as Social Security numbers or full bank account numbers.</p>

<h2 id="your-choices">Your choices and rights</h2>
<p>You can ask us to access, correct or delete the personal information we hold about you by emailing
<a href="mailto:{EMAIL}">{EMAIL}</a>. We will respond within a reasonable time and may need to verify your identity. We
may keep some information where the law requires it or where we need it to complete work you ordered. Depending on
where you live, you may have additional rights under state privacy laws; we will honor them as required.</p>

<h2 id="children">Children</h2>
<p>This site is intended for adults and businesses. We don't knowingly collect personal information from children
under 13. If you believe a child has sent us information, contact us and we will delete it.</p>

<h2 id="links">Links to other sites</h2>
<p>We link to other websites, such as PAscope.com and Stripe. Their privacy practices are their own; please read their
policies.</p>

<h2 id="changes">Changes to this policy</h2>
<p>We may update this policy. When we do, we will change the effective date at the top of this page. Significant
changes will be noted on the site.</p>

<h2 id="contact">Contact</h2>
<p>Roof Estimate Pro · {ADDR} · <a href="tel:{BIZ['phone_href']}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""

TERMS_BODY = f"""
<p><strong>Effective date: {EFFECTIVE}</strong></p>
<p>These terms govern your use of roofestimatepro.com, including our free calculators, and the estimating services you
order from Roof Estimate Pro ("we", "us"). By using the site or ordering a service, you agree to these terms. If you
don't agree, please don't use the site.</p>

<h2 id="what-we-provide">What we provide</h2>
<p>We provide free roof estimating calculators and paid estimating services: line-item residential and commercial roof
estimates, claim estimate reviews and scopes of damages. We are an estimating company. We are not a roofing contractor,
an insurance company, an insurance adjuster or a law firm, and we don't act as anyone's adjuster or representative
on an insurance claim.</p>

<h2 id="calculators">Calculator results are planning figures</h2>
<p>Results from the calculators are estimates for planning and education. They are not quotes, bids, offers to
perform work, appraisals or insurance determinations. They depend entirely on the inputs you enter and on default
prices that may not match any particular contractor, market or date. Always get a written bid from a qualified,
properly insured contractor before work begins, and check your local building code and permit requirements.</p>

<h2 id="services">Professional services</h2>
<ul>
<li><strong>Scope of work.</strong> We prepare estimates, reviews and scopes remotely, from the photos, measurements,
documents and information you provide. We don't inspect properties in person. The quality and completeness of our
work depends on what you send; where something can't be confirmed, we note it.</li>
<li><strong>Not insurance, legal or engineering advice.</strong> Our work documents the roof and the cost of the work. It
is not a coverage opinion, legal advice, an engineering report or a guarantee that any carrier, contractor or other
party will accept or pay any amount. For coverage questions, consult your policy, your agent, a licensed public
adjuster or an attorney.</li>
<li><strong>No guarantee of outcome.</strong> We don't guarantee any claim result, payment, settlement or appraisal
award.</li>
<li><strong>Turnaround.</strong> Delivery times depend on the project. We confirm an expected delivery time when you
order; it is an estimate, not a guarantee.</li>
<li><strong>Your responsibilities.</strong> You confirm that you have the right to share the information and files you
send us, including information about property owners or insureds you represent, and that it is accurate to the best
of your knowledge.</li>
</ul>

<h2 id="pricing-payment">Pricing and payment</h2>
<p>The claim estimate review is ${REVIEW} per claim and the scope of damages is ${SCOPE} per property, unless a different
price is shown when you order or a valid discount code applies. Full estimates are quoted per project before work
starts. Payments are processed by Stripe, and Stripe's terms apply to the payment transaction. Prices may change, but a
change won't affect work you have already ordered and paid for.</p>
<p>If we can't complete a paid service because the files you provide are not enough to do the work, we will tell you
what is missing. If the work can't be completed and we haven't started it, contact us about a refund. Once work has
been delivered, fees are generally non-refundable, but if you believe something is wrong with the work, tell us and we
will review it.</p>

<h2 id="use-of-work">Use of our work</h2>
<p>When you pay for a service, you may use the estimate, review or scope we deliver for the property and purpose it was
prepared for, including sharing it with a carrier, contractor, adjuster, appraiser or attorney. Our templates, methods,
the site's content and the calculators remain ours. Please don't copy, resell or republish the site's content or tools
without permission.</p>

<h2 id="acceptable-use">Acceptable use</h2>
<p>Don't use the site to break the law, submit false or misleading information, upload malware, interfere with the
site's operation, scrape it at scale, or send us information you are not allowed to share. We may refuse or stop
service to anyone who misuses the site or our services.</p>

<h2 id="third-parties">Third-party sites and services</h2>
<p>The site links to services we don't control, including PAscope.com for DIY scopes and Stripe for payments. Their
terms and policies apply to your use of them, and we are not responsible for their content or practices.</p>

<h2 id="disclaimers">Disclaimers</h2>
<p>The site and the calculators are provided "as is" and "as available". To the fullest extent the law allows, we
disclaim all warranties, express or implied, including warranties of merchantability, fitness for a particular purpose
and non-infringement. We don't warrant that the site will be uninterrupted or error-free, or that default prices or
other content are current or complete for your situation.</p>

<h2 id="liability">Limitation of liability</h2>
<p>To the fullest extent the law allows, we are not liable for indirect, incidental, special, consequential or punitive
damages, or for lost profits, revenue or claim payments, arising from your use of the site or our services. Our total
liability for any claim related to a paid service is limited to the amount you paid us for that service. Our total
liability for use of the free calculators and other free content is limited to $100.</p>

<h2 id="indemnity">Indemnity</h2>
<p>You agree to defend and indemnify us against claims arising from information or files you provided without the
right to share them, or from your misuse of the site or our work.</p>

<h2 id="governing-law">Governing law and disputes</h2>
<p>These terms are governed by the laws of the State of Texas, without regard to its conflict-of-law rules. Any dispute
will be brought in the state or federal courts located in Dallas County, Texas, and you and we consent to their
jurisdiction. Before filing anything, please contact us; most problems can be solved with a conversation.</p>

<h2 id="changes">Changes to these terms</h2>
<p>We may update these terms. The effective date at the top of this page shows when they last changed. Continued use
of the site after a change means you accept the updated terms; work already ordered stays under the terms in effect
when you ordered it.</p>

<h2 id="general">General</h2>
<p>If any part of these terms is found unenforceable, the rest stays in effect. Our failure to enforce a term is not a
waiver. These terms, together with our <a href="/privacy-policy/">privacy policy</a> and any quote you accept, are the
entire agreement between you and us about the site and our services.</p>

<h2 id="contact">Contact</h2>
<p>Roof Estimate Pro · {ADDR} · <a href="tel:{BIZ['phone_href']}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""

PRIVACY = {
    "path": "/privacy-policy/",
    "title": "Privacy Policy | Roof Estimate Pro",
    "description": "How Roof Estimate Pro handles calculator inputs, form submissions, uploaded files and payments. We don't sell personal information or use tracking cookies.",
    "h1": "Privacy policy",
    "kicker": "Legal",
    "lede": f"What we collect, how we use it and the choices you have. Effective {EFFECTIVE}.",
    "body": PRIVACY_BODY,
    "side": False,
    "no_cta": True,
    "crumb": "Privacy policy",
    "priority": "0.2",
}

TERMS = {
    "path": "/terms-of-use/",
    "title": "Terms of Use | Roof Estimate Pro",
    "description": "Terms for using Roof Estimate Pro's free roof calculators and paid estimating services: planning figures, pricing, payments, liability and Texas law.",
    "h1": "Terms of use",
    "kicker": "Legal",
    "lede": f"The rules for using our site, calculators and estimating services. Effective {EFFECTIVE}.",
    "body": TERMS_BODY,
    "side": False,
    "no_cta": True,
    "crumb": "Terms of use",
    "priority": "0.2",
}

PAGES = [ABOUT, HOW, FAQ_PAGE, AREAS, PRIVACY, TERMS]
