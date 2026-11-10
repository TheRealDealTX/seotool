<h1>Posts <small class="muted"><?= number_format($total) ?></small></h1>
<form class="card filters" method="get">
  <div class="filters-grid">
    <label>Search<input type="search" name="q" value="<?= e($s) ?>" placeholder="Text or username"></label>
    <label>Status<select name="status"><option value="">All</option><option value="visible"<?= $status === 'visible' ? ' selected' : '' ?>>Visible</option><option value="hidden"<?= $status === 'hidden' ? ' selected' : '' ?>>Hidden</option></select></label>
  </div>
  <div class="filters-foot"><span class="spacer"></span><button class="btn btn-primary btn-sm">Filter</button></div>
</form>
<div class="card table-card"><div class="table-wrap"><table class="table">
  <thead><tr><th>Author</th><th>Post</th><th>Engagement</th><th>Status</th><th>Date</th><th></th></tr></thead>
  <tbody>
  <?php foreach ($posts as $p): ?>
  <tr>
    <td class="small"><a href="/admin/users/<?= (int)$p['user_id'] ?>">@<?= e($p['username']) ?></a></td>
    <td class="small post-cell"><?= e(mb_strimwidth($p['body'], 0, 160, '…')) ?><?= $p['image'] ? ' <span class="tag">photo</span>' : '' ?><?= $p['property_name'] ? '<br><span class="muted">' . e($p['property_name']) . '</span>' : '' ?></td>
    <td class="small muted"><?= (int)$p['likes'] ?> likes · <?= (int)$p['comments'] ?> comments</td>
    <td><span class="tag <?= $p['status'] === 'visible' ? 'tag-ok' : 'tag-warn' ?>"><?= e($p['status']) ?></span></td>
    <td class="small muted"><?= e(date('M j, Y', strtotime($p['created_at']))) ?></td>
    <td class="actions"><form method="post"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$p['id'] ?>">
      <?php if ($p['status'] === 'visible'): ?><a class="btn btn-ghost btn-xs" href="/post/<?= (int)$p['id'] ?>" target="_blank">View</a><button class="btn btn-outline btn-xs" name="action" value="hide">Hide</button>
      <?php else: ?><button class="btn btn-outline btn-xs" name="action" value="show">Unhide</button><?php endif; ?>
      <button class="btn btn-ghost btn-xs danger" name="action" value="delete" data-confirm="Delete this post permanently?">Delete</button>
    </form></td>
  </tr>
  <?php endforeach; ?>
  <?php if (!$posts): ?><tr><td colspan="6" class="muted">No posts.</td></tr><?php endif; ?>
  </tbody>
</table></div></div>
<?php partial('partials/pager', ['page' => $page, 'pages' => $pages]); ?>
