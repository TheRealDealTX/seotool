<?php
/** 7-day forecast cards. Vars: $fc (cached_fetch result or null), $mini (bool) */
$days = !empty($fc['data']) ? forecast_days($fc['data']) : [];
?>
<?php if ($days): ?>
<div class="<?= empty($mini) ? 'wx-forecast' : 'wx-mini-days' ?>">
  <?php foreach ($days as $i => $d): ?>
  <div class="wx-day reveal" style="--d:<?= $i * 50 ?>ms">
    <span class="wx-day-name"><?= e($i === 0 ? 'Today' : date('D', strtotime($d['date']))) ?><?php if (empty($mini)): ?> <small class="muted"><?= e(date('n/j', strtotime($d['date']))) ?></small><?php endif; ?></span>
    <?= wx_svg(wx_icon_key((string) $d['icon'], $d['isDay']), $d['short']) ?>
    <span class="wx-day-temps"><?= $d['hi'] !== null ? (int) $d['hi'] . '&deg;' : '—' ?><span class="lo"><?= $d['lo'] !== null ? (int) $d['lo'] . '&deg;' : '' ?></span></span>
    <?php if (empty($mini)): ?><span class="wx-day-short"><?= e($d['short']) ?></span><?php endif; ?>
    <span class="wx-pop" title="Chance of precipitation"><?= icon('droplets', 'icon icon-sm') ?> <?= $d['pop'] !== null ? (int) $d['pop'] . '%' : '0%' ?></span>
    <?php if (empty($mini) && $d['qpf'] !== null): ?><span class="small muted"><?= e(number_format((float) $d['qpf'], 2)) ?>" rain</span><?php endif; ?>
  </div>
  <?php endforeach; ?>
</div>
<?php if (empty($mini)): ?>
<p class="small muted mt-0" style="margin-top:12px">Forecast issued by NWS Brownsville/Rio Grande Valley for grid <?= e($fc['data']['office'] . ' ' . $fc['data']['grid']) ?><?= !empty($fc['data']['updated']) ? ', updated ' . e(date('M j, g:i A T', strtotime($fc['data']['updated']))) : '' ?>. Rain amounts are NWS forecast precipitation totals for each calendar day.<?= !empty($fc['stale']) ? ' <strong>The latest forecast could not be loaded; showing the last available forecast.</strong>' : '' ?></p>
<?php endif; ?>
<?php else: ?>
<div class="wx-fallback">
  <p class="mb-0"><strong>The 7-day forecast is temporarily unavailable.</strong> The National Weather Service feed did not respond. View the official forecast at <a href="https://forecast.weather.gov/MapClick.php?lat=26.2034&amp;lon=-98.23" target="_blank" rel="noopener">forecast.weather.gov</a>.</p>
</div>
<?php endif; ?>
