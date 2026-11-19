<?php defined('M1S') || exit; ?>
<header class="page-head">
  <h1>Renter essentials</h1>
  <p class="lede">The gear our guides keep coming back to: organizers that fit small spaces, deposit-safe upgrades, smart-home helpers, and the tools that make an insurance claim easier. Each link opens Amazon so you can compare options and reviews.</p>
  <p class="disclosure"><?= e(amazon_disclosure()) ?></p>
</header>
<?php foreach ($groups as [$t, $rows]): ?>
  <section class="block">
    <div class="section-head"><h2><?= e($t['name']) ?></h2><a href="<?= e(topic_url($t)) ?>">Read the <?= e($t['name']) ?> guides →</a></div>
    <?= product_box($rows, '') ?>
  </section>
<?php endforeach; ?>
<?php if (!$groups): ?><p class="empty">Products are coming soon.</p><?php endif; ?>
