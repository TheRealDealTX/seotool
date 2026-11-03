<?php
defined('SCC') || (http_response_code(404) && exit);
require __DIR__ . '/_legal.php';
legal_page('/affiliate-disclosure/', 'Affiliate Disclosure | Solar CCTV Camera', 'Affiliate disclosure',
'How Solar CCTV Camera earns money through affiliate links, and the rules we follow so commissions never influence our solar camera recommendations.', <<<'HTML'
<p>Solar CCTV Camera (SolarCCTVCamera.com) is reader-supported. Some links on this site are affiliate links, which means that if you click one and make a purchase, we may earn a commission at no additional cost to you.</p>
<h2>Amazon Associates</h2>
<p>Solar CCTV Camera is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate we earn from qualifying purchases.</p>
<h2>Our rules</h2>
<ul>
<li>We never accept payment, free products or other compensation in exchange for including or ranking a product.</li>
<li>Commission rates play no part in which products we recommend. Picks are chosen by situation (connectivity, power, subscription needs) based on specifications, solar math and owner feedback.</li>
<li>Every page that contains affiliate links says so near the top, and affiliate links are marked <code>rel="sponsored"</code>.</li>
<li>Prices and availability change. Always confirm the current price and specifications on the retailer’s page before buying.</li>
</ul>
<h2>Questions</h2>
<p>If you have questions about this policy, <a href="/contact/">contact us</a>.</p>
HTML);
