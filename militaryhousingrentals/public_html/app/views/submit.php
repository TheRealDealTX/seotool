<?php
require APP . '/forms.php';
$fields = [
    'name' => ['Your name', true, 'text'], 'email' => ['Your email', true, 'email'], 'phone' => ['Your phone', true, 'tel'],
    'pname' => ['Property name', true, 'text'], 'address' => ['Address', true, 'text'], 'base' => ['Nearest installation', false, 'text'],
    'price' => ['Starting price', false, 'text'], 'beds' => ['Bedrooms', false, 'number'], 'bath' => ['Bathrooms', false, 'number'],
    'area' => ['Area (sq ft)', false, 'number'], 'pets' => ['Pet policy', false, 'text'],
    'description' => ['Property description', true, 'textarea'], 'amenities' => ['Property amenities', false, 'textarea'],
    'photos' => ['Gallery photos (Google Drive link)', false, 'url'],
];
$res = form_handle('submit', $fields);
$v = $res['values'] ?? [];
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Submit Property', null]]);
layout_start(['title' => 'Submit Your Military Housing Rental Property', 'description' => 'List your rental property on Military Housing Rentals and reach service members and military families looking for housing near base.',
    'path' => '/submit-property/', 'nav' => '/submit-property/', 'schema' => [$crumb_schema]]);
?>
<section class="page-hero">
  <div class="wrap"><?= $crumbs ?><p class="eyebrow">For landlords, owners &amp; agents</p><h1>Submit your property for listing</h1>
  <p class="lead">Have a rental that would be a great fit for service members and military families? Submit it here to be featured on Military Housing Rentals.</p></div>
</section>
<section class="section section-tight">
  <div class="wrap contact-layout">
    <div class="card form-card">
      <ol class="form-steps" aria-hidden="true"><li class="on">Your details</li><li>Property</li><li>Description &amp; photos</li></ol>
      <?= form_notice($res, "Thank you! We received your property. Our team will review it and contact you to confirm the details and process payment securely via Stripe.") ?>
      <form method="post" action="/submit-property/" class="form" novalidate data-form data-steps>
        <?= form_hidden() ?>
        <fieldset data-step>
          <legend>Your details</legend>
          <div class="form-grid">
            <?= form_field('name', 'Your name', 'text', true, $v['name'] ?? '', 'autocomplete="name"') ?>
            <?= form_field('email', 'Your email', 'email', true, $v['email'] ?? '', 'autocomplete="email"') ?>
            <?= form_field('phone', 'Your phone', 'tel', true, $v['phone'] ?? '', 'autocomplete="tel"') ?>
          </div>
        </fieldset>
        <fieldset data-step>
          <legend>Property</legend>
          <div class="form-grid">
            <?= form_field('pname', 'Property name', 'text', true, $v['pname'] ?? '') ?>
            <?= form_field('address', 'Address', 'text', true, $v['address'] ?? '', 'autocomplete="street-address"') ?>
            <label class="field" for="f-base"><span>Nearest installation</span>
              <input id="f-base" name="base" list="base-list" value="<?= e($v['base'] ?? '') ?>">
              <datalist id="base-list"><?php foreach (bases() as $b): ?><option value="<?= e($b['name']) ?>"><?php endforeach; ?></datalist>
            </label>
            <?= form_field('price', 'Starting price', 'text', false, $v['price'] ?? '', 'placeholder="$1,800/mo"') ?>
            <?= form_field('beds', 'Bedrooms', 'number', false, $v['beds'] ?? '', 'min="0" max="12"') ?>
            <?= form_field('bath', 'Bathrooms', 'number', false, $v['bath'] ?? '', 'min="0" max="12" step="0.5"') ?>
            <?= form_field('area', 'Area (sq ft)', 'number', false, $v['area'] ?? '', 'min="0"') ?>
            <?= form_field('pets', 'Pet policy', 'text', false, $v['pets'] ?? '', 'placeholder="e.g. 2 pets, no breed restrictions"') ?>
          </div>
        </fieldset>
        <fieldset data-step>
          <legend>Description &amp; photos</legend>
          <?= form_field('description', 'Property description', 'textarea', true, $v['description'] ?? '') ?>
          <?= form_field('amenities', 'Property amenities', 'textarea', false, $v['amenities'] ?? '', 'placeholder="Garage, fenced yard, washer/dryer…"') ?>
          <?= form_field('photos', 'Gallery photos (Google Drive link)', 'url', false, $v['photos'] ?? '', 'placeholder="https://drive.google.com/…"') ?>
        </fieldset>
        <div class="step-nav">
          <button class="btn btn-light" type="button" data-step-prev hidden>Back</button>
          <button class="btn btn-primary" type="button" data-step-next>Next <?= icon('arrow') ?></button>
          <button class="btn btn-accent btn-lg" type="submit" data-step-submit><?= icon('check') ?> Submit property</button>
        </div>
      </form>
    </div>
    <aside class="contact-aside">
      <div class="card">
        <h3>How it works</h3>
        <ol class="mini-steps">
          <li>Submit your property details and photos.</li>
          <li>Our team reviews your listing and contacts you to confirm the information.</li>
          <li>We process payment securely via Stripe and publish your listing.</li>
        </ol>
        <p class="fineprint">Your contact details are used only for verification, confirmation and communication about your listing, never for anything else.</p>
        <p>Need help? <a href="/contact-us/">Contact us</a> or call <a href="<?= e(cfg('phone_href')) ?>"><?= e(cfg('phone')) ?></a>.</p>
      </div>
      <?= sidebar_listings() ?>
    </aside>
  </div>
</section>
<?php layout_end();
