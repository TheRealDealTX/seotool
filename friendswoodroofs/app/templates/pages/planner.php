<?php
$questions = require FR_APP . '/content/planner.php';

// Server-side summary (used when JavaScript is unavailable).
$submitted = isset($_GET['planner']);
$answers = [];
$plannerErrors = [];
$summary = '';
$suggestService = '';
$tips = [];
$links = [];
if ($submitted) {
    foreach ($questions as $key => $q) {
        $v = $_GET[$key] ?? '';
        if (is_string($v) && isset($q['options'][$v])) {
            $answers[$key] = $v;
        } else {
            $plannerErrors[$key] = 'Please choose an answer for: ' . $q['legend'];
        }
    }
    $notes = clean_text($_GET['notes'] ?? '', 1000);
    if (!$plannerErrors) {
        $lines = ['Roofing Project Planner summary', ''];
        foreach ($questions as $key => $q) {
            $lines[] = $q['label'] . ': ' . $q['options'][$answers[$key]][0];
        }
        if ($notes !== '') {
            $lines[] = 'Notes: ' . $notes;
        }
        $summary = implode("\n", $lines);
        $c = $questions['concern']['options'][$answers['concern']];
        $suggestService = $c['service'];
        $links[] = [$c['link'], $c['link_label']];
        if (!empty($questions['damage']['options'][$answers['damage']]['tip'])) {
            $tips[] = $questions['damage']['options'][$answers['damage']]['tip'];
        }
    }
}
$checked = fn (string $key, string $val) => (($answers[$key] ?? ($_GET[$key] ?? null)) === $val) ? ' checked' : '';

partial('page-hero', [
    'eyebrow' => 'Planning tool',
    'title'   => 'Roofing Project Planner',
    'lead'    => 'Answer five quick questions to organize your roofing concern. You will get a short summary you can copy or send with an estimate request.',
    'actions' => false,
]);
?>
<section class="section section--first">
  <div class="container narrow">
    <div class="callout" role="note">
      <p><?= icon('info', 'icon icon-sm') ?> <strong>This is a note-taking tool, not a diagnosis.</strong> It does not inspect your roof, provide a quote or make a definitive recommendation. Answer from what you can see from the ground or inside your home. Please don't climb onto your roof.</p>
    </div>

    <?php if ($plannerErrors): ?>
    <div class="form-status" role="alert">
      <p class="form-status-title"><?= icon('alert', 'icon icon-sm') ?> <span>Please answer every question. "Not sure" is always an option.</span></p>
      <ul><?php foreach ($plannerErrors as $k => $msg): ?><li><a href="#q-<?= e($k) ?>"><?= e($msg) ?></a></li><?php endforeach; ?></ul>
    </div>
    <?php endif; ?>

    <form class="planner" method="get" action="/roofing-project-planner/#planner-result" data-planner novalidate>
      <input type="hidden" name="planner" value="1">
      <?php $n = 0; foreach ($questions as $key => $q): $n++; ?>
      <fieldset class="planner-q" id="q-<?= e($key) ?>"<?= isset($plannerErrors[$key]) ? ' aria-describedby="qerr-' . e($key) . '"' : '' ?> data-question="<?= e($key) ?>" data-label="<?= e($q['label']) ?>">
        <legend><span class="planner-num" aria-hidden="true"><?= $n ?></span> <?= e($q['legend']) ?> <span class="req" aria-hidden="true">*</span></legend>
        <div class="option-grid">
          <?php foreach ($q['options'] as $val => $opt): $id = 'q-' . $key . '-' . $val; ?>
          <div class="option">
            <input type="radio" name="<?= e($key) ?>" id="<?= e($id) ?>" value="<?= e($val) ?>" required<?= $checked($key, $val) ?>
              <?php if (!empty($opt['service'])): ?> data-service="<?= e($opt['service']) ?>" data-link="<?= e($opt['link']) ?>" data-link-label="<?= e($opt['link_label']) ?>"<?php endif; ?>
              <?php if (!empty($opt['tip'])): ?> data-tip="<?= e($opt['tip']) ?>"<?php endif; ?>>
            <label for="<?= e($id) ?>"><?= e($opt[0]) ?></label>
          </div>
          <?php endforeach; ?>
        </div>
        <p class="field-error" id="qerr-<?= e($key) ?>"<?= isset($plannerErrors[$key]) ? '' : ' hidden' ?>><?= icon('alert', 'icon icon-sm') ?><span>Please choose an answer.</span></p>
      </fieldset>
      <?php endforeach; ?>

      <div class="field planner-notes">
        <label for="planner-notes">Anything else to note? <span class="optional">(optional)</span></label>
        <textarea id="planner-notes" name="notes" rows="3" maxlength="1000" aria-describedby="planner-notes-hint"><?= e(clean_text($_GET['notes'] ?? '', 1000)) ?></textarea>
        <p class="field-hint" id="planner-notes-hint">For example: which room shows the stain, when it started, or recent storms.</p>
      </div>

      <div class="form-actions">
        <button class="btn btn-accent btn-lg" type="submit">Create my summary</button>
        <a class="btn btn-ghost-dark" href="/roofing-project-planner/" data-planner-reset>Start over</a>
      </div>
    </form>

    <section class="planner-result" id="planner-result" aria-labelledby="planner-result-heading" data-planner-result<?= $summary === '' ? ' hidden' : '' ?> tabindex="-1">
      <h2 id="planner-result-heading">Your roofing summary</h2>
      <p>Copy this summary or add it to your estimate request below. You can edit it before sending.</p>
      <label class="sr-only" for="planner-summary">Roofing summary text</label>
      <textarea id="planner-summary" class="summary-box" rows="9" readonly data-planner-summary><?= e($summary) ?></textarea>
      <div class="summary-actions">
        <button class="btn btn-outline" type="button" data-copy-summary hidden><?= icon('copy') ?><span>Copy summary</span></button>
        <a class="btn btn-accent" href="#estimate-form" data-use-summary><?= icon('clipboard') ?><span>Add to estimate request</span></a>
      </div>
      <p class="copy-status" data-copy-status role="status" aria-live="polite"></p>
      <div class="planner-next" data-planner-next>
        <h3>Helpful notes</h3>
        <ul data-planner-tips>
          <?php foreach ($tips as $t): ?><li><?= e($t) ?></li><?php endforeach; ?>
          <li>Keep photos and notes together. Dated photos are useful for any later conversation with your insurer.</li>
        </ul>
        <p data-planner-link><?php foreach ($links as [$href, $label]): ?>Related reading: <a href="<?= e($href) ?>"><?= e($label) ?></a><?php endforeach; ?></p>
        <p class="small">This summary records what you've told us. Only an inspection can confirm what your roof needs.</p>
      </div>
    </section>
  </div>
</section>

<section class="section section--tint estimate-section">
  <div class="container estimate-layout">
    <div class="estimate-aside">
      <p class="eyebrow">Next step</p>
      <p class="estimate-aside-title">Send your summary with an estimate request</p>
      <p>Your summary is only sent if you submit this form. Nothing you enter in the planner is stored or sent before then.</p>
      <a class="call-panel" href="<?= e(phone_href()) ?>">
        <?= icon('phone') ?>
        <span><span class="call-panel-label">Or call and read it to us</span><span class="call-panel-number"><?= e(phone_display()) ?></span></span>
      </a>
    </div>
    <?php partial('estimate-form', [
        'returnTo' => '/roofing-project-planner/',
        'heading'  => 'Request an Estimate',
        'prefillMessage' => $summary,
        'prefillService' => $suggestService,
    ]); ?>
  </div>
</section>
