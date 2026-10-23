<?php defined('SS_APP') || exit;
// Messages are appended to a JSON-lines file outside the web root and, where
// the host allows it, emailed to SITE_EMAIL. See README, "Contact form".
$sent = false; $err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $name = trim(substr($_POST['name'] ?? '', 0, 100));
    $email = trim(substr($_POST['email'] ?? '', 0, 150));
    $topic = trim(substr($_POST['topic'] ?? '', 0, 40));
    $msg = trim(substr($_POST['message'] ?? '', 0, 4000));
    $tooFast = (time() - (int)($_POST['t'] ?? 0)) < 3;
    if (!empty($_POST['website']) || $tooFast) {
        $sent = true; // silently drop bots
    } elseif ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($msg) < 10) {
        $err = 'Please enter your name, a valid email address and a message of at least 10 characters.';
    } else {
        $row = json_encode(['at' => date('c'), 'name' => $name, 'email' => $email, 'topic' => $topic, 'message' => $msg,
                            'ip' => $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? ''], JSON_UNESCAPED_UNICODE) . "\n";
        $dir = dirname(__DIR__, 3) . '/ss-data';
        if (!is_dir($dir)) @mkdir($dir, 0700, true);
        $stored = @file_put_contents($dir . '/messages.jsonl', $row, FILE_APPEND | LOCK_EX) !== false;
        $mailed = @mail(SITE_EMAIL, '[' . SITE_NAME . '] ' . ($topic ?: 'Contact form'), "From: $name <$email>\nTopic: $topic\n\n$msg",
                        'From: ' . SITE_EMAIL . "\r\nReply-To: " . str_replace(["\r", "\n"], '', $email));
        if ($stored || $mailed) $sent = true;
        else $err = 'Sorry, your message could not be sent. Please email us directly at ' . SITE_EMAIL . '.';
    }
}
echo page_hero($GLOBALS['ss_route'], 'Questions, corrections, new research or a product you\'d like us to review? Send the Saffron Supplement team a message.', 'Contact');
?>
<div class="narrow section">
<?php if ($sent): ?>
  <div class="note note-good"><strong>Thank you!</strong> Your message has been received. We read every message and aim to reply within a few working days.</div>
  <p><a href="/">Back to the homepage</a></p>
<?php else: ?>
  <?php if ($err): ?><div class="note note-warn" role="alert"><?= e($err) ?></div><?php endif; ?>
  <form class="tool" method="post" action="/contact/" novalidate>
    <div class="row">
      <div class="field"><label for="c-name">Your name</label><input type="text" id="c-name" name="name" required maxlength="100" value="<?= e($_POST['name'] ?? '') ?>" autocomplete="name"></div>
      <div class="field"><label for="c-email">Email address</label><input type="email" id="c-email" name="email" required maxlength="150" value="<?= e($_POST['email'] ?? '') ?>" autocomplete="email"></div>
    </div>
    <div class="field"><label for="c-topic">Topic</label>
      <select id="c-topic" name="topic">
        <?php foreach (['General question', 'Correction', 'New research', 'Product suggestion', 'Partnership'] as $t): ?>
        <option<?= ($_POST['topic'] ?? '') === $t ? ' selected' : '' ?>><?= e($t) ?></option>
        <?php endforeach; ?>
      </select></div>
    <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="6" required maxlength="4000"><?= e($_POST['message'] ?? '') ?></textarea></div>
    <div style="position:absolute;left:-9999px" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
    <input type="hidden" name="t" value="<?= time() ?>">
    <button class="btn" type="submit">Send Message</button>
    <p class="small" style="margin-top:14px">We can't give personal medical advice. For health questions, please speak to your doctor or pharmacist. See our <a href="/privacy-policy/">privacy policy</a>.</p>
  </form>
  <p>Prefer email? Write to <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a>.</p>
<?php endif; ?>
</div>
