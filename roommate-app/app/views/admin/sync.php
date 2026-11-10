<h1>Sync listings from Rise Apartments</h1>
<p class="muted">Imports every apartment listing from the Rise Apartments website so renters can pick them as preferred properties. Existing listings are updated (name, address, photo, link); renters' picks are kept. A daily automatic sync also runs on the server.</p>
<div class="stat-grid small-stats">
  <div class="stat card"><span>Synced listings</span><strong><?= number_format($stats['synced']) ?></strong></div>
  <div class="stat card"><span>Added manually / by members</span><strong><?= number_format($stats['manual']) ?></strong></div>
  <div class="stat card"><span>Last sync</span><strong style="font-size:1rem"><?= $last ? e($last) : 'Never' ?></strong></div>
</div>
<section class="card form-section">
  <h2>Run sync now</h2>
  <p class="small muted">Takes a minute or two. Keep this tab open until it finishes.</p>
  <button class="btn btn-primary" id="sync-go" type="button"><?= icon('link') ?> Start sync</button>
  <div class="progress" style="margin-top:16px" hidden id="sync-bar"><span style="width:0"></span></div>
  <p class="small" id="sync-log"></p>
</section>
<section class="card form-section">
  <h2>Source</h2>
  <form method="post" class="form"><?= csrf_field() ?><input type="hidden" name="save_source" value="1">
    <label>WordPress site URL<input type="url" name="sync_source" value="<?= e($source) ?>" required></label>
    <button class="btn btn-outline btn-sm">Save</button>
  </form>
</section>
<script>
document.getElementById('sync-go').addEventListener('click', function () {
  var btn = this, bar = document.getElementById('sync-bar'), log = document.getElementById('sync-log');
  var csrf = document.querySelector('meta[name=csrf]').content, added = 0, updated = 0;
  btn.disabled = true; bar.hidden = false;
  function step(page) {
    var fd = new FormData(); fd.append('_csrf', csrf); fd.append('page', page);
    fetch('/admin/sync', { method: 'POST', body: fd, headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j.error) throw new Error(j.error);
        added += j.added; updated += j.updated;
        var total = Math.max(j.total_pages, 1);
        bar.firstElementChild.style.width = Math.min(100, page / total * 100) + '%';
        log.textContent = 'Page ' + page + ' of ' + total + ' — ' + added + ' new, ' + updated + ' updated';
        if (page < j.total_pages) step(page + 1); else { log.textContent += '. Done!'; btn.disabled = false; }
      })
      .catch(function (e) { log.textContent = 'Stopped on page ' + page + ': ' + e.message + '. Click Start to retry.'; btn.disabled = false; });
  }
  step(1);
});
</script>
