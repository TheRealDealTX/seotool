<h1>Site settings</h1>
<form method="post" class="card form form-section narrow-lg">
  <?= csrf_field() ?>
  <label>Site name<input type="text" name="site_name" value="<?= e($v['site_name']) ?>" required maxlength="60"></label>
  <label>Tagline<input type="text" name="tagline" value="<?= e($v['tagline']) ?>" maxlength="120"></label>
  <label>Announcement banner <small class="muted">(shown to everyone at the top of every page; leave empty to hide)</small><textarea name="announcement" rows="2" maxlength="500"><?= e($v['announcement']) ?></textarea></label>
  <label>Admin alert email <small class="muted">(new reports and property submissions are emailed here)</small><input type="email" name="admin_email" value="<?= e($v['admin_email']) ?>" placeholder="marketing@riseapartments.com"></label>
  <label>GIPHY API key <small class="muted">(turns on GIF search in posts, comments and chats — get a free key at developers.giphy.com)</small><input type="text" name="giphy_key" value="<?= e($v['giphy_key']) ?>" autocomplete="off" placeholder="Paste your GIPHY API key"></label>
  <h2>Community rules</h2>
  <label class="switch"><input type="checkbox" name="registration_open" value="1"<?= $v['registration_open'] === '1' ? ' checked' : '' ?>><span></span> Allow new sign-ups</label>
  <label class="switch"><input type="checkbox" name="messaging_friends_only" value="1"<?= $v['messaging_friends_only'] === '1' ? ' checked' : '' ?>><span></span> Only friends can message each other</label>
  <label class="switch"><input type="checkbox" name="allow_property_submissions" value="1"<?= $v['allow_property_submissions'] === '1' ? ' checked' : '' ?>><span></span> Members can submit new properties</label>
  <label class="switch"><input type="checkbox" name="require_property_approval" value="1"<?= $v['require_property_approval'] === '1' ? ' checked' : '' ?>><span></span> Member-submitted properties need admin approval</label>
  <div class="form-actions"><button class="btn btn-primary">Save settings</button></div>
</form>
<form method="post" class="card form form-section narrow-lg">
  <?= csrf_field() ?><input type="hidden" name="test_email" value="1">
  <h2>Email delivery</h2>
  <p class="muted small">Password resets, notifications and admin alerts are sent from the site's mailbox. Send yourself a test to confirm it works.</p>
  <label>Send test to<input type="email" name="test_to" value="<?= e(current_user()['email']) ?>"></label>
  <button class="btn btn-outline btn-sm">Send test email</button>
</form>
