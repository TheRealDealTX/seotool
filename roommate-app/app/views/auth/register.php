<?php $err = fn($k) => isset($errors[$k]) ? '<span class="field-error">' . e($errors[$k]) . '</span>' : ''; ?>
<div class="auth-card card">
  <h1>Find your roommate</h1>
  <p class="muted">Join renters looking for roommates at the apartments they love.</p>
  <form method="post" class="form" novalidate>
    <?= csrf_field() ?>
    <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <label>Full name<input type="text" name="name" value="<?= e(old('name')) ?>" required maxlength="80" autocomplete="name"><?= $err('name') ?></label>
    <label>Email<input type="email" name="email" value="<?= e(old('email')) ?>" required autocomplete="email"><?= $err('email') ?></label>
    <label>Username
      <div class="input-prefix"><span>@</span><input type="text" name="username" value="<?= e(old('username')) ?>" required pattern="[A-Za-z0-9_]{3,30}" maxlength="30" autocomplete="off"></div><?= $err('username') ?></label>
    <label>Password<input type="password" name="password" required minlength="8" autocomplete="new-password"><?= $err('password') ?></label>
    <fieldset class="choice-group">
      <legend>I'm looking to…</legend>
      <label class="choice"><input type="radio" name="looking_for" value="need_place" checked><span>Find a room / place</span></label>
      <label class="choice"><input type="radio" name="looking_for" value="have_place"><span>Fill a room I have</span></label>
      <label class="choice"><input type="radio" name="looking_for" value="either"><span>Team up &amp; find one together</span></label>
    </fieldset>
    <label class="check"><input type="checkbox" name="agree" value="1" required> I agree to the <a href="/terms" target="_blank">Terms</a> and <a href="/privacy" target="_blank">Privacy Policy</a>, and I'm 18 or older.</label><?= $err('agree') ?>
    <button class="btn btn-primary btn-block" type="submit">Create account</button>
  </form>
  <p class="auth-alt">Already a member? <a href="/login">Log in</a></p>
</div>
