<?php
defined('TR_ROOT') || exit;
$crumbs = [['Roofing Tools', '/tools/']];
layout_start([
    'title' => 'Free Roofing Tools & Calculators', 'description' => 'Free roofing tools for Temple homeowners: roof replacement cost calculator, roof pitch and area calculator and a storm damage self-check.',
    'path' => '/tools/', 'crumbs' => $crumbs,
]);
page_hero(['h1' => 'Free Roofing Tools for Temple Homeowners', 'lead' => 'Plan a budget, measure your roof and check for storm damage — right in your browser, with no sign-up.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true]);
?>
<section class="section">
  <div class="container">
    <div class="tool-grid tool-grid--lg">
      <?php foreach (catalog('tools') as $slug => $t): ?><?= tool_card($slug, $t) ?><?php endforeach; ?>
      <article class="tool-card reveal">
        <span class="tool-card__icon"><?= icon('cloud-sun') ?></span>
        <h3 class="tool-card__title"><a href="/weather/">Temple Weather &amp; Roofing Forecast</a></h3>
        <p>Live conditions, a seven-day forecast with wind gusts and storm chances, and active National Weather Service alerts for Temple.</p>
        <a class="card__link" href="/weather/">Check the forecast <?= icon('arrow-right') ?></a>
      </article>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container split">
    <div class="split__copy reveal">
      <h2 class="section-title">How to Use These Tools</h2>
      <p>The calculators do real math on the numbers you enter, and they show their assumptions so you can see how each figure is produced. They are designed for planning: getting a feel for the size of a project, comparing materials or deciding whether a storm warrants a closer look.</p>
      <p>What they cannot do is see your roof. Hidden decking damage, flashing details, ventilation problems and code requirements all affect the real scope and price. When you are ready for real numbers, a <a href="/free-roof-inspection/">free roof inspection</a> gives you a written estimate based on your actual roof.</p>
    </div>
    <div class="split__media reveal"><figure class="media-frame"><?= img('asphalt-shingles-closeup', 'Close-up of asphalt roof shingles', ['sizes' => '(max-width: 900px) 100vw, 50vw']) ?></figure></div>
  </div>
</section>
<?php final_cta('Want Exact Numbers? Get a Free Roof Inspection.', '', '/tools/'); ?>
<?php layout_end();
