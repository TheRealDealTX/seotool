<div class="page-head"><h1>Properties <small class="muted"><?= number_format($total) ?></small></h1><a class="btn btn-primary btn-sm" href="/admin/properties/new"><?= icon('plus') ?> New property</a></div>
<form class="card filters" method="get">
  <div class="filters-grid">
    <label>Search<input type="search" name="q" value="<?= e($s) ?>" placeholder="Name or city"></label>
    <label>Status<select name="status"><option value="">All</option><?php foreach (['pending', 'approved', 'rejected'] as $st): ?><option value="<?= $st ?>"<?= $status === $st ? ' selected' : '' ?>><?= ucfirst($st) ?></option><?php endforeach; ?></select></label>
  </div>
  <div class="filters-foot"><span class="spacer"></span><button class="btn btn-primary btn-sm">Filter</button></div>
</form>
<div class="card table-card"><div class="table-wrap"><table class="table">
  <thead><tr><th>Property</th><th>City</th><th>Rent</th><th>Interested</th><th>Status</th><th>Added by</th><th></th></tr></thead>
  <tbody>
  <?php foreach ($props as $p): ?>
  <tr>
    <td><a href="/admin/properties/<?= (int)$p['id'] ?>"><strong><?= e($p['name']) ?></strong></a><?php if ($p['is_featured']): ?> <span class="tag tag-feature">Featured</span><?php endif; ?></td>
    <td class="small"><?= e($p['city']) ?></td>
    <td class="small"><?= e(money($p['rent_min'])) ?><?= $p['rent_max'] ? '–' . e(money($p['rent_max'])) : '' ?></td>
    <td class="num"><?= (int)$p['interested'] ?></td>
    <td><span class="tag <?= ['approved' => 'tag-ok', 'pending' => 'tag-warn', 'rejected' => 'tag-danger'][$p['status']] ?>"><?= e($p['status']) ?></span></td>
    <td class="small muted"><?= $p['creator'] ? '@' . e($p['creator']) : '—' ?></td>
    <td class="actions">
      <form method="post"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$p['id'] ?>">
        <?php if ($p['status'] !== 'approved'): ?><button class="btn btn-primary btn-xs" name="action" value="approve">Approve</button><?php endif; ?>
        <?php if ($p['status'] === 'pending'): ?><button class="btn btn-outline btn-xs" name="action" value="reject">Reject</button><?php endif; ?>
        <?php if ($p['status'] === 'approved'): ?><button class="btn btn-outline btn-xs" name="action" value="feature"><?= $p['is_featured'] ? 'Unfeature' : 'Feature' ?></button><?php endif; ?>
        <a class="btn btn-ghost btn-xs" href="/admin/properties/<?= (int)$p['id'] ?>">Edit</a>
        <button class="btn btn-ghost btn-xs danger" name="action" value="delete" data-confirm="Delete this property? Renter interests in it will be removed.">Delete</button>
      </form>
    </td>
  </tr>
  <?php endforeach; ?>
  <?php if (!$props): ?><tr><td colspan="7" class="muted">No properties.</td></tr><?php endif; ?>
  </tbody>
</table></div></div>
<?php partial('partials/pager', ['page' => $page, 'pages' => $pages]); ?>
