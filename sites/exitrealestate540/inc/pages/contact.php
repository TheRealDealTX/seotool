<?php
defined('ERE') or exit;
$crumbs = [['Home', '/'], ['Contact', '/contact/']];
$sent = false; $error = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $name = trim((string) ($_POST['name'] ?? ''));
    $email = trim((string) ($_POST['email'] ?? ''));
    $topic = trim((string) ($_POST['topic'] ?? ''));
    $msg = trim((string) ($_POST['message'] ?? ''));
    $trap = (string) ($_POST['website'] ?? '');
    $ts = (int) ($_POST['ts'] ?? 0);
    if ($trap !== '' || ($ts && time() - $ts < 3)) {
        $sent = true; // silently drop bots
    } elseif ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($msg) < 10) {
        $error = 'Please enter your name, a valid email address and a message.';
    } else {
        $rec = ['time' => date('c'), 'name' => mb_substr($name, 0, 100), 'email' => $email, 'topic' => mb_substr($topic, 0, 60), 'message' => mb_substr($msg, 0, 5000), 'ip' => $_SERVER['REMOTE_ADDR'] ?? ''];
        // Stored as a PHP file that exits immediately, so it can never be read over HTTP
        // (the host serves files in the web root directly and ignores .htaccess).
        $file = ROOT . '/site-data/messages.php';
        if (!is_dir(dirname($file))) @mkdir(dirname($file), 0700, true);
        if (!is_file($file)) @file_put_contents($file, "<?php http_response_code(404); exit; ?>\n");
        $stored = @file_put_contents($file, json_encode($rec, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP) . "\n", FILE_APPEND | LOCK_EX) !== false;
        $mailed = false;
        if ($to = cfg('contact_email')) {
            $safeName = preg_replace('/[\r\n]+/', ' ', $rec['name']);
            $mailed = @mail($to, '[ERE540] ' . ($rec['topic'] ?: 'Contact form') . ' - ' . $safeName,
                "Name: {$rec['name']}\nEmail: {$email}\nTopic: {$rec['topic']}\n\n{$rec['message']}",
                "From: no-reply@exitrealestate540.com\r\nReply-To: {$email}\r\nContent-Type: text/plain; charset=UTF-8");
        }
        if ($stored || $mailed) $sent = true; else $error = 'Sorry, your message could not be sent right now. Please try again later.';
    }
}
page_head([
    'title' => 'Contact Exit Real Estate 540',
    'description' => 'Questions, corrections, partnership or guest post ideas? Contact the Exit Real Estate 540 editorial team.',
    'path' => '/contact/',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'ContactPage', 'url' => abs_url('/contact/'), 'name' => 'Contact Exit Real Estate 540']],
]);
?>
<section class="page-head">
  <div class="wrap wrap--narrow">
    <?php breadcrumbs($crumbs); ?>
    <h1>Contact us</h1>
    <p class="lead">Spotted something out of date, have a question about a guide, or want to work together? Send us a note and we will get back to you.</p>
  </div>
</section>
<section class="section section--compact">
  <div class="wrap wrap--narrow">
<?php if ($sent): ?>
    <div class="notice notice--ok" role="status"><strong>Thanks - your message is on its way.</strong> We read every note and usually reply within a few business days.</div>
<?php else: ?>
<?php if ($error): ?><div class="notice notice--err" role="alert"><?= e($error) ?></div><?php endif; ?>
    <form class="form" method="post" action="/contact/">
      <label class="fld"><span class="fld__label">Your name</span><span class="fld__input"><input type="text" name="name" required maxlength="100" autocomplete="name" value="<?= e($_POST['name'] ?? '') ?>"></span></label>
      <label class="fld"><span class="fld__label">Email</span><span class="fld__input"><input type="email" name="email" required maxlength="150" autocomplete="email" value="<?= e($_POST['email'] ?? '') ?>"></span></label>
      <label class="fld"><span class="fld__label">Topic</span><span class="fld__input"><select name="topic">
        <?php foreach (['General question', 'Correction or update', 'Guest post / Write for us', 'Advertising or partnership', 'Other'] as $t): ?><option<?= ($_POST['topic'] ?? '') === $t ? ' selected' : '' ?>><?= e($t) ?></option><?php endforeach; ?>
      </select></span></label>
      <label class="fld"><span class="fld__label">Message</span><span class="fld__input"><textarea name="message" rows="6" required maxlength="5000"><?= e($_POST['message'] ?? '') ?></textarea></span></label>
      <div class="hp" aria-hidden="true"><label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="ts" value="<?= time() ?>">
      <button class="btn btn--primary" type="submit">Send message</button>
      <p class="fine">We use your details only to reply. See our <a href="/privacy-policy/">privacy policy</a>. Please do not send policy numbers, Social Security numbers or other sensitive information.</p>
    </form>
<?php endif; ?>
  </div>
</section>
<?php page_foot();
