<?php
defined('INC') || exit;
require INC . '/forms.php';
$state = ['ok' => false, 'errors' => [], 'values' => []];
$sent = false;
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $state = process_form('contact', [
        'name' => ['name', true, 120, 'text'],
        'email' => ['email', true, 200, 'email'],
        'phone' => ['phone', false, 40, 'text'],
        'topic' => ['topic', false, 60, 'text'],
        'message' => ['message', true, 5000, 'text'],
    ]);
    $sent = $state['ok'];
}
page_start([
    'title' => 'Contact Vintique Flea | Houston Vintage Market',
    'description' => 'Contact Vintique Flea, the curated indoor vintage market at Silver Street Studios in Houston. Questions about market dates, vendors or partnerships.',
    'path' => '/contact/',
]);
add_schema(['@type' => 'ContactPage', 'name' => 'Contact Vintique Flea', 'url' => abs_url('/contact/')]);
?>
<div class="wrap">
  <?= breadcrumbs([['Contact', '/contact/']]) ?>
  <header class="page-head">
    <h1>Contact Vintique Flea</h1>
    <p class="lede">Questions about market dates, booths, food trucks or partnerships? Send us a note and we'll get back to you.</p>
  </header>
  <div class="layout-2">
    <div>
<?php if ($sent): ?>
      <div class="notice notice--ok" role="status"><h2>Thanks, your message is on its way!</h2><p>We usually reply within a few days.</p></div>
<?php else: ?>
<?php if (!empty($state['errors']['_form'])): ?><div class="notice notice--err" role="alert"><?= e($state['errors']['_form']) ?></div><?php endif; ?>
      <form class="form" method="post" action="/contact/" novalidate>
        <?= form_hidden() ?>
        <div class="form-row">
          <?= form_field('name', 'Name', $state, 'text', ['required' => true, 'autocomplete' => 'name']) ?>
          <?= form_field('email', 'Email', $state, 'email', ['required' => true, 'autocomplete' => 'email']) ?>
        </div>
        <div class="form-row">
          <?= form_field('phone', 'Phone (optional)', $state, 'tel', ['autocomplete' => 'tel']) ?>
          <?= form_field('topic', 'Topic', $state, 'select', ['options' => ['General question', 'Market dates & tickets', 'Vendor booth', 'Food truck', 'Press & partnerships']]) ?>
        </div>
        <?= form_field('message', 'Message', $state, 'textarea', ['required' => true]) ?>
        <button class="btn btn--primary" type="submit">Send message</button>
      </form>
<?php endif; ?>
    </div>
    <aside class="side">
      <div class="side-card">
        <h2>Market location</h2>
        <address><?= e(VENUE['name']) ?><br><?= e(VENUE['street']) ?><br><?= e(VENUE['city']) ?>, <?= e(VENUE['region']) ?> <?= e(VENUE['postal']) ?></address>
        <p class="small">Washington Avenue Arts District</p>
      </div>
      <div class="side-card">
        <h2>Selling at the market?</h2>
        <a class="btn btn--ghost btn--block" href="/vendors/">Vendor application</a>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
