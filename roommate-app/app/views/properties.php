<div class="page-head">
  <div><h1>Apartment properties</h1><p class="muted">Pick the places you'd love to live. We'll match you with renters who want the same.</p></div>
  <a class="btn btn-primary" href="/properties/new"><?= icon('plus') ?> Add a property</a>
</div>
<form class="card filters" method="get">
  <div class="filters-grid">
    <label>Search<input type="search" name="q" value="<?= e($qstr) ?>" placeholder="Name, address or ZIP"></label>
    <label>City<select name="city"><option value="">All cities</option><?php foreach ($cities as $c): ?><option<?= $c === $city ? ' selected' : '' ?>><?= e($c) ?></option><?php endforeach; ?></select></label>
    <label>Sort<select name="sort">
      <option value="popular"<?= $sort === 'popular' ? ' selected' : '' ?>>Most popular</option>
      <option value="name"<?= $sort === 'name' ? ' selected' : '' ?>>Name</option>
      <option value="rent"<?= $sort === 'rent' ? ' selected' : '' ?>>Lowest rent</option>
      <option value="newest"<?= $sort === 'newest' ? ' selected' : '' ?>>Newest</option>
    </select></label>
  </div>
  <div class="filters-foot">
    <label class="check"><input type="checkbox" name="mine" value="1"<?= $mineOnly ? ' checked' : '' ?>> Only my properties</label>
    <span class="spacer"></span>
    <button class="btn btn-primary btn-sm" type="submit"><?= icon('search') ?> Search</button>
  </div>
</form>
<?php if (!$props): ?>
  <div class="card empty-state"><?= icon('building') ?><h3>No properties found</h3><p class="muted">Can't find yours? Add it and others can join you.</p><a class="btn btn-primary" href="/properties/new">Add a property</a></div>
<?php endif; ?>
<div class="grid grid-3">
  <?php foreach ($props as $p) partial('partials/property_card', ['p' => $p, 'interestedIn' => $interestedIn]); ?>
</div>
<?php partial('partials/pager', ['page' => $page, 'pages' => $pages]); ?>
