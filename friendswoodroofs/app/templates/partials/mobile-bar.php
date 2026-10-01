<?php defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/** @var bool $hasForm */ ?>
<div class="mobile-bar" aria-label="Quick actions" role="region">
  <a class="mobile-bar-btn mobile-bar-call" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call Now</span></a>
  <a class="mobile-bar-btn mobile-bar-estimate" href="<?= $hasForm ? '#estimate-form' : '/contact/#estimate-form' ?>"><?= icon('clipboard') ?><span>Request an Estimate</span></a>
</div>
