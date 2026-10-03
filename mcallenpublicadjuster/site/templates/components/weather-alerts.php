<?php
/** Active NWS alerts. Vars: $al (cached_fetch result or null) */
$list = $al['data'] ?? null;
?>
<?php if ($list === null): ?>
<div class="wx-fallback"><p class="mb-0"><strong>Alert status unavailable.</strong> We could not reach the National Weather Service. Check <a href="https://www.weather.gov/alerts" target="_blank" rel="noopener">weather.gov/alerts</a> or local broadcast media for watches and warnings.</p></div>
<?php elseif (!$list): ?>
<div class="wx-none"><?= icon('shield', 'icon') ?> <span><strong>No active watches, warnings, or advisories</strong> for McAllen right now. <span class="small">Checked <?= e(time_ago((int) $al['fetched'])) ?>.</span></span></div>
<?php else: ?>
<?php foreach ($list as $a): $sev = strtolower($a['severity']); ?>
<article class="wx-alert sev-<?= e(in_array($sev, ['extreme', 'severe'], true) ? 'severe' : ($sev === 'moderate' ? 'moderate' : 'minor')) ?>">
  <h3><?= icon('alert', 'icon icon-sm') ?> <?= e($a['event']) ?></h3>
  <p class="wx-alert-meta"><?= e($a['severity']) ?> &middot; <?= $a['effective'] ? 'From ' . e(date('M j, g:i A', strtotime($a['effective']))) : '' ?><?= $a['expires'] ? ' until ' . e(date('M j, g:i A T', strtotime($a['expires']))) : '' ?> &middot; <?= e($a['sender']) ?></p>
  <?php if ($a['headline']): ?><p><?= e($a['headline']) ?></p><?php endif; ?>
  <details><summary>Full alert text</summary><pre><?= e(trim($a['description'] . "\n\n" . $a['instruction'])) ?></pre><p class="small muted">Areas: <?= e($a['area']) ?></p></details>
</article>
<?php endforeach; ?>
<?php endif; ?>
