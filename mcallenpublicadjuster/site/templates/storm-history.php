<?php
/** Storm History — filterable NOAA NCEI record for Hidalgo County. */
require_once MPA_ROOT . '/includes/storms.php';
$h = storm_history();
$s = storm_stats();
$places = read_json_file(data_path('places.json'), ['places' => []]);
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
$sig = array_values(array_filter($h['events'] ?? [], fn($e) => in_array($e['fam'], ['hail', 'wind', 'tornado', 'tropical'], true)));
?>
<section class="section section-navy section-tight">
  <div class="container">
    <div class="stats">
      <div class="stat reveal"><span class="stat-num" data-count="<?= (int) $s['hail'] ?>">0</span><span class="stat-label">hail reports since <?= (int) ($s['hail_first'] ?? $s['first_year']) ?></span></div>
      <div class="stat reveal" style="--d:80ms"><span class="stat-num" data-count="<?= (int) $s['hail_175'] ?>">0</span><span class="stat-label">reports of golf-ball hail (1.75&quot;) or larger</span></div>
      <div class="stat reveal" style="--d:160ms"><span class="stat-num" data-count="<?= (int) $s['wind'] ?>">0</span><span class="stat-label">thunderstorm wind reports</span></div>
      <div class="stat reveal" style="--d:240ms"><span class="stat-num" data-count="<?= (int) $s['tornado'] ?>">0</span><span class="stat-label">tornado reports</span></div>
    </div>
    <p class="small" style="margin-top:14px;color:#9fb2c4">Counts of individual reports in the NOAA NCEI Storm Events Database for Hidalgo County, Texas (<?= (int) $s['first_year'] ?>–<?= (int) $s['last_year'] ?>). One storm can produce many reports. Data updated <?= !empty($h['updated']) ? e(date('M j, Y', strtotime($h['updated']))) : '—' ?>.</p>
  </div>
</section>
<section class="section" aria-labelledby="tool-h">
  <div class="container" data-storm-app="history" data-api="/api/storms.php?set=history">
    <h2 id="tool-h">Search the storm record</h2>
    <form class="filters" data-filters onsubmit="return false">
      <div class="field"><label for="f-type">Event type</label>
        <select id="f-type" name="fam"><option value="">All types</option><option value="hail">Hail</option><option value="wind">Wind</option><option value="tornado">Tornado &amp; funnel cloud</option><option value="tropical">Tropical storm / hurricane</option><option value="flood">Flood &amp; heavy rain</option><option value="winter">Freeze &amp; winter</option></select></div>
      <div class="field"><label for="f-from">From date</label><input id="f-from" name="from" type="date" min="1950-01-01"></div>
      <div class="field"><label for="f-to">To date</label><input id="f-to" name="to" type="date"></div>
      <div class="field"><label for="f-loc">Location contains</label><input id="f-loc" name="loc" type="text" list="loc-list" placeholder="e.g. McAllen, Mission"><datalist id="loc-list"><?php foreach ($places['places'] as $p): ?><option value="<?= e($p['name']) ?>"><?php endforeach; ?></datalist></div>
      <div class="field"><label for="f-wind">Min. wind (mph)</label><input id="f-wind" name="wind" type="number" min="0" max="200" step="5" inputmode="numeric" placeholder="e.g. 60"></div>
      <div class="field"><label for="f-hail">Min. hail (inches)</label><select id="f-hail" name="hail"><option value="">Any</option><option value="0.75">0.75&quot; penny</option><option value="1">1.00&quot; quarter</option><option value="1.75">1.75&quot; golf ball</option><option value="2.75">2.75&quot; baseball</option></select></div>
      <div class="field"><label for="f-q">Keyword</label><input id="f-q" name="q" type="search" placeholder="e.g. roof, shingles"></div>
      <div class="filters-actions"><button class="btn btn-ghost btn-sm" type="reset">Reset</button></div>
    </form>
    <div class="results-bar"><span data-count-label aria-live="polite">Loading storm records…</span><span>Source: <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA NCEI Storm Events Database</a></span></div>
    <h3>Timeline (events per year)</h3>
    <div class="storm-chart" data-chart role="group" aria-label="Number of matching events per year"></div>
    <div class="storm-chart-labels" data-chart-labels></div>
    <p class="chart-tip" data-chart-tip aria-live="polite"></p>
    <h3>Map of reports with coordinates</h3>
    <div class="storm-map" data-map aria-label="Map of storm report locations"></div>
    <p class="small muted">Map shows reports that include latitude/longitude (most county-level reports since the mid-1990s). Zone-wide events such as tropical storms and freezes have no single point. Map data &copy; OpenStreetMap contributors.</p>
    <h3>Matching events</h3>
    <div class="table-wrap"><table class="storm-table" data-nowrap><thead><tr><th scope="col">Date</th><th scope="col">Type</th><th scope="col">Location</th><th scope="col">Magnitude</th><th scope="col">Summary</th><th scope="col">Source</th></tr></thead>
      <tbody data-rows>
        <?php foreach (array_slice($sig, 0, 40) as $e): ?>
        <tr><td><?= e(date('M j, Y', strtotime($e['date']))) ?></td><td class="ev-type"><?= e($e['type']) ?></td><td><?= e($e['loc']) ?></td><td><?= e(storm_severity($e) ?: '—') ?></td><td class="ev-narr"><?= e(mb_substr($e['text'], 0, 220)) ?><?= mb_strlen($e['text']) > 220 ? '…' : '' ?></td><td><a href="<?= e($e['url']) ?>" target="_blank" rel="noopener">NCEI record</a></td></tr>
        <?php endforeach; ?>
      </tbody></table></div>
    <div class="pager" data-pager></div>
    <p class="disclaimer-box"><strong>Important:</strong> These are official weather reports, not damage determinations. A nearby report does not prove that hail or wind damaged a specific property, and the absence of a report does not prove a storm did not affect it. Reports reflect where observers were. Use this record as one piece of supporting documentation alongside a physical inspection. Magnitudes are as recorded by NCEI (wind speeds converted from knots to mph).</p>
  </div>
</section>
<section class="section section-alt section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php component('cta-storm'); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
