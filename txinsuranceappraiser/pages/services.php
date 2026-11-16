<?php
$title = 'Insurance Appraisal & Estimating Services | TX Insurance Appraiser';
$desc  = 'Insurance appraisal, umpire services, Matterport 3D scans, and Xactimate and Symbility estimates for Texas property claims.';
$svc = [
    ['appraisal', 'scale', 'Insurance Appraisal', 'TX-Insurance-Appraiser-Appraisals.webp', 'We act as your appraiser under the policy’s appraisal clause — inspecting, estimating and negotiating a fair award for underpaid claims.'],
    ['umpire', 'gavel', 'Umpire Services', 'TX-Insurance-Appraiser-Offers.webp', 'Neutral umpire services for Texas appraisals when the two appraisers can’t agree on the amount of loss.'],
    ['matterport', 'cube', 'Matterport 3D Scans', 'TX-Insurance-Appraiser-Matterport.webp', 'Measurable 3D digital twins of damaged property — evidence preserved before repairs begin.'],
    ['xactimate-estimate', 'calc', 'Xactimate Estimates', 'TX-Insurance-Appraiser-Matterport-Xactimate.webp', 'Line-item estimates in the platform most carriers use, priced for your ZIP code and date of loss.'],
    ['symbility-estimate', 'doc', 'Symbility Estimates', 'TX-Insurance-Appraiser-Matterport-Symbility.webp', 'Estimates that match carriers using CoreLogic’s Symbility platform for a true apples-to-apples comparison.'],
];
$faqs = [
    ['q' => 'Which TX Insurance Appraiser service do I need?', 'a' => 'If your carrier accepted the claim but underpaid it and negotiation has stalled, start with insurance appraisal. If you only need a professional estimate to support a supplement, an Xactimate or Symbility estimate may be enough. Matterport is ideal for documenting interior damage before repairs.'],
    ['q' => 'Do you handle both residential and commercial claims?', 'a' => 'Yes. We work on homes, multi-family properties, HOAs, churches, hotels, retail, office and industrial buildings throughout Texas.'],
    ['q' => 'Do you provide legal advice?', 'a' => 'No. TX Insurance Appraiser is not a law firm. We determine and document the amount of loss. For coverage denials or legal claims, consult a Texas attorney.'],
];
ob_start(); ?>
<section class="hero hero-sm">
  <div class="hero-bg" style="background-image:url(/assets/img/site/TX-Insurance-Appraiser-Background.webp)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Our services</span>
      <h1 class="anim">Insurance Appraisal &amp; Estimating Services in Texas</h1>
      <p class="lead anim">Five specialized services, one goal: a complete, defensible amount of loss for your Texas property claim.</p>
      <div class="hero-actions anim"><a class="btn btn-gold btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> <?= e(SITE['phone_short']) ?></a><a class="btn btn-ghost-light btn-lg" href="/contact-us/">Free claim review</a></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap grid g3">
    <?php foreach ($svc as $i => [$slug, $ic, $t, $img, $d]): ?>
    <article class="card card-img tilt reveal d<?= $i % 3 + 1 ?>">
      <a class="ci-media" href="/services/<?= $slug ?>/"><img src="/assets/img/site/<?= $img ?>" alt="<?= e($t) ?> by TX Insurance Appraiser" width="800" height="420" loading="lazy"></a>
      <div class="ci-body">
        <div class="ic-badge" style="margin-top:-50px;position:relative"><?= icon($ic, 26) ?></div>
        <h2 style="font-size:1.35rem"><a href="/services/<?= $slug ?>/" style="text-decoration:none;color:inherit"><?= e($t) ?></a></h2>
        <p><?= e($d) ?></p>
        <a class="link-arrow" href="/services/<?= $slug ?>/">Learn more <?= icon('arrow', 16) ?></a>
      </div>
    </article>
    <?php endforeach; ?>
    <article class="card reveal d3" style="background:linear-gradient(160deg,var(--navy-3),var(--navy));color:#d9e6f1">
      <div class="ic-badge ic-gold"><?= icon('search', 26) ?></div>
      <h2 style="font-size:1.35rem;color:#fff">Free Claim Review</h2>
      <p style="color:#cfe0ee">Not sure which service fits? Send your carrier’s estimate and we’ll recommend the most cost-effective path — even if that means you don’t need us.</p>
      <a class="btn btn-gold" href="/contact-us/">Start my review</a>
    </article>
  </div>
</section>
<?= faq_html($faqs, 'Services FAQs') ?>
<?= cta_band() ?>
<?php
$content = (string) ob_get_clean();
$list = ['@type' => 'ItemList', 'itemListElement' => array_map(fn($s, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $s[2], 'url' => abs_url('/services/' . $s[0] . '/')], $svc, array_keys($svc))];
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/services/',
    'crumbs' => [['Home', '/'], ['Services', '/services/']],
    'schema' => [schema_webpage('CollectionPage', $title, $desc, '/services/'), $list, schema_faq($faqs)],
], $content);
