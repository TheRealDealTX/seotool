<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
$groups = faq_groups();
partial('page-hero', [
    'eyebrow' => 'FAQs',
    'title'   => 'Roofing FAQs for Friendswood Homeowners',
    'lead'    => 'Straight answers to common questions about estimates, repairs, replacement, materials, inspections, storm damage and maintenance.',
]);
?>
<section class="section">
  <div class="container faq-layout">
    <nav class="faq-toc" aria-label="FAQ topics">
      <p class="faq-toc-title">Topics</p>
      <ul>
        <?php foreach (array_keys($groups) as $g): ?>
        <li><a href="#<?= e(category_slug($g)) ?>"><?= e($g) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </nav>
    <div class="faq-groups">
      <div class="callout" role="note">
        <p><?= icon('info', 'icon icon-sm') ?> <strong>Many answers depend on your roof.</strong> Condition, materials, insurance policy and the details of your project all affect what applies to you. An inspection is the only way to confirm what your roof needs.</p>
      </div>
      <?php foreach ($groups as $g => $items): ?>
      <section class="faq-group" id="<?= e(category_slug($g)) ?>" aria-labelledby="h-<?= e(category_slug($g)) ?>">
        <h2 id="h-<?= e(category_slug($g)) ?>"><?= e($g) ?></h2>
        <?php partial('faq-list', ['items' => array_map(fn ($i) => [$i['q'], $i['a']], $items)]); ?>
      </section>
      <?php endforeach; ?>
      <p class="section-foot">Still have a question? <a href="/contact/">Contact us</a> or call <a href="<?= e(phone_href()) ?>"><?= e(phone_display()) ?></a>. You can also browse our <a href="/services/">services</a> and <a href="/blog/">roofing guides</a>.</p>
    </div>
  </div>
</section>
<?php partial('cta-band'); ?>
