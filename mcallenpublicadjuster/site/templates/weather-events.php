<?php
/** Automatically updated weather events (NWS Local Storm Reports). */
require_once MPA_ROOT . '/includes/storms.php';
$data = weather_events_data();
$events = $data['events'] ?? [];
$status = $data['status'] ?? [];
$al = weather_alerts();
$recentCut = date('Y-m-d', strtotime('-12 months'));
$recent = array_values(array_filter($events, fn($e) => $e['date'] >= $recentCut));
$older = array_values(array_filter($events, fn($e) => $e['date'] < $recentCut));
$fams = [];
foreach ($events as $e) { $fams[$e['fam']] = ($fams[$e['fam']] ?? 0) + 1; }
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-tight">
  <div class="container">
    <div class="notice notice-info">
      <p class="mb-0"><strong><?= count($events) ?> storm report<?= count($events) === 1 ? '' : 's' ?></strong> for Hidalgo County on file<?= $data['updated'] ?? null ? ' &middot; Last updated ' . e(date('M j, Y g:i A T', strtotime($data['updated']))) : '' ?>.
      Sources: National Weather Service Brownsville/Rio Grande Valley Local Storm Reports (via <a href="https://api.weather.gov/" target="_blank" rel="noopener">api.weather.gov</a> and the <a href="https://mesonet.agron.iastate.edu/lsr/" target="_blank" rel="noopener">Iowa Environmental Mesonet LSR archive</a>).
      <?php if (isset($status['ok']) && !$status['ok']): ?><br><strong>The most recent automatic update could not reach the data sources; the reports below are from the last successful update.</strong><?php endif; ?></p>
    </div>
    <h2>Active alerts</h2>
    <?php component('weather-alerts', ['al' => $al]); ?>
  </div>
</section>
<section class="section section-alt" aria-labelledby="recent-h">
  <div class="container">
    <div class="results-bar">
      <h2 id="recent-h" class="mb-0">Reports from the last 12 months</h2>
      <div class="chip-list" role="group" aria-label="Filter by event type" data-event-filter>
        <button class="chip" type="button" data-fam="all" aria-pressed="true">All</button>
        <?php foreach ($fams as $f => $n): ?><button class="chip" type="button" data-fam="<?= e($f) ?>" aria-pressed="false"><?= e(storm_family_label($f)) ?> (<?= $n ?>)</button><?php endforeach; ?>
      </div>
    </div>
    <?php if ($recent): ?>
    <div class="event-list" data-event-list>
      <?php foreach ($recent as $ev) component('event-card', ['ev' => $ev]); ?>
    </div>
    <?php else: ?>
    <div class="wx-fallback"><p class="mb-0">No hail, wind, tornado, or flood reports have been logged for Hidalgo County in the last 12 months. New reports are added automatically when the National Weather Service issues them.</p></div>
    <?php endif; ?>
    <?php component('cta-storm'); ?>
    <?php if ($older): ?>
    <details class="accordion-item" style="margin-top:24px">
      <summary>Earlier reports (<?= count($older) ?>)<span class="accordion-icon" aria-hidden="true"></span></summary>
      <div class="accordion-body"><div class="event-list" data-event-list><?php foreach ($older as $ev) component('event-card', ['ev' => $ev]); ?></div></div>
    </details>
    <?php endif; ?>
    <p class="disclaimer-box"><strong>Preliminary data.</strong> Local Storm Reports are preliminary reports from spotters, emergency managers, the public, and instruments. Sizes, speeds, times, and locations can be estimated and may later be revised. The verified record is published later in the <a href="/storm-history/">NOAA Storm Events Database</a>. A nearby weather report does not prove that damage occurred at a specific property; physical inspection is still required.</p>
  </div>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
<script>
(function(){var g=document.querySelector('[data-event-filter]');if(!g)return;g.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;g.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});var f=b.getAttribute('data-fam');document.querySelectorAll('[data-event-list] .event-card').forEach(function(c){c.hidden=!(f==='all'||c.classList.contains('t-'+f))})})})();
</script>
