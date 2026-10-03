<?php
/** Property Damage Documentation Checklist. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
$cats = [['hail', 'Hail damage', 'hail'], ['wind', 'Wind damage', 'wind'], ['fire', 'Fire damage', 'fire'], ['water', 'Water damage', 'water'], ['roof', 'Roof damage', 'home'], ['commercial', 'Commercial property', 'building']];
?>
<section class="section section-alt" aria-labelledby="cl-h">
  <div class="container" data-checklist>
    <h2 id="cl-h" class="center">1. Choose the type of damage</h2>
    <div class="cat-picker no-print" role="group" aria-label="Damage category">
      <?php foreach ($cats as [$k, $label, $ic]): ?>
      <button type="button" class="cat-btn" data-cat="<?= e($k) ?>" aria-pressed="false"><?= icon($ic, 'icon') ?><?= e($label) ?></button>
      <?php endforeach; ?>
    </div>
    <div class="tool-panel" data-cl-panel hidden>
      <div class="results-bar"><h2 class="mb-0" data-cl-title>Checklist</h2>
        <label class="save-toggle no-print"><input type="checkbox" data-cl-save> Save my progress on this device</label></div>
      <p class="print-only">McAllen Public Adjuster &middot; Claim Documentation Checklist &middot; <span data-print-date></span></p>
      <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-label="Checklist progress"><span data-cl-bar></span></div>
      <div class="progress-label"><span data-cl-count>0 of 0 complete</span><span data-cl-pct>0%</span></div>
      <div data-cl-items></div>
      <div class="field field-full">
        <label for="cl-notes">My general notes (claim number, adjuster name, dates, contacts)</label>
        <textarea id="cl-notes" data-cl-notes rows="5" maxlength="5000"></textarea>
      </div>
      <div class="tool-actions no-print">
        <button class="btn btn-gold btn-sm" type="button" data-cl-print><?= icon('printer', 'icon icon-sm') ?> Print checklist</button>
        <button class="btn btn-ghost btn-sm" type="button" data-cl-download><?= icon('download', 'icon icon-sm') ?> Download checklist</button>
        <button class="btn btn-ghost btn-sm" type="button" data-cl-reset><?= icon('refresh', 'icon icon-sm') ?> Reset progress</button>
      </div>
      <p class="small muted" style="margin-top:14px"><?= icon('shield', 'icon icon-sm') ?> Private by design: your checkmarks and notes stay in this browser. Nothing is sent to us. If you turn on &ldquo;Save my progress,&rdquo; they are stored only in this browser's local storage until you reset or clear it.</p>
    </div>
    <?php component('cta-band', ['heading' => 'Want a professional to review your documentation?']); ?>
  </div>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
