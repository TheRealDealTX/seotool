<?php
/** Contact + Free Claim Review pages: copy beside the form. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page + ['hide_hero_cta' => true]]);
?>
<section class="section section-alt">
  <div class="container split split-form">
    <div class="prose reveal-left">
      <?= $body ?>
      <div class="sidebar-card" style="margin-top:24px">
        <ul class="footer-contact" style="margin:0">
          <li><?= icon('phone', 'icon icon-sm') ?> <span><strong>Call or text:</strong> <a href="<?= e(tel_link()) ?>"><?= e(cfg('phone_display')) ?></a></span></li>
          <li><?= icon('mail', 'icon icon-sm') ?> <span><strong>Email:</strong> <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a></span></li>
          <li><?= icon('map', 'icon icon-sm') ?> <span><strong>Service area:</strong> McAllen, Hidalgo County, and surrounding Rio Grande Valley communities</span></li>
          <li><?= icon('shield', 'icon icon-sm') ?> <span><?= e(cfg('company')) ?> &middot; TDI License #<?= e(cfg('license')) ?></span></li>
        </ul>
      </div>
    </div>
    <div class="form-card reveal-right" id="form">
      <h2 class="form-card-title">Free Claim Review request</h2>
      <p class="small muted">Fields marked <span class="req">*</span> are required. It takes about two minutes.</p>
      <?php component('claim-form', ['context' => $page['title']]); ?>
    </div>
  </div>
</section>
<?php if (!empty($page['faqs'])): ?>
<section class="section"><div class="container narrow"><?php component('faq', ['faqs' => $page['faqs']]); ?></div></section>
<?php endif; ?>
