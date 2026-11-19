<?php defined('M1S') || exit; ?>
<div class="narrow">
  <h1>Account settings</h1>
  <p class="muted">Signed in as <a href="<?= e(user_url($u)) ?>">u/<?= e($u['username']) ?></a> · <?= number_format((int)$u['karma']) ?> karma · member since <?= e(nice_date($u['created_at'])) ?></p>
  <form class="form card-pad" method="post" action="/settings/">
    <?= csrf_field() ?><input type="hidden" name="section" value="profile">
    <h2>Profile</h2>
    <label for="display_name">Display name</label>
    <input id="display_name" name="display_name" maxlength="60" value="<?= e((string)$u['display_name']) ?>">
    <label for="bio">About you</label>
    <textarea id="bio" name="bio" rows="3" maxlength="500"><?= e((string)$u['bio']) ?></textarea>
    <div class="form-row"><button class="btn btn-accent" type="submit">Save profile</button></div>
  </form>
  <form class="form card-pad" method="post" action="/settings/">
    <?= csrf_field() ?><input type="hidden" name="section" value="email">
    <h2>Email</h2>
    <label for="email">Email address</label>
    <input id="email" name="email" type="email" required value="<?= e((string)$u['email']) ?>">
    <label for="cp1">Current password</label>
    <input id="cp1" name="current_password" type="password" autocomplete="current-password" required>
    <div class="form-row"><button class="btn btn-accent" type="submit">Update email</button></div>
  </form>
  <form class="form card-pad" method="post" action="/settings/">
    <?= csrf_field() ?><input type="hidden" name="section" value="password">
    <h2>Password</h2>
    <label for="cp2">Current password</label>
    <input id="cp2" name="current_password" type="password" autocomplete="current-password" required>
    <label for="np">New password</label>
    <input id="np" name="new_password" type="password" autocomplete="new-password" required minlength="10">
    <div class="form-row"><button class="btn btn-accent" type="submit">Change password</button></div>
  </form>
</div>
