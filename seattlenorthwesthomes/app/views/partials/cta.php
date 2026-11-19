<?php defined('SNW') || (http_response_code(404) && exit); ?>
<section class="cta-band">
  <div class="wrap cta-inner">
    <div>
      <h2><?= e($title ?? 'Ready to make your move in Seattle?') ?></h2>
      <p><?= e($text ?? 'Whether you are buying your first condo or selling the family home, we will help you plan every step.') ?></p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-accent" href="/buy-a-home-in-seattle/">I Want to Buy</a>
      <a class="btn btn-ghost" href="/sell-your-home-seattle/">I Want to Sell</a>
    </div>
  </div>
</section>
