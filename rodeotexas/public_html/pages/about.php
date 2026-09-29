<?php
defined('RT_APP') || exit;

use RT\Db;

$sources = Db::all("SELECT name, homepage, access_status FROM sources WHERE access_status = 'active' AND enabled = 1 ORDER BY name");
$page = [
    'title' => 'About Rodeo Texas & Our Data Sources',
    'description' => 'Rodeo Texas is an independent guide to rodeos held across Texas. Learn where our listings come from and how we verify them.',
    'canonical' => '/about/',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<div class="wrap narrow prose">
  <h1>About Rodeo Texas</h1>
  <p>Welcome to Rodeo Texas — your one-stop source for rodeo across the Lone Star State. From small-town arenas to major championship circuits, Texas is home to some of the biggest and most exciting rodeo events in the country. Our mission is simple: to keep you informed and connected with rodeos happening throughout the state, all in one easy-to-navigate place.</p>
  <p>Whether you're a die-hard rodeo fan, a traveling competitor, or just looking to experience authentic Texas culture, Rodeo Texas helps you plan your rodeo season with schedules, event details and local highlights.</p>
  <p>At Rodeo Texas, we believe rodeo is more than a sport — it's a way of life. It's the dust rising from the arena, the roar of the crowd as the gates fly open, the pride of small towns coming together, and the heritage passed down through generations.</p>
  <p>You can now <a href="/rodeos/">search rodeos by city, ZIP code, region, association or date</a>, switch between list, calendar and map views, save favorites, add events to your calendar, and <a href="/submit-event/">submit your own rodeo</a>.</p>

  <h2 id="data">Where our listings come from</h2>
  <p>We only list events that take place in Texas, based on the venue's location. Listings come from:</p>
  <ul>
    <li><strong>Official organizer and venue calendars</strong> that publish machine-readable schedules we are allowed to read. We check them every Monday morning. Current automatic sources:
      <?php if ($sources): ?><ul><?php foreach ($sources as $s): ?><li><?= $s['homepage'] ? '<a href="' . e($s['homepage']) . '" rel="noopener">' . e($s['name']) . '</a>' : e($s['name']) ?></li><?php endforeach; ?></ul><?php endif; ?></li>
    <li><strong>Organizers and fans</strong> who submit events. A person reviews every submission against the official source before it is published.</li>
    <li><strong>Our editors</strong>, who add rodeos from official announcements.</li>
  </ul>
  <p>We never fill in missing details with guesses. If show times, prices, parking or accessibility information aren't published by the organizer, the listing says so. Each event page shows its information source and the date it was last verified.</p>
  <p>No single source covers every rodeo in Texas, so some events may be missing. If you know of one, please <a href="/submit-event/">tell us about it</a>. Rodeo Texas is independent and is not affiliated with the PRCA, PRORODEO or any other rodeo association.</p>

  <h2>Canceled or changed events</h2>
  <p>We mark an event as canceled or postponed only when the organizer says so. An event disappearing from a calendar is not treated as a cancellation. Please confirm with the organizer before you travel.</p>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
