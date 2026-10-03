<?php /** Sidebar shared by pages, posts, and services. Uses $page and $toc. */ ?>
<div class="sidebar-sticky">
  <?php if (!empty($toc) && count($toc) >= 3): ?>
  <nav class="toc" aria-label="On this page">
    <p class="toc-title">On this page</p>
    <ol>
      <?php foreach ($toc as $t): ?><li><a href="#<?= e($t['id']) ?>"><?= e($t['text']) ?></a></li><?php endforeach; ?>
    </ol>
  </nav>
  <?php endif; ?>
  <div class="sidebar-card sidebar-cta">
    <p class="sidebar-cta-title">Free Claim Review</p>
    <p>Questions about a denied, delayed, or underpaid claim? Talk with a licensed Texas public adjuster.</p>
    <a class="btn btn-gold btn-block" href="/free-claim-review/">Request a Review</a>
    <a class="btn btn-outline-light btn-block" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_short')) ?></a>
  </div>
  <div class="sidebar-card">
    <p class="sidebar-title">Claim tools</p>
    <ul class="sidebar-links">
      <li><a href="/claim-calculator/"><?= icon('calc', 'icon icon-sm') ?> Settlement calculator</a></li>
      <li><a href="/claim-documentation-checklist/"><?= icon('clipboard', 'icon icon-sm') ?> Documentation checklist</a></li>
      <li><a href="/storm-lookup/"><?= icon('search', 'icon icon-sm') ?> Storm event lookup</a></li>
      <li><a href="/weather-events/"><?= icon('storm', 'icon icon-sm') ?> Recent weather events</a></li>
      <li><a href="/local-building-codes/"><?= icon('hammer', 'icon icon-sm') ?> McAllen building codes</a></li>
    </ul>
  </div>
</div>
