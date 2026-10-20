<?php
/** One storm report card. Vars: $ev */
$fam = $ev['fam'];
$sev = storm_severity($ev);
?>
<article class="event-card t-<?= e($fam) ?> reveal">
  <span class="event-type"><?= icon(storm_family_icon($fam), 'icon icon-sm') ?> <?= e($ev['type']) ?></span>
  <h3><?= e($ev['loc'] ?: $ev['area']) ?></h3>
  <div class="event-meta">
    <span><?= icon('calendar', 'icon icon-sm') ?> <?= e(date('M j, Y', strtotime($ev['date']))) ?><?= !empty($ev['time']) ? ' &middot; ' . e(date('g:i A', strtotime($ev['date'] . ' ' . $ev['time']))) : '' ?></span>
    <span><?= icon('map', 'icon icon-sm') ?> <?= e($ev['area']) ?></span>
  </div>
  <?php if ($sev): ?><span class="event-sev"><?= e($sev) ?></span><?php endif; ?>
  <?php if (!empty($ev['text'])): ?><p><?= e($ev['text']) ?></p><?php endif; ?>
  <p class="event-src">
    Source: <a href="<?= e($ev['url']) ?>" target="_blank" rel="noopener"><?= $ev['src'] === 'NCEI' ? 'NOAA NCEI Storm Events Database' : 'NWS Local Storm Report' ?></a><?= !empty($ev['reporter']) ? ' &middot; Reported by ' . e($ev['reporter']) : '' ?>
    <?php if (!empty($ev['verified'])): ?><br>Last verified <?= e(date('M j, Y g:i A T', strtotime($ev['verified']))) ?><?php endif; ?>
  </p>
</article>
