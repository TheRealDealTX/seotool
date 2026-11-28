<?php
require_once ROOT . '/inc/mailer.php';
if (session_status() !== PHP_SESSION_ACTIVE) session_start();
$status = null; $vals = ['name' => '', 'email' => '', 'topic' => 'General question', 'message' => ''];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    foreach ($vals as $k => $_) $vals[$k] = trim((string) ($_POST[$k] ?? ''));
    $tooFast = (time() - (int) ($_POST['t'] ?? 0)) < 3;
    $tokenOk = hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? ''));
    $recent = (time() - ($_SESSION['last_mail'] ?? 0)) < 60;
    if (!empty($_POST['website']) || $tooFast || !$tokenOk) $status = ['bad', 'Sorry, your message could not be verified. Please try again.'];
    elseif ($recent) $status = ['bad', 'Please wait a minute before sending another message.'];
    elseif ($vals['name'] === '' || !filter_var($vals['email'], FILTER_VALIDATE_EMAIL) || mb_strlen($vals['message']) < 10) $status = ['bad', 'Please fill in your name, a valid email and a message (10+ characters).'];
    else {
        $topic = in_array($vals['topic'], ['General question', 'Calculator bug', 'Tool request', 'Content correction', 'Partnership'], true) ? $vals['topic'] : 'General question';
        $text = "New message from freegradecalculator.com\n\nName: {$vals['name']}\nEmail: {$vals['email']}\nTopic: $topic\nIP: " . ($_SERVER['REMOTE_ADDR'] ?? '') . "\n\n" . mb_substr($vals['message'], 0, 5000);
        if (send_mail(SITE_EMAIL, "[FGC] $topic — " . mb_substr($vals['name'], 0, 60), $text, $vals['email'])) {
            $_SESSION['last_mail'] = time(); $status = ['ok', 'Thanks! Your message is on its way — we usually reply within 2 business days.'];
            $vals = ['name' => '', 'email' => '', 'topic' => 'General question', 'message' => ''];
        } else $status = ['bad', 'Our mail server didn’t respond. Please email us directly at ' . SITE_EMAIL . '.'];
    }
}
$_SESSION['csrf'] = bin2hex(random_bytes(16));
page_start(['title' => 'Contact Us | Free Grade Calculator', 'description' => 'Questions, bug reports or calculator ideas? Contact the FreeGradeCalculator team at info@freegradecalculator.com or use our quick contact form.', 'path' => '/contact', 'schema' => [breadcrumb_schema([['Home', '/'], ['Contact', '/contact']])]]);
?>
<section class="page-hero"><div class="hero-bg" aria-hidden="true"><div class="blob blob-1"></div><div class="blob blob-2"></div></div><div class="wrap"><?= breadcrumbs_html([['Home', '/'], ['Contact', '/contact']]) ?><h1>Get in touch</h1><p class="lead">Found a bug, want a new calculator, or have a question about your grades? We’d love to hear from you.</p></div></section>
<div class="wrap split" style="align-items:start;padding-bottom:40px">
  <form class="form-card" method="post" action="/contact" novalidate>
    <?php if ($status): ?><div class="alert alert-<?= $status[0] ?>" role="alert"><?= e($status[1]) ?></div><?php endif; ?>
    <input type="hidden" name="csrf" value="<?= e($_SESSION['csrf']) ?>"><input type="hidden" name="t" value="<?= time() ?>">
    <div class="hp" aria-hidden="true"><label>Website <input name="website" tabindex="-1" autocomplete="off"></label></div>
    <div class="grid-2"><div class="field"><label for="c-name">Name</label><input class="input" id="c-name" name="name" required value="<?= e($vals['name']) ?>" autocomplete="name"></div><div class="field"><label for="c-email">Email</label><input class="input" id="c-email" name="email" type="email" required value="<?= e($vals['email']) ?>" autocomplete="email"></div></div>
    <div class="field" style="margin-top:12px"><label for="c-topic">Topic</label><select class="select" id="c-topic" name="topic"><?php foreach (['General question', 'Calculator bug', 'Tool request', 'Content correction', 'Partnership'] as $t): ?><option<?= $vals['topic'] === $t ? ' selected' : '' ?>><?= e($t) ?></option><?php endforeach; ?></select></div>
    <div class="field"><label for="c-msg">Message</label><textarea class="input" id="c-msg" name="message" rows="6" required><?= e($vals['message']) ?></textarea></div>
    <button class="btn btn-primary" type="submit" style="width:100%"><?= icon('mail') ?> Send message</button>
    <p class="note">We only use your email to reply. See our <a href="/privacy-policy">privacy policy</a>.</p>
  </form>
  <div class="prose">
    <h2>Other ways to reach us</h2>
    <p><a class="btn btn-ghost" href="mailto:<?= e(SITE_EMAIL) ?>"><?= icon('mail') ?> <?= e(SITE_EMAIL) ?></a></p>
    <h3>Before you write</h3>
    <ul><li>Grading scales differ between schools — check your syllabus if a result doesn’t match your portal.</li><li>For bug reports, tell us which calculator, what you entered and what you expected.</li><li>We can’t change grades or contact your school on your behalf.</li></ul>
    <figure class="figure"><?= photo('student-at-computer', 'Student working on a computer', '', true) ?></figure>
  </div>
</div>
<?php page_end();
