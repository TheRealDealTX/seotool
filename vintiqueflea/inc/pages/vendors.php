<?php
defined('INC') || exit;
require INC . '/forms.php';
$state = ['ok' => false, 'errors' => [], 'values' => []];
$sent = false;
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $state = process_form('vendor', [
        'name' => ['name', true, 120, 'text'],
        'business' => ['business name', true, 160, 'text'],
        'email' => ['email', true, 200, 'email'],
        'phone' => ['phone', false, 40, 'text'],
        'category' => ['category', true, 80, 'text'],
        'links' => ['website or Instagram', false, 300, 'text'],
        'about' => ['description of what you sell', true, 4000, 'text'],
    ]);
    $sent = $state['ok'];
}
page_start([
    'title' => 'Become a Vendor: Sell Vintage in Houston | Vintique Flea',
    'description' => 'Apply for a booth at Vintique Flea, a curated indoor vintage market in Houston. We welcome vintage dealers, salvage pros, makers and local food trucks.',
    'path' => '/vendors/',
    'image' => 'vendors',
]);
?>
<div class="wrap">
  <?= breadcrumbs([['Become a Vendor', '/vendors/']]) ?>
  <header class="page-head">
    <h1>Become a Vintique Flea vendor</h1>
    <p class="lede">Sell your vintage, salvage, antiques or handmade goods to Houston treasure hunters at Silver Street Studios. Food trucks welcome too.</p>
  </header>
  <figure class="banner banner--wide"><?= photo('vendors', 'A boutique display of hats, shirts and textiles', '', true, '(max-width: 1180px) 100vw, 1140px') ?></figure>
  <div class="layout-2">
    <div>
      <div class="prose">
        <h2>Who we're looking for</h2>
        <p>Vintique Flea is <strong>curated</strong>. We review every application to keep the mix fresh and the quality high. We're especially interested in:</p>
        <ul>
          <li>Mid-century modern furniture and decor dealers</li>
          <li>Vintage clothing, jewelry and accessories</li>
          <li>Architectural salvage, industrial and antique specialists</li>
          <li>Rustic and farmhouse decor, refinished furniture</li>
          <li>Records, ephemera, collectibles and curiosities</li>
          <li>Local food trucks, coffee, and craft beverage vendors</li>
        </ul>
        <h2>Apply</h2>
        <p>Tell us about your business below. Photos help: include your Instagram or website so we can see your goods and booth style.</p>
      </div>
<?php if ($sent): ?>
      <div class="notice notice--ok" role="status"><h2>Application received!</h2><p>Thanks for applying. We'll be in touch when booth space for the next edition opens up.</p></div>
<?php else: ?>
<?php if (!empty($state['errors']['_form'])): ?><div class="notice notice--err" role="alert"><?= e($state['errors']['_form']) ?></div><?php endif; ?>
      <form class="form" method="post" action="/vendors/" novalidate>
        <?= form_hidden() ?>
        <div class="form-row">
          <?= form_field('name', 'Your name', $state, 'text', ['required' => true, 'autocomplete' => 'name']) ?>
          <?= form_field('business', 'Business name', $state, 'text', ['required' => true, 'autocomplete' => 'organization']) ?>
        </div>
        <div class="form-row">
          <?= form_field('email', 'Email', $state, 'email', ['required' => true, 'autocomplete' => 'email']) ?>
          <?= form_field('phone', 'Phone (optional)', $state, 'tel', ['autocomplete' => 'tel']) ?>
        </div>
        <div class="form-row">
          <?= form_field('category', 'What do you sell?', $state, 'select', ['required' => true, 'options' => ['Mid-century modern', 'Vintage clothing & accessories', 'Architectural salvage & industrial', 'Antiques & collectibles', 'Rustic home decor', 'Records & retro tech', 'Handmade / maker', 'Food truck', 'Beverages', 'Other']]) ?>
          <?= form_field('links', 'Website or Instagram', $state, 'text', ['autocomplete' => 'url']) ?>
        </div>
        <?= form_field('about', 'Tell us about your goods', $state, 'textarea', ['required' => true]) ?>
        <button class="btn btn--primary" type="submit">Submit application</button>
      </form>
<?php endif; ?>
    </div>
    <aside class="side">
      <div class="side-card">
        <h2>Why sell here?</h2>
        <ul class="checks">
          <li>Indoor venue: no weather cancellations</li>
          <li>Shoppers who come specifically for vintage</li>
          <li>Food trucks, beer &amp; wine keep crowds lingering</li>
          <li>Run by the founders of Rice Village Flea</li>
        </ul>
      </div>
      <div class="side-card">
        <h2>Booth essentials</h2>
        <p>Folding tables, display risers, a card reader and good lighting.</p>
        <a class="btn btn--ghost btn--block" href="/shop/flea-market-gear/">Vendor &amp; picker gear</a>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
