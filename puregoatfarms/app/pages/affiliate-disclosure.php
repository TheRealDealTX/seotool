<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['Affiliate Disclosure', '/affiliate-disclosure/']];
$page = [
    'path'   => '/affiliate-disclosure/',
    'title'  => 'Affiliate Disclosure — Pure Goat Farms',
    'desc'   => 'How Pure Goat Farms uses affiliate links, including the Amazon Associates program, and how we choose the products we mention.',
    'crumbs' => $crumbs,
];
ob_start();
?>
<section class="page-hero page-hero--slim">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Affiliate Disclosure</h1>
    <p class="page-hero__lead">Effective Date: October 2026</p>
  </div>
</section>
<section class="section section--tight">
  <div class="container narrow prose">
    <p>Pure Goat Farms is reader-supported. Some articles include links to products we use or recommend. If you click one of these links and make a purchase, we may earn a small commission <strong>at no extra cost to you</strong>.</p>
    <h2>Amazon Associates</h2>
    <p>Pure Goat Farms is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate, Pure Goat Farms earns from qualifying purchases.</p>
    <h2>How we choose products</h2>
    <p>We only mention products that are relevant to the guide you are reading and that fit how we run our own herd — milking equipment, udder care, feed supplements, cheese-making supplies and reference books. Commissions never decide what we recommend, and many of our guides contain no affiliate links at all.</p>
    <h2>How to recognize affiliate links</h2>
    <p>Affiliate links on Pure Goat Farms appear in clearly labelled product boxes with the note “Opens on Amazon. We may earn a commission.” Posts that contain affiliate links also carry a disclosure at the top.</p>
    <h2>Questions</h2>
    <p>If you have any questions about this disclosure, email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a>. See also our <a href="/privacy-policy/">Privacy Policy</a> and <a href="/terms-of-use/">Terms of Use</a>.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
