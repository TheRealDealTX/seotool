<?php
require dirname(__DIR__) . '/inc/config.php';
$page = ['title' => 'Terms of Use | ' . SITE_NAME, 'description' => 'Terms of use for Insurance Adjuster Salary: how to use our adjuster salary estimates, calculators and licensing information, plus affiliate link disclosures.', 'path' => '/terms-of-use/', 'image' => 'signing-documents.webp'];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Legal', 'Terms of Use', 'Last updated October 19, 2026.', 'signing-documents.webp', ['Terms of Use' => null]);
?>
<section class="section"><div class="container narrow prose legal">
  <p>By using <?= e(SITE_NAME) ?> you agree to these terms.</p>
  <h2>Informational purposes only</h2>
  <p>Salary figures, fee estimates and calculator results are general estimates for research and educational purposes. They are not job offers, financial advice, tax advice or legal advice. Pay varies by employer, location, experience, claim volume and market conditions.</p>
  <h2>Licensing and fee rules</h2>
  <p>Insurance adjuster licensing requirements and public adjuster fee limits are set by each state and change over time. Always confirm current rules with your state department of insurance before relying on them.</p>
  <h2>Affiliate links</h2>
  <p>Some links on this site, including links to online adjuster courses, may earn us a commission at no extra cost to you.</p>
  <h2>Intellectual property</h2>
  <p>Site content and design are owned by <?= e(SITE_NAME) ?>. Photos are used under the Unsplash License. You may link to our pages and quote short excerpts with attribution.</p>
  <h2>No warranty</h2>
  <p>The site is provided &ldquo;as is&rdquo; without warranties of any kind. We are not liable for decisions made based on information on this site.</p>
</div></section>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
