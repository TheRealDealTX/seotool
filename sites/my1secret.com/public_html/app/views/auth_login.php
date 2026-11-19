<?php defined('M1S') || exit; ?>
<div class="narrow auth">
  <h1>Log in</h1>
  <form class="form card-pad" method="post" action="/login/">
    <?= csrf_field() ?>
    <input type="hidden" name="next" value="<?= e($next) ?>">
    <label for="username">Username or email</label>
    <input id="username" name="username" type="text" autocomplete="username" required value="<?= e(old('username')) ?>">
    <label for="password">Password</label>
    <input id="password" name="password" type="password" autocomplete="current-password" required>
    <div class="form-row"><a href="/forgot-password/">Forgot password?</a><button class="btn btn-accent" type="submit">Log in</button></div>
  </form>
  <p class="center">New here? <a href="/register/<?= $next !== '/' ? '?next=' . e(rawurlencode($next)) : '' ?>">Create a free account</a></p>
</div>
