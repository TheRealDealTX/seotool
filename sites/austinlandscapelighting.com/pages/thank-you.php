<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$page = [
    'title' => 'Thank You | Austin Landscape Lighting',
    'description' => 'Your estimate request has reached Austin Landscape Lighting. A lighting designer will be in touch within one business day.',
    'path' => '/thank-you/',
    'robots' => 'noindex, nofollow',
    'schema' => [schema_webpage(['title' => 'Thank you', 'description' => 'Request received.', 'path' => '/thank-you/'])],
];
$mailWarn = isset($_GET['mail']) && $_GET['mail'] === '0';
ob_start(); ?>
<section class="sub-hero spotlight" data-spotlight>
  <div class="stars" data-stars></div>
  <div class="container" style="text-align:center;max-width:760px" data-reveal>
    <p class="eyebrow">Request received</p>
    <h1 class="display">Thank you. Your evenings are about to get better.</h1>
    <p class="lede" style="margin:0 auto">A designer from Austin Landscape Lighting will reach out within one business day to schedule your free dusk consultation. If it is urgent, call <a href="<?= BIZ['phone_href'] ?>"><?= e(BIZ['phone_display']) ?></a>.</p>
    <?php if ($mailWarn): ?><p class="form-status form-status--err" style="margin-top:20px">We saved your request but our email notification did not go through. To be safe, please also call or text <?= e(BIZ['phone_display']) ?>.</p><?php endif; ?>
    <ol class="thanks-steps">
      <li><div><strong>We call or text to confirm</strong><br><span style="color:var(--ink-2)">Usually same day, to pick a time near dusk.</span></div></li>
      <li><div><strong>Free walkthrough and design</strong><br><span style="color:var(--ink-2)">Fixture-by-fixture plan with a written, itemized estimate.</span></div></li>
      <li><div><strong>One-day install and night aiming</strong><br><span style="color:var(--ink-2)">Then your two-year workmanship warranty begins.</span></div></li>
    </ol>
    <div class="cta-band__actions">
      <a class="btn btn--primary" href="/tools/">Try a planning tool while you wait <?= icon('arrow') ?></a>
      <a class="btn btn--ghost" href="/gallery/">Browse the gallery <?= icon('camera') ?></a>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
