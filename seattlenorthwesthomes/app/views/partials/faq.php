<?php defined('SNW') || (http_response_code(404) && exit); if (!$faq) return; ?>
<section class="faq">
  <h2><?= e($heading ?? 'Frequently Asked Questions') ?></h2>
<?php foreach ($faq as $f): ?>
  <details><summary><?= e($f['q']) ?></summary><p><?= e($f['a']) ?></p></details>
<?php endforeach ?>
</section>
