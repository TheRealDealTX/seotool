<?php defined('APP') || exit;

cache_private();
$sent = false; $err = null;
if (is_post()) {
    if ($g = form_guard()) $err = $g;
    elseif (!rate_limit('contactpage', 4, 3600)) $err = 'Too many messages. Please try again later.';
    else {
        $name = mb_substr(post('name'), 0, 120); $email = strtolower(post('email')); $msg = mb_substr(post('message'), 0, 4000);
        if (mb_strlen($name) < 2 || !valid_email($email) || mb_strlen($msg) < 10) $err = 'Please fill in your name, a valid email and a message.';
        else {
            insert('messages', ['listing_id' => null, 'kind' => 'contact', 'sender_name' => $name, 'sender_email' => $email, 'body' => $msg, 'ip' => client_ip(), 'created_at' => now()]);
            send_mail(cfg('admin_notify') ?: cfg('smtp.from'), '[The Sublet] Contact form: ' . $name, '<p><strong>' . e($name) . '</strong> &lt;' . e($email) . '&gt;</p><p>' . nl2br(e($msg)) . '</p>', $email);
            $sent = true;
        }
    }
}
ob_start(); ?>
<div class="wrap narrow section">
  <h1>Contact The Sublet</h1>
  <?php if ($sent): ?>
    <div class="flash flash-ok">Thanks — we’ve got your message and will reply by email.</div>
  <?php else: ?>
    <p>Questions about a listing, your account or a payment? Send us a note. To reach a host, use the Contact form on their listing. To flag a suspicious listing, use “Report listing” on that page.</p>
    <?php if ($err): ?><div class="flash flash-err"><?= e($err) ?></div><?php endif; ?>
    <form method="post" class="stack"><?= csrf_field() ?><?= honeypot_field() ?>
      <label>Name<input type="text" name="name" required maxlength="120" value="<?= e(post('name')) ?>"></label>
      <label>Email<input type="email" name="email" required maxlength="190" value="<?= e(post('email')) ?>"></label>
      <label>Message<textarea name="message" rows="6" required maxlength="4000"><?= e(post('message')) ?></textarea></label>
      <button class="btn" type="submit">Send</button>
    </form>
  <?php endif; ?>
</div>
<?php
page(['title' => 'Contact | The Sublet', 'description' => 'Contact The Sublet about listings, accounts or payments.', 'canonical' => '/contact/', 'body' => ob_get_clean()]);
