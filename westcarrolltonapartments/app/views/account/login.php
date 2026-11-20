<?php defined('WCA') || exit; ?>
<div class="wrap narrow section">
  <div class="card auth-card">
    <h1 class="h2">Owner sign in</h1>
    <?php if ($sent): ?>
      <div class="alert alert-success">If an owner account exists for that email, we just sent a sign-in link. It expires in 30 minutes. Check your spam folder if you don't see it.</div>
    <?php else: ?>
      <p>No password needed. Enter the email on your owner account and we'll email you a secure sign-in link.</p>
      <?php if ($errors): ?><div class="alert alert-error"><?= e($errors[0]) ?></div><?php endif; ?>
      <form method="post" class="form">
        <?= csrf_field() ?>
        <label>Email<input type="email" name="email" required autocomplete="email" autofocus></label>
        <button class="btn btn-block" type="submit">Email me a sign-in link</button>
      </form>
    <?php endif; ?>
    <hr>
    <p class="small">Don't have an account? Accounts are created when you <a href="/apartments/">claim a listing</a> or publish an <a href="/list-your-property/">owner listing</a> ($<?= listing_price_cents() / 100 ?>).</p>
  </div>
</div>
