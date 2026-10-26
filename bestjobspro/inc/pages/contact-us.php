<?php
$err = [];
$v = [];
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    [$err, $v] = handle_contact_form();
}
$sent = isset($_GET['sent']);
page_start([
    'title'       => 'Contact Best Jobs Pro | Call 210-903-9471 (24/7)',
    'description' => 'Contact Best Jobs Pro: call 210-903-9471 any time, email careers@bestjobspro.com or send a message. Office at 2140 E Southlake Blvd, Southlake, TX.',
    'path'        => '/contact-us/',
    'crumbs'      => [['Contact Us', '/contact-us/']],
    'robots'      => $err ? 'noindex, follow' : null,
    'schema'      => [['@type' => 'ContactPage', 'name' => 'Contact Best Jobs Pro', 'url' => url('/contact-us/'), 'about' => ['@id' => SITE_URL . '/#organization']]],
]);
page_hero('Contact Best Jobs Pro', 'Looking for work or looking for workers? Call us any time, day or night, or send a message and the Best Jobs Pro team will get back to you quickly.', [['Contact Us', '/contact-us/']], '', 'We are here 24/7');
?>
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div class="reveal in">
      <h2>Get in touch</h2>
      <p>Tell us what is on your mind and what you are looking for. Job seekers can also <a href="/applications/">apply online</a> directly.</p>
      <div class="tiles">
        <div class="tile"><span class="tile__ico"><?= icon('clock') ?></span><span><small>Hours</small><b>24/7 around-the-clock service</b></span></div>
        <a class="tile" href="tel:<?= SITE_TEL ?>"><span class="tile__ico"><?= icon('phone') ?></span><span><small>Phone</small><b><?= SITE_PHONE ?></b></span></a>
        <a class="tile" href="mailto:<?= SITE_EMAIL ?>"><span class="tile__ico"><?= icon('mail') ?></span><span><small>Email</small><b><?= SITE_EMAIL ?></b></span></a>
        <a class="tile" href="<?= SITE_MAP ?>" target="_blank" rel="noopener"><span class="tile__ico"><?= icon('pin') ?></span><span><small>Office</small><b><?= SITE_STREET ?>, <?= SITE_CITY ?>, <?= SITE_REGION ?> <?= SITE_ZIP ?>, USA</b></span></a>
      </div>
      <div class="map"><iframe title="Map of the Best Jobs Pro office in Southlake, Texas" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=<?= urlencode(SITE_STREET . ', ' . SITE_CITY . ', ' . SITE_REGION . ' ' . SITE_ZIP) ?>&amp;output=embed"></iframe></div>
    </div>
    <div class="form-card reveal in" id="contact-form">
<?php if ($sent): ?>
      <div class="alert alert--ok" role="status"><?= icon('check') ?><p><strong>Thanks, your message was sent.</strong> We will be in touch shortly. Need us now? Call <?= SITE_PHONE ?>.</p></div>
<?php endif; ?>
<?php if (isset($err['form'])): ?>
      <div class="alert alert--err" role="alert"><p><?= e($err['form']) ?></p></div>
<?php elseif ($err): ?>
      <div class="alert alert--err" role="alert"><p>Please fix the highlighted fields below.</p></div>
<?php endif; ?>
      <h2 style="font-size:1.5rem">Send us a message</h2>
      <form method="post" action="/contact-us/#contact-form" novalidate>
        <?= form_guard_fields() ?>
        <div class="form-grid">
          <div class="field"><label for="c-first">First name <span class="req">*</span></label><input id="c-first" name="first" autocomplete="given-name" required value="<?= old($v, 'first') ?>"<?= aria_err($err, 'first') ?>><?= field_error($err, 'first') ?></div>
          <div class="field"><label for="c-last">Last name <span class="req">*</span></label><input id="c-last" name="last" autocomplete="family-name" required value="<?= old($v, 'last') ?>"<?= aria_err($err, 'last') ?>><?= field_error($err, 'last') ?></div>
          <div class="field"><label for="c-phone">Phone number</label><input id="c-phone" name="phone" type="tel" autocomplete="tel" value="<?= old($v, 'phone') ?>"></div>
          <div class="field"><label for="c-email">Email <span class="req">*</span></label><input id="c-email" name="email" type="email" autocomplete="email" required value="<?= old($v, 'email') ?>"<?= aria_err($err, 'email') ?>><?= field_error($err, 'email') ?></div>
          <div class="field field--full"><label for="c-role">I am a <span class="req">*</span></label>
            <select id="c-role" name="role" required<?= aria_err($err, 'role') ?>>
              <option value="">Select one</option>
<?php foreach (['Job seeker', 'Employer'] as $r): ?>
              <option<?= ($v['role'] ?? '') === $r ? ' selected' : '' ?>><?= $r ?></option>
<?php endforeach; ?>
            </select><?= field_error($err, 'role') ?></div>
          <div class="field field--full"><label for="c-message">Message <span class="req">*</span></label><textarea id="c-message" name="message" rows="6" required<?= aria_err($err, 'message') ?>><?= old($v, 'message') ?></textarea><?= field_error($err, 'message') ?></div>
        </div>
        <div class="form-foot"><button class="btn" type="submit"><?= icon('send') ?> Send message</button><small>See our <a href="/privacy-policy/">privacy policy</a>.</small></div>
      </form>
    </div>
  </div>
</section>
<?php page_end();
