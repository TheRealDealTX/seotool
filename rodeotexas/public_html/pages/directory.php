<?php
/**
 * The event directory: /rodeos/ (upcoming), /past-events/ and the
 * /rodeos/region|association|type|level/<slug>/ landing pages.
 * Views: list (paginated), calendar (month grid), map (Leaflet + OSM).
 */
defined('RT_APP') || exit;

use RT\Dates;
use RT\Db;
use RT\EventRepo;
use RT\Seo;
use RT\View;

$mode = $mode ?? 'upcoming';
$past = $mode === 'past';
$input = $_GET;
$landing = null;
if (!empty($preset)) {
    [$pk, $pv] = $preset;
    $input[$pk] = $pv;
    $landing = match ($pk) {
        'region' => Db::one('SELECT name FROM regions WHERE slug = ?', [$pv])['name'] ?? null,
        'association' => (($r = Db::one('SELECT abbr, name FROM associations WHERE slug = ?', [$pv])) ? $r['name'] . ' (' . $r['abbr'] . ')' : null),
        'type' => Db::one('SELECT name FROM event_types WHERE slug = ?', [$pv])['name'] ?? null,
        'level' => in_array($pv, levels(), true) ? level_label($pv) : null,
        default => null,
    };
    if ($landing === null) {
        rt_not_found();
    }
}
$f = EventRepo::filtersFrom($input);
if ($past) {
    $f['view'] = 'list';
}
$regions = EventRepo::regions();
$assocs = EventRepo::associations();
$types = EventRepo::types();

// ----- data for the chosen view
$result = ['rows' => [], 'total' => 0, 'pages' => 1, 'page' => 1, 'note' => null];
$calRows = [];
$ym = null;
if ($f['view'] === 'calendar') {
    $ym = $f['month'] ?? substr($f['from'] ?? Dates::today(), 0, 7);
    $calRows = EventRepo::month($f, $ym);
} elseif ($f['view'] === 'list') {
    $result = EventRepo::search($f, $past);
}

// ----- SEO
$base = $past ? '/past-events/' : (request_path());
$hasFilters = (bool) array_filter([$f['q'], $f['from'], $f['to'], $f['when'], $f['view'] !== 'list' ? 1 : null,
    $landing ? null : ($f['region'] ?: $f['association'] ?: $f['type'] ?: $f['level'])]);
if ($past) {
    $h1 = 'Past Texas rodeos';
    $title = 'Past Texas Rodeos & Results Archive';
    $desc = 'Archive of rodeos previously held in Texas, with dates and venues. Find the next edition of your favorite rodeo.';
} elseif ($landing) {
    $h1 = ($preset[0] === 'region' ? 'Rodeos in ' : '') . $landing . ($preset[0] === 'region' ? '' : ' rodeos in Texas');
    $title = $h1 . ' — Upcoming Dates';
    $desc = 'Upcoming ' . $landing . ($preset[0] === 'region' ? ' rodeos' : ' events') . ' in Texas with dates, venues, show times and official links.';
} else {
    $h1 = $f['when'] === 'weekend' ? 'Rodeos this weekend in Texas' : ($f['when'] === 'month' ? 'Rodeos this month in Texas' : 'Upcoming Texas rodeos');
    $title = $h1 === 'Upcoming Texas rodeos' ? 'Texas Rodeo Schedule — Upcoming Rodeos' : $h1;
    $desc = 'Search the Texas rodeo schedule by date, city, ZIP code, region, association and event type. List, calendar and map views.';
}
$page = [
    'title' => $title,
    'description' => $desc,
    'canonical' => $base . ($f['page'] > 1 && $f['view'] === 'list' && !$hasFilters ? '?page=' . $f['page'] : ''),
    // Filtered/variant URLs are useful for visitors but duplicate content for search engines.
    'robots' => $hasFilters ? 'noindex,follow' : 'index,follow',
    'jsonld' => [Seo::breadcrumbs(array_filter([['Home', '/'], [$past ? 'Past events' : 'Rodeos', $past ? '/past-events/' : '/rodeos/'], $landing ? [$landing, request_path()] : null]))],
    'body_class' => 'page-directory',
    'head_extra' => $f['view'] === 'map' ? '<link rel="preconnect" href="https://tile.openstreetmap.org" crossorigin>' : '',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';

$fq = View::filterQuery($f);
$viewUrl = static function (string $v) use ($fq, $base): string {
    $q = $fq;
    unset($q['view']);
    if ($v !== 'list') {
        $q['view'] = $v;
    }
    return $base . ($q ? '?' . http_build_query($q) : '');
};
$chip = static function (?string $when) use ($fq, $base): string {
    $q = $fq;
    unset($q['when'], $q['from'], $q['to']);
    if ($when) {
        $q['when'] = $when;
    }
    return $base . ($q ? '?' . http_build_query($q) : '');
};
?>
<div class="wrap directory">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">›</span> <?= $landing ? '<a href="/rodeos/">Rodeos</a> <span aria-hidden="true">›</span> ' . e($landing) : e($past ? 'Past events' : 'Rodeos') ?></nav>
  <h1><?= e($h1) ?></h1>

  <form class="filters" action="<?= e($base) ?>" method="get" role="search" data-autosubmit>
    <?php if ($f['view'] !== 'list'): ?><input type="hidden" name="view" value="<?= e($f['view']) ?>"><?php endif; ?>
    <div class="filters__search">
      <label for="f-q">Search</label>
      <input id="f-q" name="q" type="search" value="<?= e($f['q']) ?>" placeholder="Event, city, venue or ZIP" autocomplete="off">
    </div>
    <?php if (!$past): ?>
    <div class="filters__row">
      <div class="field"><label for="f-from">From</label><input id="f-from" type="date" name="from" value="<?= e($f['when'] ? '' : $f['from']) ?>"></div>
      <div class="field"><label for="f-to">To</label><input id="f-to" type="date" name="to" value="<?= e($f['when'] ? '' : $f['to']) ?>"></div>
      <?php if (!$landing || $preset[0] !== 'region'): ?>
      <div class="field"><label for="f-region">Region</label>
        <select id="f-region" name="region"><option value="">All Texas</option>
          <?php foreach ($regions as $r): ?><option value="<?= e($r['slug']) ?>"<?= $f['region'] === $r['slug'] ? ' selected' : '' ?>><?= e($r['name']) ?></option><?php endforeach; ?>
        </select></div>
      <?php endif; ?>
      <?php if (!$landing || $preset[0] !== 'association'): ?>
      <div class="field"><label for="f-assoc">Association</label>
        <select id="f-assoc" name="association"><option value="">Any</option>
          <?php foreach ($assocs as $a): ?><option value="<?= e($a['slug']) ?>"<?= $f['association'] === $a['slug'] ? ' selected' : '' ?>><?= e($a['abbr'] . ' — ' . $a['name']) ?></option><?php endforeach; ?>
        </select></div>
      <?php endif; ?>
      <?php if (!$landing || $preset[0] !== 'type'): ?>
      <div class="field"><label for="f-type">Event type</label>
        <select id="f-type" name="type"><option value="">Any</option>
          <?php foreach ($types as $t): ?><option value="<?= e($t['slug']) ?>"<?= $f['type'] === $t['slug'] ? ' selected' : '' ?>><?= e($t['name']) ?></option><?php endforeach; ?>
        </select></div>
      <?php endif; ?>
      <?php if (!$landing || $preset[0] !== 'level'): ?>
      <div class="field"><label for="f-level">Level</label>
        <select id="f-level" name="level"><option value="">Any</option>
          <?php foreach (levels() as $l): ?><option value="<?= e($l) ?>"<?= $f['level'] === $l ? ' selected' : '' ?>><?= e(level_label($l)) ?></option><?php endforeach; ?>
        </select></div>
      <?php endif; ?>
    </div>
    <?php endif; ?>
    <div class="filters__actions">
      <button class="btn btn--primary" type="submit">Show events</button>
      <a class="btn btn--ghost" href="<?= e($base) ?>">Reset</a>
    </div>
  </form>

  <?php if (!$past): ?>
  <div class="toolbar">
    <ul class="quick-chips" aria-label="Date shortcuts">
      <li><a class="chip<?= !$f['when'] && !$f['from'] && !$f['to'] ? ' is-active' : '' ?>" href="<?= e($chip(null)) ?>">All upcoming</a></li>
      <li><a class="chip<?= $f['when'] === 'weekend' ? ' is-active' : '' ?>" href="<?= e($chip('weekend')) ?>" <?= $f['when'] === 'weekend' ? 'aria-current="true"' : '' ?>>This weekend</a></li>
      <li><a class="chip<?= $f['when'] === 'month' ? ' is-active' : '' ?>" href="<?= e($chip('month')) ?>" <?= $f['when'] === 'month' ? 'aria-current="true"' : '' ?>>This month</a></li>
    </ul>
    <div class="view-tabs" role="tablist" aria-label="View">
      <?php foreach (['list' => 'List', 'calendar' => 'Calendar', 'map' => 'Map'] as $v => $label): ?>
        <a role="tab" aria-selected="<?= $f['view'] === $v ? 'true' : 'false' ?>" class="view-tab<?= $f['view'] === $v ? ' is-active' : '' ?>" href="<?= e($viewUrl($v)) ?>"><?= e($label) ?></a>
      <?php endforeach; ?>
    </div>
  </div>
  <?php endif; ?>

  <?php if ($f['view'] === 'list'): ?>
    <p class="result-count" role="status"><?= (int) $result['total'] ?> event<?= $result['total'] === 1 ? '' : 's' ?>
      <?= $f['from'] || $f['to'] ? ' · ' . e(Dates::range($f['from'] ?? Dates::today(), $f['to'] ?? ($f['from'] ?? Dates::today()))) : '' ?></p>
    <?php if ($result['note']): ?><p class="notice"><?= e($result['note']) ?></p><?php endif; ?>
    <?php if ($result['rows']): ?>
      <div class="event-list">
        <?php
        $lastMonth = '';
        foreach ($result['rows'] as $ev) {
            $mon = date('F Y', strtotime($ev['start_date']));
            if ($mon !== $lastMonth && !$past) {
                echo '<h2 class="month-divider">' . e($mon) . '</h2>';
                $lastMonth = $mon;
            }
            echo View::eventCard($ev);
        }
        ?>
      </div>
      <?= View::pagination($result['page'], $result['pages'], $f, $base) ?>
    <?php else: ?>
      <div class="empty">
        <p><strong>No events match these filters.</strong></p>
        <p>Try a wider date range, another region, or <a href="<?= e($base) ?>">clear all filters</a>. Know of a rodeo we're missing? <a href="/submit-event/">Submit it</a>.</p>
      </div>
    <?php endif; ?>

  <?php elseif ($f['view'] === 'calendar'):
    $first = new DateTimeImmutable($ym . '-01');
    $prev = $first->modify('-1 month')->format('Y-m');
    $next = $first->modify('+1 month')->format('Y-m');
    $byDay = [];
    foreach ($calRows as $ev) {
        $d = max($ev['start_date'], $first->format('Y-m-01'));
        $end = min($ev['end_date'], $first->format('Y-m-t'));
        while ($d <= $end) {
            $byDay[$d][] = $ev;
            $d = date('Y-m-d', strtotime($d . ' +1 day'));
        }
    }
    $calQ = static function (string $m) use ($fq, $base): string {
        $q = $fq;
        unset($q['when'], $q['from'], $q['to']);
        $q['view'] = 'calendar';
        $q['month'] = $m;
        return $base . '?' . http_build_query($q);
    };
    $today = Dates::today();
  ?>
    <div class="cal-head">
      <a class="btn btn--ghost" href="<?= e($calQ($prev)) ?>" aria-label="Previous month">‹ <?= e(date('M', strtotime($prev . '-01'))) ?></a>
      <h2><?= e($first->format('F Y')) ?></h2>
      <a class="btn btn--ghost" href="<?= e($calQ($next)) ?>" aria-label="Next month"><?= e(date('M', strtotime($next . '-01'))) ?> ›</a>
    </div>
    <p class="result-count" role="status"><?= count($calRows) ?> event<?= count($calRows) === 1 ? '' : 's' ?> in <?= e($first->format('F Y')) ?></p>
    <div class="calendar" role="table" aria-label="<?= e($first->format('F Y')) ?> events">
      <div class="calendar__row calendar__dow" role="row">
        <?php foreach (['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as $dow): ?><div role="columnheader"><?= $dow ?></div><?php endforeach; ?>
      </div>
      <?php
      $offset = (int) $first->format('w');
      $days = (int) $first->format('t');
      $cells = (int) ceil(($offset + $days) / 7) * 7;
      for ($i = 0; $i < $cells; $i++):
          if ($i % 7 === 0) { echo '<div class="calendar__row" role="row">'; }
          $dayNum = $i - $offset + 1;
          if ($dayNum < 1 || $dayNum > $days) {
              echo '<div class="calendar__cell is-out" role="cell"></div>';
          } else {
              $date = $first->format('Y-m-') . str_pad((string) $dayNum, 2, '0', STR_PAD_LEFT);
              $evs = $byDay[$date] ?? [];
              echo '<div class="calendar__cell' . ($evs ? ' has-events' : '') . ($date === $today ? ' is-today' : '') . '" role="cell">';
              echo '<span class="calendar__date"><span class="visually-hidden">' . e(date('l, F j', strtotime($date))) . '</span><span aria-hidden="true">' . $dayNum . '</span></span>';
              if ($evs) {
                  echo '<ul>';
                  foreach (array_slice($evs, 0, 4) as $ev) {
                      $s = Dates::status($ev)['key'];
                      echo '<li class="cal-ev cal-ev--' . e($s) . '"><a href="/rodeos/' . e($ev['slug']) . '/" title="' . e($ev['title'] . ' — ' . View::place($ev)) . '">' . e($ev['title']) . '</a></li>';
                  }
                  if (count($evs) > 4) {
                      echo '<li class="cal-more">+' . (count($evs) - 4) . ' more</li>';
                  }
                  echo '</ul>';
              }
              echo '</div>';
          }
          if ($i % 7 === 6) { echo '</div>'; }
      endfor; ?>
    </div>

  <?php else: /* map */
    $apiQ = $fq;
    unset($apiQ['view']);
  ?>
    <div class="map-wrap">
      <div id="event-map" class="event-map" data-map-endpoint="/api/events.json<?= e($apiQ ? '?' . http_build_query($apiQ) : '') ?>"
           data-tiles="<?= e((string) cfg('map.tile_url')) ?>" data-attribution="<?= e((string) cfg('map.attribution')) ?>"
           role="region" aria-label="Map of events">
        <p class="map-fallback">Loading map… If it does not appear, <a href="<?= e($viewUrl('list')) ?>">use the list view</a>.</p>
      </div>
      <p class="fineprint">Pins show the venue; a hollow pin means only the city is known. Map © OpenStreetMap contributors.</p>
      <div id="map-list" class="event-list event-list--compact" aria-live="polite"></div>
    </div>
  <?php endif; ?>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
