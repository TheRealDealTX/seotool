<?php
defined('RT_APP') || exit;

use RT\Db;
use RT\EventRepo;
use RT\Seo;
use RT\View;

$counts = EventRepo::counts();
$upcoming = EventRepo::upcoming(8);
$regions = EventRepo::regions();
$articles = Db::all("SELECT slug, title, excerpt, featured_image, featured_alt, featured_width, featured_height FROM articles WHERE status = 'published' ORDER BY published_at DESC LIMIT 3");

$page = [
    'title' => 'Rodeo Texas — Find Upcoming Rodeos Across Texas',
    'title_full' => true,
    'description' => 'Find upcoming Texas rodeos by date, city, ZIP code, region or association. Pro, amateur, youth, high school and ranch rodeos with venues, show times and official links.',
    'canonical' => '/',
    'jsonld' => [Seo::website(), [
        '@context' => 'https://schema.org', '@type' => 'Organization', 'name' => cfg('site_name'), 'url' => abs_url('/'),
        'logo' => abs_url('/assets/img/logo-512.png'),
    ]],
    'body_class' => 'page-home',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<section class="hero">
  <div class="wrap hero__inner">
    <p class="hero__kicker">The Texas rodeo schedule</p>
    <h1 class="hero__title">Find a rodeo near you</h1>
    <p class="hero__lead">Search rodeos held in Texas — from PRCA pro rodeos to youth, high school and ranch rodeos.</p>
    <form class="hero-search" action="/rodeos/" method="get" role="search">
      <label class="visually-hidden" for="hero-q">Search by event, city, venue or ZIP code</label>
      <input id="hero-q" name="q" type="search" placeholder="Event, city, venue or ZIP code" autocomplete="off" enterkeyhint="search">
      <button class="btn btn--primary" type="submit">Search</button>
    </form>
    <ul class="quick-chips" aria-label="Quick filters">
      <li><a class="chip" href="/rodeos/?when=weekend">This weekend <span class="chip__n"><?= (int) $counts['weekend'] ?></span></a></li>
      <li><a class="chip" href="/rodeos/?when=month">This month <span class="chip__n"><?= (int) $counts['month'] ?></span></a></li>
      <li><a class="chip" href="/rodeos/?view=calendar">Calendar</a></li>
      <li><a class="chip" href="/rodeos/?view=map">Map</a></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <h2>Coming up in Texas</h2>
      <a class="link-more" href="/rodeos/">All <?= (int) $counts['upcoming'] ?> upcoming events →</a>
    </div>
    <?php if ($upcoming): ?>
      <div class="event-list">
        <?php foreach ($upcoming as $ev) { echo View::eventCard($ev); } ?>
      </div>
    <?php else: ?>
      <div class="empty">
        <p><strong>No upcoming events are listed right now.</strong> New dates are added every week from official organizer sources and reviewed submissions.</p>
        <p><a class="btn" href="/submit-event/">Submit a rodeo</a> <a class="btn btn--ghost" href="/past-events/">Browse past events</a></p>
      </div>
    <?php endif; ?>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <h2>Browse by region</h2>
    <ul class="region-grid">
      <?php foreach ($regions as $r): ?>
        <li><a class="region-tile region-tile--<?= e($r['slug']) ?>" href="/rodeos/region/<?= e($r['slug']) ?>/"><span><?= e($r['name']) ?></span></a></li>
      <?php endforeach; ?>
    </ul>
    <p class="fineprint">Regions are approximate and based on the venue's location.</p>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <h2>Know before you go</h2>
      <p>New to rodeo or planning a family trip? Our guides explain the events, scoring, and what to wear.</p>
      <ul class="article-list">
        <?php foreach ($articles as $a): ?>
          <li class="article-card">
            <?php if ($a['featured_image']): ?>
              <img src="<?= e($a['featured_image']) ?>" alt="<?= e($a['featured_alt']) ?>" width="<?= (int) ($a['featured_width'] ?: 1200) ?>" height="<?= (int) ($a['featured_height'] ?: 800) ?>" loading="lazy" decoding="async">
            <?php endif; ?>
            <div><h3><a href="/<?= e($a['slug']) ?>/"><?= e($a['title']) ?></a></h3><p><?= e(excerpt($a['excerpt'], 120)) ?></p></div>
          </li>
        <?php endforeach; ?>
      </ul>
      <p><a class="link-more" href="/blog/">All rodeo guides →</a></p>
    </div>
    <aside class="callout">
      <h2>Organizing a rodeo?</h2>
      <p>Send us your dates, venue and official links. Every submission is reviewed by a person before it is published.</p>
      <p><a class="btn btn--primary" href="/submit-event/">Submit your event</a></p>
      <p class="fineprint">Spotted a mistake on a listing? Use “Report a correction” on any event page.</p>
    </aside>
  </div>
</section>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
