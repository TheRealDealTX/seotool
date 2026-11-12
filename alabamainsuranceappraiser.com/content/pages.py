"""About, contact, FAQ, process, glossary, legal pages, HTML sitemap, thank-you and 404."""

import re

from components import (BIZ, CITIES, ORG_ID, RESOURCES, SERVICES, TOOLS, btn, call_btn, callout, card, checklist,
                        contact_form, fig, faq_html, faq_schema, grid, icon, kicker, section_head, steps_html,
                        table, url)
from content.posts import POSTS
from siteconfig import TODAY


def about():
    p = {
        "path": "/about-us/", "title": "About Alabama Insurance Appraiser | Who We Are",
        "description": "About Alabama Insurance Appraiser: independent property claim appraisal, estimating and documentation for home and commercial losses statewide.",
        "h1": "About Alabama Insurance Appraiser",
        "lead": "Independent property insurance appraisal, estimating and claim documentation for residential and commercial losses throughout Alabama.",
        "kicker": "Who we are", "hero_img": "residential", "nav_active": "/about-us/", "schema_type": "AboutPage",
        "crumbs": [("Home", "/"), ("About Us", "/about-us/")], "priority": "0.8",
    }
    p["body"] = f'''
<p class="lead-p">When a property claim comes down to a disagreement over the amount of loss, the details decide the outcome. Two estimates can differ because of scope, measurements, repair method, material pricing, labor, access or damage that one side simply missed. Our role is to look closely at those differences and develop a clear, well-supported valuation from the property and the evidence.</p>
<p>Alabama Insurance Appraiser has a simple focus: carefully evaluate the amount of property damage, and provide organized documentation that supports the appraisal process set out in the applicable insurance policy.</p>
<h2>Focused on the amount of loss</h2>
<p>Insurance appraisal is used when a policyholder and carrier disagree about the value of a property loss. That disagreement might involve roofing, siding, interior finishes, water damage, fire damage, commercial building components, labor costs or quantities. Usually it isn't one big issue but dozens of small ones spread across competing estimates. Our appraisal work is built around finding and evaluating each of them.</p>
<p>Depending on the assignment, we review:</p>
{checklist(["Insurance carrier estimates", "Contractor estimates", "Photographs and inspection reports", "Property measurements", "Repair quantities and sequencing",
            "Labor and material pricing", "Roofing and exterior components", "Interior finishes", "Commercial building systems", "Demolition and replacement requirements",
            "Xactimate and Symbility estimates", "Matterport scans", "Engineering and specialty reports", "Other claim correspondence"], "checklist two-col")}
<h2>A detailed approach to property appraisal</h2>
<p>Every property is different. A single-story home's roof needs a very different repair approach than a steep commercial roof. Water damage in one room is a different problem from a loss running through several floors of an apartment building. Fire and smoke can involve structural repair, cleaning, demolition, electrical work and extensive interior restoration. That's why effective appraisal means more than comparing final totals &mdash; it means examining the components behind the numbers.</p>
{fig("inspect", "Insurance appraiser documenting roof damage on an Alabama home", "We document the property ourselves rather than relying only on someone else's photos.")}
<h2>Residential and commercial experience</h2>
{grid([card("Residential", "Hail, wind, roof, storm, water, plumbing, fire, smoke, interior and exterior damage to homes, condos and rentals.", "/services/residential-property-appraisal/", "home"),
       card("Commercial", "Office, retail, apartments, churches, warehouses, industrial plants, restaurants and institutional buildings.", "/services/commercial-property-appraisal/", "building")], 2)}
<h2>Modern estimating and documentation tools</h2>
<p>Property appraisal is increasingly data-driven. We use <a href="/services/xactimate-estimates/">Xactimate</a> and <a href="/services/symbility-estimates/">Symbility</a> to break repair scope into individual line items, and <a href="/services/matterport-documentation/">Matterport</a> to create measurable 3D records of rooms, layouts and damage.</p>
<h2>Our principles</h2>
{grid([card("Evidence first", "Positions are built from the property and the documentation, not assumptions or generic figures.", None, "search"),
       card("Clarity", "We make valuation differences easier to understand, not the process more complicated.", None, "target"),
       card("Honesty", "If appraisal isn't the right tool for your situation, we'll tell you.", None, "shield")], 3)}
<h2>Serving property claims across Alabama</h2>
<p>Severe thunderstorms, tornadoes, hail, hurricanes, plumbing failures and fires create damage that varies widely from one property to the next. We take assignments statewide, including <a href="/service-areas/birmingham-al/">Birmingham</a>, <a href="/service-areas/huntsville-al/">Huntsville</a>, <a href="/service-areas/montgomery-al/">Montgomery</a>, <a href="/service-areas/mobile-al/">Mobile</a>, <a href="/service-areas/tuscaloosa-al/">Tuscaloosa</a> and the communities in between, urban and rural.</p>
<h2>Our commitment</h2>
<p>Property loss valuations should be supported by careful evaluation and organized documentation. Whether it's a residential roof, an interior water loss or a commercial storm claim, we approach the valuation by examining every component that contributes to the total repair cost &mdash; and we aim to provide clear, detailed and professional appraisal support for property owners and claim professionals throughout Alabama.</p>
'''
    return p


def contact():
    p = {
        "path": "/contact/", "title": "Contact Alabama Insurance Appraiser | (844) 537-1427",
        "description": "Contact Alabama Insurance Appraiser about a property claim dispute. Call (844) 537-1427, email us or send your claim details for a free consultation.",
        "h1": "Contact Alabama Insurance Appraiser",
        "lead": "Have a property claim with a disagreement over the amount of loss? Tell us about the property, the damage and where the claim stands.",
        "kicker": "Free claim conversation", "hero_img": "residential", "nav_active": "/contact/", "layout": "wide",
        "schema_type": "ContactPage", "crumbs": [("Home", "/"), ("Contact", "/contact/")], "cta": False, "priority": "0.8",
    }
    p["body"] = f'''
<section class="section section-white"><div class="container split" style="align-items:start">
  <div class="reveal">
    {kicker("Get in touch")}
    <h2>Talk with an appraiser</h2>
    <p>Whether you need insurance appraisal, a detailed estimate, Matterport documentation or help understanding the differences between two estimates, share a few details. We'll use them to understand the assignment and tell you how we can help.</p>
    <div class="contact-cards" style="margin:26px 0">
      <a class="contact-card" href="tel:{BIZ['phone_href']}"><span class="card-ico">{icon("phone")}</span><span><small>Phone</small><strong>{BIZ['phone_display']}</strong></span></a>
      <a class="contact-card" href="mailto:{BIZ['email']}"><span class="card-ico">{icon("mail")}</span><span><small>Email</small><strong>{BIZ['email']}</strong></span></a>
      <div class="contact-card"><span class="card-ico">{icon("map")}</span><span><small>Service area</small><strong>All of Alabama &mdash; 67 counties</strong></span></div>
    </div>
    {callout("<p>Submitting this form does not create an appraiser-client relationship or confirm acceptance of an assignment. Please don't send sensitive personal information such as Social Security or bank numbers.</p>", "info", "Before you send")}
    <h3>What helps us help you</h3>
    {checklist(["The property address or city", "Date and type of loss", "The carrier's estimate amount and your contractor's estimate amount", "Where the claim stands now (paid, supplemented, denied in part)"])}
  </div>
  <div class="form-shell reveal">{kicker("Send claim details")}<h2 class="h4">Tell us about your claim</h2>{contact_form()}</div>
</div></section>'''
    return p


FAQ_GROUPS = [
    ("Appraisal basics", [
        ("What is insurance appraisal?", "<p>A process in many property policies for resolving disagreements over the amount of loss. Each side picks an appraiser, the appraisers evaluate the loss, and an umpire resolves anything they can't agree on.</p>"),
        ("What does an Alabama Insurance Appraiser do?", "<p>Evaluates the disputed amount of loss: inspection, measurements, scope, pricing, competing estimates and the documentation that supports a valuation. See <a href='/what-does-an-insurance-appraiser-do/'>what does an insurance appraiser do</a>.</p>"),
        ("Is appraisal the same as arbitration?", "<p>No. Alabama courts treat appraisal as a contractual process distinct from arbitration, which is why the policy wording matters.</p>"),
        ("Does appraisal decide coverage?", "<p>Generally no. Appraisal addresses value. Coverage disputes usually call for legal advice.</p>"),
    ]),
    ("Starting appraisal", [
        ("How do I invoke appraisal?", "<p>Usually by written demand under the policy's appraisal provision. See our step-by-step guide on <a href='/how-to-invoke-the-appraisal-clause-in-alabama/'>invoking appraisal in Alabama</a>.</p>"),
        ("Are there deadlines?", "<p>Often. Many policies set a period (frequently 20 days) to name appraisers after a demand, and most set a deadline for filing suit. Check yours.</p>"),
        ("Can the carrier demand appraisal?", "<p>Under many policies, yes &mdash; either party can demand it.</p>"),
        ("What documents do I need?", "<p>The full policy, every estimate, photos, reports, payment letters and correspondence. Use our <a href='/tools/appraisal-readiness-checklist/'>readiness checklist</a>.</p>"),
    ]),
    ("Costs &amp; timing", [
        ("How much does an appraiser cost?", "<p>Fees depend on the size and complexity of the loss and are agreed in writing in advance. Each side usually pays its own appraiser and splits the umpire's fee.</p>"),
        ("How long does appraisal take?", "<p>Weeks for a well-documented residential claim; longer for large commercial losses. See <a href='/how-long-does-insurance-appraisal-take/'>how long appraisal takes</a>.</p>"),
        ("Is appraisal worth it for a small gap?", "<p>Often not. A supplement may be more efficient. Use the <a href='/tools/claim-gap-calculator/'>claim gap calculator</a> to frame the decision.</p>"),
    ]),
    ("Our services", [
        ("Do you handle commercial claims?", "<p>Yes &mdash; office, retail, multi-family, churches, industrial and institutional property.</p>"),
        ("Which estimating platforms do you use?", "<p>Xactimate and Symbility, plus Matterport for 3D documentation.</p>"),
        ("Where do you work?", "<p>Statewide, in all 67 Alabama counties. See our <a href='/service-areas/'>service areas</a>.</p>"),
        ("Do you work for contractors and attorneys?", "<p>Yes. We provide appraisal and estimating support to contractors, property managers and attorneys as well as policyholders.</p>"),
    ]),
]


def faq():
    allfaqs = [qa for _, g in FAQ_GROUPS for qa in g]
    p = {
        "path": "/faq/", "title": "Insurance Appraisal FAQ | Alabama Insurance Appraiser",
        "description": "Answers to common questions about property insurance appraisal in Alabama: how it works, deadlines, costs, timelines, umpires and our services.",
        "h1": "Insurance Appraisal FAQ", "lead": "Straight answers to the questions Alabama property owners ask most about appraisal.",
        "kicker": "Frequently asked questions", "hero_img": "inspect", "nav_active": "/blog/", "schema_type": "FAQPage",
        "crumbs": [("Home", "/"), ("FAQ", "/faq/")], "hero_actions": "", "priority": "0.7",
        "sidebar_title": "Helpful guides", "sidebar_links": [(q["h1"], f"/{q['slug']}/") for q in POSTS[:6]],
    }
    p["body"] = "".join(f"<h2>{g}</h2>{faq_html(items, open_first=False)}" for g, items in FAQ_GROUPS)
    s = faq_schema(p, allfaqs)
    s["@id"] = url("/faq/#faq")
    p["schema"] = [s]
    p["schema_type"] = "WebPage"
    return p


def process():
    steps = [
        ("Disagreement over the amount of loss", "The carrier accepts a covered loss, but after estimates, supplements and re-inspections, the two sides still disagree on what it's worth."),
        ("Read the appraisal provision", "Find out who can demand appraisal, whether the demand must be written, deadlines, appraiser qualifications and how costs and umpire selection work."),
        ("Send a written demand", "Invoke appraisal in writing, by a method that proves delivery, identifying the policy, claim and disagreement."),
        ("Each side names an appraiser", "Typically within the period the policy sets. Many policies require competent and impartial or disinterested appraisers."),
        ("The appraisers select an umpire", "If they can't agree in time, either side can usually ask a court to appoint one."),
        ("Inspection and evaluation", "The appraisers inspect, measure, review documentation and develop estimates."),
        ("Negotiation item by item", "Agreed items are set aside; disagreements narrow to specific line items."),
        ("Umpire resolves differences", "Unresolved items are submitted to the umpire with each side's support."),
        ("Award is signed", "Under many policies, an award signed by any two of the three sets the amount of loss."),
        ("Payment under the policy", "The carrier applies deductibles, prior payments and policy terms and pays according to the policy."),
    ]
    p = {
        "path": "/insurance-appraisal-process/", "title": "The Insurance Appraisal Process in Alabama, Step by Step",
        "description": "How Alabama insurance appraisal works: the dispute, written demand, appraisers and umpire, inspection, negotiation, award and payment.",
        "h1": "The Insurance Appraisal Process in Alabama",
        "lead": "Ten steps from a disputed estimate to a signed appraisal award &mdash; and what to watch for at each one.",
        "kicker": "Step-by-step guide", "hero_img": "storm", "nav_active": "/blog/",
        "crumbs": [("Home", "/"), ("Appraisal Process", "/insurance-appraisal-process/")], "priority": "0.8",
    }
    p["body"] = f'''
<p class="lead-p">Appraisal is a way to resolve a disagreement over the value of a covered property loss without going to court. Most property policies contain an appraisal clause, and while the wording varies, the process usually follows the same pattern.</p>
{callout("<p>Alabama courts treat appraisal as a contract process separate from arbitration. Your policy's appraisal provision controls who can invoke it, the deadlines and the procedure.</p>", "info", "Alabama specifics")}
<h2>The ten steps</h2>
{steps_html(steps)}
<h2>Appraisal vs. other options</h2>
{table(["Option", "Best for", "Cost &amp; time", "Decides coverage?"], [
    ["Supplement / re-inspection", "Small, clear gaps with good photos", "Low / fast", "No"],
    ["Estimate review", "Understanding the gap before deciding", "Low / fast", "No"],
    ["Appraisal", "Larger valuation disputes", "Moderate / weeks to months", "Generally no"],
    ["Mediation (if available)", "Broader disputes both sides want to settle", "Moderate", "By agreement"],
    ["Litigation", "Coverage, bad faith, refusal to appraise", "High / months to years", "Yes"],
])}
<h2>Tips for a smoother appraisal</h2>
{checklist(["Get a certified copy of the full policy", "Organize every estimate, photo and letter before sending a demand", "Calendar every deadline, including the suit-limitation period",
            "Choose an appraiser with estimating experience in your type of loss", "Agree on everything reasonable so the umpire sees only real disputes"])}
<h2>Related guides</h2>
<ul><li><a href="/how-to-invoke-the-appraisal-clause-in-alabama/">How to invoke the appraisal clause in Alabama</a></li><li><a href="/what-is-an-insurance-appraisal-umpire/">What is an insurance appraisal umpire?</a></li>
<li><a href="/how-long-does-insurance-appraisal-take/">How long does insurance appraisal take?</a></li><li><a href="/what-does-an-insurance-appraiser-do/">What does an insurance appraiser do?</a></li></ul>
'''
    p["schema"] = [{"@type": "HowTo", "@id": url("/insurance-appraisal-process/#howto"), "name": "How the insurance appraisal process works in Alabama",
                    "description": p["description"],
                    "step": [{"@type": "HowToStep", "position": n, "name": t, "text": re.sub(r"<[^>]+>", "", b)} for n, (t, b) in enumerate(steps, 1)]}]
    return p


GLOSSARY = [
    ("Actual cash value (ACV)", "Replacement cost minus depreciation. Many policies pay ACV first and the rest after repairs."),
    ("Additional living expenses (ALE)", "Coverage D: reasonable extra costs of living elsewhere while a home is uninhabitable after a covered loss."),
    ("Amount of loss", "The dollar value of a covered loss. This is what appraisal decides."),
    ("Appraisal award", "The written decision setting the amount of loss, usually signed by two of the three appraisal panel members."),
    ("Appraisal clause", "The policy provision describing how a disagreement over the amount of loss can be resolved by appraisers and an umpire."),
    ("Coverage A", "Dwelling coverage &mdash; the limit for the house itself. Percentage deductibles are calculated on it."),
    ("Declarations page", "The summary page of your policy listing coverages, limits, deductibles and the insured property."),
    ("Depreciation", "Reduction in value for age and wear. Recoverable depreciation is paid after repairs on replacement cost policies."),
    ("Disinterested appraiser", "An appraiser with no financial stake in the outcome beyond a reasonable fee. Many policies require one."),
    ("FORTIFIED roof", "A roof built to IBHS FORTIFIED standards for wind resistance; often eligible for premium discounts in Alabama."),
    ("Hurricane / named-storm deductible", "A deductible stated as a percentage of Coverage A that applies when the policy's storm trigger is met."),
    ("Matching", "Whether repaired or replaced materials reasonably match the undamaged materials around them."),
    ("Matterport", "3D capture technology that creates a measurable digital model of a property."),
    ("Mitigation", "Steps taken to prevent further damage after a loss, such as tarping or water extraction."),
    ("Ordinance or law coverage", "Coverage for added costs of meeting current building codes during repairs, subject to limits."),
    ("Overhead and profit (O&amp;P)", "A general contractor's markup, commonly 10% and 10%, for coordinating multiple trades."),
    ("Proof of loss", "A sworn statement of the amount claimed, which some policies require within a set time."),
    ("Replacement cost value (RCV)", "The cost to repair or replace damaged property with like kind and quality, without deducting depreciation."),
    ("Roofing square", "100 square feet of roof surface &mdash; the unit used in roofing estimates."),
    ("Scope of loss", "The list of damaged items and the repairs needed to restore them."),
    ("Supplement", "An additional request for payment for items missed or underpaid in the original estimate."),
    ("Symbility", "Claims estimating software used by a number of insurers and adjusting firms."),
    ("Umpire", "A neutral third person who resolves items the two appraisers can't agree on."),
    ("Waste factor", "Extra material added to an estimate to account for cutting and fitting, especially on roofs."),
    ("Xactimate", "The estimating software most widely used by insurers, adjusters and contractors."),
]


def glossary():
    letters = sorted({t[0].upper() for t, _ in GLOSSARY})
    az = "".join(f'<a href="#letter-{l}">{l}</a>' for l in letters)
    items, cur = [], None
    for t, d in GLOSSARY:
        l = t[0].upper()
        anchor = f' id="letter-{l}"' if l != cur else ""
        cur = l
        slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"&amp;", "and", t.lower())).strip("-")
        items.append(f'<div class="term"{anchor}><dt id="{slug}">{t}</dt><dd>{d}</dd></div>')
    p = {
        "path": "/glossary/", "title": "Insurance Claim Glossary | Appraisal &amp; Estimating Terms",
        "description": "Plain-English glossary of insurance claim and appraisal terms: ACV, RCV, depreciation, appraisal clause, umpire, O&P, matching and more.",
        "h1": "Insurance Claim &amp; Appraisal Glossary", "lead": "Plain-English definitions of the terms you'll see on estimates, policies and appraisal paperwork.",
        "kicker": "Resources", "hero_img": "inspect", "nav_active": "/blog/", "hero_actions": "",
        "crumbs": [("Home", "/"), ("Glossary", "/glossary/")], "priority": "0.6",
    }
    p["body"] = (f'<div class="gloss-search">{icon("search")}<input type="search" placeholder="Search terms…" aria-label="Search glossary terms" data-gloss-search></div>'
                 f'<nav class="az" aria-label="Jump to letter">{az}</nav><dl class="glossary">{"".join(items)}</dl>')
    p["schema"] = [{"@type": "DefinedTermSet", "@id": url("/glossary/#terms"), "name": "Insurance claim and appraisal glossary",
                    "hasDefinedTerm": [{"@type": "DefinedTerm", "name": re.sub("&amp;", "&", t), "description": re.sub(r"&mdash;", "—", re.sub("&amp;", "&", d))} for t, d in GLOSSARY]}]
    return p


def legal(path, title, desc, h1, body):
    return {"path": path, "title": title, "description": desc, "h1": h1, "kicker": "Legal", "hero_img": "inspect",
            "crumbs": [("Home", "/"), (h1, path)], "hero_actions": "", "body": body, "cta": False,
            "priority": "0.3", "changefreq": "yearly",
            "hero_meta": f'<div class="hero-meta"><span>Last updated {TODAY}</span></div>',
            "sidebar_title": "Site information", "sidebar_links": [("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms-of-use/"), ("Disclaimer", "/disclaimer/"), ("Contact", "/contact/")]}


PRIVACY = f'''
<p>This Privacy Policy explains how {BIZ["name"]} ("we", "us") collects, uses and protects information when you visit {BIZ["origin"].replace("https://", "")} (the "Site") or contact us.</p>
<h2>Information we collect</h2>
<h3>Information you give us</h3>
<p>When you submit our contact form, call or email us, we collect what you provide: typically your name, email, phone number, role, property location, type of loss and a description of your claim. Please don't send Social Security numbers, bank details or other sensitive identifiers.</p>
<h3>Information collected automatically</h3>
<p>Like most websites, our hosting provider records standard server logs (IP address, browser type, pages requested, date and time) for security and performance. We may use privacy-respecting analytics to understand how the Site is used. Fonts are loaded from Google Fonts, which receives your IP address when the page loads.</p>
<h3>Information stored only in your browser</h3>
<p>Our free tools run entirely in your browser. Numbers you type into calculators are not sent to us. The Appraisal Readiness Checklist saves your progress in your browser's local storage on your own device; you can clear it at any time with the Reset button or your browser settings.</p>
<h2>How we use information</h2>
<ul><li>To respond to your inquiry and discuss possible services</li><li>To provide services you engage us for</li><li>To keep a record of inquiries, including a backup copy of form submissions stored securely on our server</li>
<li>To protect the Site from spam, abuse and security threats</li><li>To comply with legal obligations</li></ul>
<h2>How we share information</h2>
<p>We do not sell your personal information. We share it only with service providers who help us operate (such as our web host and email provider), when you ask us to (for example, with the other appraiser or umpire on your claim), or when required by law.</p>
<h2>Data retention and security</h2>
<p>We keep inquiry information as long as needed to respond and for reasonable business records, then delete it. We use HTTPS, access controls and spam protection, but no system is perfectly secure.</p>
<h2>Your choices</h2>
<p>You can ask us to access, correct or delete your information by emailing <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>.</p>
<h2>Children</h2>
<p>The Site is not directed to children under 13, and we don't knowingly collect their information.</p>
<h2>Changes</h2>
<p>We may update this policy and will post the new date at the top of this page.</p>
<h2>Contact</h2>
<p>{BIZ["name"]} &middot; <a href="tel:{BIZ["phone_href"]}">{BIZ["phone_display"]}</a> &middot; <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></p>'''

TERMS = f'''
<p>By using {BIZ["origin"].replace("https://", "")} (the "Site") you agree to these Terms of Use. If you don't agree, please don't use the Site.</p>
<h2>Informational purposes only</h2>
<p>Content on the Site, including articles, FAQs, glossary entries and tools, is general and educational. It is not legal advice, does not interpret any specific insurance policy and is not an appraisal or estimate of any particular loss. Appraisal rights, deadlines and procedures depend on your policy and the facts of your claim.</p>
<h2>No appraiser-client relationship</h2>
<p>Using the Site, calling, emailing or submitting the contact form does not create an appraiser-client relationship. A relationship begins only when we accept an assignment in a signed written agreement.</p>
<h2>Free tools</h2>
<p>Calculators and checklists provide rough planning estimates based solely on what you enter. Results may not reflect how your insurer, an appraiser or an umpire would value a loss. Use them at your own risk.</p>
<h2>Intellectual property</h2>
<p>The Site's text, graphics, logos, images, tools and code are owned by or licensed to {BIZ["name"]} and protected by law. You may view and print pages for personal, non-commercial use. You may not copy, republish or distribute content without permission.</p>
<h2>Acceptable use</h2>
<p>Don't use the Site unlawfully, submit false or misleading information, send spam, attempt to gain unauthorized access, or interfere with the Site's operation.</p>
<h2>Third-party links</h2>
<p>Links to other websites are provided for convenience. We don't control and aren't responsible for their content.</p>
<h2>Disclaimer of warranties</h2>
<p>The Site is provided "as is" without warranties of any kind. We don't guarantee it will be accurate, complete, current or uninterrupted.</p>
<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, {BIZ["name"]} is not liable for any damages arising from your use of, or reliance on, the Site or its content.</p>
<h2>Governing law</h2>
<p>These Terms are governed by the laws of the State of Alabama.</p>
<h2>Changes</h2>
<p>We may update these Terms at any time by posting a new version here.</p>
<h2>Contact</h2>
<p>Questions? Email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a> or call <a href="tel:{BIZ["phone_href"]}">{BIZ["phone_display"]}</a>.</p>'''

DISCLAIMER = f'''
<p>{BIZ["name"]} provides independent property insurance appraisal, estimating and documentation services. Please read the following before relying on anything on this website.</p>
<h2>Not legal advice</h2>
<p>We are not a law firm and do not provide legal advice. Information about appraisal clauses, deadlines, coverage, court decisions and Alabama law is general and may not apply to your situation. For coverage disputes, bad-faith concerns, lawsuit deadlines or other legal questions, consult a licensed Alabama attorney.</p>
<h2>Not a public adjuster or insurer</h2>
<p>We are not your insurance company, agent or adjuster, and we do not negotiate claims on a policyholder's behalf outside the role of an appraiser or estimator. We are not affiliated with any insurance carrier, the Alabama Department of Insurance, Xactimate (Verisk), Symbility (CoreLogic) or Matterport. Those names are trademarks of their owners.</p>
<h2>No guaranteed results</h2>
<p>Every claim is different. We don't promise any particular award, payment or outcome. Examples on this site are hypothetical illustrations.</p>
<h2>Tool estimates</h2>
<p>Our calculators provide rough educational estimates only and are not appraisals, estimates or offers.</p>
<h2>Your policy controls</h2>
<p>Your insurance policy, its endorsements and the facts of your claim determine your rights. Always read your policy.</p>'''


def sitemap_page(all_pages):
    def sec(t, links):
        return f'<section><h2 class="h4">{t}</h2><ul>{"".join(f"<li><a href=\"{h}\">{n}</a></li>" for n, h in links)}</ul></section>'
    body = '<div class="sitemap-cols">' + "".join([
        sec("Main", [("Home", "/"), ("About Us", "/about-us/"), ("Contact", "/contact/"), ("Services", "/services/"), ("Service Areas", "/service-areas/"), ("Tools", "/tools/"), ("Blog", "/blog/")]),
        sec("Services", [(n, f"/services/{s}/") for s, n, _, _ in SERVICES]),
        sec("Service Areas", [(f"{c}, AL", f"/service-areas/{s}/") for c, s in CITIES]),
        sec("Free Tools", [(n, f"/tools/{s}/") for s, n, _, _ in TOOLS]),
        sec("Guides", [(p["h1"], f"/{p['slug']}/") for p in POSTS]),
        sec("Resources", [(n, h) for h, n, _, _ in RESOURCES] + [("General articles", "/category/general/")]),
        sec("Legal", [("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms-of-use/"), ("Disclaimer", "/disclaimer/")]),
    ]) + "</div>"
    return {"path": "/sitemap/", "title": "Sitemap | Alabama Insurance Appraiser", "description": "Every page on the Alabama Insurance Appraiser website: services, Alabama service areas, free claim tools, guides and legal pages.",
            "h1": "Sitemap", "kicker": "All pages", "hero_img": "inspect", "crumbs": [("Home", "/"), ("Sitemap", "/sitemap/")], "hero_actions": "",
            "layout": "wide", "body": f'<section class="section section-white"><div class="container">{body}</div></section>', "cta": False, "priority": "0.3"}


def thank_you():
    return {"path": "/thank-you/", "title": "Thank You | Alabama Insurance Appraiser", "description": "Thanks for contacting Alabama Insurance Appraiser. We received your claim details.",
            "h1": "Thank you &mdash; we received your claim details", "lead": "We'll review what you sent and get back to you shortly. If your matter is urgent, please call.",
            "kicker": "Message sent", "hero_img": "residential", "crumbs": [("Home", "/"), ("Thank You", "/thank-you/")], "noindex": True, "layout": "wide",
            "hero_actions": f'<div class="hero-actions">{call_btn()}{btn("Back to home", "/", "ghost-light", "home")}</div>',
            "body": f'<section class="section section-white"><div class="container">{section_head("While you wait", "Get your documents ready", "", True)}'
                    f'{grid([card("Readiness checklist", "Track the documents to gather before appraisal.", "/tools/appraisal-readiness-checklist/", "clipboard", link_label="Open tool"), card("Claim gap calculator", "See how far apart the estimates are.", "/tools/claim-gap-calculator/", "calculator", link_label="Open tool"), card("Appraisal process", "Know what happens next.", "/insurance-appraisal-process/", "list", link_label="Read guide")], 3)}</div></section>',
            "cta": False}


def not_found():
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for n, h in [("Services", "/services/"), ("Service areas", "/service-areas/"), ("Free tools", "/tools/"), ("Blog", "/blog/"), ("Contact", "/contact/")])
    return {"path": "/404.html", "title": "Page Not Found | Alabama Insurance Appraiser", "description": "The page you were looking for could not be found.",
            "h1": "Page not found", "crumbs": [("Home", "/"), ("404", "/404.html")], "noindex": True, "layout": "raw",
            "body": f'<section class="notfound"><div class="container"><div class="big">404</div><h1>We couldn&rsquo;t find that page</h1>'
                    f'<p class="section-lead" style="margin:0 auto 28px;max-width:560px">It may have moved when we rebuilt the site. Try one of these, or call us at {BIZ["phone_short"]}.</p>'
                    f'<div class="hero-actions" style="justify-content:center">{btn("Go to homepage", "/", "primary", "home")}{call_btn("ghost")}</div>'
                    f'<ul class="tags" style="justify-content:center;margin-top:30px">{links}</ul></div></section>'}


def pages():
    out = [about(), contact(), faq(), process(), glossary(),
           legal("/privacy-policy/", "Privacy Policy | Alabama Insurance Appraiser",
                 "How Alabama Insurance Appraiser collects, uses and protects information from website visitors, contact form submissions and our free claim tools.", "Privacy Policy", PRIVACY),
           legal("/terms-of-use/", "Terms of Use | Alabama Insurance Appraiser",
                 "Terms of Use for the Alabama Insurance Appraiser website: informational content, free tools, intellectual property, liability and acceptable use.", "Terms of Use", TERMS),
           legal("/disclaimer/", "Disclaimer | Alabama Insurance Appraiser",
                 "Alabama Insurance Appraiser does not give legal advice, is not an insurer or public adjuster, and does not guarantee any claim outcome.", "Disclaimer", DISCLAIMER),
           thank_you(), not_found()]
    out.append(sitemap_page(out))
    return out
