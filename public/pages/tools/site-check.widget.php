<?php defined('SCC') || (http_response_code(404) && exit);
$qs = [
    ['sun', 'How many hours of direct sun hit the panel spot on a clear day?', [['0', 'Under 1 h'], ['1', '1–2 h'], ['2', '2–4 h'], ['3', '4–6 h'], ['4', '6+ h']], '2'],
    ['shade', 'What shades that spot?', [['3', 'Nothing'], ['2', 'Leafy trees (summer only)'], ['1', 'A building/hill blocks low winter sun'], ['0', 'Shaded most of the day']], '3'],
    ['face', 'Which way can the panel face?', [['2', 'South (north in S. hemisphere)'], ['1', 'East or west'], ['0', 'Only away from the sun']], '2'],
    ['clim', 'Your winters are…', [['3', 'Sunny (Sunbelt, Australia)'], ['2', 'Mixed (most of the US)'], ['1', 'Grey & short (UK, Pacific NW, Canada)'], ['0', 'Very long & snowy']], '2'],
    ['act', 'How busy is the area the camera watches?', [['3', 'Quiet: under 10 events/day'], ['2', 'Normal: 10–40'], ['1', 'Busy: 40–100'], ['0', 'Street/parking: 100+']], '2'],
    ['panel', 'Panel options', [['2', 'Separate panel on a cable'], ['1', 'Built-in panel only'], ['3', 'Separate panel, can mount it in the sunniest spot']], '2'],
    ['net', 'Connectivity at the camera', [['3', 'Strong Wi‑Fi'], ['2', 'Weak Wi‑Fi'], ['1', 'No Wi‑Fi, good cell signal'], ['0', 'No Wi‑Fi, no cell signal']], '3'],
];
?>
<div class="tool" data-tool="site-check">
  <div class="tool-head"><?= icon('compass', 22) ?><strong>Solar Camera Site Check</strong><span>7 questions · 30 seconds</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
<?php foreach ($qs as [$name, $q, $opts, $def]): ?>
      <div class="quiz-q"><p><?= e($q) ?></p><div class="seg">
<?php foreach ($opts as [$v, $l]): ?>
        <label><input type="radio" name="<?= $name ?>" value="<?= $v ?>"<?= $v === $def ? ' checked' : '' ?>><span><?= e($l) ?></span></label>
<?php endforeach; ?>
      </div></div>
<?php endforeach; ?>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="gauge" data-o="gauge"></div>
      <div class="verdict" data-o="verdict"></div>
      <h4>What to do</h4>
      <ul data-o="recs"></ul>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button><a class="btn btn-line btn-sm" href="/tools/solar-camera-battery-calculator/">Run the numbers →</a></div>
    </div>
  </form>
</div>
