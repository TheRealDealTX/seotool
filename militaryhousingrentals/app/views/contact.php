<?php
require APP . '/forms.php';
$fields = ['name' => ['Name', true, 'text'], 'email' => ['Email', true, 'email'], 'phone' => ['Phone', false, 'tel'],
           'topic' => ['Topic', false, 'text'], 'message' => ['Message', true, 'textarea']];
$res = form_handle('contact', $fields);
$v = $res['values'] ?? [];
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Contact Us', null]]);
layout_start(['title' => 'Contact Us', 'description' => 'Questions about a listing, a base, or listing your rental? Contact Military Housing Rentals by phone, email or our contact form.',
    'path' => '/contact-us/', 'schema' => [$crumb_schema, ['@type' => 'ContactPage', 'url' => abs_url('/contact-us/'), 'name' => 'Contact Us']]]);
?>
<section class="page-hero">
  <div class="wrap"><?= $crumbs ?><h1>Contact us</h1><p class="lead">Have a question, a suggestion, or need help finding housing near your next duty station? We're here to help.</p></div>
</section>
<section class="section section-tight">
  <div class="wrap contact-layout">
    <div class="card form-card">
      <h2>Send us a message</h2>
      <p class="muted">If you're asking about a specific listing or a problem with the site, include as much detail as you can so we can help faster.</p>
      <?= form_notice($res, "Thanks! Your message is on its way. We'll get back to you as soon as possible.") ?>
      <form method="post" action="/contact-us/" class="form" novalidate data-form>
        <?= form_hidden() ?>
        <div class="form-grid">
          <?= form_field('name', 'Name', 'text', true, $v['name'] ?? '', 'autocomplete="name"') ?>
          <?= form_field('email', 'Email', 'email', true, $v['email'] ?? '', 'autocomplete="email"') ?>
          <?= form_field('phone', 'Phone', 'tel', false, $v['phone'] ?? '', 'autocomplete="tel"') ?>
          <label class="field" for="f-topic"><span>Topic</span>
            <select id="f-topic" name="topic">
              <?php foreach (['I need help finding housing', 'Question about a listing', 'Listing my property', 'Report a problem', 'Something else'] as $o): ?>
                <option<?= ($v['topic'] ?? '') === $o ? ' selected' : '' ?>><?= e($o) ?></option>
              <?php endforeach; ?>
            </select>
          </label>
        </div>
        <?= form_field('message', 'Message', 'textarea', true, $v['message'] ?? '') ?>
        <button class="btn btn-primary btn-lg" type="submit"><?= icon('mail') ?> Send message</button>
      </form>
    </div>
    <aside class="contact-aside">
      <div class="card">
        <h3>Talk to us</h3>
        <p><a class="contact-line" href="<?= e(cfg('phone_href')) ?>"><?= icon('phone') ?> <?= e(cfg('phone')) ?></a></p>
        <p><a class="contact-line" href="mailto:<?= e(cfg('email')) ?>"><?= icon('mail') ?> <?= e(cfg('email')) ?></a></p>
      </div>
      <div class="card card-accent">
        <h3>Listing a property?</h3>
        <p>Use our property submission form so we get every detail we need.</p>
        <a class="btn btn-accent btn-block" href="/submit-property/">Submit your property <?= icon('arrow') ?></a>
      </div>
      <?= sidebar_listings() ?>
    </aside>
  </div>
</section>
<?php layout_end();
