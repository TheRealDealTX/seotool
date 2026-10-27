<?php
defined('HA_ROOT') || exit;
$title = 'Listings';
$actions = '<a class="btn primary" href="/admin/listings/new/">＋ Add a listing</a>';
$qs = fn ($extra) => '?' . http_build_query(array_filter(array_merge($f, $extra)));
?>
<form class="card filters" method="get">
  <input type="search" name="q" value="<?= e($f['q']) ?>" placeholder="Search by name, street or ZIP…" aria-label="Search listings">
  <select name="area" aria-label="Area"><option value="">All areas</option><?php foreach (AREAS as $k => $a): ?><option value="<?= $k ?>"<?= $f['area'] === $k ? ' selected' : '' ?>><?= e($a['name']) ?></option><?php endforeach ?></select>
  <select name="status" aria-label="Status"><option value="">Live &amp; hidden</option><option value="publish"<?= $f['status'] === 'publish' ? ' selected' : '' ?>>Live only</option><option value="hidden"<?= $f['status'] === 'hidden' ? ' selected' : '' ?>>Hidden only</option></select>
  <select name="source" aria-label="Source"><option value="">Any source</option><option value="manual"<?= $f['source'] === 'manual' ? ' selected' : '' ?>>Added by hand</option><option value="rise"<?= $f['source'] === 'rise' ? ' selected' : '' ?>>From Rise (auto-sync)</option><option value="edited"<?= $f['source'] === 'edited' ? ' selected' : '' ?>>From Rise (edited here)</option></select>
  <button class="btn" type="submit">Filter</button>
  <?php if (array_filter($f)): ?><a class="link" href="/admin/listings/">Clear</a><?php endif ?>
</form>
<p class="muted count"><?= number_format($total) ?> listing<?= $total === 1 ? '' : 's' ?></p>
<div class="card table-card">
  <table class="table">
    <thead><tr><th></th><th>Property</th><th>Area</th><th>Starts at</th><th>Beds</th><th>Status</th><th>Source</th><th></th></tr></thead>
    <tbody>
    <?php foreach ($rows as $r): ?>
      <tr>
        <td><a href="/admin/listings/<?= $r['id'] ?>/"><img class="thumb" src="<?= e($r['photo'] ?: '/assets/img/Houston-High-Rise.webp') ?>" alt="" loading="lazy"></a></td>
        <td><a class="strong" href="/admin/listings/<?= $r['id'] ?>/"><?= e($r['name']) ?></a><br><small class="muted"><?= e(trim($r['street'] . ', ' . $r['city'] . ' ' . $r['zip'], ', ')) ?></small></td>
        <td><?= e($r['neighborhood']) ?></td>
        <td><?= $r['price_min'] ? money($r['price_min']) : '<span class="muted">—</span>' ?></td>
        <td><?= e(beds_range($r)) ?></td>
        <td><span class="pill <?= $r['status'] === 'publish' ? 's-leased' : 's-closed' ?>"><?= $r['status'] === 'publish' ? 'Live' : 'Hidden' ?></span></td>
        <td><small><?= $r['source'] === 'manual' ? 'Added by hand' : ($r['locked'] ? 'Rise · edited' : 'Rise · auto') ?></small></td>
        <td class="nowrap"><a class="btn small" href="/admin/listings/<?= $r['id'] ?>/">Edit</a> <a class="btn small ghost" href="/apartment/<?= e($r['slug']) ?>/" target="_blank" rel="noopener">View ↗</a></td>
      </tr>
    <?php endforeach ?>
    <?php if (!$rows): ?><tr><td colspan="8" class="empty">No listings match. <a href="/admin/listings/new/">Add one</a>.</td></tr><?php endif ?>
    </tbody>
  </table>
</div>
<?php if ($pages > 1): ?>
<nav class="pager"><?php for ($n = 1; $n <= $pages; $n++): ?><a href="<?= e($qs(['page' => $n > 1 ? $n : null])) ?>"<?= $n === $page ? ' class="on"' : '' ?>><?= $n ?></a><?php endfor ?></nav>
<?php endif ?>
