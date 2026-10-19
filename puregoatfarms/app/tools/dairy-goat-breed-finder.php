<?php
defined('PGF') || exit;
$q = [
    ['goal', 'What matters most in the milk?', [['volume', 'As much milk as possible'], ['rich', 'Rich, high-butterfat milk'], ['balance', 'A good balance of both']]],
    ['space', 'How much room do you have?', [['small', 'Backyard / under an acre'], ['medium', 'A few acres'], ['large', 'Plenty of pasture']]],
    ['climate', 'What is your climate like?', [['hot', 'Hot summers'], ['cold', 'Cold winters'], ['mild', 'Fairly mild']]],
    ['noise', 'Close neighbors?', [['quiet', 'Yes — quiet goats please'], ['ok', 'Some noise is fine']]],
    ['experience', 'Your goat experience?', [['new', 'Brand new to goats'], ['some', 'Kept goats before']]],
];
ob_start(); ?>
<form class="quiz" id="bf-quiz" novalidate>
  <div class="quiz__progress" aria-hidden="true"><span id="bf-bar"></span></div>
<?php foreach ($q as $i => [$name, $label, $opts]): ?>
  <fieldset class="quiz__q" data-step="<?= $i ?>"<?= $i ? ' hidden' : '' ?>>
    <legend><span class="quiz__n"><?= $i + 1 ?>/<?= count($q) ?></span> <?= e($label) ?></legend>
    <div class="quiz__opts">
<?php foreach ($opts as [$v, $l]): ?>
      <label class="opt-card"><input type="radio" name="<?= $name ?>" value="<?= $v ?>"><span><?= e($l) ?></span></label>
<?php endforeach; ?>
    </div>
  </fieldset>
<?php endforeach; ?>
  <div class="quiz__nav"><button type="button" class="btn btn--ghost btn--sm" id="bf-back" hidden>Back</button></div>
</form>
<div class="quiz__result" id="bf-result" hidden aria-live="polite">
  <p class="out-label">Your best-fit dairy breeds</p>
  <ol class="match-list" id="bf-list"></ol>
  <p class="center"><button type="button" class="btn btn--ghost btn--sm" id="bf-restart">Start over</button></p>
</div>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Dairy Goat Breed Finder Quiz — Best Goat Breed for You | Pure Goat Farms',
    'desc'  => 'Which dairy goat breed is best for you? Answer five quick questions about milk, space, climate and noise and get your top matches: Saanen, Alpine, Nubian, LaMancha and more.',
    'intro' => 'Five quick questions about your milk goals, space, climate and neighbors — and we\'ll match you with the dairy goat breeds most likely to suit you.',
    'widget' => $widget,
    'how' => '<h2>How the breed finder scores your answers</h2>
<p>Each of the seven recognized dairy breeds — plus Nigerian-based mini dairy crosses — is scored on milk volume, butterfat, size, heat and cold tolerance, noise and ease of handling. Your answers weight those traits, and the breeds with the highest combined score come out on top.</p>
<p>Use it as a starting point, then meet the goats. Udder quality, the dam\'s milk records and herd health testing matter as much as the breed name. The full comparison is in our guide to the <a href="/best-dairy-goat-breeds-for-milk/">best dairy goat breeds for milk</a>.</p>',
    'faq' => [
        ['What is the best dairy goat breed for beginners?', 'Nigerian Dwarfs and LaManchas are popular beginner choices: Nigerians for their small size and rich milk, LaManchas for their calm, quiet temperament and solid production.'],
        ['Which dairy goat is the quietest?', 'LaManchas, Saanens and Oberhaslis are generally the quietest dairy breeds. Nubians are known for being the most vocal.'],
    ],
    'posts' => ['best-dairy-goat-breeds-for-milk', 'how-much-milk-does-a-goat-produce-per-day'],
];
