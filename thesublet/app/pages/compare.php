<?php defined('APP') || exit;
cache_public();
ob_start(); ?>
<div class="wrap section">
  <h1>Compare sublets</h1>
  <p class="muted">Tick “Compare” on up to four listings to see them side by side.</p>
  <div class="table-scroll" data-compare-table><p class="muted">Loading…</p></div>
  <div class="empty-state" data-cmp-empty hidden><h3>Nothing to compare yet</h3><p>Use the “Compare” checkbox on listing cards.</p><p><a class="btn" href="/sublets/">Browse sublets</a></p></div>
</div>
<?php
page(['title' => 'Compare sublets | The Sublet', 'robots' => 'noindex, follow', 'canonical' => '/compare/', 'body' => ob_get_clean()]);
