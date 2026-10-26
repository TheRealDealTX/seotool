<?php defined('BO') || exit;
$crumbs = [['Home', '/'], ['Terms of Use', '/terms-of-use/']];
page_head(['title' => 'Terms of Use | Better Outdoors', 'desc' => 'The terms that apply when you use Better Outdoors, including our archery safety disclaimer, tool estimates, affiliate links and content ownership.', 'path' => '/terms-of-use/', 'schema' => [breadcrumb_schema($crumbs)]]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html($crumbs) ?><h1>Terms of Use</h1><p>Last updated <?= fmt_date('2026-10-26') ?></p></div></section>
<div class="page-body prose">
<p>By using betteroutdoors.net (&ldquo;Better Outdoors&rdquo;), you agree to these Terms of Use. If you do not agree, please do not use the site.</p>
<h2 id="informational-purposes">Informational Purposes Only</h2>
<p>All content on Better Outdoors, including bow reviews, tuning guides and calculators, is provided for general information. Specifications are gathered from manufacturer and retailer listings and can change; always confirm with the manufacturer or an authorized dealer before buying.</p>
<h2 id="safety">Archery and Hunting Safety Disclaimer</h2>
<p>Archery equipment stores significant energy and can cause serious injury or property damage. Never dry-fire a bow. Adjusting cams, modules, strings or limbs can be dangerous; if you are unsure, use a bow press and consult a qualified archery pro shop. You are responsible for following all hunting laws, seasons and equipment regulations in your area. Better Outdoors is not liable for injury, loss or damage resulting from use of our content.</p>
<h2 id="tools">Calculators and Estimates</h2>
<p>Our tools produce estimates based on common formulas and rules of thumb. Results such as draw length, arrow speed and kinetic energy are not guarantees and should be confirmed by measurement (for example with a chronograph or at a pro shop).</p>
<h2 id="h-product-reviews-affiliate-links">Product Reviews &amp; Affiliate Links</h2>
<ul>
  <li>Better Outdoors includes product reviews, recommendations and affiliate links, including Amazon Associates links.</li>
  <li>We may earn commissions from qualifying purchases at no additional cost to you.</li>
  <li>Prices and availability are set by retailers and can change at any time.</li>
</ul>
<h2 id="ip">Intellectual Property</h2>
<p>Text, graphics, logos and tools on this site belong to Better Outdoors unless otherwise noted. You may share links and brief quotes with attribution, but may not republish full articles without permission. Product names and brands are trademarks of their respective owners; Better Outdoors is not affiliated with Mathews, Bear Archery, PSE or Amazon.</p>
<h2 id="conduct">Acceptable Use</h2>
<p>Do not attempt to disrupt the site, scrape it at scale, or use our contact form to send spam or unlawful content.</p>
<h2 id="links">Third-Party Links</h2>
<p>We link to other websites for reference and shopping. We are not responsible for their content, policies or products.</p>
<h2 id="liability">Limitation of Liability</h2>
<p>To the fullest extent permitted by law, Better Outdoors provides the site &ldquo;as is&rdquo; without warranties of any kind and is not liable for any indirect or consequential damages arising from its use.</p>
<h2 id="changes">Changes</h2>
<p>We may update these terms at any time. Continued use of the site means you accept the current version.</p>
<h2 id="contact">Contact</h2>
<p>Email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a> with any questions.</p>
</div>
<?php page_foot(false); ?>
