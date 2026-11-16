<?php
$title = 'Free Insurance Claim Calculators & Tools | TX Insurance Appraiser';
$desc  = 'Free tools for Texas property owners: recoverable depreciation calculator, appraisal cost calculator, roof square calculator, claim deadlines and checklist.';
ob_start(); ?>
<section class="hero hero-sm">
  <div class="hero-bg" style="background-image:url(/assets/img/site/TX-Insurance-Appraiser-Matterport-Xactimate.webp)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Free claim tools</span>
      <h1 class="anim">Free Insurance Claim Calculators for Texas Property Owners</h1>
      <p class="lead anim">Check your settlement, understand depreciation, verify roof measurements and track Texas deadlines — free, private and instant. Nothing you enter leaves your browser.</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap grid g3">
    <?php $i = 0; foreach (TOOLS as $slug => $t): ?>
    <a class="card tilt reveal d<?= $i++ % 3 + 1 ?>" href="/tools/<?= $slug ?>/" style="text-decoration:none">
      <div class="ic-badge ic-gold"><?= icon($t['icon'], 28) ?></div>
      <h2 style="font-size:1.3rem"><?= e($t['title']) ?></h2>
      <p><?= e($t['short']) ?></p>
      <span class="link-arrow">Open the tool <?= icon('arrow', 16) ?></span>
    </a>
    <?php endforeach; ?>
    <div class="card reveal" style="background:linear-gradient(160deg,var(--navy-3),var(--navy));color:#cfe0ee">
      <div class="ic-badge"><?= icon('chat', 28) ?></div>
      <h2 style="font-size:1.3rem;color:#fff">Want a professional opinion?</h2>
      <p style="color:#cfe0ee">Calculators give estimates. For a real review of your carrier’s estimate, talk to TX Insurance Appraiser — free.</p>
      <a class="btn btn-gold" href="/contact-us/">Free claim review</a>
    </div>
  </div>
</section>
<?= cta_band() ?>
<?php
$content = (string) ob_get_clean();
$items = [];
$n = 0;
foreach (TOOLS as $slug => $t) {
    $items[] = ['@type' => 'ListItem', 'position' => ++$n, 'name' => $t['title'], 'url' => abs_url('/tools/' . $slug . '/')];
}
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/tools/',
    'crumbs' => [['Home', '/'], ['Free Tools', '/tools/']],
    'schema' => [schema_webpage('CollectionPage', $title, $desc, '/tools/'), ['@type' => 'ItemList', 'itemListElement' => $items]],
], $content);
