<?php
$meta['title'] = 'Galveston Weather Events: 70+ MPH Wind Days (Updated Weekly)';
$meta['description'] = 'Every day Galveston winds reached 70 mph or more — updated automatically each week from NWS and model data. Had damage? Get a free windstorm claim review.';
$meta['crumb'] = 'Weather Events';
$events = weather_events();
$status = weather_status();
echo page_hero(icon('wind', 18) . ' Updated automatically every week', 'Galveston Weather Events: Winds Over 70 MPH',
    'Every week we check Galveston wind data for sustained winds or gusts of ' . WIND_EVENT_MPH . ' mph or more — the range where shingles begin to crease, lift and blow off. Qualifying days are posted here automatically.');
?>
<section class="section">
  <div class="wrap narrow">
    <div class="status-strip">
      <?= icon('clock', 22) ?>
      <span><strong>Last checked:</strong> <?= !empty($status['last_checked']) ? e(date('F j, Y g:i a', strtotime($status['last_checked']))) . ' CT' : 'first check pending' ?></span>
      <?php if (isset($status['max_wind_mph_this_check'])): ?><span class="tag">Peak wind in last check: <?= (int)$status['max_wind_mph_this_check'] ?> mph</span><?php endif ?>
      <?php if (!empty($status['active_alerts'])): ?><span class="tag red">Active: <?= e(implode(', ', array_unique($status['active_alerts']))) ?></span><?php endif ?>
      <span class="tag hot"><?= count($events) ?> event<?= count($events) === 1 ? '' : 's' ?> on record</span>
    </div>

    <?php if (!$events): ?>
      <div class="card center"><h2>No 70+ mph wind days recorded yet</h2><p class="muted">When Galveston winds reach <?= WIND_EVENT_MPH ?> mph, the event will appear here automatically. Meanwhile, see the <a href="/galveston-storm-history/">storms that shaped the island</a>.</p></div>
    <?php endif ?>

    <div class="grid" style="gap:18px">
    <?php foreach ($events as $ev): $peak = max($ev['max_gust_mph'], $ev['max_sustained_mph']); ?>
      <article class="card event reveal">
        <?= art_gauge($peak) ?>
        <div>
          <div class="post-meta"><span class="tag <?= $peak >= 74 ? 'red' : 'hot' ?>"><?= $peak >= 111 ? 'Major hurricane-force' : ($peak >= 74 ? 'Hurricane-force' : 'Damaging wind') ?></span><span><?= fmt_date($ev['date']) ?></span></div>
          <h3>Galveston wind event — <?= fmt_date($ev['date']) ?></h3>
          <p><?= e($ev['summary']) ?></p>
          <p class="small muted">Peak gust <?= (int)$ev['max_gust_mph'] ?> mph · peak sustained <?= (int)$ev['max_sustained_mph'] ?> mph · Source: <?= e(implode('; ', $ev['sources'])) ?><?php if (!empty($ev['alerts'])): ?> · Alerts: <?= e(implode(', ', array_unique($ev['alerts']))) ?><?php endif ?></p>
          <p style="margin:0"><?= phone_link('btn btn-cta', icon('phone', 16) . ' Damage from this storm? ' . PHONE) ?></p>
        </div>
      </article>
    <?php endforeach ?>
    </div>

    <?= banner('Wind damage after a storm? Call for an expert consultation.', 'TWIA claims must be filed within one year of the date of damage.') ?>

    <h2>How this page works</h2>
    <p>Once a week, our system pulls measured observations from the National Weather Service station at Scholes International Airport (KGLS) on Galveston Island and modeled daily wind maximums for the island from Open-Meteo. Any day with a gust or sustained wind at or above <?= WIND_EVENT_MPH ?> mph is logged here with its source. Modeled values are estimates; measured station data takes priority when available.</p>
    <p>Why 70 mph? It's roughly where older 60 mph–rated 3-tab shingles start to fail outright and where aged seal strips on higher-rated shingles begin to let go. Use the <a href="/calculators/">shingle wind damage calculator</a> to see what a given wind speed means for your roof.</p>
  </div>
</section>
