<?php
/** Current conditions panel. Vars: $cur (cached_fetch result or null), $mini (bool) */
$c = $cur['data'] ?? null;
?>
<?php if ($c): ?>
<div class="wx-now">
  <p class="eyebrow eyebrow-gold mt-0">Now in McAllen</p>
  <div class="wx-now-top">
    <?= wx_svg(wx_icon_key($c['icon']), $c['text']) ?>
    <div>
      <div class="wx-temp"><?= fmt_num($c['temp_f']) ?><sup>&deg;F</sup></div>
      <p class="wx-cond"><?= e($c['text'] ?: 'Conditions unavailable') ?></p>
    </div>
  </div>
  <dl class="wx-stats">
    <div><dt>Wind</dt><dd><?= $c['wind_mph'] === null ? '—' : (round($c['wind_mph']) < 1 ? 'Calm' : e(deg_to_compass($c['wind_dir'])) . ' ' . fmt_num($c['wind_mph'], 0, ' mph')) ?></dd></div>
    <div><dt>Gusts</dt><dd><?= $c['gust_mph'] ? fmt_num($c['gust_mph'], 0, ' mph') : 'None reported' ?></dd></div>
    <div><dt>Humidity</dt><dd><?= fmt_num($c['humidity'], 0, '%') ?></dd></div>
    <div><dt><?= $c['heat_index_f'] !== null && $c['heat_index_f'] > $c['temp_f'] + 1 ? 'Heat index' : 'Dew point' ?></dt><dd><?= $c['heat_index_f'] !== null && $c['heat_index_f'] > $c['temp_f'] + 1 ? fmt_num($c['heat_index_f'], 0, '&deg;F') : fmt_num($c['dewpoint_f'], 0, '&deg;F') ?></dd></div>
    <?php if (empty($mini)): ?>
    <div><dt>Pressure</dt><dd><?= fmt_num($c['pressure_inhg'], 2, ' inHg') ?></dd></div>
    <div><dt>Visibility</dt><dd><?= fmt_num($c['visibility_mi'], 0, ' mi') ?></dd></div>
    <?php endif; ?>
  </dl>
  <p class="wx-updated">Observed <?= e(date('M j, g:i A T', strtotime($c['time']))) ?> at McAllen-Miller International Airport (<?= e($c['station']) ?>) &middot; Source: National Weather Service<?= !empty($cur['stale']) ? ' &middot; <strong>Showing the last available reading</strong>' : '' ?></p>
</div>
<?php else: ?>
<div class="wx-now">
  <p class="eyebrow eyebrow-gold mt-0">Now in McAllen</p>
  <p class="wx-cond">Live conditions are temporarily unavailable.</p>
  <p>The National Weather Service data feed did not respond. Please check back shortly, or see current conditions directly at <a href="https://forecast.weather.gov/MapClick.php?lat=26.2034&amp;lon=-98.23" target="_blank" rel="noopener" style="color:var(--gold-light)">weather.gov</a>.</p>
</div>
<?php endif; ?>
