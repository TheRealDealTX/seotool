<?php
/** Favorites stored in the visitor's browser (localStorage); rendered by app.js. */
defined('RT_APP') || exit;

$page = [
    'title' => 'Your Favorite Rodeos',
    'description' => 'Rodeos you have saved on this device.',
    'canonical' => '/favorites/',
    'robots' => 'noindex,follow',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<div class="wrap">
  <h1>Your favorites</h1>
  <p>Favorites are saved in this browser only — no account needed. They are not shared with us.</p>
  <div id="favorites" class="event-list" data-favorites aria-live="polite">
    <noscript><p class="notice">Favorites need JavaScript turned on.</p></noscript>
  </div>
  <p id="favorites-empty" class="empty" hidden>You haven't saved any events yet. Tap the star on any event to save it. <a href="/rodeos/">Browse rodeos</a>.</p>
  <p><button type="button" class="btn btn--ghost" data-fav-clear hidden>Clear all favorites</button></p>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
