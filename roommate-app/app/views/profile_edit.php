<div class="narrow-lg">
  <div class="page-head"><div><h1><?= $welcome ? 'Set up your profile' : 'Edit profile' ?></h1><p class="muted">The more you share, the better your matches.</p></div>
  <a class="btn btn-ghost" href="/u/<?= e($u['username']) ?>">View profile</a></div>
  <?php if ($errors): ?><div class="alert alert-error"><ul><?php foreach ($errors as $er): ?><li><?= e($er) ?></li><?php endforeach; ?></ul></div><?php endif; ?>
  <form method="post" enctype="multipart/form-data" class="form">
    <?= csrf_field() ?>
    <?php if ($welcome): ?><input type="hidden" name="welcome" value="1"><?php endif; ?>

    <section class="card form-section">
      <h2>Basics</h2>
      <div class="avatar-edit">
        <div class="avatar-preview"><?= avatar($u, 'xl') ?></div>
        <div>
          <label class="btn btn-outline btn-sm"><?= icon('image') ?> Upload photo<input type="file" name="avatar" accept="image/*" hidden class="js-avatar-input"></label>
          <?php if ($u['avatar']): ?><label class="check small"><input type="checkbox" name="remove_avatar" value="1"> Remove photo</label><?php endif; ?>
          <p class="muted small">A clear, friendly photo of your face works best.</p>
        </div>
      </div>
      <div class="row-2">
        <label>Full name<input type="text" name="name" value="<?= e($u['name']) ?>" required maxlength="80"></label>
        <label>Birth year<input type="number" name="birth_year" value="<?= e($u['birth_year']) ?>" min="<?= date('Y') - 100 ?>" max="<?= date('Y') - 18 ?>" placeholder="e.g. 1998"></label>
      </div>
      <div class="row-2">
        <label>Gender<select name="gender"><?= options('gender', $u['gender']) ?></select></label>
        <label>City / area<input type="text" name="city" value="<?= e($u['city']) ?>" maxlength="100" placeholder="e.g. Austin"></label>
      </div>
      <label>Occupation<input type="text" name="occupation" value="<?= e($u['occupation']) ?>" maxlength="100" placeholder="e.g. Nurse, Student at UT, Software engineer"></label>
      <label>About you<textarea name="bio" rows="5" maxlength="1500" placeholder="What's a typical week like? What are you looking for in a roommate?"><?= e($u['bio']) ?></textarea></label>
      <label>Interests <small class="muted">(comma separated)</small><input type="text" name="interests" value="<?= e($u['interests']) ?>" maxlength="255" placeholder="hiking, cooking, gaming, live music"></label>
      <label>Instagram <small class="muted">(optional)</small><div class="input-prefix"><span>@</span><input type="text" name="instagram" value="<?= e($u['instagram']) ?>" maxlength="60"></div></label>
    </section>

    <section class="card form-section">
      <h2>Housing</h2>
      <fieldset class="choice-group">
        <legend>I'm looking to…</legend>
        <?php foreach (LABELS['looking_for'] as $k => $v): ?>
        <label class="choice"><input type="radio" name="looking_for" value="<?= e($k) ?>"<?= $u['looking_for'] === $k ? ' checked' : '' ?>><span><?= e($v) ?></span></label>
        <?php endforeach; ?>
      </fieldset>
      <div class="row-3">
        <label>Budget min ($/mo)<input type="number" name="budget_min" value="<?= e($u['budget_min']) ?>" min="0" step="25"></label>
        <label>Budget max ($/mo)<input type="number" name="budget_max" value="<?= e($u['budget_max']) ?>" min="0" step="25"></label>
        <label>Lease length<select name="lease_months"><option value="">Flexible</option><?php foreach ([3, 6, 9, 12, 15, 18, 24] as $m): ?><option value="<?= $m ?>"<?= (int)$u['lease_months'] === $m ? ' selected' : '' ?>><?= $m ?> months</option><?php endforeach; ?></select></label>
      </div>
      <label>Target move-in date<input type="date" name="move_in_date" value="<?= e($u['move_in_date']) ?>"></label>
    </section>

    <section class="card form-section">
      <h2>Preferred apartment properties</h2>
      <p class="muted small">You'll be matched with renters interested in the same properties. Can't find yours? <a href="/properties/new">Add a property</a>.</p>
      <div class="prop-search">
        <input type="search" class="js-prop-search" data-target="#prop-picker" placeholder="Search by apartment name, city or ZIP…" autocomplete="off">
        <ul class="prop-search-results" hidden></ul>
      </div>
      <div class="prop-picker" id="prop-picker">
        <?php foreach ($properties as $p): ?>
        <label class="pick" data-name="<?= e(strtolower($p['name'] . ' ' . $p['city'])) ?>"><input type="checkbox" name="properties[]" value="<?= (int)$p['id'] ?>"<?= in_array((int)$p['id'], $mine, true) ? ' checked' : '' ?>><span><?= icon('building') ?><?= e($p['name']) ?><?php if ($p['city']): ?><small><?= e($p['city']) ?></small><?php endif; ?></span></label>
        <?php endforeach; ?>
        <?php if (!$properties): ?><p class="muted small js-none">Search above to add the properties you're interested in.</p><?php endif; ?>
      </div>
    </section>

    <section class="card form-section">
      <h2>Lifestyle</h2>
      <label>Cleanliness <output class="range-out"><?= e(label('cleanliness', $u['cleanliness'])) ?></output>
        <input type="range" name="cleanliness" min="1" max="5" value="<?= (int)$u['cleanliness'] ?>" class="js-range" data-labels='<?= e(json_encode(array_values(LABELS['cleanliness']))) ?>'></label>
      <div class="row-2">
        <label>Sleep schedule<select name="sleep_schedule"><?= options('sleep_schedule', $u['sleep_schedule']) ?></select></label>
        <label>Smoking<select name="smoking"><?= options('smoking', $u['smoking']) ?></select></label>
      </div>
      <div class="row-2">
        <label>Pets<select name="pets"><?= options('pets', $u['pets']) ?></select></label>
        <label>Guests<select name="guests"><?= options('guests', $u['guests']) ?></select></label>
      </div>
      <div class="row-2">
        <label>Roommate gender preference<select name="gender_pref"><?= options('gender_pref', $u['gender_pref']) ?></select></label>
        <label class="check check-pad"><input type="checkbox" name="work_from_home" value="1"<?= $u['work_from_home'] ? ' checked' : '' ?>> I work from home</label>
      </div>
    </section>

    <div class="form-actions sticky-actions">
      <a class="btn btn-ghost" href="/u/<?= e($u['username']) ?>">Cancel</a>
      <button class="btn btn-primary" type="submit"><?= $welcome ? 'Save & find matches' : 'Save profile' ?></button>
    </div>
  </form>
</div>
