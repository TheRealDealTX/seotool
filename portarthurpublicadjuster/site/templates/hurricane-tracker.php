<?php
/** Live hurricane tracker: NHC active storms + NWS alerts for Port Arthur + season status. */
require_once MPA_ROOT . '/includes/tropics.php';
$tr = tropics_current();
$al = weather_alerts();
$storms = $tr['data'] ?? null;
$atl = $storms === null ? [] : array_values(array_filter($storms, fn($s) => $s['basin'] === 'al'));
$other = $storms === null ? [] : array_values(array_filter($storms, fn($s) => $s['basin'] !== 'al'));
$season = hurricane_season();
$tropicalAlerts = array_values(array_filter($al['data'] ?? [], fn($a) => preg_match('/hurricane|tropical|storm surge/i', $a['event'])));
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-tight" aria-labelledby="status-h">
  <div class="container">
    <div class="results-bar"><h2 id="status-h" class="mb-0">Tropical status for Port Arthur</h2><span class="badge badge-live">Live from NHC &amp; NWS</span></div>
    <div class="tropics-status">
      <div class="tropics-card glass-card reveal">
        <span class="tropics-card-label">Hurricane season <?= (int) $season['year'] ?></span>
        <?php if ($season['in']): ?>
        <strong class="tropics-card-big"><?= (int) $season['days_left'] ?> days left</strong>
        <span class="season-meter" role="img" aria-label="Season <?= (int) $season['pct'] ?>% complete"><span style="width:<?= (int) $season['pct'] ?>%"></span></span>
        <span class="small">June 1 &ndash; November 30 &middot; peak mid-August through September</span>
        <?php else: ?>
        <strong class="tropics-card-big"><?= (int) $season['days'] ?> days</strong>
        <span class="small">until the Atlantic season opens June 1, <?= (int) $season['year'] ?>. Now is the time to review your policies.</span>
        <?php endif; ?>
      </div>
      <div class="tropics-card glass-card reveal" style="--d:80ms">
        <span class="tropics-card-label">Active Atlantic systems</span>
        <strong class="tropics-card-big"><?= $storms === null ? '&mdash;' : count($atl) ?></strong>
        <span class="small"><?= $storms === null ? 'NHC feed unavailable right now' : ($atl ? 'Closest: ' . e($atl[0]['label'] . ' ' . $atl[0]['name']) . ', ' . number_format($atl[0]['miles']) . ' mi ' . e($atl[0]['bearing']) : 'No named or numbered Atlantic systems') ?></span>
      </div>
      <div class="tropics-card glass-card reveal" style="--d:160ms">
        <span class="tropics-card-label">Tropical alerts for Port Arthur</span>
        <strong class="tropics-card-big<?= $tropicalAlerts ? ' is-alert' : '' ?>"><?= $al === null ? '&mdash;' : count($tropicalAlerts) ?></strong>
        <span class="small"><?= $tropicalAlerts ? e(implode(', ', array_unique(array_column($tropicalAlerts, 'event')))) : 'No hurricane, tropical storm, or surge watches/warnings' ?></span>
      </div>
    </div>
    <?php if ($tropicalAlerts): ?><div style="margin-top:20px"><?php component('weather-alerts', ['al' => ['data' => $tropicalAlerts, 'fetched' => $al['fetched']]]); ?></div><?php endif; ?>
  </div>
</section>

<section class="section section-tight section-alt" aria-labelledby="map-h">
  <div class="container">
    <div class="results-bar"><h2 id="map-h" class="mb-0">Storm map</h2><?php if ($tr): ?><span class="small muted">Updated <?= e(time_ago((int) $tr['fetched'])) ?><?= !empty($tr['stale']) ? ' (cached copy)' : '' ?></span><?php endif; ?></div>
    <div class="tropics-map-wrap" data-tropics-app data-lat="<?= e((string) cfg('lat')) ?>" data-lon="<?= e((string) cfg('lon')) ?>">
      <script type="application/json" data-tropics><?= json_encode($storms ?? [], JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) ?></script>
      <div class="storm-map tropics-map" data-map role="region" aria-label="Map of active tropical systems and Port Arthur"></div>
      <p class="small muted" style="margin-top:10px">Rings show 200, 400, and 800 miles from Port Arthur. Positions are the latest NHC advisory center points, not forecast tracks&mdash;always use the official <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">NHC cone graphics</a> for decisions.</p>
    </div>
  </div>
</section>

<section class="section section-tight" aria-labelledby="active-h">
  <div class="container">
    <h2 id="active-h">Active tropical cyclones</h2>
    <?php if ($storms === null): ?>
    <div class="wx-fallback"><p class="mb-0"><strong>The National Hurricane Center feed did not respond.</strong> Check <a href="https://www.nhc.noaa.gov/" target="_blank" rel="noopener">nhc.noaa.gov</a> directly for the latest advisories.</p></div>
    <?php elseif (!$storms): ?>
    <div class="wx-none"><?= icon('shield', 'icon') ?> <span><strong>No active tropical cyclones</strong> in the Atlantic, Eastern Pacific, or Central Pacific right now. <span class="small">Checked <?= e(time_ago((int) $tr['fetched'])) ?>.</span></span></div>
    <?php else: ?>
    <div class="storm-cards">
      <?php foreach (array_merge($atl, $other) as $i => $s): ?>
      <article class="storm-card reveal<?= $s['basin'] === 'al' ? ' is-atlantic' : '' ?>" style="--d:<?= ($i % 3) * 80 ?>ms">
        <header>
          <span class="storm-card-icon"><?= icon('hurricane', 'icon') ?></span>
          <div><p class="eyebrow mb-0"><?= e($s['basin'] === 'al' ? 'Atlantic' : ($s['basin'] === 'ep' ? 'Eastern Pacific' : 'Central Pacific')) ?></p>
          <h3 class="mb-0"><?= e($s['label'] . ' ' . $s['name']) ?><?= $s['category'] ? ' <span class="badge">Cat ' . (int) $s['category'] . '</span>' : '' ?></h3></div>
        </header>
        <dl class="storm-facts">
          <div><dt>Max winds</dt><dd><?= (int) $s['wind_mph'] ?> mph</dd></div>
          <div><dt>Pressure</dt><dd><?= $s['pressure'] ? (int) $s['pressure'] . ' mb' : '&mdash;' ?></dd></div>
          <div><dt>Position</dt><dd><?= e(number_format(abs($s['lat']), 1) . '°' . ($s['lat'] >= 0 ? 'N' : 'S') . ' ' . number_format(abs($s['lon']), 1) . '°' . ($s['lon'] < 0 ? 'W' : 'E')) ?></dd></div>
          <div><dt>Movement</dt><dd><?= $s['move_mph'] ? e(deg_to_compass($s['move_dir'])) . ' at ' . (int) $s['move_mph'] . ' mph' : 'Stationary' ?></dd></div>
          <div><dt>From Port Arthur</dt><dd><?= number_format($s['miles']) ?> mi <?= e($s['bearing']) ?></dd></div>
          <div><dt>Advisory</dt><dd>#<?= e($s['adv_num']) ?> &middot; <?= e(date('M j, g:i A T', strtotime($s['updated']))) ?></dd></div>
        </dl>
        <p class="storm-links"><?php if ($s['advisory']): ?><a href="<?= e($s['advisory']) ?>" target="_blank" rel="noopener">Public advisory <?= icon('external', 'icon icon-sm') ?></a><?php endif; ?><?php if ($s['graphics']): ?><a href="<?= e($s['graphics']) ?>" target="_blank" rel="noopener">Cone &amp; graphics <?= icon('external', 'icon icon-sm') ?></a><?php endif; ?></p>
      </article>
      <?php endforeach; ?>
    </div>
    <?php endif; ?>
  </div>
</section>

<section class="section section-tight section-alt" aria-labelledby="outlook-h">
  <div class="container split" style="align-items:center">
    <div>
      <h2 id="outlook-h">NHC 7-day tropical weather outlook</h2>
      <p>The National Hurricane Center's outlook shows areas being watched for development over the next week, color-coded by formation chance. It updates every six hours during the season.</p>
      <p><a class="btn btn-ghost btn-sm" href="https://www.nhc.noaa.gov/gtwo.php?basin=atlc&amp;fdays=7" target="_blank" rel="noopener">Open the official outlook <?= icon('external', 'icon icon-sm') ?></a></p>
    </div>
    <figure class="outlook-figure">
      <img src="https://www.nhc.noaa.gov/xgtwo/two_atl_7d0.png" alt="National Hurricane Center 7-day Atlantic tropical weather outlook map" width="898" height="540" loading="lazy" decoding="async" onerror="this.closest('figure').classList.add('img-failed')">
      <figcaption class="small muted">Image: NOAA National Hurricane Center (public domain), loaded live.</figcaption>
    </figure>
  </div>
</section>

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
