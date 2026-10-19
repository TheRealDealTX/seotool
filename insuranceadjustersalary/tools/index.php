<?php
require dirname(__DIR__) . '/inc/config.php';

$page = [
    'title' => 'Free Insurance Adjuster Tools & Salary Calculators',
    'description' => 'Free insurance adjuster tools: salary calculator, CAT deployment earnings estimator, public adjuster fee calculator and a salary-by-state explorer.',
    'path' => '/tools/',
    'image' => 'women-laptop.webp',
];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Free tools', 'Insurance Adjuster Calculators &amp; Tools', 'Run the numbers before you take the job, the deployment or the claim. Every tool is free, works on your phone and never asks for an email.', 'women-laptop.webp', ['Tools' => null]);
?>
<section class="section">
  <div class="container">
    <div class="grid-2">
<?php foreach (tools() as $i => $t): ?>
      <a class="card tool-card spotlight tilt reveal reveal-delay-<?= $i % 2 ?>" href="<?= e($t['path']) ?>" style="padding:38px">
        <div class="icon-wrap"><?= icon($t['icon'], 28) ?></div>
        <h2 style="font-size:1.6rem"><?= e($t['name']) ?></h2>
        <p><?= e($t['blurb']) ?></p>
        <span class="link-arrow">Open tool <?= icon('arrow', 16) ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section-soft">
  <div class="container split">
    <div class="photo-frame reveal"><img src="/assets/img/coins-growth.webp" alt="Coins with a growing plant - planning adjuster income" width="1200" height="800" loading="lazy"></div>
    <div class="reveal reveal-delay-1">
      <span class="eyebrow">Why we built these</span>
      <h2>Adjuster pay is hard to compare</h2>
      <p>A staff salary, a fee schedule, a daily rate and a contingency percentage are four different ways to get paid. Our calculators turn each one into the same thing &mdash; dollars per year, per day and per hour &mdash; so you can compare a carrier offer against a storm season or a public adjusting practice.</p>
      <p>Start with the <a href="/salary-calculator/">insurance adjuster salary calculator</a>, then read our guide on <a href="<?= BLOG_BASE ?>how-do-insurance-adjusters-get-paid/">how insurance adjusters get paid</a>.</p>
    </div>
  </div>
</section>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
