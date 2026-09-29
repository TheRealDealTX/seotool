<?php
/** Contact page (content carried over from the previous site). */
defined('RT_APP') || exit;

use RT\PublicForm;
use RT\Submissions;

$errors = [];
$v = ['first_name' => '', 'last_name' => '', 'phone' => '', 'email' => '', 'message' => ''];
$sent = isset($_GET['sent']);
if (is_post()) {
    header('Cache-Control: no-store');
    foreach ($v as $k => $_) {
        $v[$k] = is_string($_POST[$k] ?? null) ? $_POST[$k] : '';
    }
    $check = PublicForm::check('contact', $_POST, 5);
    if ($check === 'spam') {
        redirect('/contact/?sent=1', 303);
    } elseif ($check !== null) {
        $errors['form'] = $check;
    }
    $email = valid_email($v['email']);
    $msg = clean_text($v['message'], 5000);
    if (!$email) { $errors['email'] = 'Enter your e-mail address so we can reply.'; }
    if (!$msg || mb_strlen($msg) < 5) { $errors['message'] = 'Enter a message.'; }
    if (!$errors) {
        $name = clean_str(trim($v['first_name'] . ' ' . $v['last_name']), 160);
        Submissions::store('contact', 'Message from ' . ($name ?: $email), [
            'phone' => clean_str($v['phone'], 40), 'message' => $msg,
        ], $name, $email);
        redirect('/contact/?sent=1', 303);
    }
}
$page = [
    'title' => 'Contact Us',
    'description' => 'Questions, suggestions or comments about Rodeo Texas? Send us a message — we read every one.',
    'canonical' => '/contact/',
    'body_class' => 'page-form',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
$err = static fn(string $k): string => isset($errors[$k]) ? '<p class="field-error" id="err-' . $k . '">' . e($errors[$k]) . '</p>' : '';
$inv = static fn(string $k): string => isset($errors[$k]) ? ' aria-invalid="true" aria-describedby="err-' . $k . '"' : '';
?>
<div class="wrap narrow">
  <h1>Contact us</h1>
  <p>We'd love to hear from you! Whether you have a question, a suggestion, a comment about the site, or just want to say howdy — don't hesitate to reach out. At Rodeo Texas, we're always looking for ways to improve and better serve the rodeo community across the state.</p>
  <p>Want an event listed? Use the <a href="/submit-event/">event submission form</a>. Found a mistake on a listing? Use “Report a correction” on the event page.</p>
  <?php if ($sent): ?>
    <div class="alert alert--success" role="status"><strong>Thanks for being part of the ride!</strong> Your message was sent. We read every submission and will get back to you as soon as we can.</div>
  <?php else: ?>
    <?php if ($errors): ?><div class="alert alert--danger" role="alert"><strong>Please fix the highlighted fields.</strong> <?= e($errors['form'] ?? '') ?></div><?php endif; ?>
    <form class="form" method="post" novalidate>
      <?= PublicForm::fields('contact') ?>
      <div class="field-row">
        <div class="field"><label for="k-fn">First name</label><input id="k-fn" name="first_name" maxlength="80" autocomplete="given-name" value="<?= e($v['first_name']) ?>"></div>
        <div class="field"><label for="k-ln">Last name</label><input id="k-ln" name="last_name" maxlength="80" autocomplete="family-name" value="<?= e($v['last_name']) ?>"></div>
      </div>
      <div class="field-row">
        <div class="field"><label for="k-ph">Phone</label><input id="k-ph" type="tel" name="phone" maxlength="40" autocomplete="tel" value="<?= e($v['phone']) ?>"></div>
        <div class="field"><label for="k-em">E-mail <span class="req">*</span></label><input id="k-em" type="email" name="email" required maxlength="255" autocomplete="email" value="<?= e($v['email']) ?>"<?= $inv('email') ?>><?= $err('email') ?></div>
      </div>
      <div class="field"><label for="k-msg">Message <span class="req">*</span></label><textarea id="k-msg" name="message" rows="6" required maxlength="5000"<?= $inv('message') ?>><?= e($v['message']) ?></textarea><?= $err('message') ?></div>
      <button class="btn btn--primary" type="submit">Send message</button>
    </form>
  <?php endif; ?>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
