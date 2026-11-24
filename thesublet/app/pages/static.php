<?php defined('APP') || exit;

cache_public();
$slug = $params[0];
function credits_html(): string
{
    $h = '<p>Listing photos are uploaded by hosts, who confirm they own them or have permission to use them. We never copy photos from other rental sites or property websites. Claimable directory listings show an illustration until the property manager adds their own photos.</p>'
       . '<p>Site, blog and city photos are royalty-free images (public domain / CC0) or Creative Commons photos used under their license terms, self-hosted as WebP. Illustrations and the logo are original artwork.</p>';
    $rows = '';
    foreach (photos() as $key => $p) {
        $lic = e($p['license'] ?? '');
        if (!empty($p['license_url'])) $lic = '<a href="' . e($p['license_url']) . '" rel="nofollow noopener" target="_blank">' . $lic . '</a>';
        $rows .= '<tr><td><img src="' . e($p['file']) . '" alt="" width="96" height="54" loading="lazy" style="width:96px;height:54px;object-fit:cover;border-radius:6px"></td><td>' . e($p['alt'] ?? '') . '</td><td>'
            . e(strip_tags((string)($p['credit'] ?? ''))) . (!empty($p['source']) ? ' / ' . e($p['source']) : '') . '</td><td>' . $lic . '</td><td>'
            . (!empty($p['url']) ? '<a href="' . e($p['url']) . '" rel="nofollow noopener" target="_blank">Source</a>' : '') . '</td></tr>';
    }
    if ($rows) $h .= '<div class="table-scroll"><table class="tbl"><tr><th></th><th>Image</th><th>Creator / source</th><th>License</th><th></th></tr>' . $rows . '</table></div>';
    return $h . '<p>If you believe an image infringes your rights, please <a href="/contact/">contact us</a> and we’ll review it promptly.</p>';
}
$price = e(price_label());
$pages = [
'about' => ['About The Sublet', 'About The Sublet — a nationwide directory of furnished sublets and 1–12 month rentals for interns, travel nurses, students and relocations.', <<<HTML
<p class="lead">The Sublet (thesublet.com) is a nationwide directory for the in-between: furnished rooms, apartments and homes for roughly one to twelve months.</p>
<p>Long-term rental sites are built around 12-month leases. Vacation sites are built around nights and weekends. But a lot of life happens in between — a summer internship, a 13-week travel-nurse contract, a semester away, a visiting fellowship, a job move where you want to learn the city before you sign a lease. The Sublet exists for those stays.</p>
<h2>What we do</h2>
<ul><li><strong>Real listings only.</strong> Every listing is posted by a host. Free listings are reviewed by a person before they go live, and we never pad the site with placeholder listings.</li><li><strong>Private by default.</strong> Renters contact hosts through a relay form, so hosts’ emails aren’t published on free listings.</li><li><strong>Simple pricing for hosts.</strong> List free, or pay a one-time {$price} for a verified listing that goes live instantly with your contact details, a Verified host badge and a dashboard.</li><li><strong>Useful local guides.</strong> Our city pages cover neighborhoods, transit and practical tips for interns, travel nurses and students.</li></ul>
<h2>What “Verified host” means</h2>
<p>It means the host paid for the listing by card and confirmed their email address. It is <em>not</em> an identity or background check, and it doesn’t mean we’ve inspected the property. Always follow our <a href="/safety/">safety tips</a>.</p>
<p>Questions? <a href="/contact/">Contact us</a>.</p>
HTML],
'safety' => ['Scam-Awareness & Safety Tips for Sublets', 'How to avoid sublet and rental scams: red flags, safe payment practices, verifying hosts, and how to report a suspicious listing on The Sublet.', <<<'HTML'
<p class="lead">Most hosts are honest people with a room to fill. A few aren’t. These habits protect you either way.</p>
<h2>Red flags</h2>
<ul class="ticks"><li>The host asks you to <strong>wire money</strong>, pay with <strong>gift cards</strong>, <strong>cryptocurrency</strong> or a payment app before you’ve met or toured.</li><li>“I’m out of the country — send the deposit and I’ll mail you the keys.”</li><li>Rent far below similar places nearby, especially in expensive neighborhoods.</li><li>Pressure to pay today because “lots of people are interested.”</li><li>They won’t do a live video tour, or the photos appear on other listings with different names.</li><li>They “accidentally” overpay you and ask you to send back the difference.</li></ul>
<h2>Do this before paying anything</h2>
<ol><li><strong>Tour first</strong> — in person, or by live video where they walk through every room and show the view out of a window and the building entrance.</li><li><strong>Confirm they can sublet.</strong> Ask to see the lease or the landlord’s written consent. Unauthorized sublets can end with you locked out.</li><li><strong>Sign a written sublease</strong> covering dates, rent, deposit, utilities and house rules. See <a href="/blog/sublease-agreement-what-to-include/">what to include</a>.</li><li><strong>Pay traceably</strong> and keep receipts. Avoid cash, wires and gift cards.</li><li><strong>Search the address and the photos</strong> — a reverse image search can reveal copied photos.</li></ol>
<h2>For hosts</h2>
<ul><li>Don’t accept overpayments or cashier’s checks for more than the amount due.</li><li>Meet renters (or video-call) before handing over keys, and document the condition of the place with dated photos.</li><li>Follow your lease and your city’s short-term-rental rules.</li></ul>
<h2>Report it</h2>
<p>Use the <strong>🚩 Report listing</strong> button on any listing and our moderators will review it. If you’ve lost money, report it to the Federal Trade Commission at <a href="https://reportfraud.ftc.gov/" rel="noopener" target="_blank">ReportFraud.ftc.gov</a>, to the FBI’s Internet Crime Complaint Center at <a href="https://www.ic3.gov/" rel="noopener" target="_blank">ic3.gov</a>, and to your local police, and contact your bank or payment provider immediately.</p>
<p>More detail: <a href="/blog/how-to-avoid-rental-scams/">How to avoid rental scams</a> · <a href="/blog/how-to-tour-a-sublet-remotely/">How to tour a sublet remotely</a>.</p>
HTML],
'fair-housing' => ['Fair Housing Notice', 'The Sublet’s fair housing notice: listings must comply with the federal Fair Housing Act and state and local anti-discrimination laws.', <<<'HTML'
<p class="lead">The Sublet is committed to equal housing opportunity.</p>
<p>The federal <strong>Fair Housing Act</strong> prohibits discrimination in housing based on race, color, religion, sex (including sexual orientation and gender identity), national origin, familial status and disability. Many states and cities protect additional characteristics — for example source of income, age, marital status or military status.</p>
<h2>What this means for listings</h2>
<ul><li>Describe the property and its rules, not the kind of person you want. Write “quiet building, no smoking” rather than describing who you prefer as a tenant.</li><li>Don’t state preferences or limitations based on protected characteristics.</li><li>Assistance animals for people with disabilities are generally not considered pets under fair housing rules; a “no pets” rule may not apply to them.</li><li>Some narrow exemptions exist (for example, certain shared-living situations). Even where an exemption applies to who you rent to, federal law still restricts discriminatory advertising, and exemptions vary by state — if you’re unsure, get local legal advice.</li></ul>
<p>We remove listings that violate fair housing rules. To report one, use “Report listing” on the listing page. You can also contact the U.S. Department of Housing and Urban Development (HUD) Office of Fair Housing and Equal Opportunity at <a href="https://www.hud.gov/fairhousing" target="_blank" rel="noopener">hud.gov/fairhousing</a>.</p>
<h2>Short-term-rental laws</h2>
<p>Hosts are responsible for complying with their lease, HOA or building rules, and local short-term-rental regulations, which may include registration, permits, occupancy limits, minimum stay lengths and taxes. The Sublet doesn’t verify legal compliance.</p>
HTML],
'pricing' => ['Free vs. Verified Listings', 'List your sublet free on The Sublet, or pay a one-time fee for a verified listing that is published instantly with contact details and a badge.', <<<HTML
<p class="lead">Two ways to list on The Sublet. No subscriptions.</p>
<div class="tiers">
<div class="tier"><h2 class="h3">Free listing</h2><p class="tier-price">\$0</p><ul><li>Reviewed by our team before publishing (usually 1–2 days)</li><li>Contact details hidden — renters message you via our relay, delivered to your inbox</li><li>Runs until your end date or 60 days, with a renew reminder</li><li>Upgrade any time for the same one-time fee</li></ul><a class="btn btn-ghost" href="/post-a-sublet/?tier=free">Post free</a></div>
<div class="tier tier-hi"><h2 class="h3">Verified listing</h2><p class="tier-price">{$price} <span class="small">one-time</span></p><ul><li>Published instantly — no queue</li><li>Your email and phone shown to renters</li><li>“Verified host” badge and higher placement</li><li>Owner dashboard: edit, upload photos, renew, mark rented</li><li>Promo codes accepted at checkout</li></ul><a class="btn" href="/post-a-sublet/?tier=paid">Get verified</a></div>
</div>
<p class="small muted">Payments are processed securely by Stripe. “Verified” means the host paid by card and verified their email; it is not an ID or background check. All listings must follow our <a href="/terms/">terms</a>, fair housing rules and local short-term-rental laws.</p>
HTML],
'terms' => ['Terms of Use', 'Terms of use for The Sublet (thesublet.com): listing rules, paid listings, the property directory, acceptable use and limits of liability.', <<<'HTML'
<p><em>Last updated November 2026.</em></p>
<p>By using thesublet.com (“The Sublet”, “we”) you agree to these terms.</p>
<h2>1. What The Sublet is</h2><p>The Sublet is a listings directory. We are not a landlord, broker or party to any rental agreement, and we don’t collect rent or deposits. Agreements are solely between hosts and renters.</p>
<h2>2. Hosts</h2><ul><li>You must have the legal right to rent the space, including any landlord consent your lease requires.</li><li>You are responsible for complying with all laws, including fair housing, short-term-rental, registration, occupancy and tax rules.</li><li>Listings must be accurate, describe a real available place, and use photos you own or have permission to use.</li><li>No requests for wire transfers, gift cards or cryptocurrency.</li></ul>
<h2>3. Renters</h2><p>Do your own due diligence: tour the property, verify the host’s right to sublet, and get a written agreement. Follow our <a href="/safety/">safety tips</a>.</p>
<h2>4. Moderation</h2><p>We may review, edit, refuse or remove any listing or account at our discretion, including for suspected fraud, discrimination or legal violations.</p>
<h2>5. Fees</h2><p>Verified listings are a one-time fee charged through Stripe. Because the listing is published immediately, fees are generally non-refundable; if we remove a paid listing for reasons other than a violation of these terms, contact us about a refund.</p>
<h2>6. Messages</h2><p>Messages sent through our relay are delivered to the host by email and stored so we can investigate abuse. Don’t send spam or harassment.</p>
<h2>7. Disclaimers</h2><p>The site is provided “as is.” To the fullest extent permitted by law, we are not liable for losses arising from listings, rentals or dealings between users. Our city guides and blog posts are general information, not legal, tax or financial advice.</p>
<h2>8. Affiliate links</h2><p>Some links to Amazon are affiliate links; as an Amazon Associate we earn from qualifying purchases.</p>
<h2>9. Contact</h2><p>info@thesublet.com · <a href="/contact/">Contact form</a></p>
HTML],
'privacy' => ['Privacy Policy', 'How The Sublet collects, uses and protects information from renters, hosts and property owners, including contact relays and payments.', <<<'HTML'
<p><em>Last updated November 2026.</em></p>
<h2>What we collect</h2><ul><li><strong>Hosts:</strong> name, email, optional phone, listing details and photos. Photos are re-encoded on upload, which removes embedded metadata such as GPS location.</li><li><strong>Renters who send messages:</strong> name, email and the message, which we relay to the host.</li><li><strong>Payments:</strong> handled by Stripe; we receive confirmation and your email, never your card number.</li><li><strong>Technical data:</strong> IP address (for rate-limiting and fraud prevention) and a session cookie for sign-in and form security.</li></ul>
<h2>How it’s used</h2><p>To publish listings, relay messages, send account and listing emails (approval, sign-in links, expiry reminders), prevent abuse, and improve the site. We don’t sell personal information.</p>
<h2>What’s public</h2><p>Listing details and an approximate map location (blurred to within a few blocks) are public. On free listings, your email and phone are not shown. On verified listings, the contact details you enter are shown.</p>
<h2>Your device</h2><p>Favorites, compare selections, the packing checklist and room planner are stored in your browser’s local storage, not on our servers. If enabled, Google Tag Manager/analytics may set cookies to measure site usage.</p>
<h2>Retention &amp; choices</h2><p>Hosts can edit or delete listings from their dashboard, or ask us to delete their data via the <a href="/contact/">contact form</a>.</p>
HTML],
'credits' => ['Photo Credits', 'Photo credits and licenses for the royalty-free and Creative Commons images used across The Sublet’s pages, city guides and blog.', credits_html()],
];
[$title, $desc, $html] = $pages[$slug];
$crumbs = [['The Sublet', '/'], [$title, "/$slug/"]];
page([
    'title' => seo_title($title),
    'description' => $desc,
    'canonical' => "/$slug/",
    'body' => '<div class="wrap">' . breadcrumbs_html($crumbs) . '<article class="narrow prose section-sm"><h1>' . e($title) . '</h1>' . $html . '</article></div>',
    'schema' => [schema_breadcrumbs($crumbs)],
]);
