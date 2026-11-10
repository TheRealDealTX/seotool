<div class="page-head">
  <div><h1>Discover roommates</h1><p class="muted"><?= number_format($total) ?> renter<?= $total === 1 ? '' : 's' ?> found<?= $f['sort'] === 'match' ? ', best matches first' : '' ?>.</p></div>
</div>
<?php if (!$hasProps): ?>
<div class="alert alert-info"><?= icon('building') ?> <span><strong>Tip:</strong> <a href="/properties">Choose your preferred apartment properties</a> to get matched with renters interested in the same place.</span></div>
<?php endif; ?>
<form class="card filters" method="get">
  <div class="filters-grid">
    <label>Search<input type="search" name="q" value="<?= e($f['q']) ?>" placeholder="Name, job, interests"></label>
    <label>Property
      <select name="property"><option value="">Any property</option>
        <?php foreach ($properties as $p): ?><option value="<?= (int)$p['id'] ?>"<?= $f['property'] === (int)$p['id'] ? ' selected' : '' ?>><?= e($p['name']) ?></option><?php endforeach; ?>
      </select></label>
    <label>City<input type="text" name="city" value="<?= e($f['city']) ?>" placeholder="Any city"></label>
    <label>Looking for
      <select name="looking_for"><option value="">Anyone</option>
        <option value="have_place"<?= $f['looking_for'] === 'have_place' ? ' selected' : '' ?>>Has a place</option>
        <option value="need_place"<?= $f['looking_for'] === 'need_place' ? ' selected' : '' ?>>Needs a place</option>
        <option value="either"<?= $f['looking_for'] === 'either' ? ' selected' : '' ?>>Open to either</option>
      </select></label>
    <label>My max budget<input type="number" name="budget" min="0" step="50" value="<?= $f['budget'] ?: '' ?>" placeholder="$"></label>
    <label>Gender
      <select name="gender"><option value="">Any</option>
        <option value="female"<?= $f['gender'] === 'female' ? ' selected' : '' ?>>Female</option>
        <option value="male"<?= $f['gender'] === 'male' ? ' selected' : '' ?>>Male</option>
        <option value="nonbinary"<?= $f['gender'] === 'nonbinary' ? ' selected' : '' ?>>Non-binary</option>
      </select></label>
    <label>Sort by
      <select name="sort">
        <option value="match"<?= $f['sort'] === 'match' ? ' selected' : '' ?>>Best match</option>
        <option value="active"<?= $f['sort'] === 'active' ? ' selected' : '' ?>>Recently active</option>
        <option value="newest"<?= $f['sort'] === 'newest' ? ' selected' : '' ?>>Newest members</option>
      </select></label>
  </div>
  <div class="filters-foot">
    <label class="check"><input type="checkbox" name="nonsmoker" value="1"<?= $f['nonsmoker'] ? ' checked' : '' ?>> Non-smokers only</label>
    <label class="check"><input type="checkbox" name="pets" value="ok"<?= $f['pets'] ? ' checked' : '' ?>> No pets / pet friendly</label>
    <span class="spacer"></span>
    <a class="btn btn-ghost btn-sm" href="/discover">Reset</a>
    <button class="btn btn-primary btn-sm" type="submit"><?= icon('search') ?> Search</button>
  </div>
</form>

<?php if (!$results): ?>
  <div class="card empty-state"><?= icon('search') ?><h3>No renters match those filters</h3><p class="muted">Try widening your search.</p></div>
<?php else: ?>
<div class="grid grid-3">
  <?php foreach ($results as $r) partial('partials/user_card', ['u' => $r['u'], 'match' => $r['m']]); ?>
</div>
<?php endif; ?>
<?php partial('partials/pager', ['page' => $page, 'pages' => $pages]); ?>
