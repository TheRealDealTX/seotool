<?php $faqs = $faqs ?? []; $heading = $heading ?? 'Frequently Asked Questions'; if ($faqs): ?>
<section class="faq-block" aria-labelledby="faq-heading-<?= e($id ?? 'main') ?>">
  <h2 id="faq-heading-<?= e($id ?? 'main') ?>"><?= e($heading) ?></h2>
  <div class="accordion">
    <?php foreach ($faqs as $f): ?>
    <details class="accordion-item">
      <summary><?= e($f['q']) ?><span class="accordion-icon" aria-hidden="true"></span></summary>
      <div class="accordion-body"><?= $f['a'] ?></div>
    </details>
    <?php endforeach; ?>
  </div>
</section>
<?php endif; ?>
