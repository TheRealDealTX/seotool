<?php
/** Repair-or-replace quiz widget. Logic: main.js → tools.quiz. Points: higher = replace. */
$questions = [
    ['How old is the roof?', [['Under 10 years', 0], ['10–15 years', 1], ['15–20 years', 2], ['Over 20 years or not sure', 3]]],
    ['What kind of damage are you seeing?', [['A single spot or a few shingles', 0], ['One slope or area', 1], ['Several areas', 2], ['Damage across the whole roof', 3]]],
    ['How many leaks in the past two years?', [['None', 0], ['One', 1], ['Two or three', 2], ['More than three', 3]]],
    ['How do the shingles look overall?', [['Flat, colorful, intact', 0], ['Some granule loss', 1], ['Curling or cracking in places', 2], ['Brittle, bald or curling everywhere', 3]]],
    ['Any sagging or soft spots?', [['No', 0], ['Not sure', 1], ['One soft spot', 2], ['Visible sag or multiple soft spots', 3]]],
    ['How long will you stay in the home?', [['Selling within 2 years', 0], ['3–7 years', 1], ['8–15 years', 2], ['15+ years', 3]]],
];
?>
<div class="tool tool-quiz" data-tool="quiz" data-total="<?= count($questions) ?>">
  <div class="quiz-progress"><span></span></div>
  <ol class="quiz-steps">
<?php foreach ($questions as $i => [$q, $opts]): ?>
    <li class="quiz-step<?= $i === 0 ? ' is-current' : '' ?>" data-step="<?= $i ?>">
      <p class="quiz-count">Question <?= $i + 1 ?> of <?= count($questions) ?></p>
      <h3><?= e($q) ?></h3>
      <div class="quiz-options">
<?php foreach ($opts as [$label, $pts]): ?>
        <button type="button" class="quiz-option" data-points="<?= $pts ?>"><?= e($label) ?></button>
<?php endforeach; ?>
      </div>
<?php if ($i > 0): ?>
      <button type="button" class="quiz-back">← Back</button>
<?php endif; ?>
    </li>
<?php endforeach; ?>
    <li class="quiz-step quiz-result" data-step="result" aria-live="polite">
      <div class="gauge" aria-hidden="true"><div class="gauge-arc"></div><div class="gauge-needle"></div><span class="g-l">Repair</span><span class="g-r">Replace</span></div>
      <h3 data-out="verdict"></h3>
      <p data-out="detail"></p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/contact/">Book a Free Inspection</a>
        <button type="button" class="btn btn-ghost quiz-restart">Retake quiz</button>
      </div>
    </li>
  </ol>
</div>
