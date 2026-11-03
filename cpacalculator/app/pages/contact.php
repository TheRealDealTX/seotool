<?php
defined('CPA') or exit;
$P['title'] = 'Contact CPA Calculator — Questions, Corrections & Ideas';
$P['description'] = 'Contact the CPA Calculator team about a calculator result, a correction, a new tool idea or a partnership. Email info@cpacalculator.com or use the form.';
$P['pageType'] = 'ContactPage';
$status = $_GET['sent'] ?? '';
$errors = [];
$old = ['name' => '', 'email' => '', 'topic' => 'question', 'message' => ''];

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
  require_once SITE_ROOT . '/app/mailer.php';
  foreach ($old as $k => $_) $old[$k] = trim((string) ($_POST[$k] ?? ''));
  $elapsed = time() - (int) ($_POST['t'] ?? 0);
  if (($_POST['website'] ?? '') !== '' || $elapsed < 3) { header('Location: /contact/?sent=1', true, 303); exit; } // bot: pretend success
  if ($old['name'] === '' || mb_strlen($old['name']) > 100) $errors[] = 'Please enter your name.';
  if (!filter_var($old['email'], FILTER_VALIDATE_EMAIL)) $errors[] = 'Please enter a valid email address.';
  if (mb_strlen($old['message']) < 10 || mb_strlen($old['message']) > 5000) $errors[] = 'Please write a message (10–5,000 characters).';
  if (preg_match_all('#https?://#i', $old['message']) > 3) $errors[] = 'Please include fewer links.';
  if (!$errors) {
    $topics = ['question' => 'Question', 'error' => 'Calculator error report', 'idea' => 'New calculator idea', 'business' => 'Business / partnership', 'other' => 'Other'];
    $body = "New message from the cpacalculator.com contact form\n\nName: {$old['name']}\nEmail: {$old['email']}\nTopic: " . ($topics[$old['topic']] ?? 'Other') .
            "\nPage: " . substr((string) ($_POST['ref'] ?? ''), 0, 200) . "\nIP: " . ($_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '') . "\n\n" . $old['message'] . "\n";
    $err = null;
    if (smtp_send(SITE_EMAIL, '[CPA Calculator] ' . ($topics[$old['topic']] ?? 'Message') . ' from ' . $old['name'], $body, $old['email'], $err)) {
      header('Location: /contact/?sent=1', true, 303); exit;
    }
    error_log('contact form mail failed: ' . $err);
    $errors[] = 'Sorry — your message could not be sent right now. Please email us directly at ' . SITE_EMAIL . '.';
  }
}
echo simple_hero('Contact us', 'Have a question about a calculator, spotted an error or want a new tool? We read every message.', 'Contact');
?>
<div class="wrap content-grid">
  <div>
    <div class="form-card">
<?php if ($status === '1'): ?>
      <div class="alert ok">Thanks — your message has been sent. We usually reply within two business days.</div>
<?php endif; foreach ($errors as $m): ?>
      <div class="alert err"><?= e($m) ?></div>
<?php endforeach; ?>
      <form method="post" action="/contact/">
        <input type="hidden" name="t" value="<?= time() ?>">
        <input type="hidden" name="ref" value="<?= e($_SERVER['HTTP_REFERER'] ?? '') ?>">
        <div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
        <div class="grid-2">
          <div class="field"><label for="c-name">Name</label><div class="inp"><input id="c-name" name="name" required maxlength="100" autocomplete="name" value="<?= e($old['name']) ?>"></div></div>
          <div class="field"><label for="c-email">Email</label><div class="inp"><input id="c-email" type="email" name="email" required autocomplete="email" value="<?= e($old['email']) ?>"></div></div>
        </div>
        <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic">
<?php foreach (['question' => 'A question about a calculator', 'error' => 'Report a calculator error', 'idea' => 'Suggest a new calculator', 'business' => 'Business or partnership', 'other' => 'Something else'] as $k => $v): ?>
          <option value="<?= $k ?>"<?= $old['topic'] === $k ? ' selected' : '' ?>><?= $v ?></option>
<?php endforeach; ?>
        </select></div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required minlength="10" maxlength="5000" placeholder="If you’re reporting a result, include the calculator, your inputs and what you expected."><?= e($old['message']) ?></textarea></div>
        <button class="btn" type="submit">Send message <?= icon('arrow') ?></button>
        <p class="hint" style="margin-top:14px">We can’t give personalized tax advice by email. Please don’t send Social Security numbers or other sensitive data. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </form>
    </div>
  </div>
  <aside class="aside"><div class="card">
    <div class="res-label" style="margin-bottom:10px">Email</div>
    <p><a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a></p>
    <div class="res-label" style="margin:18px 0 10px">Before you write</div>
    <ul class="toc"><li><a href="/our-methodology/">How our calculators work</a></li><li><a href="/calculators/">All calculators</a></li><li><a href="/blog/">Tax guides</a></li><li><a href="/disclaimer/">Disclaimer</a></li></ul>
  </div></aside>
</div>
