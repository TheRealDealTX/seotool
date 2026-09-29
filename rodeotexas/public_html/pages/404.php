<?php
defined('RT_APP') || exit;

use RT\EventRepo;
use RT\View;

$upcoming = EventRepo::upcoming(4);
$page = [
    'title' => 'Page not found',
    'description' => 'The page you were looking for could not be found.',
    'robots' => 'noindex,follow',
    'canonical' => request_path(),
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<div class="wrap narrow">
  <h1>We couldn't find that page</h1>
  <p>The page may have moved when we rebuilt the site. Try searching for a rodeo instead:</p>
  <form class="hero-search hero-search--light" action="/rodeos/" method="get" role="search">
    <label class="visually-hidden" for="nf-q">Search rodeos</label>
    <input id="nf-q" name="q" type="search" placeholder="Event, city, venue or ZIP code">
    <button class="btn btn--primary" type="submit">Search</button>
  </form>
  <?php if ($upcoming): ?>
    <h2>Coming up</h2>
    <div class="event-list"><?php foreach ($upcoming as $ev) { echo View::eventCard($ev); } ?></div>
  <?php endif; ?>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
