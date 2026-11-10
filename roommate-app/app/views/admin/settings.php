<h1>Site settings</h1>
<form method="post" class="card form form-section narrow-lg">
  <?= csrf_field() ?>
  <label>Site name<input type="text" name="site_name" value="<?= e($v['site_name']) ?>" required maxlength="60"></label>
  <label>Tagline<input type="text" name="tagline" value="<?= e($v['tagline']) ?>" maxlength="120"></label>
  <label>Announcement banner <small class="muted">(shown to everyone at the top of every page; leave empty to hide)</small><textarea name="announcement" rows="2" maxlength="500"><?= e($v['announcement']) ?></textarea></label>
  <h2>Community rules</h2>
  <label class="switch"><input type="checkbox" name="registration_open" value="1"<?= $v['registration_open'] === '1' ? ' checked' : '' ?>><span></span> Allow new sign-ups</label>
  <label class="switch"><input type="checkbox" name="messaging_friends_only" value="1"<?= $v['messaging_friends_only'] === '1' ? ' checked' : '' ?>><span></span> Only friends can message each other</label>
  <label class="switch"><input type="checkbox" name="allow_property_submissions" value="1"<?= $v['allow_property_submissions'] === '1' ? ' checked' : '' ?>><span></span> Members can submit new properties</label>
  <label class="switch"><input type="checkbox" name="require_property_approval" value="1"<?= $v['require_property_approval'] === '1' ? ' checked' : '' ?>><span></span> Member-submitted properties need admin approval</label>
  <div class="form-actions"><button class="btn btn-primary">Save settings</button></div>
</form>
