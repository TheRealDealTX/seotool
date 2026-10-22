<?php $heading = $heading ?? null; ?>
<aside class="cta-band reveal" aria-label="Free Claim Review">
  <div class="cta-band-icon"><?= icon('clipboard', 'icon icon-lg') ?></div>
  <div class="cta-band-text">
    <p class="cta-band-title"><?= e($heading ?: 'Not sure your claim was handled fairly?') ?></p>
    <p>Request a <strong>Free Claim Review</strong>. We will look at what happened, what your insurer has said, and explain your options&mdash;no cost, no obligation.</p>
  </div>
  <div class="cta-band-actions">
    <a class="btn btn-gold" href="/free-claim-review/">Free Claim Review</a>
    <a class="btn btn-ghost" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_short')) ?></a>
  </div>
</aside>
