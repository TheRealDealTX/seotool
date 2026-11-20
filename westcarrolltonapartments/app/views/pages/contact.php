<?php defined('WCA') || exit; ?>
<div class="wrap narrow section">
  <h1>Contact us</h1>
  <p class="lead">Questions about a listing, a correction, or help with your owner account? Send us a message and we'll reply by email.</p>
  <?php if ($sent): ?>
    <div class="alert alert-success">Thanks! Your message was sent. We usually reply within 1–2 business days.</div>
  <?php else: ?>
    <?php if ($errors): ?><div class="alert alert-error"><?php foreach ($errors as $er): ?><div><?= e($er) ?></div><?php endforeach; ?></div><?php endif; ?>
    <form method="post" class="form card">
      <?= csrf_field() ?><?= honeypot_field() ?>
      <div class="grid-2">
        <label>Name *<input name="name" required maxlength="120" value="<?= e(post('name')) ?>" autocomplete="name"></label>
        <label>Email *<input type="email" name="email" required maxlength="190" value="<?= e(post('email')) ?>" autocomplete="email"></label>
      </div>
      <label>Subject<input name="subject" maxlength="190" value="<?= e(post('subject') ?: ($_GET['subject'] ?? '')) ?>"></label>
      <label>Message *<textarea name="message" rows="6" required maxlength="5000"><?= e(post('message')) ?></textarea></label>
      <button class="btn" type="submit">Send message</button>
    </form>
  <?php endif; ?>
  <p class="muted">Or email <a href="mailto:info@westcarrolltonapartments.com">info@westcarrolltonapartments.com</a>. We can't schedule tours or process applications; please contact the property directly for that.</p>
</div>
