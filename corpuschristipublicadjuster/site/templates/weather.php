<?php
/** Live Corpus Christi weather app: conditions, hourly, 7-day, radar, tides, tropics, alerts. */
require_once CCPA_ROOT . '/includes/weather.php';
$cur = weather_current();
$fc = weather_forecast();
$al = weather_alerts();
$hr = weather_hourly();
$station = preg_replace('/\D/', '', (string) ($_GET['tide'] ?? '8775296'));
$tides = tides_data($station);
$tropics = tropics_data();
$sun = sun_times();
$season = hurricane_season_status();
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page + ['hero_wave_fill' => '#ffffff']]);
$days = !empty($fc['data']) ? forecast_days($fc['data']) : [];
$hours = $hr['data']['periods'] ?? [];
?>
<section class="section section-tight" aria-labelledby="alerts-h">
  <div class="container">
    <div class="results-bar"><h2 id="alerts-h" class="mb-0">Severe weather alerts</h2><span class="badge badge-live">Live from NWS</span></div>
    <?php component('weather-alerts', ['al' => $al]); ?>
  </div>
</section>

<section class="section section-tight section-alt" aria-labelledby="now-h">
  <div class="container wx-app">
    <h2 id="now-h" class="sr-only">Current conditions and hourly forecast</h2>
    <div class="wx-app-top">
      <?php component('weather-now', ['cur' => $cur]); ?>
      <div class="wx-panel">
        <div class="wx-panel-head">
          <h3><?= icon('clock', 'icon') ?> Next 48 hours</h3>
          <div class="wx-chip-row">
            <?php if ($sun['rise']): ?><span class="wx-chip">Sunrise <?= e(date('g:i A', $sun['rise'])) ?></span><?php endif; ?>
            <?php if ($sun['set']): ?><span class="wx-chip hot">Sunset <?= e(date('g:i A', $sun['set'])) ?></span><?php endif; ?>
          </div>
        </div>
        <?php if ($hours): ?>
        <?= svg_line_chart(array_map(fn($h) => [strtotime($h['start']), (float) $h['temp']], $hours), [
            'class' => 'wx-temp-chart', 'grad' => 'wxGrad', 'h' => 150, 'unit' => '°', 'label' => 'Hourly temperature forecast for the next 48 hours',
            'labels' => array_map(fn($h) => [strtotime($h['start']), date('ga', strtotime($h['start']))], array_values(array_filter($hours, fn($h, $i) => $i % 6 === 0, ARRAY_FILTER_USE_BOTH))),
        ]) ?>
        <div class="wx-hourly" tabindex="0" aria-label="Hourly forecast, scrollable">
          <?php foreach (array_slice($hours, 0, 24) as $h): ?>
          <div class="wx-hour">
            <small><?= e(date('D ga', strtotime($h['start']))) ?></small>
            <?= wx_svg(wx_icon_key($h['icon'], $h['isDay']), $h['short']) ?>
            <b><?= (int) $h['temp'] ?>&deg;</b>
            <span class="pop"><?= $h['pop'] !== null ? (int) $h['pop'] . '% rain' : '&nbsp;' ?></span>
            <small><?= e($h['wind']) ?></small>
          </div>
          <?php endforeach; ?>
        </div>
        <p class="small muted mb-0">NWS hourly forecast for Corpus Christi<?= !empty($hr['data']['updated']) ? ', updated ' . e(date('M j, g:i A T', strtotime($hr['data']['updated']))) : '' ?>.</p>
        <?php else: ?>
        <p class="wx-fallback mb-0">The hourly forecast is temporarily unavailable. See <a href="https://forecast.weather.gov/MapClick.php?lat=27.8006&amp;lon=-97.3964&amp;FcstType=graphical" target="_blank" rel="noopener">weather.gov</a>.</p>
        <?php endif; ?>
      </div>
    </div>
    <div class="wx-panel">
      <h3><?= icon('calendar', 'icon') ?> 7-day forecast</h3>
      <?php component('weather-forecast', ['fc' => $fc]); ?>
    </div>
  </div>
</section>

<section class="section section-tight" aria-labelledby="radar-h">
  <div class="container">
    <div class="wx-panel">
      <div class="wx-panel-head">
        <h2 id="radar-h" class="h3" style="font-size:1.25rem;margin:0;display:flex;gap:10px;align-items:center"><?= icon('storm', 'icon') ?> Live radar loop</h2>
        <span class="badge badge-live">Last ~50 minutes</span>
      </div>
      <div class="wx-radar" id="wx-radar" data-lat="<?= e((string) cfg('lat')) ?>" data-lon="<?= e((string) cfg('lon')) ?>"><noscript><p style="color:#fff;padding:20px">The radar map needs JavaScript. View the official loop at <a href="https://radar.weather.gov/station/KCRP/standard" style="color:#ffbc7d">radar.weather.gov</a>.</p></noscript></div>
      <div class="wx-radar-bar">
        <button class="wx-play" type="button" data-radar-play aria-label="Pause radar animation"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg></button>
        <input type="range" min="0" max="10" value="10" step="1" data-radar-slider aria-label="Radar frame">
        <span class="wx-radar-time" data-radar-time>Loading radar&hellip;</span>
      </div>
      <p class="small muted mb-0" style="margin-top:10px">NEXRAD base reflectivity composite via the <a href="https://mesonet.agron.iastate.edu/" target="_blank" rel="noopener">Iowa Environmental Mesonet</a>, updated every 5 minutes. Map &copy; OpenStreetMap contributors. Official radar: <a href="https://radar.weather.gov/station/KCRP/standard" target="_blank" rel="noopener">NWS Corpus Christi (KCRP)</a>.</p>
    </div>
  </div>
</section>

<section class="section section-tight section-alt" aria-labelledby="coast-h">
  <div class="container">
    <h2 id="coast-h" class="sr-only">Tides, tropics, and hurricane season</h2>
    <div class="wx-grid-3">
      <div class="wx-panel" id="tides">
        <h3><?= icon('droplets', 'icon') ?> Tides &amp; water level</h3>
        <form method="get" action="/weather/#tides" class="wx-chip-row" style="margin-bottom:10px">
          <label class="sr-only" for="tide-station">Tide station</label>
          <select id="tide-station" name="tide" onchange="this.form.submit()" style="padding:8px 10px;border-radius:10px;border:1.5px solid var(--gray-2);max-width:100%">
            <?php foreach (tide_stations() as $id => $label): ?><option value="<?= e($id) ?>"<?= ($tides['data']['station'] ?? '8775296') === $id ? ' selected' : '' ?>><?= e($label) ?></option><?php endforeach; ?>
          </select>
          <noscript><button class="btn btn-sm btn-ghost" type="submit">Show</button></noscript>
        </form>
        <?php if (!empty($tides['data'])):
            $td = $tides['data'];
            $lastObs = $td['observed'] ? end($td['observed']) : null;
            $predAtObs = null;
            if ($lastObs) { foreach ($td['predicted'] as $p) { if ($p[0] <= $lastObs[0]) { $predAtObs = $p[1]; } } }
            $diff = ($lastObs && $predAtObs !== null) ? $lastObs[1] - $predAtObs : null;
        ?>
        <?= svg_line_chart($td['predicted'], ['extra' => [$td['observed']], 'now' => true, 'unit' => ' ft', 'label' => 'Predicted tide and observed water level', 'color' => '#2b8bb8',
            'labels' => array_map(fn($t) => [$t, date('D ga', $t)], [strtotime('today'), strtotime('tomorrow'), strtotime('+2 days 00:00')])]) ?>
        <p class="small mb-0"><span style="color:#2b8bb8;font-weight:700">&#9644; Predicted</span> &nbsp; <span style="color:#ff8a5b;font-weight:700">&#9644; Observed</span><?php if ($diff !== null): ?> &middot; Water is running <strong><?= e(number_format(abs($diff), 1)) ?> ft <?= $diff >= 0 ? 'above' : 'below' ?></strong> the prediction<?php endif; ?></p>
        <ul class="tide-list">
          <?php foreach (array_slice(array_values(array_filter($td['hilo'], fn($x) => $x['t'] > time() - 3600)), 0, 6) as $x): ?>
          <li><span><?= $x['type'] === 'H' ? 'High' : 'Low' ?> &middot; <?= e(date('D g:i A', $x['t'])) ?></span><b><?= e(number_format($x['v'], 1)) ?> ft</b></li>
          <?php endforeach; ?>
        </ul>
        <p class="small muted mb-0" style="margin-top:10px">Feet above MLLW. Source: <a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=<?= e($td['station']) ?>" target="_blank" rel="noopener">NOAA Tides &amp; Currents</a>. Observed data are preliminary.</p>
        <?php else: ?>
        <p class="wx-fallback mb-0">Tide data is temporarily unavailable. See <a href="https://tidesandcurrents.noaa.gov/" target="_blank" rel="noopener">NOAA Tides &amp; Currents</a>.</p>
        <?php endif; ?>
      </div>

      <div class="wx-panel">
        <h3><?= icon('hurricane', 'icon') ?> Tropics watch</h3>
        <?php $storms = $tropics['data']['storms'] ?? null; ?>
        <?php if ($storms === null): ?>
        <p class="wx-fallback mb-0">The National Hurricane Center feed is temporarily unavailable. Check <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">nhc.noaa.gov</a>.</p>
        <?php elseif (!$storms): ?>
        <div class="tropics-quiet"><?= icon('check', 'icon') ?><span>No active tropical cyclones right now in the Atlantic or Eastern Pacific.</span></div>
        <?php else: ?>
        <ul class="tropics-list">
          <?php foreach (array_slice($storms, 0, 4) as $st): ?>
          <li class="tropics-item">
            <span class="hurr"><?= icon('hurricane', 'icon') ?></span>
            <div><strong><?= e($st['class'] . ' ' . $st['name']) ?></strong>
            <span><?= e($st['basin']) ?> &middot; <?= $st['wind_mph'] ? e($st['wind_mph'] . ' mph winds') : '' ?><?= $st['movement'] ? ' &middot; moving ' . e($st['movement']) : '' ?><br>About <?= e(number_format($st['miles'])) ?> miles from Corpus Christi &middot; <a href="<?= e($st['link']) ?>" target="_blank" rel="noopener">NHC advisory</a></span></div>
          </li>
          <?php endforeach; ?>
        </ul>
        <?php endif; ?>
        <p class="small muted mb-0" style="margin-top:12px">Source: <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">National Hurricane Center</a>. Distance is straight-line from downtown Corpus Christi, not a forecast.</p>
      </div>

      <div class="wx-panel">
        <h3><?= icon('shield', 'icon') ?> Hurricane season</h3>
        <p class="calc-big" style="background:linear-gradient(100deg,#355a91,#ff8a5b);-webkit-background-clip:text;background-clip:text;margin:0"><?= (int) $season['days'] ?></p>
        <p class="mb-0" style="font-weight:600;color:var(--navy)"><?= e($season['label']) ?></p>
        <div class="progress" style="margin:14px 0 6px"><span style="width:<?= $season['active'] ? (int) round(100 - $season['days'] / 183 * 100) : 0 ?>%"></span></div>
        <p class="small muted">The Atlantic hurricane season runs June 1 through November 30.</p>
        <ul class="sidebar-links">
          <li><a href="/hurricane-season-guide/"><?= icon('clipboard', 'icon icon-sm') ?> Hurricane season guide</a></li>
          <li><a href="/hurricane-deductible-calculator/"><?= icon('calc', 'icon icon-sm') ?> Hurricane deductible calculator</a></li>
          <li><a href="/services/twia-windstorm-claims/"><?= icon('shield', 'icon icon-sm') ?> TWIA windstorm claims</a></li>
          <li><a href="/storm-lookup/"><?= icon('search', 'icon icon-sm') ?> Storm event lookup</a></li>
        </ul>
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
    <aside class="sidebar"><?php include CCPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
