<?php
page_start([
    'title'       => 'Free Career Tools & Calculators | Best Jobs Pro',
    'description' => 'Free career tools from Best Jobs Pro: Texas paycheck calculator, 1099 tax estimator, freelance rate calculator, résumé keyword checker and job match quiz.',
    'path'        => '/career-tools/',
    'crumbs'      => [['Career Tools', '/career-tools/']],
    'schema'      => [[
        '@type' => 'ItemList', 'name' => 'Best Jobs Pro career tools',
        'itemListElement' => array_map(fn($slug, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => TOOLS[$slug][0], 'url' => url('/career-tools/' . $slug . '/')], array_keys(TOOLS), range(0, count(TOOLS) - 1)),
    ]],
]);
page_hero('Free Career Tools', 'Calculators and checkers that help you plan your pay, sharpen your résumé, price your freelance work and hire smarter. Free, private and built by Best Jobs Pro.', [['Career Tools', '/career-tools/']], '', 'Job search pro toolkit');
?>
<section class="section">
  <div class="wrap">
    <div class="section__head reveal"><p class="eyebrow">For job seekers &amp; freelancers</p><h2>Pick a tool</h2><p>Everything runs in your browser. Nothing you type is stored or sent anywhere.</p></div>
    <div class="cards cards--3 tool-cards stagger">
<?php foreach (TOOLS as $slug => [$title, $desc, $ic]): ?>
      <article class="card tilt"><div class="card__ico"><?= icon($ic) ?></div><h3><a href="/career-tools/<?= $slug ?>/" style="color:inherit;text-decoration:none"><?= e($title) ?></a></h3><p><?= e($desc) ?></p><a class="card__link" href="/career-tools/<?= $slug ?>/">Open tool <?= icon('arrow') ?></a></article>
<?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Try it now</p>
      <h2>What will you take home?</h2>
      <p>Texas has no state income tax, so your paycheck goes further than in many states. Enter an hourly wage or salary to see your estimated take-home pay per week, paycheck, month and year.</p>
      <p>Comparing offers? Run each one and see the difference in real dollars, including overtime.</p>
      <a class="btn btn--outline" href="/job-postings/">See Texas job openings <?= icon('arrow') ?></a>
    </div>
    <div class="reveal"><?= tool_widget('paycheck', true) ?></div>
  </div>
</section>
<?= cta_band('Tools help. A recruiter helps more.', 'Talk to Best Jobs Pro about jobs that match your skills and pay goals. Free for job seekers, 24/7.') ?>
<?php page_end(['/assets/js/tools.js']);
