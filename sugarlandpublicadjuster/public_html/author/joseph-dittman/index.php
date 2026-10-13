<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';

$path = AUTHOR['url'];
$crumbs = [['Home', '/'], ['About Us', '/about-us/'], ['Joseph Dittman', $path]];
page_start([
    'title' => 'Joseph Dittman, Licensed Public Adjuster | Sugar Land Public Adjuster',
    'description' => 'Joseph Dittman is a licensed Texas public adjuster with Rise Public Adjusting LLC who represents Sugar Land homeowners and businesses on property insurance claims.',
    'path' => $path,
    'page_type' => 'ProfilePage',
    'image' => AUTHOR['image'],
    'breadcrumbs' => $crumbs,
    'main_entity' => SITE['origin'] . '/#joseph-dittman',
]);
?>
<section class="page-hero">
  <div class="container">
    <?php breadcrumb_nav($crumbs); ?>
    <div class="split" style="grid-template-columns:auto 1fr;gap:36px">
      <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman, licensed Texas public adjuster" width="220" height="220" style="border-radius:50%;width:220px">
      <div>
        <p class="eyebrow">Author &amp; public adjuster</p>
        <h1>Joseph Dittman</h1>
        <p class="lead"><?= e(AUTHOR['title']) ?> · <?= e(SITE['firm']) ?> (license #<?= e(SITE['firm_license']) ?>)</p>
        <div class="btn-row"><a class="btn btn-light" href="tel:<?= SITE['phone_href'] ?>">Call <?= e(SITE['phone_display']) ?></a><a class="btn btn-outline-light" href="mailto:<?= e(SITE['email']) ?>">Email Joseph</a></div>
      </div>
    </div>
  </div>
</section>

<div class="container content-layout">
  <div class="prose">
    <h2>About Joseph</h2>
    <p><?= e(AUTHOR['short']) ?></p>
    <p>Joseph works exclusively for policyholders. His firm, <?= e(SITE['firm']) ?>, operates <a href="https://txpublicadjusting.com/" rel="noopener" target="_blank">TX Public Adjusting</a>, which represents property owners across Texas—from Houston and the Gulf Coast to Dallas–Fort Worth, Austin and San Antonio—after hailstorms, hurricanes, wind, water intrusion, roof damage and fires. Sugar Land Public Adjuster brings that same representation to Fort Bend County.</p>

    <h2>How Joseph approaches a claim</h2>
    <ul class="checklist">
      <li><strong>Document everything.</strong> Photos, measurements, moisture readings and, where it helps, Matterport 3D imaging so nothing is left to memory.</li>
      <li><strong>Price it like the insurer does.</strong> Estimates built in Xactimate and Symbility, the platforms carriers use, so the negotiation is line item against line item.</li>
      <li><strong>Read the whole policy.</strong> Endorsements, ordinance-or-law, additional living expenses and other coverages that often go unclaimed.</li>
      <li><strong>Communicate clearly.</strong> Regular updates and straight answers—even when they’re not what you want to hear.</li>
    </ul>

    <h2>Claim types Joseph handles</h2>
    <ul class="chips">
      <li><a href="/services/hurricane-wind-damage-claims/">Hurricane &amp; wind</a></li>
      <li><a href="/services/hail-damage-claims/">Hail</a></li>
      <li><a href="/services/water-damage-claims/">Water &amp; burst pipes</a></li>
      <li><a href="/services/fire-smoke-damage-claims/">Fire &amp; smoke</a></li>
      <li><a href="/services/flood-damage-claims/">Flood</a></li>
      <li><a href="/services/commercial-property-claims/">Commercial property</a></li>
      <li><a href="/services/denied-underpaid-claims/">Denied &amp; underpaid</a></li>
    </ul>

    <h2>Articles by Joseph Dittman</h2>
  </div>
  <?php sidebar_cta(); ?>
</div>
<section class="section section-alt" style="padding-top:40px">
  <div class="container">
    <div class="post-grid">
<?php foreach (POSTS as $p) post_card($p); ?>
    </div>
  </div>
</section>
<?php page_end(); ?>
