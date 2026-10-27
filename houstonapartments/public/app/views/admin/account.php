<?php
defined('HA_ROOT') || exit;
$title = 'My account';
?>
<form class="card narrow" method="post">
  <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
  <label class="block">Your name<input name="name" value="<?= e($u['name']) ?>"></label>
  <label class="block">Email<input value="<?= e($u['email']) ?>" disabled></label>
  <label class="block">Current password<input name="current" type="password" required autocomplete="current-password"></label>
  <label class="block">New password <small>(10+ characters)</small><input name="password" type="password" minlength="10" required autocomplete="new-password"></label>
  <label class="block">Repeat new password<input name="confirm" type="password" minlength="10" required autocomplete="new-password"></label>
  <button class="btn primary" type="submit">Save</button>
</form>
