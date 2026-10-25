<?php
require __DIR__ . '/../inc/layout.php';

$niches = ['Fashion', 'Motocross', 'Mountain Biking', 'Fitness', 'Luxury', 'Real Estate', 'Finance', 'Beauty', 'Gaming', 'Travel', 'Food', 'Tech', 'Other'];
$platforms = ['instagram' => 'Instagram', 'tiktok' => 'TikTok', 'youtube' => 'YouTube', 'facebook' => 'Facebook', 'pinterest' => 'Pinterest'];
$ranges = ['Under 1K', '1K - 10K', '10K - 50K', '50K - 100K', '100K - 500K', '500K+'];

page_start([
    'title' => 'Get Started With Monetizing Influencers',
    'description' => 'Get started with Monetizing Influencers: tell us about your channel and get a free outline of the brand deals and income streams that fit your niche.',
    'path' => '/get-started/',
    'extra_css' => ['/assets/css/pages.css'],
]);

page_hero('Free monetization plan',
    'Get Started With <span class="grad-text">Monetizing Influencers</span>',
    'Partner with Monetizing Influencers to find the most profitable ways to earn from your audience. Answer a few quick questions and we will send you a free outline of the income streams, brand categories and next steps that fit your niche, platform and goals.',
    [['Get Started', '/get-started/']]);
?>
<script>document.documentElement.classList.add('js');</script>
<section class="section" style="padding-top:10px">
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 class="reveal">What happens next</h2>
      <div class="card-grid" style="margin-top:20px">
        <div class="card reveal"><span class="ico-badge"><?= icon('file') ?></span><h3>1. You tell us about your channel</h3><p>Platform, niche, audience size and goals. It takes about two minutes.</p></div>
        <div class="card reveal"><span class="ico-badge"><?= icon('search') ?></span><h3>2. We review your audience</h3><p>We look at your content, engagement and the brands already spending in your niche.</p></div>
        <div class="card reveal"><span class="ico-badge"><?= icon('mail') ?></span><h3>3. You get a plan by email</h3><p>Within 2 business days: your best income streams, a suggested rate range and the first brands to pitch.</p></div>
      </div>
      <div class="callout reveal"><?= icon('shield') ?><p>Free and no obligation. We never share your details. Read our <a href="/privacy-policy/">privacy policy</a>.</p></div>
    </div>

    <div class="glass-panel gradient-border reveal" id="get-started">
      <?= form_flash('get-started') ?>
      <form class="form js-form ms-form" action="/api/form.php" method="post" novalidate>
        <?= form_guard('get-started', '/get-started/') ?>
        <div class="ms-progress js-only" aria-hidden="true" style="display:none"><span class="done"></span><span></span><span></span></div>
        <p class="ms-label js-only" style="display:none" aria-live="polite">Step 1 of 3</p>

        <fieldset class="ms-step active">
          <legend>About you</legend>
          <div class="field"><label for="gs-name">Name *</label><input id="gs-name" type="text" name="name" required autocomplete="name"></div>
          <div class="field"><label for="gs-email">Email *</label><input id="gs-email" type="email" name="email" required autocomplete="email"></div>
          <div class="field"><label for="gs-company">Company or brand name <span class="hint">(optional)</span></label><input id="gs-company" type="text" name="company"></div>
          <div class="field"><label for="gs-country">Country</label><input id="gs-country" type="text" name="country" autocomplete="country-name"></div>
        </fieldset>

        <fieldset class="ms-step">
          <legend>Your channel</legend>
          <div class="field"><span class="field-label" style="display:block;font-weight:700;font-size:.92rem;margin-bottom:6px">Primary platform</span>
            <div class="choice-grid">
<?php foreach ($platforms as $v => $label): ?>
              <label><input type="radio" name="primary_platform" value="<?= e($label) ?>"<?= $v === 'instagram' ? ' checked' : '' ?>><span><?= icon($v) ?> <?= e($label) ?></span></label>
<?php endforeach; ?>
            </div>
          </div>
          <div class="field"><label for="gs-niche">Niche</label>
            <select id="gs-niche" name="niche"><option value="">Choose your niche</option><?php foreach ($niches as $n): ?><option><?= e($n) ?></option><?php endforeach; ?></select></div>
          <div class="field"><label for="gs-followers">Followers on that platform</label>
            <select id="gs-followers" name="followers"><?php foreach ($ranges as $r): ?><option><?= e($r) ?></option><?php endforeach; ?></select></div>
          <div class="field"><label for="gs-handle">Handle or channel link</label><input id="gs-handle" type="text" name="handle" placeholder="@yourname"></div>
        </fieldset>

        <fieldset class="ms-step">
          <legend>Your goals</legend>
          <div class="field"><span style="display:block;font-weight:700;font-size:.92rem;margin-bottom:6px">What do you want help with?</span>
            <div class="choice-grid">
<?php foreach (['Brand deals', 'Pricing my content', 'Affiliate income', 'My own products', 'A website', 'Growing my audience'] as $g): ?>
              <label><input type="checkbox" name="interests[]" value="<?= e($g) ?>"><span><?= e($g) ?></span></label>
<?php endforeach; ?>
            </div>
          </div>
          <div class="field"><label for="gs-goals">Anything else we should know?</label><textarea id="gs-goals" name="goals" placeholder="Your current income streams, brands you love, a revenue goal..."></textarea></div>
        </fieldset>

        <div class="ms-nav">
          <button class="btn btn-ghost js-only ms-back" type="button" style="display:none"><?= icon('arrow', 'ico flip') ?> Back</button>
          <button class="btn btn-glow js-only ms-next" type="button" style="display:none">Next <?= icon('arrow') ?></button>
          <button class="btn btn-glow ms-submit" type="submit"><?= icon('rocket') ?> Send my free plan request</button>
        </div>
      </form>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap">
    <div class="section-head"><span class="kicker reveal">While you wait</span><h2 class="reveal">Free tools to try right now</h2></div>
    <div class="card-grid cols-3">
      <article class="card tool-card tilt reveal"><a href="/tools/influencer-earnings-calculator/"><span class="ico-badge"><?= icon('calc') ?></span><h3>Earnings Calculator</h3><p>See what a sponsored post on your account is worth.</p><span class="more">Calculate <?= icon('arrow') ?></span></a></article>
      <article class="card tool-card tilt reveal"><a href="/tools/media-kit-builder/"><span class="ico-badge"><?= icon('file') ?></span><h3>Media Kit Builder</h3><p>Make a one-page media kit to send to brands.</p><span class="more">Build it <?= icon('arrow') ?></span></a></article>
      <article class="card tool-card tilt reveal"><a href="/monetization/"><span class="ico-badge"><?= icon('dollar') ?></span><h3>Monetization Guide</h3><p>All 12 ways influencers get paid, with first steps.</p><span class="more">Read the guide <?= icon('arrow') ?></span></a></article>
    </div>
  </div>
</section>

<style>.ico.flip{transform:rotate(180deg)}</style>
<script>
document.addEventListener('DOMContentLoaded', function () {
  var form = document.querySelector('.ms-form');
  if (!form) return;
  var steps = form.querySelectorAll('.ms-step'), bars = form.querySelectorAll('.ms-progress span'),
      label = form.querySelector('.ms-label'), back = form.querySelector('.ms-back'), next = form.querySelector('.ms-next'),
      submit = form.querySelector('.ms-submit'), cur = 0;
  form.querySelector('.ms-progress').style.display = '';
  label.style.display = '';
  function show(i) {
    cur = i;
    steps.forEach(function (s, k) { s.classList.toggle('active', k === i); });
    bars.forEach(function (b, k) { b.classList.toggle('done', k <= i); });
    label.textContent = 'Step ' + (i + 1) + ' of ' + steps.length;
    back.style.display = i > 0 ? '' : 'none';
    next.style.display = i < steps.length - 1 ? '' : 'none';
    submit.style.display = i === steps.length - 1 ? '' : 'none';
  }
  function valid(i) {
    var ok = true;
    steps[i].querySelectorAll('[required]').forEach(function (el) { if (ok && !el.checkValidity()) { el.reportValidity(); ok = false; } });
    return ok;
  }
  next.addEventListener('click', function () { if (valid(cur)) { show(cur + 1); var f = steps[cur].querySelector('input,select,textarea'); if (f) f.focus(); } });
  back.addEventListener('click', function () { show(cur - 1); });
  form.addEventListener('submit', function (e) {
    for (var i = 0; i < steps.length; i++) { if (!valid(i)) { show(i); valid(i); e.preventDefault(); e.stopImmediatePropagation(); return; } }
  }, true);
  form.addEventListener('reset', function () { setTimeout(function () { show(0); }, 0); });
  show(0);
});
</script>
<?php page_end();
