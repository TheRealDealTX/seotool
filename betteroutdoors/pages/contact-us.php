<?php defined('BO') || exit;
// Contact page with a mail() form handler (honeypot + timing check, no database).
$crumbs = [['Home', '/'], ['Contact Us', '/contact-us/']];
$sent = false;
$err  = '';
$val  = ['name' => '', 'email' => '', 'topic' => 'General question', 'message' => ''];
$topics = ['General question', 'Bow review request', 'Correction or update', 'Partnership', 'Other'];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    foreach ($val as $k => $_) $val[$k] = trim((string)($_POST[$k] ?? ''));
    $elapsed = time() - (int)($_POST['ts'] ?? 0);
    if (!empty($_POST['website']) || $elapsed < 3) {
        $sent = true; // silently drop bots
    } elseif ($val['name'] === '' || $val['message'] === '' || !filter_var($val['email'], FILTER_VALIDATE_EMAIL)) {
        $err = 'Please enter your name, a valid email address and a message.';
    } elseif (strlen($val['message']) > 5000) {
        $err = 'Please keep your message under 5,000 characters.';
    } else {
        $topic = in_array($val['topic'], $topics, true) ? $val['topic'] : 'Other';
        $name  = str_replace(["\r", "\n"], ' ', $val['name']);
        $body  = "Name: {$name}\nEmail: {$val['email']}\nTopic: {$topic}\n\n{$val['message']}\n";
        $hdrs  = "From: Better Outdoors <" . SITE_EMAIL . ">\r\nReply-To: {$val['email']}\r\nContent-Type: text/plain; charset=UTF-8";
        if (@mail(SITE_EMAIL, '[Better Outdoors] ' . $topic . ' from ' . $name, $body, $hdrs)) {
            $sent = true;
        } else {
            $err = 'Sorry, your message could not be sent. Please email us directly at ' . SITE_EMAIL . '.';
        }
    }
}

page_head([
    'title' => 'Contact Better Outdoors | Questions, Corrections & Review Requests',
    'desc'  => 'Contact Better Outdoors with archery questions, bow review requests or corrections. We read every message and reply as soon as we can.',
    'path'  => '/contact-us/',
    'schema' => [breadcrumb_schema($crumbs), ['@type' => 'ContactPage', 'name' => 'Contact Better Outdoors', 'url' => SITE_URL . '/contact-us/']],
]);
?>
<section class="page-hero mist-after">
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Contact Better Outdoors</h1>
    <p>Have a question, a bow you want reviewed, or a correction for one of our guides? We&rsquo;d love to hear from you.</p>
  </div>
</section>
<section class="section-mist" style="padding-bottom:90px">
  <div class="wrap contact-grid">
    <div class="result reveal">
      <h2 style="font-size:1.4rem">Get in touch</h2>
      <p>Use the form and we&rsquo;ll respond as soon as possible, usually within two business days.</p>
      <ul class="game-list">
        <li class="ok"><i class="fa-solid fa-envelope"></i> <a href="mailto:<?= SITE_EMAIL ?>" style="color:#fff"><?= SITE_EMAIL ?></a></li>
        <li class="ok"><i class="fa-solid fa-bullseye"></i> Bow review requests welcome</li>
        <li class="ok"><i class="fa-solid fa-pen"></i> Spot an outdated spec? Tell us</li>
      </ul>
      <p style="margin-top:20px;font-size:.92rem">Please note: Better Outdoors is a publication, not a store or archery pro shop, so we can&rsquo;t process orders or warranty claims.</p>
    </div>
    <div class="panel reveal reveal-d2">
<?php if ($sent): ?>
      <div class="notice notice-ok" role="status"><strong>Thanks!</strong> Your message is on its way. We&rsquo;ll get back to you soon.</div>
      <p><a class="btn btn-teal" href="/blog/">Browse the latest guides</a></p>
<?php else: ?>
<?php if ($err): ?><div class="notice notice-err" role="alert"><?= e($err) ?></div><?php endif; ?>
      <form method="post" action="/contact-us/" novalidate>
        <div class="field"><label for="c-name">Name</label><input type="text" id="c-name" name="name" required maxlength="100" value="<?= e($val['name']) ?>" autocomplete="name"></div>
        <div class="field"><label for="c-email">Email</label><input type="email" id="c-email" name="email" required maxlength="200" value="<?= e($val['email']) ?>" autocomplete="email"></div>
        <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic">
<?php foreach ($topics as $t): ?>
          <option<?= $t === $val['topic'] ? ' selected' : '' ?>><?= e($t) ?></option>
<?php endforeach; ?>
        </select></div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required maxlength="5000"><?= e($val['message']) ?></textarea></div>
        <div class="hp" aria-hidden="true"><label for="c-web">Website</label><input type="text" id="c-web" name="website" tabindex="-1" autocomplete="off"></div>
        <input type="hidden" name="ts" value="<?= time() ?>">
        <button class="btn btn-orange" type="submit"><i class="fa-solid fa-paper-plane" aria-hidden="true"></i> Send Message</button>
        <p class="hint" style="font-size:.84rem;color:var(--muted);margin-top:12px">We only use your details to reply. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </form>
<?php endif; ?>
    </div>
  </div>
</section>
<?php page_foot(); ?>
