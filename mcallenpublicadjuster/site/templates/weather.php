<?php
/** Live McAllen weather page. */
require_once MPA_ROOT . '/includes/weather.php';
$cur = weather_current();
$fc = weather_forecast();
$al = weather_alerts();
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
$days = !empty($fc['data']) ? forecast_days($fc['data']) : [];
?>
<section class="section section-tight" aria-labelledby="alerts-h">
  <div class="container">
    <div class="results-bar"><h2 id="alerts-h" class="mb-0">Severe weather alerts</h2><span class="badge badge-live">Live from NWS</span></div>
    <?php component('weather-alerts', ['al' => $al]); ?>
  </div>
</section>
<section class="section section-tight section-alt" aria-labelledby="now-h">
  <div class="container">
    <h2 id="now-h" class="sr-only">Current conditions and 7-day forecast</h2>
    <div class="wx-grid">
      <?php component('weather-now', ['cur' => $cur]); ?>
      <div>
        <h3>7-day forecast</h3>
        <?php component('weather-forecast', ['fc' => $fc]); ?>
      </div>
    </div>
  </div>
</section>
<?php if ($days): ?>
<section class="section section-tight" aria-labelledby="detail-h">
  <div class="container narrow">
    <h2 id="detail-h">Detailed forecast</h2>
    <div class="accordion">
      <?php foreach ($days as $i => $d): ?>
      <details class="accordion-item"<?= $i === 0 ? ' open' : '' ?>>
        <summary><?= e(date('l, F j', strtotime($d['date']))) ?> &mdash; <?= e($d['short']) ?><span class="accordion-icon" aria-hidden="true"></span></summary>
        <div class="accordion-body">
          <?php foreach ($d['detailed'] as $line): ?><p><?= e($line) ?></p><?php endforeach; ?>
          <p class="small muted">High <?= $d['hi'] !== null ? (int) $d['hi'] . '&deg;F' : '—' ?> &middot; Low <?= $d['lo'] !== null ? (int) $d['lo'] . '&deg;F' : '—' ?> &middot; Chance of precipitation <?= (int) $d['pop'] ?>%<?= $d['qpf'] !== null ? ' &middot; Forecast rainfall ' . e(number_format((float) $d['qpf'], 2)) . ' in' : '' ?></p>
        </div>
      </details>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php component('cta-storm'); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
