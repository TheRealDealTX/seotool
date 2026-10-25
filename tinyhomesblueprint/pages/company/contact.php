<?php
// Contact / plan order form. Posts to itself, emails SITE_EMAIL and keeps a copy of each
// lead in thb-leads.log one level above the web root (outside public_html), then redirects
// back with ?sent=1 so a refresh never re-submits.
session_start();
$errors = [];
$old = ['name' => '', 'email' => '', 'phone' => '', 'plan' => (string)($_GET['plan'] ?? ''), 'timeline' => '', 'lot' => '', 'builder' => '', 'message' => ''];
$choices = [
    'timeline' => ['0-3 months', '3-6 months', '6-12 months', 'More than 1 year', 'Need to sell a house first'],
    'lot'      => ['No', 'Yes', 'In process', 'Multiple lots'],
    'builder'  => ['No', 'Yes, I am a builder', 'Owner-builder'],
];
if (empty($_SESSION['thb_csrf'])) $_SESSION['thb_csrf'] = bin2hex(random_bytes(16));

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    foreach ($old as $k => $_) $old[$k] = trim((string)($_POST[$k] ?? ''));
    $spam = ($_POST['website'] ?? '') !== ''
        || !hash_equals($_SESSION['thb_csrf'], (string)($_POST['csrf'] ?? ''))
        || (time() - (int)($_POST['t'] ?? 0)) < 3;
    if ($old['name'] === '' || mb_strlen($old['name']) > 100) $errors['name'] = 'Please enter your name.';
    if (!filter_var($old['email'], FILTER_VALIDATE_EMAIL)) $errors['email'] = 'Please enter a valid email address.';
    if (mb_strlen($old['message']) < 5 || mb_strlen($old['message']) > 5000) $errors['message'] = 'Please tell us a little about your project.';
    foreach ($choices as $k => $opts) if ($old[$k] !== '' && !in_array($old[$k], $opts, true)) $old[$k] = '';
    foreach (['phone' => 40, 'plan' => 60] as $k => $max) $old[$k] = mb_substr($old[$k], 0, $max);

    if (!$errors) {
        if (!$spam) {
            $clean = fn($s) => str_replace(["\r", "\n"], ' ', $s);
            $body = "New message from tinyhomesblueprint.com\n\n";
            foreach (['name' => 'Name', 'email' => 'Email', 'phone' => 'Phone', 'plan' => 'Plan', 'timeline' => 'Start construction', 'lot' => 'Has a lot', 'builder' => 'Builder'] as $k => $label) {
                $body .= str_pad($label . ':', 20) . ($old[$k] !== '' ? $old[$k] : '-') . "\n";
            }
            $body .= "\nMessage:\n" . $old['message'] . "\n";
            $subject = 'Website inquiry' . ($old['plan'] !== '' ? ' - ' . $clean($old['plan']) : '') . ' - ' . $clean($old['name']);
            $headers = "From: " . SITE_NAME . " Website <noreply@tinyhomesblueprint.com>\r\n"
                     . "Reply-To: " . $clean($old['name']) . " <" . $clean($old['email']) . ">\r\n"
                     . "Content-Type: text/plain; charset=UTF-8\r\n";
            @mail(SITE_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-fnoreply@tinyhomesblueprint.com');
            $log = dirname(__DIR__, 3) . '/thb-leads.log';
            @file_put_contents($log, json_encode(['time' => date('c'), 'ip' => $_SERVER['REMOTE_ADDR'] ?? ''] + $old, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
        }
        header('Location: /contact/?sent=1#form', true, 303);
        exit;
    }
}
$sent = isset($_GET['sent']);

page_start([
    'breadcrumbs' => [['Home', '/'], ['Contact', null]],
    'robots' => ($sent || isset($_GET['plan'])) ? 'noindex,follow' : null,
    'schema' => [['@context' => 'https://schema.org', '@type' => 'ContactPage', 'name' => 'Contact ' . SITE_NAME, 'url' => abs_url('/contact/')]],
]);
$sel = function (string $name, string $label) use ($choices, $old) {
    echo '<div class="field"><label for="f-' . $name . '">' . e($label) . '</label><select id="f-' . $name . '" name="' . $name . '"><option value="">Select</option>';
    foreach ($choices[$name] as $c) echo '<option' . ($old[$name] === $c ? ' selected' : '') . '>' . e($c) . '</option>';
    echo '</select></div>';
};
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Contact Tiny Homes Blueprint</h1>
    <p class="lead">Order a plan, ask about a modification or tell us about your project. A real person at Tiny Homes Blueprint reads every message and replies within one business day.</p>
  </div>
</section>

<section class="section">
  <div class="wrap two-col top">
    <div class="panel" id="form">
      <?php if ($sent): ?>
        <div class="alert alert-ok" role="status"><strong>Thanks, your message is on its way.</strong> We will reply by email within one business day. Need it sooner? Call <?= SITE_PHONE ?>.</div>
      <?php endif; ?>
      <?php if ($errors): ?>
        <div class="alert alert-err" role="alert">Please fix the highlighted fields and try again.</div>
      <?php endif; ?>
      <h2>Send us a message</h2>
      <form method="post" action="/contact/#form" novalidate>
        <input type="hidden" name="csrf" value="<?= e($_SESSION['thb_csrf']) ?>">
        <input type="hidden" name="t" value="<?= time() ?>">
        <div class="hp" aria-hidden="true"><label for="f-website">Website</label><input type="text" id="f-website" name="website" tabindex="-1" autocomplete="off"></div>
        <div class="field-row">
          <div class="field"><label for="f-name">Name *</label><input type="text" id="f-name" name="name" required autocomplete="name" value="<?= e($old['name']) ?>"<?= isset($errors['name']) ? ' aria-invalid="true"' : '' ?>><?php if (isset($errors['name'])) echo '<small style="color:var(--warn)">' . e($errors['name']) . '</small>'; ?></div>
          <div class="field"><label for="f-email">Email *</label><input type="email" id="f-email" name="email" required autocomplete="email" value="<?= e($old['email']) ?>"<?= isset($errors['email']) ? ' aria-invalid="true"' : '' ?>><?php if (isset($errors['email'])) echo '<small style="color:var(--warn)">' . e($errors['email']) . '</small>'; ?></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="f-phone">Phone</label><input type="tel" id="f-phone" name="phone" autocomplete="tel" value="<?= e($old['phone']) ?>"></div>
          <div class="field"><label for="f-plan">Plan number (optional)</label><input type="text" id="f-plan" name="plan" value="<?= e($old['plan']) ?>" placeholder="e.g. Plan 12-2418"></div>
        </div>
        <div class="field-row">
          <?php $sel('timeline', 'When do you want to start construction?'); ?>
          <?php $sel('lot', 'Do you have a lot?'); ?>
        </div>
        <?php $sel('builder', 'Are you a builder?'); ?>
        <div class="field"><label for="f-message">How can we help? *</label><textarea id="f-message" name="message" required placeholder="Tell us about your project: plan, changes you want, location, timeline."<?= isset($errors['message']) ? ' aria-invalid="true"' : '' ?>><?= e($old['message']) ?></textarea><?php if (isset($errors['message'])) echo '<small style="color:var(--warn)">' . e($errors['message']) . '</small>'; ?></div>
        <button class="btn btn-wood" type="submit">Send message</button>
        <p class="form-note">We use your details only to answer your inquiry. See our <a href="/privacy-policy/">privacy policy</a>.</p>
      </form>
    </div>
    <div>
      <h2>Other ways to reach us</h2>
      <div class="feature-grid" style="grid-template-columns:1fr">
        <div class="feature"><span class="link-ico"><?= icon('phone') ?></span><h3>Call or text</h3><p><a href="tel:<?= SITE_TEL ?>"><?= SITE_PHONE ?></a><br>Order a plan by phone or ask a quick question.</p></div>
        <div class="feature"><span class="link-ico"><?= icon('mail') ?></span><h3>Email</h3><p><a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a><br>Send sketches, lot surveys or photos.</p></div>
        <div class="feature"><span class="link-ico"><?= icon('ruler') ?></span><h3>Plan modifications</h3><p>Include the plan number and a list of changes (flip, loft, porch, foundation, size) and we will quote it.</p></div>
      </div>
      <h3 class="mt-2">Before you write</h3>
      <p>These free tools help you send us a more specific request:</p>
      <ul>
        <li><a href="/tools/tiny-house-cost-calculator/">Tiny house cost calculator</a></li>
        <li><a href="/tools/tiny-house-layout-planner/">Layout planner</a> (download your sketch as an image)</li>
        <li><a href="/tools/how-big-should-my-tiny-house-be/">Size calculator</a></li>
      </ul>
    </div>
  </div>
</section>
<?php page_end(); ?>
