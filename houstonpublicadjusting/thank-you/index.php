<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Thank You', '/thank-you/']];
page_start(['title' => 'Thank You | Houston Public Adjusters', 'desc' => 'Thanks for contacting Houston Public Adjusters. A licensed public adjuster will be in touch shortly.', 'path' => '/thank-you/', 'crumbs' => $crumbs, 'noindex' => true, 'no_popup' => true]);
?>
<section class="page-hero"><div class="wrap"><h1>Thank you &mdash; we&rsquo;ve got your request</h1><p class="lede">A licensed Houston public adjuster will contact you shortly. If your situation is urgent, call or text us now at <a style="color:#fff" href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a>.</p></div></section>
<section class="section"><div class="wrap prose">
  <h2>While you wait</h2>
  <ul class="checklist">
    <li>Gather photos, your claim number and any letters or estimates from your insurer</li>
    <li>Don&rsquo;t sign a settlement or release until we&rsquo;ve reviewed it</li>
    <li>Prevent further damage and keep your receipts</li>
  </ul>
  <p><a class="btn btn-dark" href="/tools/">Try our claim calculators</a> <a class="btn btn-outline" href="/blog/">Read our claim guides</a></p>
</div></section>
<?php
page_end(false);
