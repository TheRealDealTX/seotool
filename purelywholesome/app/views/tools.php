<?php
$crumbs = [['Home', '/'], ['Farm Tools', '/tools/']];
$heroTitle = 'Free Farm & Kitchen Tools'; $heroEyebrow = count(tools()) . ' interactive tools';
$heroLede = 'Calculators and quick checks from Purely Wholesome Farm for the numbers that matter in a farm kitchen and barn: salt ratios, pull temperatures, kidding dates, altitude adjustments and more. Free, no sign-up, made for your phone.';
include __DIR__ . '/partials/page-hero.php';
?>
<section class="section section--tight">
  <div class="wrap">
    <div class="tool-cards tool-cards--page">
      <?php $n = 0; foreach (tools() as $slug => $t): ?>
        <a class="tool-card tool-card--light reveal" href="/tools/<?= $slug ?>/" style="--d:<?= $n++ * 50 ?>ms">
          <span class="tool-card__icon tool-card__icon--<?= $t['color'] ?>"><?= icon($t['icon']) ?></span>
          <strong><?= e($t['name']) ?></strong><small><?= e($t['short']) ?></small>
          <span class="tool-card__go">Open tool <?= icon('arrow') ?></span>
        </a>
      <?php endforeach ?>
    </div>
  </div>
</section>
