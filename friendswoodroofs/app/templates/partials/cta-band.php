<?php
/** @var string $title  @var string $text  @var string $service optional service slug to prefill */
$title ??= 'Ready to talk about your roof?';
$text  ??= 'Tell us what you are seeing and we will explain your options in plain language, with a written estimate before any work begins.';
$service ??= '';
$href = '/contact/' . ($service ? '?service=' . rawurlencode($service) : '') . '#estimate-form';
?>
<section class="cta-band" aria-labelledby="cta-<?= e(md5($title)) ?>">
  <div class="container cta-inner" data-reveal>
    <div>
      <h2 id="cta-<?= e(md5($title)) ?>"><?= e($title) ?></h2>
      <p><?= e($text) ?></p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-accent btn-lg" href="<?= e($href) ?>"><?= icon('clipboard') ?><span>Request an Estimate</span></a>
      <a class="btn btn-light btn-lg" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call <?= e(phone_display()) ?></span></a>
    </div>
  </div>
</section>
