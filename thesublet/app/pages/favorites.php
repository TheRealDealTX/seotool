<?php defined('APP') || exit;
cache_public();
ob_start(); ?>
<div class="wrap section">
  <h1>Saved sublets</h1>
  <p class="muted">Favorites are stored on this device only — no account needed.</p>
  <div class="grid cards" data-favorites-list><p class="muted">Loading…</p></div>
  <div class="empty-state" data-fav-empty hidden><h3>No saved sublets yet</h3><p>Tap the ♡ on any listing to save it here.</p><p><a class="btn" href="/sublets/">Browse sublets</a></p></div>
  <div class="compare-bar" hidden><span><strong data-cmp-count>0</strong> selected to compare</span> <a class="btn btn-sm" href="/compare/" data-cmp-link>Compare</a> <button type="button" class="btn btn-sm btn-ghost" data-cmp-clear>Clear</button></div>
</div>
<?php
page(['title' => 'Saved sublets | The Sublet', 'robots' => 'noindex, follow', 'canonical' => '/favorites/', 'body' => ob_get_clean()]);
