"""Privacy policy and terms of use.

Carried across from the WordPress site's own legal pages and rewritten to match
this build. Both are noindex,follow -- they exist for users and for the footer
link, not for search.
"""

from siteconfig import BIZ

PHONE = BIZ["phone_display"]
EMAIL = BIZ["email"]
ORIGIN = BIZ["origin"]

LEGAL = [
    {
        "path": "/privacy-policy/",
        "slug": "privacy-policy",
        "title": "Privacy Policy | Roof Tarp",
        "description": "How Roof Tarp collects, uses and protects the information you provide.",
        "h1": "Privacy Policy",
        "h1_plain": "Privacy Policy",
        "body": f"""
<p>This policy explains what information {BIZ['name']} collects when you use
<a href="{ORIGIN}">{ORIGIN.split('//')[1]}</a> or contact us, how it is used, and the choices you have.</p>

<h2>Information we collect</h2>
<p>We collect information you give us directly when you call, email or submit the callback form:
your name, phone number, email address, property address or ZIP code, and whatever you tell us about
the damage. We ask for this because we cannot dispatch a crew or quote a job without it.</p>
<p>We also receive standard technical information automatically when you visit the site, such as
IP address, browser type, pages viewed and referring page. This is ordinary web server and analytics
data.</p>

<h2>How we use it</h2>
<ul>
<li>To respond to your enquiry and dispatch a crew</li>
<li>To prepare quotes, invoices and job documentation</li>
<li>To supply photographs and paperwork to you or, at your request, to your insurer</li>
<li>To keep records of work performed</li>
<li>To improve the website and understand how it is used</li>
</ul>
<p>We do not sell your personal information. We do not share it with third parties for their own
marketing.</p>

<h2>When we share information</h2>
<p>We share information only where it is necessary to do the work or where the law requires it:</p>
<ul>
<li><strong>With your insurer or adjuster</strong>, when you ask us to</li>
<li><strong>With service providers</strong> who operate our phone, email, hosting or scheduling
systems, and only as needed to provide those services</li>
<li><strong>Where required by law</strong>, or to establish or defend legal claims</li>
</ul>

<h2>Job photographs</h2>
<p>We photograph damage and completed work as a standard part of every job, because insurers ask for
evidence of the original damage and the mitigation step. Those photographs are kept as part of the job
record and provided to you. We do not publish identifiable photographs of your property without your
permission.</p>

<h2>Cookies</h2>
<p>The site uses cookies for basic functionality and analytics. Most browsers let you refuse or delete
cookies through their settings. Refusing them may affect how parts of the site behave.</p>

<h2>Data retention</h2>
<p>We keep job records, including photographs and invoices, for as long as needed for business,
accounting, warranty and legal purposes. Enquiries that do not become jobs are kept for a shorter
period.</p>

<h2>Security</h2>
<p>We take reasonable measures to protect the information we hold. No method of transmission or storage
is completely secure, and we cannot guarantee absolute security.</p>

<h2>Children</h2>
<p>This site is not directed at children under 13 and we do not knowingly collect their information.</p>

<h2>Your choices</h2>
<p>You can ask us what information we hold about you, ask us to correct it, or ask us to delete it
where we are not required to keep it. Contact us using the details below.</p>

<h2>Changes</h2>
<p>We may update this policy. The current version is always the one posted on this page.</p>

<h2>Contact</h2>
<p>{BIZ['name']}<br>
Phone: <a href="tel:{BIZ['phone_href']}">{PHONE}</a><br>
Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
""",
    },
    {
        "path": "/terms-of-use/",
        "slug": "terms-of-use",
        "title": "Terms of Use | Roof Tarp",
        "description": "The terms that apply to your use of the Roof Tarp website.",
        "h1": "Terms of Use",
        "h1_plain": "Terms of Use",
        "body": f"""
<p>These terms apply to your use of <a href="{ORIGIN}">{ORIGIN.split('//')[1]}</a>. By using the site
you accept them. If you do not accept them, please do not use the site.</p>

<h2>What this site is</h2>
<p>This site provides information about {BIZ['name']}'s emergency roof tarping services and a way to
contact us. It is informational. It is not a contract for work, and submitting the callback form does
not by itself create one &mdash; work is agreed directly, with a price given before it starts.</p>

<h2>Information is general, not advice for your roof</h2>
<p>The guides and service descriptions on this site are general information about roof tarping. They
are not an inspection, a diagnosis or professional advice about your specific roof. Every roof is
different, and the right method depends on its covering, pitch, structural condition and the damage it
has taken.</p>
<p>In particular, the DIY guidance in our blog describes what is involved in tarping a roof. It is not
a recommendation that you climb onto a damaged roof. Working at height on wet or compromised roofing is
dangerous and has killed people. If the roof is steep, tall, wet, tile, metal or structurally
compromised, call a professional.</p>

<h2>No guarantee of outcome</h2>
<p>A tarp is a temporary protective covering, not a roof and not a repair. Correctly installed, it
substantially reduces water entry through the breach it covers. It cannot guarantee that no water will
enter, that existing damage will not worsen, or that a specific insurance claim will be paid.</p>

<h2>Cost figures</h2>
<p>Any cost information on this site is a general planning range, not a quote. Actual pricing depends
on the property and is given to you before work begins.</p>

<h2>Intellectual property</h2>
<p>The content of this site &mdash; text, layout, graphics and code &mdash; belongs to {BIZ['name']}
unless stated otherwise. You may view and print it for your own personal, non-commercial use. You may
not republish or redistribute it without permission.</p>

<h2>Links to other sites</h2>
<p>We may link to third-party sites for convenience. We do not control them and are not responsible
for their content or practices.</p>

<h2>Limitation of liability</h2>
<p>To the fullest extent permitted by law, {BIZ['name']} is not liable for any indirect, incidental or
consequential damages arising from your use of this site or reliance on its content. This does not
limit any liability that cannot lawfully be limited.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of the State of Texas.</p>

<h2>Changes</h2>
<p>We may update these terms. The current version is always the one posted on this page.</p>

<h2>Contact</h2>
<p>{BIZ['name']}<br>
Phone: <a href="tel:{BIZ['phone_href']}">{PHONE}</a><br>
Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
""",
    },
]
