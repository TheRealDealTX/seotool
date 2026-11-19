<?php defined('M1S') || exit; ?>
<div class="narrow auth">
  <h1>Join My 1 Secret</h1>
  <p class="lede">Free account. Post questions, share your secrets, comment on guides and vote on the best answers.</p>
  <form class="form card-pad" method="post" action="/register/">
    <?= csrf_field() ?><?= bot_check_fields() ?>
    <input type="hidden" name="next" value="<?= e($next) ?>">
    <label for="username">Username</label>
    <input id="username" name="username" type="text" autocomplete="username" required minlength="3" maxlength="20" pattern="[A-Za-z0-9_\-]{3,20}" value="<?= e(old('username')) ?>">
    <p class="hint">3 to 20 letters, numbers, - or _. This is public and cannot be changed.</p>
    <label for="email">Email</label>
    <input id="email" name="email" type="email" autocomplete="email" required maxlength="190" value="<?= e(old('email')) ?>">
    <p class="hint">Only used for password resets. Never shown publicly.</p>
    <label for="password">Password</label>
    <input id="password" name="password" type="password" autocomplete="new-password" required minlength="10">
    <p class="hint">At least 10 characters.</p>
    <label class="check"><input type="checkbox" name="agree" value="1" required> I agree to the <a href="/community-guidelines/" target="_blank">community guidelines</a> and <a href="/terms/" target="_blank">terms</a>.</label>
    <div class="form-row"><button class="btn btn-accent" type="submit">Create account</button></div>
  </form>
  <p class="center">Already a member? <a href="/login/">Log in</a></p>
</div>
