<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => 'Terms of Use', 'crumbs' => [['Terms of Use', '']]]); ?>
<section class="section tight">
  <div class="wrap prose narrow">
    <p><em>Last updated: November 19, 2026</em></p>
    <h2>Use of this site</h2>
    <p>By using <?= e(parse_url(cfg('url'), PHP_URL_HOST)) ?> you agree to these terms. The site is provided for general information about real estate in Seattle and the surrounding area.</p>
    <h2>Listing information</h2>
    <p>Property information, prices, photos and availability are provided for general information only, are deemed reliable but not guaranteed, and may change or be withdrawn without notice. Square footage, lot size and other details are approximate. Please verify all information independently and contact us for current status before relying on it.</p>
    <h2>Not professional advice</h2>
    <p>Blog articles and guides are general information, not legal, tax, financial or insurance advice. Consult a qualified professional about your situation.</p>
    <h2>Fair housing</h2>
    <p>We are committed to the letter and spirit of federal, state and local fair housing laws and do not discriminate on the basis of race, color, religion, sex, disability, familial status, national origin or any other protected class.</p>
    <h2>Intellectual property</h2>
    <p>Site content, design and original text belong to <?= e(cfg('name')) ?> or its licensors. Some photography is used under license. Please don't republish content without permission.</p>
    <h2>Third-party links</h2>
    <p>Links to other websites are provided for convenience; we are not responsible for their content or practices.</p>
    <h2>Limitation of liability</h2>
    <p>The site is provided "as is." To the fullest extent permitted by law, <?= e(cfg('name')) ?> is not liable for any damages arising from your use of the site.</p>
    <h2>Contact</h2>
    <p>Questions? Email <a href="mailto:<?= e(cfg('email')) ?>"><?= e(cfg('email')) ?></a>.</p>
  </div>
</section>
