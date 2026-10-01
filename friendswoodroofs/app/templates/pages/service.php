<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/** @var array $page */
$s = $page['service'];
partial('page-hero', ['eyebrow' => 'Roofing services', 'title' => $s['h1'], 'lead' => '', 'service' => $s['slug']]);
?>
<section class="section section--first">
  <div class="container split">
    <div class="prose" data-reveal>
      <p class="lead-dark"><?= e($s['lead']) ?></p>
      <h2>Problems this service addresses</h2>
      <p><?= e($s['problems_intro']) ?></p>
      <ul class="problem-list">
        <?php foreach ($s['problems'] as [$title, $desc]): ?>
        <li><strong><?= e($title) ?>.</strong> <?= e($desc) ?></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <figure class="split-media" data-reveal>
      <?= photo($s['image'], '(min-width: 900px) 45vw, 100vw', true) ?>
    </figure>
  </div>
</section>

<section class="section section--tint" aria-labelledby="scope-heading">
  <div class="container split split--even">
    <div data-reveal>
      <h2 id="scope-heading">What's included</h2>
      <p>The exact scope depends on your roof and is listed in your written estimate. Typical work includes:</p>
      <ul class="check-list">
        <?php foreach ($s['scope'] as $item): ?><li><?= e($item) ?></li><?php endforeach; ?>
      </ul>
    </div>
    <div data-reveal>
      <h2>What affects the cost</h2>
      <p>Every roof is different, so pricing is based on an inspection rather than a flat rate. The main factors are:</p>
      <ul class="dot-list">
        <?php foreach ($s['cost_factors'] as $item): ?><li><?= e($item) ?></li><?php endforeach; ?>
      </ul>
      <p class="small">Your estimate itemizes these so you can see what you are paying for.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="process-heading">
  <div class="container">
    <div class="section-head" data-reveal>
      <h2 id="process-heading">The typical process</h2>
    </div>
    <ol class="timeline">
      <?php foreach ($s['process'] as $i => [$title, $desc]): ?>
      <li data-reveal><span class="step-num" aria-hidden="true"><?= $i + 1 ?></span><div><h3><?= e($title) ?></h3><p><?= e($desc) ?></p></div></li>
      <?php endforeach; ?>
    </ol>
  </div>
</section>

<section class="section section--tint" aria-labelledby="faq-heading">
  <div class="container narrow">
    <h2 id="faq-heading"><?= e($s['name']) ?> FAQs</h2>
    <p>Answers here are general. Your situation depends on your roof's condition, which an inspection confirms.</p>
    <?php partial('faq-list', ['items' => $s['faqs']]); ?>
  </div>
</section>

<section class="section" aria-labelledby="next-heading">
  <div class="container">
    <div class="next-step" data-reveal>
      <div>
        <h2 id="next-heading">Next step: request a <?= e(strtolower($s['name'])) ?> estimate</h2>
        <p>Tell us what you are seeing and roughly where. A phone number is all we need to get in touch, and email is optional. We will follow up to arrange a time to look at your roof.</p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-accent btn-lg" href="/contact/?service=<?= e(rawurlencode($s['slug'])) ?>#estimate-form"><?= icon('clipboard') ?><span>Request an Estimate</span></a>
        <a class="btn btn-outline btn-lg" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call <?= e(phone_display()) ?></span></a>
      </div>
    </div>

    <div class="related-grid">
      <div data-reveal>
        <h2 class="h3">Related services</h2>
        <ul class="link-list">
          <?php foreach ($s['related'] as $slug): $r = service($slug); if (!$r) continue; ?>
          <li><a href="<?= e($r['url']) ?>"><?= e($r['name']) ?></a></li>
          <?php endforeach; ?>
          <li><a href="/services/">All roofing services</a></li>
        </ul>
      </div>
      <div data-reveal>
        <h2 class="h3">Related articles</h2>
        <ul class="link-list">
          <?php foreach ($s['articles'] as $slug): $a = article($slug); if (!$a) continue; ?>
          <li><a href="<?= e($a['url']) ?>"><?= e($a['title']) ?></a></li>
          <?php endforeach; ?>
        </ul>
      </div>
      <div data-reveal>
        <h2 class="h3">Plan ahead</h2>
        <p>Use the <a href="/roofing-project-planner/">Roofing Project Planner</a> to organize your concern, or read our <a href="/faqs/">roofing FAQs</a>.</p>
      </div>
    </div>
  </div>
</section>
