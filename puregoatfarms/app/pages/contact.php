<?php
defined('PGF') || exit;

$errors = $errors ?? [];
$old = $old ?? ['name' => '', 'email' => '', 'topic' => '', 'message' => ''];
$sent = isset($_GET['sent']);
$crumbs = [['Home', '/'], ['Contact', '/contact/']];
$page = [
    'path'   => '/contact/',
    'title'  => 'Contact Pure Goat Farms — Ask Us Anything About Goats',
    'desc'   => 'Questions from readers regularly turn into new field notes. Contact Pure Goat Farms with your goat breed, health, milking or farm-life question.',
    'crumbs' => $crumbs,
    'schema' => [
        ['@type' => 'ContactPage', '@id' => SITE_URL . '/contact/#webpage', 'url' => SITE_URL . '/contact/', 'name' => 'Contact Pure Goat Farms', 'isPartOf' => ['@id' => SITE_URL . '/#website']],
    ],
];
ob_start();
?>
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal">Contact</p>
    <h1 class="reveal">Ask us anything about goats.</h1>
    <p class="page-hero__lead reveal">Questions from readers regularly turn into new field notes. If you're stuck on something goat-related, there's a good chance others are too.</p>
  </div>
</section>

<section class="section">
  <div class="container contact">
    <div class="contact__form card reveal">
<?php if ($sent): ?>
      <div class="notice notice--ok" role="status"><?= icon('check') ?><div><strong>Thanks — your message is on its way.</strong><p>We typically reply within 2–3 business days.</p></div></div>
<?php endif; ?>
<?php if ($errors): ?>
      <div class="notice notice--err" role="alert"><ul><?php foreach ($errors as $er): ?><li><?= e($er) ?></li><?php endforeach; ?></ul></div>
<?php endif; ?>
      <form method="post" action="/contact/" class="form" novalidate>
        <div class="form__row">
          <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" type="text" required maxlength="100" autocomplete="name" value="<?= e($old['name']) ?>"></div>
          <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required maxlength="200" autocomplete="email" value="<?= e($old['email']) ?>"></div>
        </div>
        <div class="field"><label for="c-topic">Topic</label>
          <select id="c-topic" name="topic">
            <option value="">- Select -</option>
<?php foreach (CONTACT_TOPICS as $t): ?>
            <option<?= $old['topic'] === $t ? ' selected' : '' ?>><?= e($t) ?></option>
<?php endforeach; ?>
          </select>
        </div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required maxlength="5000"><?= e($old['message']) ?></textarea></div>
        <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <input type="hidden" name="ts" value="<?= time() ?>">
        <button class="btn btn--rust btn--lg" type="submit">Send Message <?= icon('arrow') ?></button>
      </form>
    </div>
    <aside class="contact__info">
      <div class="info-card reveal"><span class="info-card__icon"><?= icon('mail') ?></span><div><h3>Email</h3><p><a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a></p></div></div>
      <div class="info-card reveal"><span class="info-card__icon"><?= icon('clock') ?></span><div><h3>Response time</h3><p>We typically reply within 2–3 business days.</p></div></div>
      <div class="info-card reveal"><span class="info-card__icon"><?= icon('pin') ?></span><div><h3>Farm visits</h3><p>Not currently open to the public, but ask — seasonal exceptions happen.</p></div></div>
      <div class="info-card info-card--tip reveal"><span class="info-card__icon"><?= icon('spark') ?></span><div><h3>Looking for a quick answer?</h3><p>Try the <a href="/faq/">goat FAQ</a> or one of our <a href="/tools/">free calculators</a> first.</p></div></div>
    </aside>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
