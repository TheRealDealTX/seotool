<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => 'Contact Our Seattle Real Estate Agents', 'crumbs' => [['Contact Us', '']],
    'lead' => 'Reach out using the form or our contact details. Let\'s get started on your real estate journey together.']); ?>
<section class="section tight">
  <div class="wrap listing-layout">
    <div>
      <?php partial('form-contact') ?>
    </div>
    <aside class="sidebar">
      <div class="sticky-card">
        <h2 class="h3">Get in Touch</h2>
        <p><strong>Email</strong><br><a href="mailto:<?= e(cfg('email')) ?>"><?= e(cfg('email')) ?></a></p>
<?php if (cfg('phone')): ?>        <p><strong>Phone</strong><br><a href="tel:<?= e(preg_replace('/\D/', '', cfg('phone'))) ?>"><?= e(cfg('phone')) ?></a></p>
<?php endif ?>
        <p><strong>Serving</strong><br>Seattle and the greater Puget Sound area</p>
        <p class="muted">We typically reply within one business day.</p>
        <hr>
        <p><a class="link-arrow" href="/buy-a-home-in-seattle/">Buying? Share your wish list</a></p>
        <p><a class="link-arrow" href="/sell-your-home-seattle/">Selling? Get a free value review</a></p>
      </div>
    </aside>
  </div>
</section>
