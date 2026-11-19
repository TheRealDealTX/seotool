<?php defined('M1S') || exit; ?>
<div class="narrow auth">
  <h1>Reset your password</h1>
  <form class="form card-pad" method="post" action="/forgot-password/">
    <?= csrf_field() ?>
    <label for="email">Account email</label>
    <input id="email" name="email" type="email" autocomplete="email" required>
    <div class="form-row"><a href="/login/">Back to log in</a><button class="btn btn-accent" type="submit">Send reset link</button></div>
  </form>
</div>
