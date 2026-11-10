<div class="narrow quiz">
  <div class="quiz-top">
    <h1>What kind of roommate are you?</h1>
    <p class="muted">8 quick questions. Your answers fill in your lifestyle preferences and give you a roommate type that improves your matches.</p>
    <div class="progress quiz-progress"><span style="width:0%"></span></div>
    <p class="small muted quiz-count">Question <b>1</b> of <?= count($quiz) ?></p>
  </div>
  <form method="post" class="quiz-form" id="quiz-form">
    <?= csrf_field() ?>
    <?php foreach ($quiz as $i => $item): ?>
    <fieldset class="quiz-step card" data-step="<?= $i ?>"<?= $i ? ' hidden' : '' ?>>
      <legend class="quiz-q"><?= e($item['q']) ?></legend>
      <div class="quiz-opts">
        <?php foreach ($item['opts'] as $j => $o): ?>
        <label class="quiz-opt"><input type="radio" name="a[<?= $i ?>]" value="<?= $j ?>" required><span><b><?= $o[0] ?></b><?= e($o[1]) ?></span></label>
        <?php endforeach; ?>
      </div>
      <div class="quiz-nav">
        <?php if ($i): ?><button type="button" class="btn btn-ghost js-quiz-back"><?= icon('back') ?> Back</button><?php else: ?><span></span><?php endif; ?>
        <?php if ($i === count($quiz) - 1): ?><button class="btn btn-gold" type="submit">See my roommate type</button><?php endif; ?>
      </div>
    </fieldset>
    <?php endforeach; ?>
  </form>
</div>
