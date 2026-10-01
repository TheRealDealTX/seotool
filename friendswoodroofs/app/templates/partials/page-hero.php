<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/** @var string $title  @var string $lead  @var string $eyebrow  @var bool $actions */
$eyebrow ??= '';
$actions ??= true;
$service ??= '';
?>
<section class="page-hero">
  <div class="container page-hero-inner">
    <?php if ($eyebrow): ?><p class="eyebrow"><?= e($eyebrow) ?></p><?php endif; ?>
    <h1><?= e($title) ?></h1>
    <?php if (!empty($lead)): ?><p class="lead"><?= e($lead) ?></p><?php endif; ?>
    <?php if ($actions): ?>
    <div class="hero-actions">
      <a class="btn btn-accent btn-lg" href="/contact/<?= $service ? '?service=' . e(rawurlencode($service)) : '' ?>#estimate-form"><?= icon('clipboard') ?><span>Request an Estimate</span></a>
      <a class="btn btn-light btn-lg" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call Now</span></a>
    </div>
    <?php endif; ?>
  </div>
</section>
