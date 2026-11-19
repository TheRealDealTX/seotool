<?php defined('M1S') || exit; ?>
<div class="narrow auth">
  <h1>Choose a new password</h1>
  <form class="form card-pad" method="post" action="/reset-password/">
    <?= csrf_field() ?>
    <input type="hidden" name="u" value="<?= (int)$uid ?>"><input type="hidden" name="t" value="<?= e($token) ?>">
    <label for="password">New password</label>
    <input id="password" name="password" type="password" autocomplete="new-password" required minlength="10">
    <div class="form-row"><button class="btn btn-accent" type="submit">Save password</button></div>
  </form>
</div>
