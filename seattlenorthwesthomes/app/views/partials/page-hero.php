<?php defined('SNW') || (http_response_code(404) && exit); ?>
<section class="page-hero<?= !empty($image) ? ' has-image' : '' ?>"<?= !empty($image) ? ' style="--hero:url(' . e($image) . ')"' : '' ?>>
  <div class="wrap">
    <?php partial('breadcrumbs', ['crumbs' => $crumbs]) ?>
    <h1><?= e($title) ?></h1>
    <?php if (!empty($lead)): ?><p class="lead"><?= e($lead) ?></p><?php endif ?>
  </div>
</section>
